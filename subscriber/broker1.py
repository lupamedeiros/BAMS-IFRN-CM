# O código cria um cliente MQTT que se conecta a um broker, assina um tópico e insere mensagens recebidas no banco de dados.

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an mqtt subscriber.
import paho.mqtt.client as mqtt
import sqlite3

# Função para inserir dados no banco de dados
def inserir_dados(dados):
    # Conectando ao banco de dados (se o banco não existir, ele será criado)
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Criando a tabela "dados_mqtt" (ou qualquer outro nome que você precise)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_mqtt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identificador único de cada registro
        topico TEXT NOT NULL,                   -- Tópico da mensagem MQTT
        payload TEXT NOT NULL                   -- Conteúdo da mensagem
    );
    ''')

    # Inserindo os dados na tabela "dados_mqtt"
    cursor.execute('''
    INSERT INTO dados_mqtt (topico, payload)
    VALUES (?, ?)
    ''', (dados['topico'], dados['payload']))

    # Salvando as mudanças no banco de dados
    conn.commit()

    # Fechando a conexão
    conn.close()

# Função a ser executada quando o cliente conectar
def on_connect(mqttc, obj, flags, reason_code, properties):
    # Definir e implementar o que o cliente deve fazer ao se conectar
    print("reason_code: " + str(reason_code))

# Função a ser executada quando o cliente receber uma mensagem
def on_message(mqttc, obj, msg):
    # Pegando os dados da mensagem recebida
    topico = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Mensagem recebida no tópico {topico}: {payload}")
    
    # Inserindo os dados no banco de dados
    dados = {
        'topico': topico,
        'payload': payload
    }
    inserir_dados(dados)

# Função a ser executada quando o cliente fizer uma nova assinatura
def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    # Definir o implementar o que o cliente deve fazer ao assinar um novo tópico
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))

# Função a ser executada quando houver log
def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

# Cria o MQTT-Cliente
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "sub_teste")

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("grupo/variavel")

mqttc.loop_forever()

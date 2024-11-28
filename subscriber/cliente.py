#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import sqlite3
import json
import schedule
import time

# Função para inserir dados no banco de dados
def inserir_dados(dados):
    conn = sqlite3.connect('dados_meteorologicos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_meteorologicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topico TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        temperatura REAL,
        chuva REAL,
        umidade_relativa REAL,
        temperatura_aparente REAL,
        is_dia INTEGER,
        precipitacao REAL,
        codigo_tempo INTEGER,
        cobertura_nuvens REAL,
        pressao_msl REAL,
        pressao_superficie REAL,
        velocidade_vento REAL,
        direcao_vento REAL,
        rajadas_vento REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    cursor.execute('''
    INSERT INTO dados_meteorologicos (topico, latitude, longitude, temperatura, chuva, umidade_relativa, temperatura_aparente,
                                      is_dia, precipitacao, codigo_tempo, cobertura_nuvens, pressao_msl, pressao_superficie,
                                      velocidade_vento, direcao_vento, rajadas_vento)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (dados['topico'], dados['latitude'], dados['longitude'], dados['temperature_2m'], dados['rain'], dados['relative_humidity_2m'],
          dados['apparent_temperature'], dados['is_day'], dados['precipitation'], dados['weather_code'], dados['cloud_cover'], 
          dados['pressure_msl'], dados['surface_pressure'], dados['wind_speed_10m'], dados['wind_direction_10m'], dados['wind_gusts_10m']))
    conn.commit()
    conn.close()

# Função a ser executada quando o cliente conectar
def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe("grupo/variavel")

# Função a ser executada quando o cliente receber uma mensagem
def on_message(mqttc, userdata, msg):
    topico = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Mensagem recebida no tópico {topico}: {payload}")
    dados = json.loads(payload)
    dados['topico'] = topico
    dados['latitude'] = -5.6344
    dados['longitude'] = -35.4256
    inserir_dados(dados)

# Função a ser executada quando o cliente fizer uma nova assinatura
def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Função a ser executada quando houver log
def on_log(mqttc, userdata, level, buf):
    print(buf)

# Função agendada para verificar dados a cada 15 minutos
def verificar_dados():
    print("Verificando dados...")

# Cria o MQTT-Cliente
mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log

mqttc.connect("127.0.0.1", 1883, 60)

# Agendando a função verificar_dados a cada 15 minutos
schedule.every(15).minutes.do(verificar_dados)

# Loop principal
while True:
    mqttc.loop_start()
    schedule.run_pending()
    time.sleep(1)

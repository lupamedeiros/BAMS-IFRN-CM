#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import sqlite3
import json
import schedule
import time

# Função para inserir dados no banco de dados
def insert_data(data):
    conn = sqlite3.connect('my.db')
    cursor = conn.cursor()

    #criando a tabela
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        temperature_2m REAL,
        rain REAL,
        relative_humidity_2m REAL,
        apparent_temperature REAL,
        is_day INTEGER,
        precipitation REAL,
        weather_code INTEGER,
        cloud_cover REAL,
        pressure_msl REAL,
        surface_pressure REAL,
        wind_speed_10m REAL,
        wind_direction_10m REAL,
        wind_gusts_10m REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    #inserindo os dados na tabela 'wheater.data'
    cursor.execute('''
    INSERT INTO weather_data (topic, latitude, longitude, temperature_2m, rain, relative_humidity_2m, apparent_temperature,
                                      is_day, precipitation, weather_code, cloud_cover, pressure_msl, surface_pressure,
                                      wind_speed_10m, wind_direction_10m, wind_gusts_10m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['topic'], data['latitude'], data['longitude'], data['temperature_2m'], data['rain'], data['relative_humidity_2m'],
          data['apparent_temperature'], data['is_day'], data['precipitation'], data['weather_code'], data['cloud_cover'], 
          data['pressure_msl'], data['surface_pressure'], data['wind_speed_10m'], data['wind_direction_10m'], data['wind_gusts_10m']))
    conn.commit()
    conn.close()

# Função a ser executada quando o cliente conectar
def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe("weather/data")

# Função a ser executada quando o cliente receber uma mensagem
def on_message(mqttc, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Mensagem recebida no tópico {topic}: {payload}")
    data = json.loads(payload)
    data['topic'] = topic
    data['latitude'] = -5.6344
    data['longitude'] = -35.4256
    insert_data(data)

# Função a ser executada quando o cliente fizer uma nova assinatura
def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Função a ser executada quando houver log
def on_log(mqttc, userdata, level, buf):
    print(buf)

# Função agendada para verificar dados a cada 15 minutos
def check_data():
    print("Verificando dados...")

# Cria o MQTT-Cliente
mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log

mqttc.connect("192.168.56.101", 1883, 60)
mqttc.username_pw_set("mosquitto", "dietpi")

# Agendando a função verificar_dados a cada 15 minutos
schedule.every(15).minutes.do(check_data)

# Loop principal
while True:
    mqttc.loop_start()
    schedule.run_pending()
    time.sleep(1)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import paho.mqtt.client as mqtt

# Função para inserir dados no banco de dados
def insert_data(topic, time, temperature_2m, rain, relative_humidity_2m, apparent_temperature, is_day, precipitation, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO weather_data (topic, time, temperature_2m, rain, relative_humidity_2m, apparent_temperature, is_day, precipitation, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, time, temperature_2m, rain, relative_humidity_2m, apparent_temperature, is_day, precipitation, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m))
    conn.commit()
    conn.close()

# Callback executado quando uma mensagem é recebida
def on_message(client, userdata, msg):
    # Aqui você pode fazer o parsing dos dados recebidos e inserir no banco de dados
    data = msg.payload.decode('utf-8').split(',')
    topic = msg.topic
    time = data[0]
    temperature_2m = float(data[1])
    rain = float(data[2])
    relative_humidity_2m = float(data[3])
    apparent_temperature = float(data[4])
    is_day = int(data[5])
    precipitation = float(data[6])
    weather_code = int(data[7])
    cloud_cover = float(data[8])
    pressure_msl = float(data[9])
    surface_pressure = float(data[10])
    wind_speed_10m = float(data[11])
    wind_direction_10m = float(data[12])
    wind_gusts_10m = float(data[13])
    
    insert_data(topic, time, temperature_2m, rain, relative_humidity_2m, apparent_temperature, is_day, precipitation, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m)

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Função de callback para autenticação
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")

# Configuração de credenciais
client.username_pw_set("mosquitto", "dietpi")

# Conexão ao broker MQTT
client.connect("192.168.56.101", 1883, 60)

# Loop para manter a conexão aberta e receber mensagens
client.loop_forever()

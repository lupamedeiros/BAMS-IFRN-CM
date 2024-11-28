import requests_cache
import pandas as pd
from retrying import retry # Biblioteca corrigida
import json
import time
import paho.mqtt.client as mqtt

cache_session = requests_cache.CachedSession('cache', expire_after=3600) #retry

# Função com tentativa de retry caso a requisição falhe      (ler dados)
@retry(stop_max_attempt_number=5, wait_fixed=200) # faz parte da biblioteca `retrying` e serve para adicionar uma lógica de reprodução automática a uma função, caso ela falhe ou lance uma exceção.
def get_weather_data(url, params):
    response = cache_session.get(url, params=params)
    response.raise_for_status()  # Levanta exceção para erros HTTP
    return response.json()

def on_connect(client, userdata, flags, rc): # funçao executada aoa conectar
    print(f"Connected with result code {rc}")
    client.subscribe("weather/data")

def conectar(broker, usuario, senha, funcao, porta=1883, naosei=60):
    client = mqtt.Client()
    client.on_connect = funcao
    client.username_pw_set(usuario, senha)  # Define o usuário e senha, se necessário
    client.connect(broker, porta, naosei)

    return client

def publicar(client, weather_data):  # Função para publicar os dados do clima via MQTT
    payload = json.dumps(weather_data)
    client.publish("weather/data", payload)


def loop(client):
    client.loop_forever()

def main():
    MQTT_BROKER = "192.168.56.101"  # Endereço do broker MQTT
    MQTT_TOPIC = "test_channel"
    username = "mosquitto"
    password = "dietpi"

    # Definição do endpoint da API Open-Meteo e parâmetros
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -5.6344,  # Coordenadas de Ceará Mirim
        "longitude": -35.4256,
        "current": ["temperature_2m", "rain","relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m",  "wind_direction_10m", "wind_gusts_10m"],
        "timezone": "America/Fortaleza"  # Zona de tempo correta
    }

    # Obtém os dados da API
    weather_data = get_weather_data(url, params=params)

    print(weather_data)

    # Processamento dos dados horários
    current_data = weather_data['current']
    current_time = pd.to_datetime(current_data['time'])  # Converte o tempo em formato datetime

    '''
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_is_day = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    current_rain = current.Variables(5).Value()
    current_weather_code = current.Variables(6).Value()
    current_cloud_cover = current.Variables(7).Value()
    current_pressure_msl = current.Variables(8).Value()
    current_surface_pressure = current.Variables(9).Value()
    current_wind_speed_10m = current.Variables(10).Value()
    current_wind_direction_10m = current.Variables(11).Value()
    current_wind_gusts_10m = current.Variables(12).Value()
  
    # Cria um dicionário com os dados processados
    weather_info = {
        "time": current_time.strftime('%Y-%m-%d %H:%M:%S').tolist(),  # Formata a data e hora
        "temperature_2m": current_temperature_2m,
        "rain": current_rain
    }

    # Inicializa o cliente MQTT e conecta ao broker
    client = conectar(MQTT_BROKER, username, password, on_connect)
    '''
    

if __name__=="__main__":
    main()
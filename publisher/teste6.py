import requests_cache
import json
import paho.mqtt.client as mqtt
from retrying import retry

# Configuração de cache para requisições
cache_session = requests_cache.CachedSession('cache', expire_after=3600)

# Função para obter dados da API com tentativa de repetição
@retry(stop_max_attempt_number=5, wait_fixed=200)
def get_weather_data(url, params):
    response = cache_session.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Callback executado ao conectar ao MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("Conexão estabelecida com sucesso!")
    else:
        print(f"Falha na conexão, código: {rc}")

# Função para conectar ao broker MQTT
def conectar(broker, usuario, senha, funcao, porta=1883, keepalive=500):
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.enable_logger()  # Habilita logs detalhados
    client.on_connect = funcao
    client.username_pw_set(usuario, senha)
    client.connect(broker, porta, keepalive)
    return client

# Função para publicar dados no broker MQTT
def publicar(client, topic, weather_data):
    payload = json.dumps(weather_data)
    client.publish(topic, payload)
    print(f"Publicado no tópico {topic}: {payload}")

# Função principal
def main():
    MQTT_BROKER = "192.168.56.101"
    MQTT_TOPIC = "weather/data"
    username = "mosquitto"
    password = "dietpi"

    # Configuração da API Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -5.6344,
        "longitude": -35.4256,
        "current":  ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "timezone": "America/Fortaleza"
    }

    try:
        # Obter dados da API
        weather_data = get_weather_data(url, params)
        current_weather = weather_data.get("current_weather", {})

        # Processar todas as variáveis listadas
        weather_info = {
            "time": current_weather.get("time"),
            "temperature_2m": current_weather.get("temperature"),
            "rain": current_weather.get("precipitation"),
            "relative_humidity_2m": current_weather.get("relative_humidity"),
            "apparent_temperature": current_weather.get("apparent_temperature"),
            "is_day": current_weather.get("is_day"),
            "precipitation": current_weather.get("precipitation"),
            "weather_code": current_weather.get("weathercode"),
            "cloud_cover": current_weather.get("cloudcover"),
            "pressure_msl": current_weather.get("pressure_msl"),
            "surface_pressure": current_weather.get("surface_pressure"),
            "wind_speed_10m": current_weather.get("windspeed"),
            "wind_direction_10m": current_weather.get("winddirection"),
            "wind_gusts_10m": current_weather.get("windgusts")
        }

        print(f"Dados Brutos: {weather_data}\n\n")
        print(f"Dados do Clima: {weather_info}")

        # Inicializa o cliente MQTT e conecta ao broker
        client = conectar(MQTT_BROKER, username, password, on_connect)

        # Publicar os dados no MQTT
        publicar(client, MQTT_TOPIC, weather_info)
        client.loop_forever()

    except Exception as e:
        print(f"Erro ao obter ou publicar dados do clima: {e}")

if __name__ == "__main__":
    main()

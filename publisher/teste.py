import openmeteo_requests
import requests_cache
import paho.mqtt.client as mqtt
from retry_requests import retry
import json

# Configure o cliente Open-Meteo API com cache e tente novamente em caso de erro
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# MQTT setup
MQTT_BROKER = "localhost"  # Endereço do broker MQTT (pode ser um IP ou domínio)
MQTT_PORT = 1883  # Porta padrão do Mosquitto
MQTT_TOPIC = "weather/ceara_mirim"  # Tópico onde os dados serão enviados
username = "mosquitto"
password = "dietpi"

# Cria o cliente 
mqtt_client = mqtt.Client()

# Conecta no broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Faz a solicitação a API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -5.6344,
    "longitude": -35.4256,
    "current": [
        "temperature_2m", "relative_humidity_2m", "apparent_temperature", 
        "is_day", "precipitation", "rain", "weather_code", "cloud_cover", 
        "pressure_msl", "surface_pressure", "wind_speed_10m", 
        "wind_direction_10m", "wind_gusts_10m" 
        ],
    "timezone": "America/Fortaleza"

}

responses = openmeteo.weather_api(url, params=params)

# Processar a localização
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

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

# Formata data JSON string pra publicar no MQTT
weather_data = {
    "latitude": response.Latitude(),
    "longitude": response.Longitude(),
    "elevation": response.Elevation(),
    "timezone": response.Timezone().decode("utf-8"),
    "current_time": current.Time(),
    "temperature_2m": current_temperature_2m,
    "relative_humidity_2m": current_relative_humidity_2m,
    "apparent_temperature": current_apparent_temperature,
    "is_day": current_is_day,
    "precipitation": current_precipitation,
    "rain": current_rain,
    "weather_code": current_weather_code,
    "cloud_cover": current_cloud_cover,
    "pressure_msl": current_pressure_msl,
    "surface_pressure": current_surface_pressure,
    "wind_speed_10m": current_wind_speed_10m,
    "wind_direction_10m": current_wind_direction_10m,
    "wind_gusts_10m": current_wind_gusts_10m
}
print(weather_data)
msg = json.dumps(weather_data, indent=4)

# Publica a data MQTT
mqtt_client.publish(MQTT_TOPIC, msg, qos=1, retain=False)
print(f"Weather data published to {MQTT_TOPIC}: {weather_data}")

# Disconecta do broker
mqtt_client.disconnect()

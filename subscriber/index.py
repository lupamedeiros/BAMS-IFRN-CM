import paho.mqtt.client as mqtt
import requests
import json

# Definir a URL da API com os parâmetros fornecidos
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = -5.6344
LONGITUDE = -35.4256
PARAMETERS = "temperature_2m,rain"
TIMEZONE = "America/Fortaleza"

# Função para conectar ao broker MQTT
def conecta_broker():
    broker = "mqtt.eclipse.org"  # Exemplo de broker MQTT público
    client = mqtt.Client("Weather_Subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    return client

# Callback de conexão bem-sucedida ao broker
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de resultado " + str(rc))
    # Assinar o tópico de clima
    client.subscribe("weather/forecast")

# Callback de mensagem recebida
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico " + msg.topic + ": " + str(msg.payload.decode("utf-8")))

# Função para obter dados da API de clima
def receber():
    try:
        response = requests.get(f"{API_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&hourly={PARAMETERS}&timezone={TIMEZONE}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erro ao receber dados da API: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exceção ao acessar a API: {e}")
        return None

# Função de loop para verificar dados periodicamente e publicá-los
def loop(client):
    while True:
        dados_clima = receber()
        if dados_clima:
            # Extraindo informações de temperatura e chuva
            temperatura = dados_clima['hourly']['temperature_2m']
            chuva = dados_clima['hourly']['rain']
            mensagem = f"Temperatura: {temperatura}, Chuva: {chuva}"
            # Publicar os dados no tópico de clima
            client.publish("weather/forecast", mensagem)
        client.loop()  # Loop para manter a conexão MQTT

# Função principal
def main():
    client = conecta_broker()  # Conectar ao broker MQTT
    loop(client)  # Iniciar o loop de recebimento e publicação de dados

# Executar o código apenas se for o script principal
if __name__ == "__main__":
    main()

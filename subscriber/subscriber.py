import paho.mqtt.client as mqtt

# Função que será chamada quando o cliente se conectar ao broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso ao broker")
        # Inscreve-se em um tópico após a conexão
        client.subscribe("seu/topico/aqui")
    else:
        print("Falha na conexão, código de resultado: ", str(rc))

# Função que será chamada quando uma mensagem for recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Criando uma instância do cliente MQTT
client = mqtt.Client()

# Atribuindo as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectando ao broker MQTT
broker_address = "broker.hivemq.com"  # Exemplo de broker público
broker_port = 1883  # Porta padrão para MQTT
try:
    client.connect(broker_address, broker_port)
except Exception as e:
    print(f"Erro ao tentar conectar ao broker: {e}")
    exit(1)

# Mantendo o loop do cliente para processar as mensagens
client.loop_forever()

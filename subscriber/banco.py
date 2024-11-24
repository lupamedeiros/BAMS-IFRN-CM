import sqlite3
import schedule
import time

# Função para inserir os dados no banco de dados
def inserir_dados(dados):
    # Conectando ao banco de dados (se o banco não existir, ele será criado)
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Criando a tabela "dados_meteorologicos" (ou qualquer outro nome que você precise)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_meteorologicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identificador único de cada registro
        latitude TEXT NOT NULL,                 -- Latitude das coordenadas
        longitude TEXT NOT NULL,                -- Longitude das coordenadas
        altitude INTEGER,                       -- Altitude em metros
        deslocamento_utc INTEGER,               -- Deslocamento UTC
        fuso_horario TEXT,                      -- Fuso horário
        abreviacao_fuso TEXT,                   -- Abreviação do fuso horário
        data_registro TEXT,                     -- Data e hora do registro
        temperatura REAL,                       -- Temperatura em °C
        umidade INTEGER,                        -- Umidade relativa em %
        temperatura_aparente REAL,              -- Temperatura aparente em °C
        status_dia TEXT,                        -- Status do dia (dia/noite)
        precipitacao REAL,                      -- Precipitação em mm
        chuva REAL,                             -- Chuva em mm
        chuviscos REAL,                         -- Chuviscos em mm
        codigo_clima INTEGER,                   -- Código do clima (WMO)
        cobertura_nuvens INTEGER,               -- Cobertura de nuvens em %
        pressao_msl REAL,                       -- Pressão MSL em hPa
        pressao_atmosferica REAL,               -- Pressão atmosférica em hPa
        velocidade_vento REAL,                  -- Velocidade do vento a 10m em km/h
        direcao_vento INTEGER,                  -- Direção do vento a 10m em graus
        rafagas_vento REAL                      -- Ráfagas de vento a 10m em km/h
    );
    ''')

    # Inserindo os dados na tabela "dados_meteorologicos"
    cursor.execute('''
    INSERT INTO dados_meteorologicos (latitude, longitude, altitude, deslocamento_utc, fuso_horario, abreviacao_fuso, data_registro, temperatura, umidade, temperatura_aparente, status_dia, precipitacao, chuva, chuviscos, codigo_clima, cobertura_nuvens, pressao_msl, pressao_atmosferica, velocidade_vento, direcao_vento, rafagas_vento)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)

    # Salvando as mudanças no banco de dados
    conn.commit()

    # Fechando a conexão
    conn.close()

# Agendando a execução da função a cada 15 minutos
dados_exemplo = (
    '52,52° N',
    '13,42° E',
    38,
    0,
    'GMT',
    'GMT',
    '2024-11-11 20:30',
    4.7,
    93,
    2.2,
    'Noite',
    0.0,
    0.0,
    0.0,
    3,
    100,
    1028.7,
    1023.9,
    6.8,
    87,
    15.1
)

schedule.every(15).minutes.do(inserir_dados, dados_exemplo)

# Loop para manter o agendamento em execução
while True:
    schedule.run_pending()
    time.sleep(1)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

# Conectando ao banco de dados (se o banco não existir, ele será criado)
conn = sqlite3.connect('dados_meteorologicos.db')
cursor = conn.cursor()

# Criando a tabela "dados_meteorologicos" (ou qualquer outro nome que você precise)
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

# Salvando as mudanças no banco de dados
conn.commit()
# Fechando a conexão
conn.close()

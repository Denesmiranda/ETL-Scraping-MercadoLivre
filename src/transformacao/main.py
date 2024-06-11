#bibliotecas
import pandas as pd
import sqlite3
from datetime import datetime

# Função para remover o ponto após o primeiro algarismo.
def remover_ponto(valor):
    if isinstance(valor, str):
        partes = valor.split('.')
        if len(partes) > 1 and len(partes[0]) == 1:
            return int(partes[0] + partes[1])
    return valor

# 1) Carrega o dataset a partir do arquivo JSON
df = pd.read_json('../data/data.jsonl', lines=True)

# 2) Define a fonte dos dados
df['_fonte'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino" 

# 3) Define a data e hora da coleta dos dados
df['_data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 4) Converte as colunas de preços para float e trata valores nulos
df['preco_antigo_reais'] = df['preco_antigo_reais'].fillna(0).astype(float)
df['preco_antigo_centavos'] = df['preco_antigo_centavos'].fillna(0).astype(float)

df['preco_novo_reais'] = df['preco_novo_reais'].fillna(0).astype(float)
df['preco_novo_centavos'] = df['preco_novo_centavos'].fillna(0).astype(float)

df['nota'] = df['nota'].fillna(0).astype(float)

# 5) Converte a coluna de quantidade de avaliações para inteiro e remove parênteses
df['qtde_avaliacoes'] = df['qtde_avaliacoes'].str.replace('[\(\)]', '', regex=True)
df['qtde_avaliacoes'] = df['qtde_avaliacoes'].fillna(0).astype(int)

# 6) Concatena os valores das colunas de reais e centavos para formar o preço total
df['preco_antigo'] = df['preco_antigo_reais'] + df['preco_antigo_centavos'] / 100
df['preco_novo'] = df['preco_novo_reais'] + df['preco_novo_centavos'] / 100

# 7) Remove o ponto após o primeiro algarismo dos valores das colunas de preços
df['preco_antigo'] = df['preco_antigo'].astype(str).apply(remover_ponto).astype(float)
df['preco_novo'] = df['preco_novo'].astype(str).apply(remover_ponto).astype(float)

# 8) Conecta ao banco de dados SQLite
conn = sqlite3.connect('../data/quotes.db')

# 9) Salva o DataFrame no banco de dados SQLite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

df.to_csv('../data/mercadolivre_items.csv', index=False, sep=';', quoting=2, quotechar='"')

# 10) Fecha a conexão com o banco de dados
conn.close()

# 11) Exibe as primeiras linhas do DataFrame
print(df.head())

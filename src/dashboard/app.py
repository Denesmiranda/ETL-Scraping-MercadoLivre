#importação das bibliotecas 
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

try:
    #1) Conecta com o banco de dados
    conn = sqlite3.connect('../data/quotes.db')

    #2) Carregar os dados da tabela 'mercadolivre_items' em um DF pandas
    df = pd.read_sql_query('SELECT * FROM mercadolivre_items', conn)

    #3) Encerra a conexão com o banco de dados
    conn.close()

    #4) Título da aplicação
    st.markdown("<h1 style='text-align: center;'>Pesquisa de Mercado <br>Tênis Esportivos no Mercado Livre</h1>", unsafe_allow_html=True)
   
    #5) Melhorar o layout com colunas para KPIs
    col1, col2 = st.columns(2)
    col1.markdown("<h3 style='text-align: left; color: darkblue; font-weight: bold;'>KPIs principais</h3>", unsafe_allow_html=True)
    
    #Data de processamento
    data_processamento = datetime.now().strftime("%d-%m-%Y")
    col2.markdown(f"<p style='text-align: right; color: red; margin-top: 10px;'>Data do Processamento: {data_processamento}</p>", unsafe_allow_html=True)

    #definindo colunas
    col1, col2, col3, col4, = st.columns(4)
    #st.write(df)
    
    #6) KP1: Número total de itens
    total_itens = df.shape[0]
    col1.metric(label="Número Total de Itens", value=total_itens)
    

    #7) KP2: Número de marcas únicas
    marcas_unicas = df['marca'].nunique()
    col2.metric(label="Número de Marcas Únicas", value=marcas_unicas)

    #8) KP3: Preço médio novo (R$)
    novo_preco_medio = df['preco_novo'].mean()
    col3.metric(label="Preço Médio Novo (R$)", value=f"{novo_preco_medio:.2f}")

    maior_preco = df['preco_novo'].max()
    indice_maior_preco = df['preco_novo'].idxmax()
    marca_maior_preco = df.loc[indice_maior_preco, 'marca']
    maior_preco_formatted = '{:.2f}'.format(maior_preco)
    col4.metric(label="O maior preço encontrado é", value=maior_preco_formatted, delta=marca_maior_preco)
    

    #9) Quais marcas são mais encontradas ate a página 10
    st.subheader("Marcas mais encontradas até a página 10")
    col1, col2 = st.columns([4, 2])
    top_10_marcas = df['marca'].value_counts().sort_values(ascending=False)
    col1.bar_chart(top_10_marcas.sort_values(ascending=True))
    col2.write(top_10_marcas)

       # 10) Qual o preço médio por marca
    st.subheader("Preço Médio por Marca")
    col1, col2 = st.columns([4, 2])
    df_non_zero_prices = df[df['preco_novo'] != 0]
    preco_medio_por_marca = df.groupby('marca')['preco_novo'].mean().sort_values(ascending=False).round(2)
    col1.bar_chart(preco_medio_por_marca)
    preco_medio_por_marca_formatted = preco_medio_por_marca.apply(lambda x: '{:.2f}'.format(x))
    col2.write(preco_medio_por_marca_formatted)


    #11) Qual a satisfação por marca
    st.subheader('Satisfação por marca')
    col1, col2 = st.columns([4, 2])
    df_non_zero_reviews = df[df['nota'] > 0]
    satisfaction_by_brand = df_non_zero_reviews.groupby('marca')['nota'].mean().sort_values(ascending=False).round(1)
    col1.bar_chart(satisfaction_by_brand)
    col2.write(satisfaction_by_brand)

except Exception as e:
    st.error(f"Ocorreu um erro ao processar os dados: {str(e)}")

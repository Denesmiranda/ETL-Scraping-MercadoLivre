# **Web Scraping - Mercado-Livre**
#
#

![etl](https://github.com/Denesmiranda/ETL-Scraping-MercadoLivre/assets/56989172/9a10a361-68a0-44ac-8474-8ca738060f21)

O projeto consiste em um conjunto de scripts em Python para coletar, limpar, processar e visualizar dados relacionados aos tênis de corrida masculinos disponíveis no Mercado Livre, utilizando-se de técnicas de Web Scraping para extrair informações detalhadas dos produtos, como marca, nome, preços antigos e novos, notas e quantidades de avaliações. Posteriormente, organiza e apresenta esses dados de forma estruturada e interativa.

### Processo
**Etapa 1**<br>
mercadolivre.py: implementa um **Web Crawler** utilizando a biblioteca Scrapy em Python. É responsável por fazer **Web Scraping** nas páginas de resultados de pesquisa do Mercado Livre. Extrai informações específicas de cada produto. Os dados coletados são então estruturados em um formato de dicionário (Json) e enviados para o pipeline do Scrapy para posterior processamento ou armazenamento.

**_Comando para rodar o crawl_**
<pasta src>
```bash
scrapy crawl mercadolivre -o ../data/data.jsonl
```
**Etapa 2**<br>
main.py: Os dados coletados previamente são carregados de um arquivo JSON. Com o Pandas, é realizado um trabalho de transformação, como a origem das informações, data/hora da coleta dos dados, conversão de tipos, tratamento de valores nulos e formatação de valores. Em seguida, os dados transformados são armazenados de forma estruturada em um banco de dados SQLite e em um arquivo CSV.

**_Comando para rodar o Pandas_**
<pasta src>
```bash
python transformacao/main.py
```
**Etapa 3**<br>
app.py: conecta com um banco de dados SQLite e carregando os dados da tabela em um DataFrame do Pandas. Em seguida, apresenta esses dados de forma interativa em uma aplicação Streamlit. 

**_Comando para rodar a apresentação das análises_**
<pasta src>
```bash
streamlit run dashboard/app.py 
```
![view](https://github.com/Denesmiranda/ETL-Scraping-MercadoLivre/assets/56989172/1473cff8-e9d4-4457-87bc-89b673068fc2)

### Tecnologias utilizadas

* **Python:** Linguagem de programação principal utilizada para desenvolver os scripts.
* **Scrapy:** Uma biblioteca em Python utilizada para fazer web scraping de forma eficiente e escalável.
* **Pandas:** Uma biblioteca em Python amplamente utilizada para manipulação e análise de dados.
* **SQLite:** Um sistema de gerenciamento de banco de dados leve e embutido, utilizado para armazenar os dados coletados.
* **Streamlit:** Uma biblioteca em Python para a criação de aplicativos web interativos para visualização de dados.
* **JSON:** Formato de arquivo utilizado para armazenar os dados coletados por web scraping.
* **CSV:** Formato de arquivo utilizado para armazenar os dados transformados em um formato tabular.
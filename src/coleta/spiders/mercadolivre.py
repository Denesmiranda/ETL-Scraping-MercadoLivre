import scrapy

class MercadoLivreSpider(scrapy.Spider):
    
    name = 'mercadolivre' 
    start_urls = ['https://lista.mercadolivre.com.br/tenis-corrida-masculino'] 
    page_count = 1 # Contador de página
    max_pages = 10 # Número máximo de páginas a serem processadas. Capturando 540 produtos (54 por página)

    def parse(self, response):
        produtos = response.css('div.ui-search-result__content')  # Seleciona todos os elementos que contêm informações sobre os produtos
        
        # Variável para contar a quantidade de produtos coletados
        #count = 0

        # Loop para capturar cada produto encontrado na página
        for produto in produtos:
            #if count < 18:  # Limita a coleta a apenas 3 produtos
                #count += 1
                
                
                # Cria um dicionário com os dados extraídos e o envia para o pipeline do Scrapy usando yield.
                yield {
                    'marca': produto.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                    'nome': produto.css('h2.ui-search-item__title::text').get(),

                    # Extrai o preço antigo (reais e centavos)
                    'preco_antigo_reais': produto.css('s.andes-money-amount--previous span.andes-money-amount__fraction::text').get(),
                    'preco_antigo_centavos': produto.css('s.andes-money-amount--previous span.andes-money-amount__cents::text').get(),
                    
                    # Extrai o preço novo (reais e centavos)
                    'preco_novo_reais': produto.css('span.andes-money-amount--cents-superscript span.andes-money-amount__fraction::text').get(),
                    'preco_novo_centavos': produto.css('s.andes-money-amount--previous span.andes-money-amount__cents::text').get(),

                    'nota': produto.css('span.ui-search-reviews__rating-number::text').get(),
                    'qtde_avaliacoes': produto.css('span.ui-search-reviews__amount::text').get()
                }
            #else:
                #break  # Sai do loop após encontrar 3 produtos

        # Verifica se ainda há páginas a serem processadas e faz a requisição para a próxima página    
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)

import requests
import os
from bs4 import BeautifulSoup

def requisitar_site(siteUrl):
    conteudoSite = requests.get(siteUrl).content
    analisar_requisicao(conteudoSite)

def analisar_requisicao(conteudoRequisicao):
    objBs4 = BeautifulSoup(conteudoRequisicao, "html.parser")

    marcas = objBs4.find_all('div', {'class': 'product-box-brand'})
    nomes = objBs4.select('div.catalog-content p.product-box-title')
    links = objBs4.find_all('a', {
        'class': 'product-box-link is-lazyloaded image product-image-rotate'
    })
    precos = objBs4.find_all('span', {'class': 'product-box-price-from'})

    for marca, nome, link, preco in zip(marcas, nomes, links, precos):
        marca = tratamento_dados(marca.text, 'Texto')
        nome = tratamento_dados(nome.text, 'Texto')
        link = link['href']
        preco = tratamento_dados(preco.text, 'Preco')
        
        armazenar_dados(
            f'{marca};{nome};{link};{preco}\n'
        )

        print (f'{marca} | {nome} | {link} | {preco}')

def tratamento_dados(dadoObtido, tipoString):
    if tipoString == 'Preco':
        return str(dadoObtido).replace('R$','').strip()
    else:
        return str(dadoObtido).replace(';',',').strip()

def armazenar_dados(dadosObtidos):
    arquivo = open('roupas.csv', 'a+', encoding='utf-8')
    arquivo.write(dadosObtidos)
    arquivo.close()

def inicio_crawler():
    contador = 1
    while True:
        print (f'PAGINA {contador}')
        url_dafiti = f'https://www.dafiti.com.br/roupas-femininas/?page={contador}'
        requisitar_site(
            url_dafiti
        )
        contador+=1

inicio_crawler()
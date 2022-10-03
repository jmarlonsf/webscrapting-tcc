import json
import time
from copy import deepcopy
from datetime import datetime
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver_path = r"C:\\chromedriver\\chromedriver_win32\\chromedriver.exe"

url_base = 'https://www.karvi.com.br'

filename = 'D:\\TCC\\datasets\\karvi.csv'

tipos = ['CONVERTIBLE', 'COUPE', 'HATCHBACK', 'PICKUP', 'SEDAN', 'SUV', 'WAGON']


def get_bs(page=1):
    url = '{0}/carros-usados/{1}'
    if page > 1:
        url = url.format(url_base, 'p-{0}/'.format(page))
    else:
        url = url.format(url_base, '')

    print(url)
    html = urlopen(url)
    # Busca página informada
    return BeautifulSoup(html, 'html.parser')


def load_card_list(bs, page):
    # Busca todos os cards da página
    rows = []
    cards = bs.find_all('div', {"class": "UsedCatalog_cardList__8Zn8l"})[0].find('section').find_all('section')
    for card in cards:
        href = card.contents[1]['href']
        # consultar pagina

        url = '{0}{1}'.format(url_base, href)
        print(url)
        browser = webdriver.Chrome(executable_path=driver_path)
        browser.get(url)
        # html = urlopen(url)
        time.sleep(3)

        html = browser.page_source
        bs = BeautifulSoup(html, 'html.parser')
        browser.close()

        data = json.loads(bs.find('script', {"id": "__NEXT_DATA__"}).text)
        data = data['props']['pageProps']['usedCar']

        origem = 'karvi'
        stock_id = data['id']
        marca = data['brand']
        modelo = data['model']
        versao = data['version']

        anomodelo = ''
        anos = data['year'].split('/')
        if len(anos) > 1:
            anomodelo = anos[1]
        else:
            anomodelo = anos[0]

        quilometragem = data['mileage']
        transmissao = data['transmission']
        promocao = 0
        preco = data['price']
        cidade = data['city']
        combustivel = data['fuel']
        portas = data['doors']
        tracao = 0
        chassi = data['bodyType']

        var = {'stock_id': stock_id, 'marca': marca, 'modelo': modelo, 'versao': versao.strip(),
               'transmissao': transmissao, 'anomodelo': anomodelo, "preco": preco, 'promocao': promocao,
               'quilometragem': quilometragem, 'origem': origem, 'tracao': tracao,
               'cidade': cidade, 'combustivel': combustivel, 'portas': portas, "chassi": chassi,
               'payload': data}

        print('Veiculo {0}'.format(var))
        rows.append(deepcopy(var))
        print('linha {0} page {1}'.format(len(rows), page))

    print('Salvando page {0} da cidade {1} e combustivel {2} - Quantidade'.format(page, cidade, combustivel, len(rows)))
    df = None
    df = pd.DataFrame.from_dict(rows)
    print(df)
    df.to_csv(path_or_buf=filename, mode='a', index=False, header=False)
    print('Salvo!')


def load_all_types(page):
    try:
        start = datetime.now()
        bs = get_bs(page)
        notfound = bs.find('h2').text
        if notfound.strip() == 'Não encontramos o que você estava buscando':
            return
        # ultima pagina
        x = bs.find('span', {"id": "page"}).find_parent().find_all('span')[1].text.strip()
        last = int(x)
        print('Page {0}/{1}'.format(page, last))

        load_card_list(bs, page)

        print('pausando')
        finish = datetime.now()
        print("inicio page - {}".format(start))
        print("fim page - {}".format(finish))
        time.sleep(3)
        print('voltando')
        page += 1
        if page <= last:
            load_all_types(page)
    except Exception:
        print("retentando page {}", page)
        load_all_types(page)
        time.sleep(2)


if __name__ == '__main__':
    print("inicio")
    page = 1
    load_all_types(page)
    print("fim")

import json
import time
from copy import deepcopy
from urllib.request import urlopen
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver_path = r"C:\\chromedriver\\chromedriver_win32\\chromedriver.exe"

url_base = 'https://www.kavak.com'

filename = 'D:\\TCC\\datasets\\kavak.csv'

tipos = ['CONVERTIBLE', 'COUPE', 'HATCHBACK', 'PICKUP', 'SEDAN', 'SUV', 'WAGON']


def get_bs(page=1):
    url = '{0}/br/{1}carros-usados'
    if page > 1:
        url = url.format(url_base, 'page-{0}/'.format(page))
    else:
        url = url.format(url_base, '')

    print(url)
    html = urlopen(url)
    # Busca página informada
    return BeautifulSoup(html, 'html.parser')


def commaIfNotEmpty(description):
    if len(description) > 0:
        description += ', '


def fuelName(description=''):
    fuel = ''
    if 'DIESEL' in description.upper():
        fuel += 'DIESEL'

    if 'GASOLINA' in description.upper():
        commaIfNotEmpty(description)
        fuel += 'GASOLINA'

    if 'HIBRIDO' in description.upper():
        commaIfNotEmpty(description)
        fuel += 'HIBRIDO'

    if 'FLEX' in description.upper():
        commaIfNotEmpty(description)
        fuel += 'FLEX'

    return fuel


def load_card_list(bs, page):
    # Busca todos os cards da página
    rows = []
    cards = bs.find_all('app-card-car')
    for card in cards:
        href = card.contents[0]['href']
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
        scripts = bs.find_all('script')
        data = None
        for script in scripts:
            if '&q;' in script.text:
                x = json.loads(script.text.replace('&q;', '\"'))
                data = x['vip']['data']

        origem = 'kavak'
        stock_id = data['id']
        marca = data['make']
        modelo = data['model']
        versao = data['version']
        anomodelo = data['carYear']
        quilometragem = data['km']
        transmissao = data['transmission']

        x = bs.find('span', string='R$')
        z = None
        if x is not None:
            y = x.find_parent()
            if y is not None:
                z = y.text.replace('R$ ', '')
        promocao = 0
        if z is not None:
            promocao = z.strip()
        else:
            promocao = data['price']

        preco = data['price']
        cidade = data['region']['name']

        js = json.loads(bs.find('script', type='application/ld+json').text)

        combustivel = ''
        if len(js['fueltype'].strip()) > 0:
            combustivel = js['fueltype']
        else:
            combustivel = fuelName(data['trim'])

        portas = 0
        for x in data['features']['otherAccessories']:
            if x['name'] == 'Exterior':
                for y in x['categories']:
                    if y['name'] == 'Portas':
                        for z in y['items']:
                            if z['code'] == 'number_doors':
                                portas = z['value']

        tracao = 0

        try:
            if data['features']['mainAccessories'] is not None:
                if data['features']['mainAccessories']['items'] is not None:
                    for d in data['features']['mainAccessories']['items']:
                        if d['name'] == 'Tração':
                            tracao = d['value']
        except KeyError:
            print("mainAccessories s age is unknown.")
            tracao = 0



        var = {'stock_id': stock_id, 'marca': marca, 'modelo': modelo, 'versao': versao.strip(),
               'transmissao': transmissao, 'anomodelo': anomodelo, "preco": preco, 'promocao': promocao,
               'quilometragem': quilometragem, 'origem': origem, 'tracao': tracao,
               'cidade': cidade, 'combustivel': combustivel, 'portas': portas,
               'payload': data}

        print('Veiculo {0}'.format(var))
        rows.append(deepcopy(var))
        print('linha {}'.format(len(rows)))

    print('Salvando page {0} da cidade {1} e combustivel {2} - Quantidade'.format(page, cidade, combustivel, len(rows)))
    df = None
    df = pd.DataFrame.from_dict(rows)
    print(df)
    df.to_csv(path_or_buf=filename, mode='a', index=False, header=False)
    print('Salvo!')


def load_all_types(page):
    start = datetime.now()
    bs = get_bs(page)
    notfound = bs.find('h2').text
    if notfound.strip() == 'Não encontramos o que você estava buscando':
        return
    # ultima pagina
    last = int(bs.find('span', 'total').text.strip())
    print('Page {0}/{1}'.format(page, last))

    load_card_list(bs, page)

    print('pausando')
    finish = datetime.now()
    print("inicio page - {}".format(start))
    print("fim page - {}".format(finish))
    time.sleep(5)
    print('voltando')
    page += 1
    if page <= last:
        load_all_types(page)


if __name__ == '__main__':
    print("inicio")
    page = 50
    load_all_types(page)
    print("fim")

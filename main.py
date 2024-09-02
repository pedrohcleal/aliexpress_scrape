from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from chrome_config import driver
import json, random
from time import sleep
from pprint import pprint

def e_primeira_compra(driver: webdriver.Chrome, wait_time):
    class_name = "price-banner--container--tdrR7MT"
    try:
        boole = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return True
    except TimeoutException:
        return False


def preco_produto(driver: webdriver.Chrome, wait_time):
    class_name = 'product-price-current'
    try:
        preco_element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        preco = preco_element.text
        return preco
    except TimeoutException as err:
        print('preço do produto não encontrado')
        raise err
    
    
def verificar_estoque(driver: webdriver.Chrome, wait_time):
    class_name = "#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-right > div > div > div.message--wrap--G6K5LJD"
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, class_name))
        )
        return False
    except TimeoutException:
        return True


def tratar_texto_frete(texto: str):
    if not texto:
        return {'free_shipping': 0, 'shipping': 0}  #---------- Sem preço de frete/ sem estoque
    texto = texto.strip()
    if texto == 'Frete grátis':
        return {'free_shipping': 1, 'shipping': 0}   #--------- Frete grátis comum
    elif 'acima de' in texto:   
        index_reais = texto.index('R$')              
        preco_frete = texto[index_reais::]           
        return {'free_shipping': 2, 'shipping': preco_frete}  # Frete grátis acima de R$99,00
    else:                                               
        index_reais = texto.index('R$')              
        preco_frete = texto[index_reais::]
        return {'free_shipping': 3, 'shipping': preco_frete}  # Frete: R$20,74


def texto_frete(driver: webdriver.Chrome, wait_time):
    selector = "#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-right > div > div > div:nth-child(3) > div:nth-child(1) > div > div > div.dynamic-shipping-line.dynamic-shipping-titleLayout > * > span > strong"
    texto_frete = ""
    try:
        frete_elemento = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        texto_frete = frete_elemento.text
        print(f'texto do frete = {texto_frete}')
    except TimeoutException:
        print('frete não encotrado')
    return tratar_texto_frete(texto_frete)

def get_ali_id(url):
    try:
        ali_id = url.split('/')[-1]
        index_html = ali_id.index('.html')
        ali_id = ali_id[:index_html:]
        int(ali_id)
        return ali_id
    except ValueError as err:
        print(f'O id aliexpress está corrompido, por favor verificar URL -> {url}')
        raise err

if __name__ == '__main__':
    print("Iniciando Scraping")
    json_file = open('exemplo.json').read() # inserir nome do arquivo para ser lido ('exemplo.json')
    json_load = json.loads(json_file)
    try:
        final_json = []
        for json_dicts in json_load:
            print(f'Verificando URL = {json_dicts['link']}')
            
            url = json_dicts['link']
            dados_item = {}
            dados_item['idProduct'] = json_dicts["idProduct"]
            dados_item['ali_id'] = get_ali_id(url)
            dados_item['ali_link'] = url
    
            driver.get(url)
            sleep(random.randrange(3,7))
            
            titulo = driver.find_element(By.CSS_SELECTOR,'#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-left > div.pdp-info > div.pdp-info-right > div.title--wrap--UUHae_g > h1')
            dados_item['ali_nome_produto'] = ' '.join((titulo.text).split(' ')).replace('\n','').strip()
            dados_item['ali_nome_produto'] = titulo.text
            
            max_wait_time = 4
            if e_primeira_compra(driver, max_wait_time):
                dados_item['e_primeira_compra'] = True
            else:
                dados_item['e_primeira_compra'] = False
                
            if verificar_estoque(driver, max_wait_time):
                dados_item['em_estoque'] = True
            else:
                dados_item['em_estoque'] = False
                
            dados_item['frete'] = texto_frete(driver, max_wait_time)
            dados_item['preco'] = preco_produto(driver, max_wait_time)              
            pprint(dados_item)
            print()
            final_json.append(dados_item)
        with open('final_updates_ali.json', 'w') as file:
            json.dump(final_json, file, indent=4)
            
    finally:
        print('fim scraping')
        driver.quit()
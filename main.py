from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from chrome_config import driver

from time import sleep


def e_primeira_compra(driver: webdriver.Chrome, wait_time):
    class_name = "price-banner--container--tdrR7MT"
    try:
        boole = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return True
    except TimeoutException:
        print('elemento de 1ª compra não encontrado')
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
        return {'free_shipping': 0, 'shipping': 0}        # sem preço de frete/ sem estoque
    texto = texto.strip()
    if texto == 'Frete grátis':
        return {'free_shipping': 1, 'shipping': 0}        # frete grátis 
    elif 'acima de' in texto:   
        index_reais = texto.index('R$')              
        preco_frete = texto[index_reais::]           # Frete grátis acima de R$99,00
        return {'free_shipping': 2, 'shipping': preco_frete}  
    else:                                               
        index_reais = texto.index('R$')              # Frete: R$20,74
        preco_frete = texto[index_reais::]
        return {'free_shipping': 3, 'shipping': preco_frete}


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
        ali_id = url.split('/')[-1]#.replace('.html','')
        index_html = ali_id.index('.html')
        ali_id = ali_id[:index_html:]
        int(ali_id)
    except ValueError as err:
        print('O id aliexpress está corrompido, por favor verificar URL ')
        raise err

if __name__ == '__main__':
    print("Iniciando Scraping")
    
    urls = [
        "https://pt.aliexpress.com/item/1005007012057921.html", #frete gratis total
        "https://pt.aliexpress.com/item/1005005970704465.html",
        "https://pt.aliexpress.com/item/1005006437203100.html",
        "https://pt.aliexpress.com/item/1005007638094274.html?spm=a2g0o.productlist.main.3.7ff4VPJiVPJizS&algo_pvid=1b3bf686-46d3-4c12-a9c9-9ed0c24f9a16&algo_exp_id=1b3bf686-46d3-4c12-a9c9-9ed0c24f9a16-1&pdp_npi=4%40dis%21BRL%213567.42%213567.42%21%21%21600.00%21600.00%21%4021015b2417251532835424525e307e%2112000041598359577%21sea%21BR%210%21ABX&curPageLogUid=g5ZgFYiSH7Z7&utparam-url=scene%3Asearch%7Cquery_from%3A",
        "https://pt.aliexpress.com/item/33021094536.html?spm=a2g0o.order_list.order_list_main.225.1d36caa4l9n3LD&gatewayAdapt=glo2bra", 
        "https://pt.aliexpress.com/item/4001316832800.html?spm=a2g0o.order_list.order_list_main.45.173bcaa4zXslqC&gatewayAdapt=glo2bra", # frete acima de 99
        "https://pt.aliexpress.com/item/1005007623311936.html?spm=a2g0o.productlist.main.5.4e6030ecYJ5hRa&pdp_ext_f=%7B%22sku_id%22%3A%2212000041545490702%22%7D&utparam-url=scene%3Asearch%7Cquery_from%3Acategory_navigate",
    ]       # frete de ....
    try:
        for url in urls:
            print(f'URL = {url}') 
            
            dados_item = {}
            dados_item['ali_id'] = get_ali_id(url)
            dados_item['ali_link'] = url
            
            driver.get(url)
            sleep(2)
            
            titulo = driver.find_element(By.CSS_SELECTOR,'#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-left > div.pdp-info > div.pdp-info-right > div.title--wrap--UUHae_g > h1')
            print(f'Nome do produto {titulo.text}')
            dados_item['ali_nome_produto'] = titulo.text
            
            max_wait_time = 2 # tempo máximo pra esperar pra achar elemento no site
            if e_primeira_compra(driver, max_wait_time):
                print('stock true (tem promo de 1ª compra)')
                dados_item['e_primeira_compra'] = True
            else:
                print('stock false (não tem promo de 1ª compra)')
                dados_item['e_primeira_compra'] = False
                
            if verificar_estoque(driver, max_wait_time):
                dados_item['em_estoque'] = True
                print('Produto com estoque disponível')
            else:
                dados_item['em_estoque'] = False
                print('Produto sem estoque disponível')
            
            frete = texto_frete(driver, max_wait_time)
            dados_item['frete'] = frete
            
            dados_item['preco'] = preco_produto(driver, max_wait_time)              
            
            import pprint
            pprint.pprint(dados_item.items())
    finally:
        print('fim scraping')
        driver.quit()
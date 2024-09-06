from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def e_primeira_compra(driver, wait_time):
    class_name = "price-banner--container--tdrR7MT"
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return True
    except TimeoutException:
        return False

def preco_produto(driver, wait_time):
    class_name = "product-price-current"
    try:
        preco_element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        preco = preco_element.text
        return preco
    except TimeoutException as err:
        print("preço do produto não encontrado")
        raise err

def verificar_estoque(driver, wait_time):
    class_name = "#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-right > div > div > div.message--wrap--G6K5LJD"
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, class_name))
        )
        return False
    except TimeoutException:
        return True

def texto_frete(driver, wait_time, tratar_texto_frete):
    selector = "#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-right > div > div > div:nth-child(3) > div:nth-child(1) > div > div > div.dynamic-shipping-line.dynamic-shipping-titleLayout > * > span > strong"
    texto_frete = ""
    try:
        frete_elemento = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        texto_frete = frete_elemento.text
        print(f"texto do frete = {texto_frete}")
    except TimeoutException:
        print("frete não encotrado")
    return tratar_texto_frete(texto_frete)

def tem_captcha(driver, wait_time):
    class_name = "rc-anchor-content"
    try:
        captcha = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return True
    except TimeoutException as err:
        print("captcha não encontrado")
        return False

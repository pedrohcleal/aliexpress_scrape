from scraping.scraping_functions import e_primeira_compra, preco_produto, verificar_estoque, texto_frete, tem_captcha
from scraping.chrome_config import get_driver
from utils.frete_utils import tratar_texto_frete
from utils.ali_id_utils import get_ali_id
from utils.json_handler import load_json_file, save_json_file
from selenium.webdriver.common.by import By
import pprint
from time import sleep
import random

if __name__ == "__main__":
    print("Iniciando Scraping")
    path_json = "exemplo.json"
    json_load = load_json_file(path_json)
    contador = 0
    driver = get_driver()
    sleep(1)
    print(f'Json lido = {path_json}')
    try:
        final_json = []
        for json_dict in json_load:
            contador += 1
            url = json_dict["link"]
            dados_item = {
                "idProduct": json_dict["idProduct"],
                "id_ali": get_ali_id(url),
                "link_ali": url,
                "oldPrice": json_dict["oldPrice"],
                "oldStock": json_dict["oldStock"]
            }

            print(f'Carregando página, URL = {json_dict["link"]}')
            driver.get(url)
            sleep(random.randrange(10, 20))  # ajustar tempo de mundança de link -> randrange(10,20) -> escolhe tempo aleatorio entre 10 a 20segundos

            titulo = driver.find_element(
                By.CSS_SELECTOR,
                "#root > div > div.pdp-body.pdp-wrap > div > div.pdp-body-top-left > div.pdp-info > div.pdp-info-right > div.title--wrap--UUHae_g > h1",
            )
            dados_item["ali_nome_produto"] = titulo.text

            max_wait_time = 1
            dados_item["frete"] = texto_frete(driver, max_wait_time, tratar_texto_frete)
            dados_item["newPrice"] = preco_produto(driver, max_wait_time)

            if e_primeira_compra(driver, max_wait_time):
                dados_item["e_primeira_compra"] = True
            else:
                dados_item["e_primeira_compra"] = False

            if verificar_estoque(driver, max_wait_time):
                dados_item["em_estoque"] = True
            else:
                dados_item["em_estoque"] = False

            final_json.append(dados_item)
            print('Produto lido:')
            pprint.pprint(dados_item)
            print(f'Quantidade de itens lidos até o momento -> {contador}')
            print()
        
        save_json_file("final_updates_ali.json", final_json)

    finally:
        print("fim scraping")
        driver.quit()

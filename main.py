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
            final_json.append(dados_item)
            print('Produto lido:')
            pprint.pprint(dados_item)
            print(f'Quantidade de itens lidos até o momento -> {contador}')
            print()
        
        save_json_file("final_updates_ali.json", final_json)

    finally:
        print("fim scraping")
        driver.quit()

# Aliexpress Scraper

Este projeto realiza scraping de dados de produtos do Aliexpress, extraindo informações como nome do produto, preço, disponibilidade em estoque, detalhes sobre frete e se é a primeira compra.

## Estrutura de Arquivos

- `/chrome_config`: Configuração do driver do Chrome para uso com Selenium.
- `main.py`: Script principal que executa o scraping dos produtos.
- `exemplo.json`: Arquivo de exemplo contendo os links e IDs dos produtos a serem analisados.

## Dependências

- `selenium`
- `chromedriver`
- `json`
- `random`

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/pedrohcleal/aliexpress_srape.git
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv     # No Linux: python3 -m venv venv
   venv\Scripts\activate   # No Linux: source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o driver do Chrome na pasta `chrome_config` caso seja necessário, mas já está pronto para uso

### Como Usar

1. Edite o arquivo `exemplo.json` com os produtos que deseja consultar. O formato é:
   ```json
   [
       {
           "link": "https://pt.aliexpress.com/item/1005007012057921.html",
           "idProduct" : 1,
           "oldPrice": 5.50,
           "oldStock" : 10
       },
       {
           "link": "https://pt.aliexpress.com/item/1005005970704465.html",
           "idProduct" : 2,
           "oldPrice": 5.50,
           "oldStock" : 10
       },
      ...
   ]
   ```

2. Execute o script:
   ```bash
   python main.py
   ```

3. O resultado será salvo no arquivo `final_updates_ali.json`.

### Funcionalidades

- **e_primeira_compra**: Verifica se é a primeira compra do usuário no produto.
- **preco_produto**: Extrai o preço atual do produto.
- **verificar_estoque**: Verifica se o produto está em estoque.
- **texto_frete**: Extrai e trata informações sobre o frete.
- **get_ali_id**: Extrai o ID do produto a partir do link da página.

### Exemplo de Saída

O script gera um arquivo `final_updates_ali.json` com as seguintes informações:

```json
[
    {
        "idProduct": "123",
        "ali_id": "456789",
        "ali_link": "https://www.aliexpress.com/item/example.html",
        "ali_nome_produto": "Exemplo de Produto",
        "e_primeira_compra": true,
        "em_estoque": false,
        "frete": {"free_shipping": 1, "shipping": "0"},
        "preco": "R$100,00",
        "OldStock": 20,
        "oldPrice": 23.40,
    }
]
```

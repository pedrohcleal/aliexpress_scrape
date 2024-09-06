def tratar_texto_frete(texto: str):
    if not texto:
        return {
            "free_shipping": 0,
            "shipping": 0,
        }
    texto = texto.strip()
    if texto == "Frete grátis":
        return {"free_shipping": 1, "shipping": 0}
    elif "acima de" in texto:
        index_reais = texto.index("R$")
        preco_frete = texto[index_reais::]
        return {
            "free_shipping": 2,
            "shipping": preco_frete,
        }
    else:
        index_reais = texto.index("R$")
        preco_frete = texto[index_reais::]
        return {"free_shipping": 3, "shipping": preco_frete}

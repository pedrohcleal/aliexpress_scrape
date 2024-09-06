def get_ali_id(url):
    try:
        ali_id = url.split("/")[-1]
        index_html = ali_id.index(".html")
        ali_id = ali_id[:index_html]
        int(ali_id)
        return ali_id
    except ValueError as err:
        print(f"O id aliexpress está corrompido, por favor verificar URL -> {url}")
        raise err

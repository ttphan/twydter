def check_status(client, url):
    return client.get(url).status_code

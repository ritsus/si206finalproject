import json
import ssl
import os
import requests

def searchProduct(product):
    try:
        request_url = 'https://api.edamam.com/search?q=chicken&app_id=15607767&app_key=866dcff09fa31e2e0e2249d52177fe20&from=0&to=3&calories=591-722&health=alcohol-free'
        r = requests.get(request_url)
        d1 = json.loads(r.text) 
    except:
        print("error when reading from file")
        d1 = {}
    return d1

if __name__ == "__main__":
    print(searchProduct('chicken'))



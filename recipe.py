import json
import os
import requests
import sqlite3

def create_request_url(product):
    app_id = "15607767"
    app_key = "866dcff09fa31e2e0e2249d52177fe20"
    
    #retrieves 100 recipes for the product given
    url = "https://api.edamam.com/search?q={}&app_id={}&app_key={}&from=0&to=100".format(product, app_id, app_key)
    return url


def searchRecipe(product):
    recipe = []
    try:
        request_url = create_request_url('chicken')
        r = requests.get(request_url)
        d1 = json.loads(r.text) 
        
        '''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        CACHE_FNAME = dir_path + '/' + "rec.json"
        outFile = open(CACHE_FNAME, 'w', encoding="utf-8")
        outFile.write(json.dumps(d1) )
        outFile.close()
        '''

    except:
        print("error when reading from file")
        d1 = {}
    
    for r in d1['hits']:
        recipe.append(r)

    return recipe

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn




if __name__ == "__main__":
    print(searchRecipe("chicken"))



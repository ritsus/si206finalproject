import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt

def create_request_url(product):
    app_id = "15607767"
    app_key = "866dcff09fa31e2e0e2249d52177fe20"

    #retrieves 100 recipes for the product given
    url = "https://api.edamam.com/search?q={}&app_id={}&app_key={}&from=0&to=100".format(product, app_id, app_key)
    return url

def searchRecipe(product):
    recipe = []
    try:
        request_url = create_request_url(product)
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
        recipe.append(r['recipe'])
    return recipe

def setUpDatabase(cur, conn, product):
    recipe = searchRecipe(product)
    cur.execute("DROP TABLE IF EXISTS Recipes")
    cur.execute("CREATE TABLE IF NOT EXISTS Recipes (dish_id INTEGER PRIMARY KEY, main_product, dish, ingredients, calories)")

    for r in recipe:
        dish = r['label']
        ingredient = ''
        calories = int(r['calories'])
        for ing in r['ingredientLines']:
            ingredient += ing + '\n'
            
        cur.execute('''INSERT INTO Recipes (main_product, dish, ingredients, calories) 
            VALUES (?,?,?,?)''',(product, dish, ingredient, calories) )

    conn.commit()

def graphTop10Caloires(cur, conn):
    cur.execute("SELECT * FROM Recipes")
    raw_recipe = cur.fetchall()
    top_ten_calorie = sorted(raw_recipe, key=lambda x:x[4], reverse=True)
    top_ten_calorie = top_ten_calorie[:10]
    name = []
    calorie = []

    for r in top_ten_calorie:
        name.append(r[2])
        calorie.append(r[-1])
    
    
   
    h = plt.bar(range(len(calorie)), calorie)
    plt.xticks(range(len(calorie)), name, fontsize=8, rotation=30)
    plt.title("Recipes with Top 10 Calories")
    plt.grid()
    plt.show()
    


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    setUpDatabase(cur, conn, 'beef')
    graphTop10Caloires(cur, conn)

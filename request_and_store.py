import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt

def create_request_url(product):
    food_search_app_id = "15607767"
    food_search_app_key = "866dcff09fa31e2e0e2249d52177fe20"
    # ingredient_key = "8df685917a724c55a3418820ffade1dc"
    # ingredient_key = "29e9db09a08e4ee29dfa3679d6d698ae"
    # ingredient_key = "9fc298539bbd4f6f802a43347cad44e4"
    ingredient_key = "57aedad6ec9349a390d0d63b37635c4c"
    food_search_url = "https://api.edamam.com/search?q={}&app_id={}&app_key={}".format(product, food_search_app_id, food_search_app_key)
    ingredient_url = "https://api.spoonacular.com/recipes/parseIngredients?apiKey=" + ingredient_key
    return(food_search_url, ingredient_url)

    # API Request - recipe search
def requestRecipe(cur, food_search_url):
    # Start index for search
    start = None
    cur.execute("SELECT max(dish_id) FROM Recipes")
    try:
        row = cur.fetchone()
        if row is None:
            start = 0
        else:
            start = row[0]
    except:
        start = 0

    if start is None: start = 0
    
    end = start + 20
    recipe = []
    # Limit search return 20 recieps at a time
    food_search_url += "&from={}&to={}".format(str(start), str(end))
    try:
        r = requests.get(food_search_url)
        d1 = json.loads(r.text) 
    except:
        print("error when reading from file")
        d1 = {}
    
    for r in d1['hits']:
        recipe.append(r['recipe'])

    return recipe


def setUpDatabase(cur, conn, product, recipe):
    for r in recipe:
        dish = r['label']
        ingredient = ''
        calories = int(r['calories'])
        carbs = int(r['totalNutrients']['CHOCDF']['quantity'])
        protein = int(r['totalNutrients']['PROCNT']['quantity'])
        fat = int(r['totalNutrients']['FAT']['quantity'])

        
        for ing in r['ingredientLines']:
            ingredient += ing + '\n'
            
        cur.execute('''INSERT INTO Recipes (main_product, dish, ingredients, calories) 
            VALUES (?,?,?,?)''',(product, dish, ingredient, calories) )

        cur.execute('''INSERT INTO Nutrients (Carbs, Protein, FAT) 
            VALUES (?,?,?)''',(carbs, protein, fat) )

    conn.commit()
    # API Request - Find Cost
def requestCost(cur, conn, product, ingredient_url):
    count = 0
    cur.execute("SELECT * FROM Recipes WHERE main_product=?", (product, ))
    all_recipes = cur.fetchall()
    for raw_recipe in all_recipes:
        # Limit to 20 API request at a time
        if(count >= 20):
            print("Retrieved 20 items, limit reached")
            break
        ingre_list = raw_recipe[3]
        dish_id = raw_recipe[0]
        cur.execute("SELECT cost_dic FROM Cost WHERE dish_id=?", (dish_id, ))
        try:
            cur.fetchone()[0]
            print("Retrieved from database")
        except:
            # Not in the database
            count += 1
            payload = {'ingredientList': ingre_list}
            r = requests.post(ingredient_url, data=payload)
            d = json.loads(r.text)
            if len(d) < 2:
                print("Daily limit reached, API limit 150 points/day")
                break
            print("Request from API")
            cost_dic = {}
            for ingre in d:
                try:
                    cost_dic[ingre['original']] = ingre['estimatedCost']['value']
                except:
                    print(ingre['original'], " is not a valid ingredient in the API")
                    continue

            cur.execute('''INSERT INTO Cost (dish_id, cost_dic) 
                VALUES (?,?)''',(dish_id, json.dumps(cost_dic)))
            conn.commit()
        
def main(product):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Cost (dish_id INTEGER PRIMARY KEY, cost_dic TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Recipes (dish_id INTEGER PRIMARY KEY, main_product, dish, ingredients, calories)")
    cur.execute("CREATE TABLE IF NOT EXISTS Nutrients (dish_id INTEGER PRIMARY KEY, Carbs, Protein, Fat)")
    (food_search_url, ingredient_url) = create_request_url(product)
    recipe = requestRecipe(cur, food_search_url)
    setUpDatabase(cur, conn, product, recipe)
    requestCost(cur, conn, product, ingredient_url)

if __name__ == "__main__":
    main()
    

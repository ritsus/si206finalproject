import json
import os
import requests
import sqlite3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# API: https://spoonacular.com/food-api/docs
def parse_ingrdient_url():
    key = "8df685917a724c55a3418820ffade1dc"
    key_url = "apiKey=" + key
    url = "https://api.spoonacular.com/recipes/parseIngredients?" + key_url
    return url  

def extract_from_database(cur, conn, product):
    cur.execute("SELECT * FROM Recipes WHERE main_product=?", (product, ))
    return cur.fetchall()
    

def request_and_calculate_cost(cur, conn, all_recipes):
    count = 0
    for raw_recipe in all_recipes:
        # Limit to 20 API request at a time
        if(count >= 20):
            print("Retrieved 20 items, limit reached")
            break
        ingre_list = raw_recipe[3]
        dish_id = raw_recipe[0]
        dish_name = raw_recipe[2]
        cur.execute("SELECT dollars FROM Cost WHERE dish_id=?", (dish_id, ))
        try:
            cost = cur.fetchone()[0]
            print("Retrieved from database")
        except:
            # Not in the database
            count += 1
            payload = {'ingredientList': ingre_list}
            url = parse_ingrdient_url()
            r = requests.post(url, data=payload)
            d = json.loads(r.text)
            print("Request from API")
            cost = 0.0
            for ingre in d:
                try:
                    cost += ingre['estimatedCost']['value']
                except:
                    print(ingre['original'], " is not a valid ingredient in the API")
            # Convert cents to dollars
            cost = cost / 100 
            cur.execute('''INSERT INTO Cost (dish_id, dish, dollars) 
                VALUES (?,?,?)''',(dish_id, dish_name, cost))
            conn.commit()
        print(cost)

def graphTop10Cost(cur, conn):
    cur.execute("SELECT * FROM Cost")
    raw_recipe = cur.fetchall()
    top_ten_cost = sorted(raw_recipe, key=lambda x:x[2], reverse=True)
    top_ten_cost = top_ten_cost[:10]
    name = []
    cost = []

    for r in top_ten_cost:
        name.append(r[1])
        cost.append(r[2])

    plt.bar(name, cost)
    plt.xticks(range(len(cost)), name, fontsize=6, rotation=30)
    plt.xlabel("Dish")
    plt.ylabel("Cost/$")
    plt.title("Top 10 Cost Recipe")
    plt.grid()
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Cost (dish_id INTEGER PRIMARY KEY, dish TEXT, dollars INTEGER)")
    all_recipes = extract_from_database(cur, conn, "beef")
    request_and_calculate_cost(cur, conn, all_recipes)
    graphTop10Cost(cur, conn)
if __name__ == "__main__":
    main()
    
    
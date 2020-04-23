import json
import os
import requests
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

# API: https://spoonacular.com/food-api/docs
def parse_ingrdient_url():
    key = "8df685917a724c55a3418820ffade1dc"
    key_url = "apiKey=" + key
    url = "https://api.spoonacular.com/recipes/parseIngredients?" + key_url
    return url  

def extract_from_database(cur,conn):
    cur.execute("SELECT * FROM Recipes")
    raw_recipe = cur.fetchone()
    ingre_list = raw_recipe[3]
    return ingre_list

def request(url, ingredient_list):
    payload = {'ingredientList': ingredient_list}
    r = requests.post(url, data=payload)
    d = json.loads(r.text)
    print(d)

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    ingre_list = extract_from_database(cur, conn)
    url = parse_ingrdient_url()
    request(url, ingre_list)
    
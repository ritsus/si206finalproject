import json
import os
import requests
import sqlite3
import translation

def calculate_cost_and_write(language_abr, product):
    path = os.path.dirname(os.path.abspath(__file__))
    write_file = open(path +"/cost.txt", "w")
    write_file_translated = open(path +"/cost_translated.txt", "w", encoding="utf-8")
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    cur.execute("SELECT dish, cost_dic FROM Recipes JOIN Cost ON Recipes.dish_id = Cost.dish_id WHERE main_product=?", (product, ))
    all_recipes = cur.fetchall()
    all_cost = {}
    for recipe in all_recipes:
        cost = 0.0
        dish_name = recipe[0]
        cost_dic = eval(recipe[1])
        for ingre_cost in cost_dic.values():
            cost += ingre_cost
        all_cost[dish_name] = cost/100
    write_file.write(json.dumps(all_cost))
    translated_text = translation.translateText(language_abr, json.dumps(all_cost))
    write_file_translated.write(translated_text)
    
if __name__ == "__main__":
    calculate_cost_and_write("en")

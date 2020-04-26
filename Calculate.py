import json
import os
import requests
import sqlite3

def calculate_cost_and_write():
    path = os.path.dirname(os.path.abspath(__file__))
    write_file = open(path +"/cost.txt", "w")
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    cur.execute("SELECT dish, cost_dic FROM Recipes JOIN Cost ON Recipes.dish_id = Cost.dish_id")
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

def main():
    calculate_cost_and_write()
    
if __name__ == "__main__":
      main()

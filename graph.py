import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import random
    
def graphTop10Caloires(cur, conn, product):
    cur.execute("SELECT * FROM Recipes WHERE main_product=?", (product,))
    raw_recipe = cur.fetchall()
    top_ten_calorie = sorted(raw_recipe, key=lambda x:x[4], reverse=True)
    top_ten_calorie = top_ten_calorie[:10]
    name = []
    calorie = []

    for r in top_ten_calorie:
        name.append(r[2])
        calorie.append(r[-1])

    plt.figure(figsize=(13,7))
    plt.bar(range(len(calorie)), calorie)
    plt.xticks(range(len(calorie)), name, fontsize=6, rotation=20)
    plt.title("Recipes with Top 10 Calories")
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.savefig("top_10_calories.png")

def graphTop10Cost(costs):
    sorted_cost = sorted(costs.items(), key=lambda x:x[1])
    sorted_cost = sorted_cost[:10]
    name, cost = zip(*sorted_cost)
    plt.figure(figsize=(13,7))
    plt.bar(name, cost)
    plt.xticks(range(len(cost)), name, fontsize=6, rotation=20)
    plt.xlabel("Dish")
    plt.ylabel("Cost/$")
    plt.title("Top 10 Cost Recipe")
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.savefig("top_10_cost.png")


def graphNutrients(cur, conn, product):
    cur.execute("SELECT dish, Carbs, Protein, Fat FROM Recipes JOIN Nutrients ON Recipes.dish_id = Nutrients.dish_id WHERE Recipes.main_product=?", (product, ))
    nutrient_list = cur.fetchall()
    # random choose 20 items from the database
    rand_start = random.randint(0, max(1, len(nutrient_list) - 21))
    nutrient_list = nutrient_list[rand_start:min(len(nutrient_list), rand_start + 20)]
    # 
    name, carbs, protein, fat = zip(*nutrient_list)
    x = np.arange(len(name))
    width = 0.3
    fig, ax = plt.subplots(figsize=(13,7))
    rects1 = ax.bar(x - width, carbs, width, label='Carbs')
    rects2 = ax.bar(x, protein, width, label='Protein')
    rects3 = ax.bar(x + width, fat, width, label='Fat')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Nutrients by grams(g)')
    ax.set_title('Nutrient facts')
    ax.set_xticks(x)
    ax.set_xticklabels(name,fontsize = 8, rotation = 30)
    ax.legend()
    fig.tight_layout()
    plt.show()
    plt.savefig("nutrients.png")
    # h = plt.bar(range(len(calorie)), calorie)
    # plt.xticks(range(len(calorie)), name, fontsize=6, rotation=20)
    # plt.title("Recipes with Top 10 Calories")
    # plt.grid()
    # plt.show()

def main(mode, product):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
    if mode == "1":
        graphTop10Caloires(cur, conn, product)
    elif mode == "2":
        read_file = open(path + "/cost.txt", "r")
        costs = json.loads(read_file.read())
        graphTop10Cost(costs)
    elif mode == "3":
        graphNutrients(cur, conn, product)


    
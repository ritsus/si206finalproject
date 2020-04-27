import request_and_store
import Calculate
import graph
import translation


if __name__ == "__main__":
    language = input("Language choice: ")
    abr = translation.lang_abr(language)
    product = input(translation.translateText(abr, "Type of food you are looking for (Ex. pork, beef, fish, etc.): "))
    mode = input(translation.translateText(abr, "What do you care about the most? 1 for calories, 2 for cost, 3 for nutritients: "))
    product = translation.translateText("en", product)


    while True:
        if mode != "1" and mode != "2" and mode != "3":
            mode = input("Invalid mode! Try again:")
        else:
            break
    request_and_store.main(product)
    Calculate.calculate_cost_and_write(abr, product)
    graph.main(mode, product)
    
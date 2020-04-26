import request_and_store
import Calculate
import graph


if __name__ == "__main__":
    product = input("Type of food you are looking for (Ex. pork, beef, fish, etc.): ")
    mode = input("What do you care about? 1 for calories, 2 for cost, 3 for nutritients ")
    while True:
        if mode != "1" and mode != "2" and mode != "3":
            mode = input("Invalid mode! Try again:")
        else:
            break
    # language = input("Language choice: ")
    request_and_store.main(product)
    Calculate.main()
    graph.main(mode)
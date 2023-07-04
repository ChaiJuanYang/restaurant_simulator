"""Created by Chai Juan Yang"""
import random


def order_input():
    """
    Takes input for menu of the day, enter "." to get default menu.
    :return: List of menu in dictionary form.
    """
    print("Welcome! Please enter today's meals : ")
    orders = []
    while True:
        order = input()
        if order == ".":
            break

        values = order.split(",")
        item = {
            "name": values[0],
            "sell_for": float(values[1]),
            "cost_to_make": float(values[2]),
            "cook_time": float(values[3]),
            "cook_time_stdev": float(values[4])
        }
        orders.append(item)

    # print(orders)
    # display_menu(orders)
    return orders


def display_menu(orders):
    """
    Display menu in a specific format after getting an input of today's menu.
    :param orders: Order obtained from order_input()
    :return: Menu in the specific format
    """
    if len(orders) < 1:
        items = {"name": "Budda Bowl (vg)", "sell_for": 25.0, "cost_to_make": 20.0, "cook_time": 10.0,
                 "cook_time_stdev": 3.0}, \
                {"name": "Eye Fillet Steak", "sell_for": 55.0, "cost_to_make": 25.0, "cook_time": 7.0,
                 "cook_time_stdev": 1.0}, \
                {"name": "Spaghetti Bolognese", "sell_for": 30.0, "cost_to_make": 22.0, "cook_time": 40.0,
                 "cook_time_stdev": 5.0}, \
                {"name": "Pad Thai (seafood)", "sell_for": 22.0, "cost_to_make": 17.0, "cook_time": 30.0,
                 "cook_time_stdev": 1.0}
        for i in items:
            orders.append(i)
    # print(orders)
    counter = 1
    for order in orders:
        ret = f"{counter}. Name: {orders[counter - 1]['name']}, Sells: ${orders[counter - 1]['sell_for']}, Costs: ${orders[counter - 1]['cost_to_make']}," \
              f" Takes: {orders[counter - 1]['cook_time']} mins"
        counter += 1
        print(ret)
    # take_order(orders)
    return orders


def take_order(orders):
    """
    Obtain user input to select which meal of choice
    :param orders: Take in menu from previous functions
    :return: Selection of customer and also the menu
    """
    print("\nPlease select your meal from our menu above:")
    no_of_meals = len(orders)

    while True:
        try:
            selection = int(input())
            if selection < 1 or selection > no_of_meals:
                raise ValueError

            print("Now cooking: " + str(orders[selection - 1]["name"]))
            break

        except ValueError:
            print("Invalid Choice. Please enter a valid meal number from the menu.")
    # classify_cooking_for_tip(selection, orders)
    return selection, orders


def classify_cooking_for_tip(selection, orders):
    """
    Classify if the food was over or undercooked, well cooked or slightly under or overcooked. If food is very over or
    undercooked, attempt recooking at most 3 times and calculate total profit from these attempts
    :param selection: Selection of food from customer
    :param orders: The menu obtained previously
    :return: the profit from all the attempts
    """
    avg_cook_time = orders[selection - 1]["cook_time"]
    standard_dev = orders[selection - 1]["cook_time_stdev"]
    counter = 0
    flag = False
    profit = 0  # Initialize profit outside the loop

    while counter < 3:
        actual_time = random.gauss(avg_cook_time, standard_dev)
        status = None
        cook_tip = 0

        if actual_time < avg_cook_time - 2 * standard_dev:
            status = "very undercooked"
            cook_tip = -100
            flag = True
        elif avg_cook_time - 2 * standard_dev <= actual_time <= avg_cook_time - standard_dev:
            status = "slightly undercooked"
            cook_tip = 0
            flag = False
        elif avg_cook_time - standard_dev < actual_time < avg_cook_time + standard_dev:
            status = "well cooked"
            cook_tip = 10
            flag = False
        elif avg_cook_time + standard_dev <= actual_time <= avg_cook_time + 2 * standard_dev:
            status = "slightly overcooked"
            cook_tip = 0
            flag = False
        elif actual_time > avg_cook_time + 2 * standard_dev:
            status = "very overcooked"
            cook_tip = -100
            flag = True

        ret = f"{orders[selection - 1]['name']} was {status} ({round(actual_time, 1)} mins vs {avg_cook_time} mins)"
        print(ret)
        tips = random_tips(cook_tip)
        profit += calculate_profit(selection, orders, tips, cook_tip)  # Accumulate the profit
        counter += 1

        if flag is False:
            break

    if counter == 3:
        print("Giving up after 3 failed attempts")
    print("Overall, the profit for this meal was $" + str(profit) + "\n")  # Print the accumulated profit
    return profit


def random_tips(tips):
    """
    Calculate tips given by customer based on a 0.1 (bad customers for 5% discount), 0.8 (normal customers who don't give
    extra tips),0.1 distribution (generous customers who give extra 5% tip).
    :param tips: Cooking tip obtained from classify_cooking_for_tip()
    :return: randomly distributed extra tip
    """
    freq = random.random()
    if freq < 0.1:
        tip = 5
        print(f"Cooking tip was {tips}%, random tip was {tip}% since the occurrence was " + str(round(freq, 1)))
    elif freq > 0.9:
        tip = -5
        print(f"Cooking tip was {tips}%, random tip was {tip}% since the occurrence was " + str(round(freq, 1)))
    else:
        tip = 0
        print(f"Cooking tip was {tips}%, random tip was {tip}% since the occurrence was " + str(round(freq, 1)))
    return tip


def calculate_profit(selection, orders, random_tip, cooking_tip):
    """
    Calculate total profit by subtracting earned money by cost.
    :param selection: Customer's selection
    :param orders: Order from the menu
    :param random_tip: obtained from random_tips()
    :param cooking_tip: obtained from classify_cooking_for_tip()
    :return: Total profit of the meals sold
    """
    selling_price = (orders[selection - 1]["sell_for"])
    cost = (orders[selection - 1]["cost_to_make"])
    total_paid = selling_price + ((selling_price * cooking_tip) / 100)
    final_paid = total_paid + ((total_paid * random_tip) / 100)
    final_paid = round(final_paid, 2)
    profit = final_paid - cost
    profit = round(profit, 2)
    print("Final selling price was $" + str(final_paid) + " for a profit of $" + str(profit))
    return profit


def order_for_x_people(customers):
    """
    The simulator function which handles how many times the process has to repeat based on number of customers
    :param customers: Number of customers for the day
    """
    order = order_input()
    profit = 0
    for i in range(customers):
        display_menu(order)
        selection, order = take_order(order)
        profit += classify_cooking_for_tip(selection, order)
    print(f"After serving meals to {customers} people, we've made a profit of ${round(profit, 2)}! ")
    print("That's all for today!  Have a good rest and see you tomorrow :) ")


if __name__ == "__main__":
    order_for_x_people(5)

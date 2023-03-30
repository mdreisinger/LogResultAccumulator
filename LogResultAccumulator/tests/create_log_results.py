"""
Module which contains a method to create a large log results file with random data
"""

import random


ITERATIONS = random.randrange(start=20, stop=1000)
FRUITS = ['apples','oranges','bananas','mangoes','grapes','strawberry', 'watermelon',\
          'blueberries', 'lemons', 'peaches', 'avacados', 'pineapple', 'cherries', \
          'cantaloupe', 'raspberries', 'pears', 'limes', 'blackberries', 'clementine', \
          'plums', 'lime', 'apricot', 'figs', 'dates', 'grapefruit', 'pomegranate']

def create_file():
    """
    Simple function to randomly generate a file to test with.
    """
    with open(f"test_data/test_{random.randrange(start=1, stop=10000)}.txt", 
                "x", encoding="utf-8") as file_handler:
        for i in range(ITERATIONS):
            file_handler.write(f"# Iteration {i}\n")
            fruit = random.choice(FRUITS)
            result = random.choice(["PASS", "FAIL"])
            number_of_tests = random.randrange(start=10, stop=500)
            for _ in range(number_of_tests):
                file_handler.write(f"# Test: {fruit} Test\n")
                file_handler.write(f"# This is {fruit} Test\n")
                file_handler.write(f"# Who is {fruit}?\n")
                file_handler.write(f"# I am not sure about {fruit}\n")
                file_handler.write(f"# Result: {result}\n")

if __name__ == "__main__":
    create_file()

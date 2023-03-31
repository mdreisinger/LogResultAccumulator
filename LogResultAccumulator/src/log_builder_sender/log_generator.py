"""
Module which contains a method to create a large log results file with random data
"""
import calendar
import pathlib
import random
import time


ITERATIONS = random.randrange(start=20, stop=1000)
FRUITS = ['apples','oranges','bananas','mangoes','grapes','strawberry', 'watermelon',\
          'blueberries', 'lemons', 'peaches', 'avacados', 'pineapple', 'cherries', \
          'cantaloupe', 'raspberries', 'pears', 'limes', 'blackberries', 'clementine', \
          'plums', 'lime', 'apricot', 'figs', 'dates', 'grapefruit', 'pomegranate']

CUR_DIR = pathlib.Path(__file__).parent.resolve()

def create_file():
    """
    Simple function to randomly generate a file to test with.
    """
    file_to_create = f"{CUR_DIR}/log_files/test_{calendar.timegm(time.gmtime())}.txt"
    with open(file_to_create, "x", encoding="utf-8") as file_handler:
        print(f"Creating file: {file_to_create}")
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

def continuous_files():
    """
    Continuously create log files forever
    """
    while True:
        create_file()
        sleep_time = random.randrange(5, 60)
        print(f"Waiting {sleep_time} seconds before creating new file")
        time.sleep(sleep_time)

"""
Main module to create logs and publish them to RabbitMQ.
"""
import random
import sys
import time

import pika


ITERATIONS = random.randrange(start=20, stop=100)
FRUITS = ['apples','oranges','bananas','mangoes','grapes','strawberry', 'watermelon',\
          'blueberries', 'lemons', 'peaches', 'avacados', 'pineapple', 'cherries', \
          'cantaloupe', 'raspberries', 'pears', 'limes', 'blackberries', 'clementine', \
          'plums', 'lime', 'apricot', 'figs', 'dates', 'grapefruit', 'pomegranate']

def create_log_results() -> str:
    """
    Simple function to randomly generate a file to test with.
    """
    log_contents = f"test_{time.time()}\n"
    for i in range(ITERATIONS):
        log_contents += f"# Iteration {i}\n"
        fruit = random.choice(FRUITS)
        number_of_tests = random.randrange(start=10, stop=50)
        for _ in range(number_of_tests):
            result = random.choice(["PASS", "FAIL"])
            log_contents += f"# Test: {fruit} Test\n"
            log_contents += f"# This is {fruit} Test\n"
            log_contents += f"# Who is {fruit}?\n"
            log_contents += f"# I am not sure about {fruit}\n"
            log_contents += f"# Result: {result}\n"
    return log_contents

if __name__ == "__main__":
    try:
        while True:
            contents = create_log_results()
            with pika.BlockingConnection(
                pika.ConnectionParameters('localhost')) as connection:

                # Create Channel
                channel = connection.channel()

                # Create Queue
                channel.queue_declare(queue='log_files', durable=True)

                # Make sure each worker is only doing one job at a time.
                channel.basic_qos(prefetch_count=1)

                # Make messages persistent
                properties = pika.BasicProperties(
                    delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE)

                # Send Message
                channel.basic_publish(exchange='',
                            routing_key="log_files",
                            body=contents, properties=properties)

            sleep_time = random.randrange(1, 10)
            print(f"Waiting {sleep_time} seconds before creating new file")
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

"""
The main algorithm for accumulating test log results.
"""

import queue
import sys
from threading import Thread
import time

import pika

from src.log_accumulator.exceptions import LogFileMisformatted
from src.log_accumulator.graph_results import graph_results
from src.log_accumulator.result import AccumulatedResult, Result


MAX_THREADS = 8 # choose 8 threads max because my computer has 8 performance cores.

class Consumer:
    # pylint:disable=too-few-public-methods
    """
    The object responsible for accumulating test log results.
    """
    def __init__(self) -> None:
        self.input_queue = queue.Queue()
        self.printer_queue = queue.Queue()
        self.threads = []
        self.printer_thread = Thread(target=self.printer, daemon=True, name='Printer')
        self.printer_thread.start()
        self.__create_threads()
        self.accumulated_result = AccumulatedResult()
        self.__start_consuming()

    def __create_threads(self) -> list:
        while len(self.threads) <= MAX_THREADS:
            self.threads.append(Thread(target=self.__worker, daemon=True).start())

    def __start_consuming(self):
        print("Starting to consume messages from broker")
        with pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')) as connection:

            # Create Channel
            channel = connection.channel()

            # Create Queue / Confirm it exists.
            channel.queue_declare(queue='log_files', durable=True)

            # Tell Pika to use our callback.
            channel.basic_consume(queue='log_files',
                      on_message_callback=self.accumulate)

            channel.start_consuming()

    def accumulate(self, ch, method, properties, body) -> None:
        #pylint:disable=unused-argument
        #pylint:disable=invalid-name
        """
        The method that is called when a message is received.
        """
        file_contents = body.decode()
        lines = file_contents.split('\n')
        graph_name = lines[0]
        self.printer_queue.put(f"length of file_contents = {len(lines)}")
        self.printer_queue.put(f"Received file and working on accumulating results: {graph_name}")
        iteration_amount = 0
        for iteration in self.get_iterations(file_contents[1:]):
            self.input_queue.put(iteration)
            iteration_amount += 1
        self.printer_queue.put(f"Got {iteration_amount} iterations")
        self.printer_queue.put(f"Input queue has {self.input_queue.qsize()} items")

        self.input_queue.join()

        self.printer_queue.put("Accumulated Results:")
        self.printer_queue.put(self.accumulated_result)
        graph_results(self.accumulated_result, show=False, save=True, file_name=graph_name)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def __worker(self) -> None:
        """
        A method which is used to accumulate results of each Test iteration individually.
        """
        #pylint:disable=too-many-nested-blocks
        #pylint:disable=too-many-branches
        self.printer_queue.put("Worker thread called.")
        while True:
            if not self.input_queue.empty():
                self.printer_queue.put("Worker thread started while loop.")
                input_list = self.input_queue.get()
                first_line = input_list[0]
                self.printer_queue.put(f"Worker thread got iteration from queue: {first_line}")

                current_fruit = None
                for row in input_list:
                    self.printer_queue.put(row)
                    if "Test: " in row:
                        words = row.split(" ")
                        try:
                            current_fruit = words[2]
                        except KeyError as exc:
                            raise LogFileMisformatted("Expected a string (fruit name) to follow "
                                                    "'Test: ' but it does not.") from exc
                        if current_fruit not in self.accumulated_result.cache:
                            self.accumulated_result.cache[current_fruit] = Result(current_fruit)
                    if "Result: " in row:
                        words = row.split(" ")
                        try:
                            test_result = words[2].strip()
                        except KeyError as exc:
                            raise LogFileMisformatted("Expected a string (test_result) to follow "
                                                        "'Result: ' but it does not.") from exc
                        if test_result == "PASS":
                            try:
                                self.accumulated_result.cache[current_fruit].passed += 1
                            except KeyError as exc:
                                raise LogFileMisformatted(f"Expected {current_fruit}"
                                                        " to be in accumulated test_result"
                                                        " but it is not.") from exc
                        elif test_result == "FAIL":
                            try:
                                self.accumulated_result.cache[current_fruit].failed += 1
                            except KeyError as exc:
                                raise LogFileMisformatted(f"Expected {current_fruit}"
                                                        " to be in accumulated test_result"
                                                        " but it is not.") from exc
                self.printer_queue.put("Worker thread finished 1 iteration.")

                self.input_queue.task_done()
            else:
                time.sleep(2)

    def get_iterations(self, body) -> list:
        """
        Break up the input file into a list of tuples, each tuple containing an iteration.
        """
        iterations = []
        iteration = ()
        for row in body.split('\n'):
            if "Iteration " in row and iteration:
                iterations.append(iteration)
                iteration = ()
            iteration += (row,)
        iterations.append(iteration)
        return iterations

    def printer(self):
        """
        Worker task for thread-safe printing.
        """
        while True:
            message = self.printer_queue.get()
            print(message)

if __name__ == '__main__':
    try:
        Consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

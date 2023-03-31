"""
The main algorithm for accumulating test log results.
"""

import json
import queue
from threading import Thread
import time
import urllib

import boto3
from memory_profiler import profile

from src.accumulator.exceptions import LogFileMisformatted
from src.accumulator.graph_results import graph_results
from src.accumulator.result import AccumulatedResult, Result
from src.accumulator.timer import timer


class Accumulator:
    # pylint:disable=too-few-public-methods
    """
    The object responsible for accumulating test log results.
    """
    def __init__(self, log_file_path: str = None, log_file_body: str = None) -> None:
        self.log_file_path = log_file_path
        self.log_file_body = log_file_body
        self.accumulated_result = AccumulatedResult()
        self.queue = queue.Queue()

    def __read_file(self) -> str:
        """
        Generator to read log files.
        """
        #pylint:disable=consider-using-with
        for row in open(self.log_file_path, "r", encoding="utf-8"):
            yield row

    def __read_body(self) -> str:
        """
        Generator to read log bodies.
        """
        #pylint:disable=consider-using-with
        for row in self.log_file_body:
            yield row

    def __worker(self) -> None:
        """
        A method which is used to accumulate results of each Test iteration individually.
        """
        while True:
            input_string = self.queue.get()
            current_fruit = None
            for row in input_string:
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
            self.queue.task_done()

    def get_iterations(self) -> list:
        """
        Break up the input file into a list of tuples, each tuple containing an iteration.
        """
        iterations = []
        iteration = ()
        if self.log_file_body:
            reader_func = self.__read_body
        else:
            reader_func = self.__read_file

        for row in reader_func():
            if "Iteration " in row and iteration:
                iterations.append(iteration)
                iteration = ()
            iteration += (row,)
        iterations.append(iteration)
        return iterations

    @timer
    @profile
    def accumulate(self) -> AccumulatedResult:
        """
        The main algorithm for accumulating test log results.
        """
        iterations = self.get_iterations()
        for iteration in iterations:
            self.queue.put(iteration)

        max_threads = 8 # choose 8 threads max because my computer has 8 performance cores.
        threads = len(iterations)//2 if len(iterations)//2 < max_threads else max_threads
        for i in range(threads):
            print(f"Creating thread {i}")
            Thread(target=self.__worker, daemon=True).start()

        self.queue.join()
        return self.accumulated_result

def lambda_handler(event, _):
    """
    The function which is called when a new file is create in the S3 log file bucket.
    """
    print("Received event: " + json.dumps(event, indent=2))

    s3_client = boto3.client('s3')

    #Get the object from the event and show its content type
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    body = s3_object['Body']

    accumulator = Accumulator(log_file_body=body)
    accumulated_results = accumulator.accumulate()
    graph_path = graph_results(accumulated_results, show=False, save=True)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    result_key = f'AccumulatedResults/{timestamp}_result.txt'
    graph_result_key = f'AccumulatedResults/{timestamp}_graph.txt'

    s3_client.put(Body=print(accumulated_results), Bucket=bucket_name, key=result_key)
    s3_client.put(graph_path, Bucket=bucket_name, key=graph_result_key)

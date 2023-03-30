"""
The main algorithm for accumulating test log results.
"""

import queue
from threading import Thread

from memory_profiler import profile

from src.exceptions import LogFileMisformatted
from src.graph_results import graph_results
from src.result import AccumulatedResult, Result
from src.timer import timer


class Accumulator:
    # pylint:disable=too-few-public-methods
    """
    The object responsible for accumulating test log results.
    """
    def __init__(self, log_file_path: str) -> None:
        self.log_file_path = log_file_path
        self.accumulated_result = AccumulatedResult()
        self.queue = queue.Queue()

    def __read_file(self) -> str:
        """
        Generator to read log files.
        """
        #pylint:disable=consider-using-with
        for row in open(self.log_file_path, "r", encoding="utf-8"):
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
                        result = words[2].strip()
                    except KeyError as exc:
                        raise LogFileMisformatted("Expected a string (result) to follow 'Result: '"
                                                    " but it does not.") from exc
                    if result == "PASS":
                        try:
                            self.accumulated_result.cache[current_fruit].passed += 1
                        except KeyError as exc:
                            raise LogFileMisformatted(f"Expected {current_fruit}"
                                                    " to be in accumulated result"
                                                    " but it is not.") from exc
                    elif result == "FAIL":
                        try:
                            self.accumulated_result.cache[current_fruit].failed += 1
                        except KeyError as exc:
                            raise LogFileMisformatted(f"Expected {current_fruit}"
                                                    " to be in accumulated result"
                                                    " but it is not.") from exc
            self.queue.task_done()

    def get_iterations(self) -> list:
        """
        Break up the input file into a list of tuples, each tuple containing an iteration.
        """
        iterations = []
        iteration = ()
        for row in self.__read_file():
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


if __name__ == "__main__":
    # Run from LogResultAccumulator/LogResultAccumulator
    # CLI syntax: python -m src.accumulator

    import pathlib
    cur_dir = pathlib.Path().resolve()
    test_dir = f"{cur_dir}/tests"
    accumulator = Accumulator(f"{test_dir}/test_data/test_8594.txt")
    result = accumulator.accumulate()
    graph_results(result)

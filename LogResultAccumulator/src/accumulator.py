"""
The main algorithm for accumulating test log results.
"""

from src.exceptions import LogFileMisformatted
from src.result import AccumulatedResult, Result



class Accumulator:
    # pylint:disable=too-few-public-methods
    """
    The object responsible for accumulating test log results.
    """
    def __init__(self, log_file_path: str) -> None:
        self.log_file_path = log_file_path
        self.accumulated_result = AccumulatedResult()

    def __read_file(self) -> str:
        """
        Generator to read log files.
        """
        #pylint:disable=consider-using-with
        for row in open(self.log_file_path, "r", encoding="utf-8"):
            yield row

    def accumulate(self) -> AccumulatedResult:
        """
        The main algorithm for accumulating test log results.
        """
        current_fruit = None
        for row in self.__read_file():
            if "Test: " in row:
                words = row.split(" ")
                try:
                    current_fruit = words[2]
                except KeyError as exc:
                    raise LogFileMisformatted("Expected a string (fruit name) to follow 'Test: '"
                                               " but it does not.") from exc
                if current_fruit not in self.accumulated_result.cache:
                    self.accumulated_result.cache[current_fruit] = Result(current_fruit)
                print(current_fruit)
            if "Result: " in row:
                words = row.split(" ")
                try:
                    result = words[2].strip()
                except KeyError as exc:
                    raise LogFileMisformatted("Expected a string (result) to follow 'Result: '"
                                                   " but it does not.") from exc
                print(result)
                print(self.accumulated_result.cache[current_fruit])
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
                print(self.accumulated_result.cache[current_fruit])

        return self.accumulated_result


if __name__ == "__main__":
    # Run from LogResultAccumulator/LogResultAccumulator
    # CLI syntax: python -m src.accumulator

    import pathlib
    cur_dir = pathlib.Path().resolve()
    test_dir = f"{cur_dir}/tests"
    accumulator = Accumulator(f"{test_dir}/simple_test_log_results.txt")
    print(accumulator.accumulate())

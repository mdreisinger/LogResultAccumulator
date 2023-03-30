"""
Module that contains the various result objects to accumulate results
"""

from dataclasses import dataclass


@dataclass
class Result:
    """
    An object to store the number of passes and fails for a single fruit.
    """
    fruit: str
    passed: int = 0
    failed: int = 0

class AccumulatedResult:
    """
    An object to store the accumulated results for multiple fruits.
    """
    def __init__(self) -> None:
        self.cache = {}

    def __str__(self) -> str:
        output = ""
        for fruit, result in self.cache.items():
            output += f"{fruit}:\n\tPASSED: {result.passed}\n\tFAILED: {result.failed}\n"
        return output

    def add_result(self, result : Result) -> None:
        """
        Method for adding a result to the cache.
        """
        if result.fruit not in self.cache:
            self.cache[result.fruit] = result

    def get_accumulated_results(self) -> dict:
        """
        Method for getting the accumulated results from the cache.
        """
        return self.cache

if __name__ == "__main__":
    # Run from LogResultAccumulator/LogResultAccumulator
    # CLI syntax: python -m src.result

    apple_result = Result("Apples")
    apple_result.passed=2
    apple_result.failed=0
    oranges_result = Result("Oranges")
    oranges_result.passed = 1
    oranges_result.failed = 1
    watermelon_result = Result("Watermelon")
    watermelon_result.passed = 0
    watermelon_result.failed = 2
    ac_result = AccumulatedResult()
    ac_result.add_result(apple_result)
    ac_result.add_result(oranges_result)
    ac_result.add_result(watermelon_result)
    print(ac_result)

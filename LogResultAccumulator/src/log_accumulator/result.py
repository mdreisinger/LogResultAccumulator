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
    #pylint:disable=too-few-public-methods
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

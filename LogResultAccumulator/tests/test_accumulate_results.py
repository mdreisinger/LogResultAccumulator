"""
Unit tests for the LogResultAccumulator
"""

import pathlib

from src.accumulator import Accumulator
from src.result import Result


def test_small_data_set():
    """
    Basic happy path test given a single log file with a few results
    """
    # Arrange
    cur_dir = pathlib.Path(__file__).parent.resolve()
    accumulator = Accumulator(f"{cur_dir}/test_data/simple_test_log_results.txt")
    expected_result = {
        "Apples": Result("Apples", passed=2, failed=0),
        "Oranges": Result("Oranges", passed=1, failed=1),
        "Watermelon": Result("Watermelon", passed=0, failed=2)
    }

    # Act
    actual_result = accumulator.accumulate()

    # Assert
    assert actual_result.cache == expected_result, (f"\nExpected:\n\t{expected_result}"
                                                     f"\nActual:\n{actual_result}")

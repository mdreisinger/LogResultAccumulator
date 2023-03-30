"""
Module which contains a function for graphing accumulated results.
"""

import numpy as np
import matplotlib.pyplot as plt

from src.result import AccumulatedResult


def graph_results(accumulated_result: AccumulatedResult) -> None:
    """
    Creates a bar graph to display the accumulated results.
    """
    results_dict = accumulated_result.get_accumulated_results()

    plt.subplots()
    bar_width = 0.25
    index = np.arange(len(results_dict))
    print(index)

    fruits = list(results_dict.keys())
    passes = [result.passed for result in results_dict.values()]
    fails = [result.failed for result in results_dict.values()]
    plt.bar(np.arange(len(results_dict)),
                      passes, width=bar_width, color='g', label="PASSED")
    plt.bar(np.arange(len(results_dict))+ bar_width,
                      fails, width=bar_width, color='r', label="FAILED")

    plt.xlabel('Fruit')
    plt.ylabel('Results')
    plt.title('Results by Fruit')
    plt.legend()
    plt.xticks(index + bar_width/2, (fruits))

    plt.show()


if __name__ == "__main__":
    # Run from LogResultAccumulator/LogResultAccumulator
    # CLI syntax: python -m src.graph_results

    from src.result import Result
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
    graph_results(ac_result)

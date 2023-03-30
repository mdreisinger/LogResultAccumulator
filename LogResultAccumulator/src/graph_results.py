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
    plt.xticks(index + bar_width/2, (fruits), rotation='vertical')

    plt.show()

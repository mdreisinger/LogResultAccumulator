"""
Module which contains a function for graphing accumulated results.
"""
import calendar
import pathlib
import time

import matplotlib.pyplot as plt
import numpy as np

from src.accumulator.result import AccumulatedResult


CUR_DIR = pathlib.Path(__file__).parent.resolve()

def graph_results(accumulated_result: AccumulatedResult, show=True, save=False) -> str:
    """
    Creates a bar graph to display the accumulated results.
    """
    results_dict = accumulated_result.get_accumulated_results()

    fig, ax = plt.subplots()
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
    fig.tight_layout()
    if show and save:
        plt.show()
        path = f"{CUR_DIR}/graphs/graph_{calendar.timegm(time.gmtime())}"
        plt.savefig(path)
        return path
    if show:
        plt.show()
        return None
    if save:
        path = f"{CUR_DIR}/graphs/graph_{calendar.timegm(time.gmtime())}"
        plt.savefig(path)
        return path

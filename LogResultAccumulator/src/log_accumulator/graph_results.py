"""
Module which contains a function for graphing accumulated results.
"""
import pathlib

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from src.log_accumulator.result import AccumulatedResult


CUR_DIR = pathlib.Path(__file__).parent.resolve()

def graph_results(accumulated_result: AccumulatedResult,
                  show=True, save=False, file_name=None) -> str:
    """
    Creates a bar graph to display the accumulated results.
    """
    results_dict = accumulated_result.cache
    matplotlib.use('SVG')

    fig, _ = plt.subplots()
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
        path = f"{CUR_DIR}/graphs/graph_{file_name}.png"
        plt.savefig(path)
        return path
    if show:
        plt.show()
        return ""
    if save:
        graph_path = f"{CUR_DIR}/graphs/graph_{file_name}.png"
        print(f"Save graph to {graph_path}")
        plt.savefig(graph_path)
        return graph_path
    return ""

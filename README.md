# LogResultAccumulator
Accumulate a large number of log results and present a condensed summary of the results

# Assumptions
1. The log file will contain a line that contains "Test: ", and before the next line that contains "Test: ", there will be a line that contains "Result: ".

# Todo
- ~~Setup threading in accumulator.~~
- ~~Create a function that will generate a huge test file for me to work with.~~
- Setup dockerfiles and docker-compose.
  - E.g., log-generator -> queue -> log_accumulator -> S3 bucket

# Optimizations
- I tried using numpy in Accumulator but it increase memory usage 3.5x
- I tried using numba in Accumulator bit it increased memory 5x
- While these may speed things up, I think that they are not worth it since this system has to scale significantly.
  - If compute resources are cheap and time is of the essence, we can use these methods to speed up the algorithm.
- For now I am going to focus on reducing memory as my first priority and decreasing time as my second priority.
  - Therefore I am going to implement multi-threading instead of multiprocessing.

## Threading Notes
- After implementing threading, I ran the accumulator on a log file with 211789 tests spread across 859 iterations, all with random fruits and results.
- The implementation used the max number of threads I allowed for it to use which is 8, based on the number of performance cores of my computer.
- The accumulation of results only took 3.4 seconds.
- Here is the memory usage:
![Alt text](documentation/mem_usage.png?raw=true "Title")
- And here is the graph that it created:
![Alt text](documentation/graph.png?raw=true "Title")
# LogResultAccumulator
Accumulate a large number of log results and present a condensed summary of the results

# Assumptions
1. The log file will contain a line that contains "Test: ", and before the next line that contains "Test: ", there will be a line that contains "Result: ".

# Todo
- Setup threading in accumulator.
- Use database instead of cache.
- Setup dockerfiles and docker-compose.
- Make graph results able to take in N AccumulatedResults.
- Create a function that will generate a huge test file for me to work with.

# Optimizations
- I tried using numpy in Accumulator but it increase memory usage 3.5x
- I tried using numba in Accumulator bit it increased memory 5x
- While these may speed things up, I think that they are not worth it since this system has to scale significantly.
  - If compute resources are cheap and time is of the essence, we can use these methods to speed up the algorithm.
- For now I am going to focus on reducing memory as my first priority and decreasing time as my second priority.
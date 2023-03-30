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
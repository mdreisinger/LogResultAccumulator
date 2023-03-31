# LogResultAccumulator
Accumulate a large number of log results and present a condensed summary of the results

# Assumptions
1. The log file will contain a line that contains "Test: ", and before the next line that contains "Test: ", there will be a line that contains "Result: ".

# Python Version
`3.9`

# Pyenv / Poetry
- [pyenv](https://realpython.com/intro-to-pyenv/)
- [poetry](https://python-poetry.org/docs/basic-usage/)

# How to use
## Install pyenv or make sure that you're running Python3.9
- `pyenv install 3.9`
- Run from root dir of this directory: `pyenv local 3.9`

## Setup poetry
- `brew install poetry`
- Run from root dir of this directory: `poetry install`

## Simply run the Accumulator locally with a single large log file and generate a graph
- Run from LogResultAccumulator/LogResultAccumulator:
- `poetry run python -m src.accumulator.accumulator`

## Run Unit Test
- Run from LogResultAccumulator/
- `poetry run pytest LogResultAccumulator/tests/test_accumulate_results.py`

# Todo
- Optimize code to reduce resource usage and runtime.
- Setup dockerfiles and docker-compose.
- Setup distributed system in cloud

## Optimizations
- Need to decide if speed or resource optimization is a priority.
  - Potential optimizations:
    - Thread (this is what I started with because it's easy)
    - Multiprocessing
    - asyncio
    - numba
    - numpy_methods
    - itertools
  - Dockerfile optimizations:
    - Use slimar docker base images. (currently using Python3.9 image)
  - If memory persistance is important, need to get rid of accumulator cache and replace it with database.

## Threading Notes
- After implementing threading, I ran the accumulator on a log file with 211789 tests spread across 859 iterations, all with random fruits and results.
- The implementation used the max number of threads I allowed for it to use which is 8, based on the number of performance cores of my computer.
- The accumulation of results only took 3.4 seconds.
- Here is the memory usage:
![Alt text](documentation/mem_usage.png?raw=true "Title")
- And here is the graph that it created:
![Alt text](documentation/graph.png?raw=true "Title")

# Push docker images to ECR
## logaccumulator
- `aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 126493000772.dkr.ecr.us-west-2.amazonaws.com`
- `docker build -t logresultaccumulator -f Dockerfile.accumulator .`
- `docker tag logresultaccumulator:latest 126493000772.dkr.ecr.us-west-2.amazonaws.com/logresultaccumulator:latest`
- `docker push 126493000772.dkr.ecr.us-west-2.amazonaws.com/logresultaccumulator:latest`

## loguploader
- `aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 126493000772.dkr.ecr.us-west-2.amazonaws.com`
- `docker build -t loguploader -f Dockerfile.loguploader .`
- `docker tag loguploader:latest 126493000772.dkr.ecr.us-west-2.amazonaws.com/loguploader:latest`
- `docker push 126493000772.dkr.ecr.us-west-2.amazonaws.com/loguploader:latest`

## loggenerator
- `aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 126493000772.dkr.ecr.us-west-2.amazonaws.com`
- `docker build -t loggenerator -f Dockerfile.loggenerator .`
- `docker tag loggenerator:latest 126493000772.dkr.ecr.us-west-2.amazonaws.com/logupgenerator:latest`
- `docker push 126493000772.dkr.ecr.us-west-2.amazonaws.com/logupgenerator:latest`

# Initial Cloud Infrastructure Concept
![Alt text](documentation/cloud_infrastructure.png?raw=true "Title")
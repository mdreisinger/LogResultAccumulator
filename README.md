# LogResultAccumulator
Accumulate a large number of log results and present a condensed summary of the results.

- This project simulates a system which sends logs files to RabbitMQ broker. The broker stores the log files in a queue. Multiple clients can subscribe to queue in RabbitMQ and process the results.
- Instead of real log files, this project contains a script that generates random log file contents and sends that to the Broker.
  - The first line of the log file contents represents the log file name, so that the clients can correlate the results with log file that it came from.

# Design Concept
![Alt text](DesugbConcept.png?raw=true "Title")

# How to run:
- Bring up RabbitMQ broker by running `docker-compose up` in the root directory.
- Start the log_producer by running `poetry run python -m src.log_producer.log_generator` from `LogResultAccumulator/LogResultAccumulator`.
- Start the log_accumulator by running `poetry run python -m src.log_accumulator.consumer` from `LogResultAccumulator/LogResultAccumulator`.
- View the graphed results in `LogResultAccumulator/LogResultAccumulator/log_accumulator/graphs/`.
- The text results are displayed to stdout from the log_accumulator.
- The RabbitMQ management console can be accessed at `localhost:8080`. This allows you to monitor and control the queues.

# Assumptions
1. The input log file will contain a line that contains "Test: ", and before the next line that contains "Test: ", there will be a line that contains "Result: ".

# Production Non-Suitability Disclaimer
- Please keep in mind that this program was built following a basic RabbitMQ tutorial. It demonstrate one new concept at a time and may intentionally oversimplify some things and leave out others. For example topics such as connection management, error handling, connection recovery, concurrency and metric collection are largely omitted for the sake of brevity. Such simplified code should not be considered production ready.

## RabbitMQ Broker
- Long term metric storage and visualisation services such as Prometheus and Grafana or the ELK stack are more suitable options for production systems.
- RabbitMQ provides first class support for Prometheus and Grafana as of 3.8. It is recommended for production environments.
  
# Improvements to make
- Setup log_producer and log_accumulator in docker containers so that everything can be run in the cloud.
- Setup better loggging
  - Need to be able to see log files from all services running in all containers in a simple way.
- Change broker creds:
  - If you wish to change the default username and password of guest / guest, you can do so with the RABBITMQ_DEFAULT_USER and RABBITMQ_DEFAULT_PASS environmental variables. These variables were available previously in the docker-specific entrypoint shell script but are now available in RabbitMQ directly.
    - `-e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password`
- Improve speed of results processessing. 
    
## Optimizations
- Need to decide if speed or resource optimization is a priority.
  - Potential optimizations:
    - asyncio
    - numba
    - numpy_methods
    - itertools
  - Dockerfile optimizations:
    - Use slimar docker base images. (currently using Python3.9 image)
  - If memory persistance is important, need to consider using a persistent database rather than the  accumulator cache.

# Python Version
`3.9`

# Pyenv / Poetry
- [pyenv](https://realpython.com/intro-to-pyenv/)
- [poetry](https://python-poetry.org/docs/basic-usage/)

# How to contribute
## Install pyenv or make sure that you're running Python3.9
- `pyenv install 3.9`
- Run from root dir of this directory: `pyenv local 3.9`

## Setup poetry
- `brew install poetry`
- Run from root dir of this directory: `poetry install`

## Simply run the Accumulator locally with a single large log file and generate a graph
- Run from LogResultAccumulator/LogResultAccumulator:
- `poetry run python -m src.accumulator.accumulator`

# moqa_locust
Masters of QA - Locust

Use https://jsonplaceholder.typicode.com as the base URL for the tests.


## Installation

Tests can be run by installing required software in your computer or using docker.

### Local

1. Install Python 3
2. Install requirements with pip (preferably in venv)
    - python3 -m pip install -r- requirements.txt

### Docker

1. Install Docker
2. Run test (see below) with -d option
    - docker image is build if not already existing and the test is run inside a docker container

## Running the tests

Use the run_test.sh script to run the tests.

Script has a help option to list all the available options:
``` shell
./run_test.sh -h
```

### Example

Run "login and auth" api tests using docker:
``` shell
./run_test.sh -f locustfiles/login_and_auth.py -u https://jsonplaceholder.typicode.com -d
```

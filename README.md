## Synopsis

The **Paint Calculator** is a hypothetical project that calculates how many gallons of paint would be required to paint a number of rooms.

## Requirements

* Python 3
* Pip

## What we're looking for

* Install Python / Pip
* Run application
* Write unit tests against the application.
* Write playwright E2E tests against the application
* You are allowed to change any of the source code as you see fit to make things easier for yourself. You are encouraged to fix any bugs you discover.
* Explain any problems you had while writing the tests, and what you did to make it easier. Pointing to localhost for the application is OK.

## Instructions

Because each applicant's code should be secret from one another, we should not submit it to the same repo.

1. Clone the repo (do not fork)
2. Create a new public repo on Github
3. Add the new repo as a new remote
* `git remote add acme <url>`
4. Initialize the new repo with what is cloned
* `git push acme master`
5. Create a new branch off of master to put your changes on
6. Run the application locally
* `pip3 install -e .`
* `python3 paint_calculator/run.py`
7. Perform testing and debugging activities

## Submitting 

To make it easier on everybody, it's best if we use a PR to diff what work was completed.

1. Make any and all commits to your new branch and push the changes
* `git push acme <branch>`
2. Create a PR to your new repo
3. Make sure you include your test plan and any automated tests, as well as update this README to instruct someone on how to run the tests
4. Include any other text in a file - which tests would be suited for a different level of execution, or any problems encountered...etc
5. Send the link to the PR

## Running Tests

### Prerequisites

Install the application and test dependencies:
```
pip3 install -e .
pip3 install -r requirements-test.txt
```

### Unit Tests

Run the unit tests:
```
python3 -m pytest tests/test_api.py -v
```

### E2E Tests

Start the application in one terminal:
```
python3 paint_calculator/run.py
```

In another terminal, run the E2E tests:
```
python3 -m pytest tests/test_e2e.py -v
```

Note: E2E tests use system Chrome browser in non-headless mode.

### Run All Tests

To run all tests at once (requires the application to be running):
```
python3 -m pytest tests/ -v
```

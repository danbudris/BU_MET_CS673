
### Unit Tests
To run just the Unit Tests:
```
python manage.py test unit_tests
```

### Selenium Tests

In order to run the Selenium tests, you will need to execute the following steps:


The Selenium Webdriver is based off the Firefox binary. As a result, you will need to install the Firefox browser.

Install the selenium python dependency into your virtualenv:
```
pip install -U selenium
```

Install the geckodriver:
```
https://github.com/mozilla/geckodriver/releases
```

Unzip the geckodriver, and copy it to the root level directory "g1".

Update your $PATH with the geckodriver location:
```
export PATH=$PATH:~/g1
```


To run all of the Selenium tests:
```
python manage.py test --liveserver=127.0.0.1:8000 selenium_tests
```

To run the Project Router App Selenium tests:
```
python manage.py test --liveserver=127.0.0.1:8000 selenium_tests.project_router
```

To run the Requirements App Selenium tests:
```
python manage.py test --liveserver=127.0.0.1:8000 selenium_tests.requirements
```

To run the Issue Tracker App Selenium tests:
```
python manage.py test --liveserver=127.0.0.1:8000 selenium_tests.issue_tracker
```

### Running Tests With Coverage
In order to run tests with coverage, you will need to do the following:

Install the coverage python library:
```
pip install coverage
```

Run all of the tests with coverage:
```
coverage run --source='.' manage.py test -v 2 --liveserver=127.0.0.1:8000
```

Run the unit tests with coverage:
```
coverage run --source='.' manage.py test -v 2 --liveserver=127.0.0.1:8000 unit_tests
```

Run the selenium tests with coverage:
```
coverage run --source='.' manage.py test -v 2 --liveserver=127.0.0.1:8000 selenium_tests
```

To generate a coverage report, after the tests have executed:
```
coverage report
```


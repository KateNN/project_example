## ... Web UI Automation Project

### Description

Technologies:

* Python
* PyTest
* Selenium
* Allure

### Tests can run (options):

* Locally or on a remote machine
* "--base_url" option: environment where tests will run. By default, it's https://stage/
* In two browsers: Chrome, Firefox: "--browser" defaulted to Chrome (chrome, firefox)
* Browser version can be set as well ("--bv"). This is for Selenoid
* Can run in different executors: "--executor" option. By default, run locally. If other address provided, will open "
  http: //{executor}:4444/wd/hub" link
* Number of threads can be set: "-n" option. By default, it's 1 thread
* Selected tests can run by pytest marks: "-m". Options:
  "regression" will run all functional regression tests
  "inactivate" will run inactivation of new Dealers and Users created during regression tests (to be run after 
  the regression tests are completed) 
* In headless mode: "--headless" - by default it's off
* See conftest.py for more details

### Reports

Allure report will be generated after test run and command:

{path to Allure}\allure-{version}\allure-{version}\bin\allure generate --clean allure-results/

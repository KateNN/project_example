import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser to run tests in")
    parser.addoption("--headless", action="store_true", help="To run tests in headless mode")
    parser.addoption("--drivers", default="C:\\drivers\\", help="Path to drivers")
    parser.addoption("--base_url", default="https://stage/", help="Base URL")
    parser.addoption("--executor", action="store", default="local",
                     help="Where tests will run (e.g. in Selenoid). Run locally by default")
    parser.addoption("--bv", help="Browser version - for Selenoid test runs")
    parser.addoption("--vnc", action="store_true", help="For Selenoid connection")


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drivers_source = request.config.getoption("--drivers")
    base_url = request.config.getoption("--base_url")
    executor = request.config.getoption("--executor")
    browser_version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")

    executor_url = f"http://{executor}:4444/wd/hub"

    if executor != "local":
        capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": vnc
            }
        }

        _driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=capabilities
        )
    else:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.headless = True
                options.add_argument("window-size=1920,1080")
            path_to_driver = ServiceChrome(f'{drivers_source}chromedriver')
            _driver = webdriver.Chrome(
                service=path_to_driver,
                options=options)
            _driver.set_page_load_timeout(30)

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            path_to_driver = ServiceFirefox(f'{drivers_source}geckodriver')
            _driver = webdriver.Firefox(
                service=path_to_driver,
                options=options)
            _driver.set_page_load_timeout(30)

        else:
            raise ValueError(f"Browser {browser_name} is not supported")

    _driver.base_url = base_url
    _driver.maximize_window()
    with allure.step(f"Opening browser: {browser_name}"):
        yield _driver

    if request.node.status != 'passed':
        tabs_opened = _driver.window_handles
        if len(tabs_opened) > 1:
            _driver.switch_to.window(tabs_opened[-1])
        with allure.step('Taking screenshot'):
            allure.attach(
                _driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )

    with allure.step("Closing browser"):
        tabs_opened = _driver.window_handles
        for i in range(len(tabs_opened)):
            _driver.switch_to.window(tabs_opened[i])
            _driver.close()

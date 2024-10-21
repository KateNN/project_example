from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import allure
import os
import random

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    PATH = ""
    TITLE = (By.XPATH, "html/head/title")

    # Common elements for all pages
    DEALERS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content") and contains(., "Dealers")]')
    GROUPS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content") and contains(., "Groups")]')
    USERS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content") and contains(., "Users")]')
    GLOBAL_SEARCH_INPUT = (By.XPATH, '(//input)[1]')
    DEFAULT_GROUP_NAME = "Windy City Demo Auto Group (101589)"
    WC_TEST_DEALER = "Windy City Chevrolet"
    EXISTING_DEALER_NAME = "Windy City BMW"
    EXISTING_DEALER_SHORT_NAME = "Windy City BMW"
    PAGE_BOTTOM = (By.XPATH, '(//div[contains(., "Copyright")])[2]')
    NO_DATA_RESULT = (By.XPATH, '//p[text()="No Data"]')
    NEW_DEALERS_FILE_NAME = 'new_dealers.txt'
    NEW_USERS_FILE_NAME = 'new_users.txt'
    UNSELECTED_DATE_IN_CALENDER = \
        (By.XPATH, '//table[@class="ant-picker-content"]//td[not(contains(@class, "ant-picker-cell-selected"))]/div')

    TIMEOUT = 20

    def __init__(self, driver):
        self.driver = driver
        self.url = driver.base_url

    def open(self):
        """Open .... page: path within the base page"""
        with allure.step(f"Opening url: {self.url}{self.PATH}"):
            self.driver.get(self.url + self.PATH)

    def click(self, element):
        """Move to the provided element and click it"""
        with allure.step(f"Clicking element: {element}"):
            ActionChains(self.driver).move_to_element(element).pause(0.1).click().perform()

    def make_screenshot(self):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG
        )

    def get_current_url(self):
        """Get URL of the current page"""
        with allure.step("Getting current URL"):
            return self.driver.current_url

    def check_page_title(self, title: str):
        """Check that the current page title matches provided title"""
        with allure.step(f"Checking that the page title is '{title}'"):
            try:
                return WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.title_is(title))
            except TimeoutException:
                with allure.step(f"The page title is not {title}, it's {self.driver.title}"):
                    self.make_screenshot()
                    raise AssertionError("Wrong page title")

    def wait_for_element_to_disappear(self, locator: tuple):
        """Wait until the element is no longer displayed"""
        with allure.step(f"Waiting for the element '{locator}' to disappear"):
            try:
                return WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until_not(EC.visibility_of_element_located(locator))
            except TimeoutException:
                with allure.step(f"Element {locator} is still displayed"):
                    self.make_screenshot()
                    raise AssertionError(f"Element {locator} is still displayed")

    def current_url_includes(self, part: str):
        """Check that the current page URL ends with the provided part"""
        with allure.step(f"Checking that current URL includes '{part}'"):
            return str(self.driver.current_url).endswith(part)

    def locate_element(self, locator: tuple):
        """Locate the element by the locator"""
        with allure.step(f"Locating element with locator {locator}"):
            try:
                return WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                with allure.step(f"Element {locator} not found"):
                    self.make_screenshot()
                    raise AssertionError(f"Element with locator {locator} not found")

    def get_clickable_element(self, locator: tuple):
        """Locate the element and wait until it is clickable"""
        with allure.step(f"Locating element with locator {locator} and waiting for it to be clickable"):
            try:
                return WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.element_to_be_clickable(locator))
            except TimeoutException:
                with allure.step(f"Element {locator} is not found or not clickable"):
                    self.make_screenshot()
                    raise AssertionError(f"Element with locator {locator} is not found or not clickable")

    def locate_all_elements(self, locator: tuple):
        """Locate all elements matching the locator"""
        with allure.step(f"Locating all elements with locator {locator}"):
            try:
                return WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_all_elements_located(locator))
            except TimeoutException:
                with allure.step(f"Elements with locator {locator} not found"):
                    self.make_screenshot()
                    raise AssertionError(f"Elements with locator {locator} not found")

    def get_attribute(self, locator: tuple, attr_name: str):
        """Get attribute value for the element located by the locator"""
        with allure.step(f"Trying to get attribute '{attr_name}' for element {locator}"):
            try:
                attribute = WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_element_located(locator)) \
                    .get_attribute(attr_name)
                if attribute is not None:
                    with allure.step(f"Found attribute '{attr_name}': '{attribute}'"):
                        return attribute
                else:
                    with allure.step(f"Couldn't find attribute '{attr_name}' for '{locator}'"):
                        self.make_screenshot()
                        raise AssertionError(f"No such attribute: '{attr_name}' for '{locator}'")
            except TimeoutException:
                with allure.step(f"Element '{locator}' not found"):
                    self.make_screenshot()
                    raise AssertionError(f"No such element with locator '{locator}'")

    def get_text(self, locator: tuple):
        """Get text for the element located by the locator"""
        with allure.step(f"Trying to get text for element {locator}"):
            try:
                elements_text = WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_element_located(locator)).text
                if elements_text:
                    with allure.step(f"Found element's text for {locator}: '{elements_text}'"):
                        return elements_text
                else:
                    with allure.step(f"Couldn't find element's text for {locator}"):
                        self.make_screenshot()
                        raise AssertionError(f"No such element with locator {locator}")
            except TimeoutException:
                with allure.step(f"Element {locator} not found"):
                    self.make_screenshot()
                    raise AssertionError(f"No such element with locator {locator}")

    def type_in_text(self, locator: tuple, text: str):
        """Type in provided text to the element located by the locator"""
        if 'password' in locator[1]:
            text_in_report = len(text) * '*'
        else:
            text_in_report = text
        with allure.step(f"Typing text '{text_in_report}' to the element with locator {locator}"):
            try:
                input_field = WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_element_located(locator))
                input_field.clear()
                for char in text:
                    input_field.send_keys(char)
                    time.sleep(0.07)

            except TimeoutException:
                with allure.step(f"Element {locator} not found or have no text field"):
                    self.make_screenshot()
                    raise AssertionError(f"Cannot enter text to the element with locator {locator}")

    def paste_text(self, locator: tuple, text: str):
        """Paste text from clipboard to the element located by the locator"""
        with allure.step(f"Pasting text '{text}' to the element with locator {locator}"):
            try:
                input_field = WebDriverWait(driver=self.driver, timeout=self.TIMEOUT) \
                    .until(EC.visibility_of_element_located(locator))
                input_field.clear()
                input_field.send_keys(text)
            except TimeoutException:
                with allure.step(f"Element {locator} not found or have no text field"):
                    self.make_screenshot()
                    raise AssertionError(f"Cannot enter text to the element with locator {locator}")

    def open_url(self, url: str):
        """Open provided URL"""
        with allure.step(f"Opening url: {url}"):
            self.driver.get(url)

    def is_button_switched_on(self, switch_button):
        """Check if the toggle switch button is on"""
        with allure.step(f"Checking if toggle switch button '{switch_button}' is On"):
            return self.get_attribute(switch_button, 'aria-checked') == 'true'

    def get_table_cell_value_from_input(self, table_locator: tuple, row_num: int, column_num: int):
        """Return value from a table cell with input type by row & column numbers"""
        with allure.step(f"Trying to get table value for row {row_num}, column {column_num}"):
            full_path = f'{table_locator[1]}/tr[{row_num}]/td[{column_num}]//input'
            locator = (By.XPATH, full_path)
            return self.get_attribute(locator, "value")

    def is_checkbox_checked(self, checkbox_status_locator: tuple, checkbox_num=1, name=None):
        """Verify if the check-box is checked by attribute in span parent to input with special class for 'checked'.
        Checkbox number can be added if several checkboxes with the same locator are on page (defaulted to 1).
        In some cases, checkbox name can be added to the report"""
        if name:
            checkbox = name
        else:
            checkbox = checkbox_num
        checkbox_status_path = f'({checkbox_status_locator[1]})[{checkbox_num}]'
        status_locator = (By.XPATH, checkbox_status_path)
        is_checked = False
        if 'ant-checkbox-checked' in self.get_attribute(status_locator, 'class'):
            is_checked = True
        with allure.step(f"Check status for checkbox '{checkbox}' is '{is_checked}'"):
            return is_checked

    def get_all_attributes_for_element(self, element):
        """Return dictionary with key: value for all attributes of the element"""
        with allure.step(f"Getting attributes for the element '{element}'"):
            all_attributes = self.driver.execute_script(
                'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) '
                '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
                element)
        with allure.step(f"Returning dict with attributes for the element '{element}': {all_attributes}"):
            return all_attributes

    def is_input_readonly(self, element):
        """Verify if input is inactive (read-only)"""
        with allure.step(f"Checking that input '{element}' is disabled (read-only)"):
            attr = self.get_all_attributes_for_element(element)
            if 'disabled' in attr.keys():
                with allure.step("'disabled' is in the attributes of the element, input is disabled (read-only)"):
                    return True
            elif 'tabindex' in attr.keys() and attr['tabindex'] == '-1':
                with allure.step("'tabindex=-1' is in the attributes of the element, input is disabled (read-only)"):
                    return True
            with allure.step("Input is enabled, not read-only!"):
                return False

    def is_element_present(self, locator: tuple):
        """Return True if the element is present on the page, else False"""
        with allure.step(f"Trying to locate element with locator {locator}"):
            try:
                WebDriverWait(driver=self.driver, timeout=3).until(EC.visibility_of_element_located(locator))
                with allure.step(f"Element {locator} is present on the page"):
                    return True
            except TimeoutException:
                with allure.step(f"Element {locator} is not present on the page"):
                    return False

    def is_button_enabled(self, element):
        """Verify if button is enabled and it can be clicked"""
        with allure.step(f"Checking if button '{element}' is enabled"):
            attr = self.get_all_attributes_for_element(element)
            if 'disabled' in attr.keys():
                with allure.step("The button is disabled and it cannot be clicked"):
                    return False
            with allure.step("The button is enabled and it can be clicked"):
                return True

    def scroll_to_element(self, element):
        """Move to the provided element"""
        with allure.step(f"Clicking element: {element}"):
            ActionChains(self.driver).scroll_to_element(element).pause(0.1).perform()

    def refresh_page(self):
        """Refresh the current page"""
        with allure.step("Refreshing the page"):
            self.driver.refresh()

    def get_tag_name(self, locator: tuple):
        """Return tag name of the element"""
        element = self.locate_element(locator)
        attr = element.tag_name
        with allure.step(f"The tag name is '{attr}'"):
            return attr

    def is_required_field(self, label_locator):
        """Checking if the form element is required"""
        return self.get_attribute(label_locator, 'class') == "ant-form-item-required"

    def modify_numeric_value(self, input_locator: tuple, action_button_locator: tuple, click_num=1):
        """Increase or decrease a numeric value in input with 'Up' or 'Down' buttons, one click by default."""
        numeric_input = self.locate_element(input_locator)
        self.click(numeric_input)
        time.sleep(1)
        action_btn = self.get_clickable_element(action_button_locator)
        for _ in range(click_num):
            with allure.step(f"Clicking button: {action_button_locator}"):
                self.click(action_btn)
                time.sleep(1)

    @staticmethod
    def get_new_objects_list(file_name):
        """Get the list of URLs to the newly created objects (Dealers or Users) if the file already exists"""
        list_of_objects = []
        if os.path.exists(file_name):
            with allure.step(f"Opening the '{file_name}' file to get the list of objects and returning it"):
                with open(file_name, 'r') as my_file:
                    list_of_objects = [line.rstrip() for line in my_file]
        with allure.step(f"Returning the list: {list_of_objects}"):
            return list_of_objects

    def add_new_objects_to_list(self, file_name):
        """Add the URL to the newly created object (Dealers or Users) to the file, if it exists, create file if not"""
        with allure.step(f"Saving the new object for later inactivation to the '{file_name}' file"):
            with open(file_name, 'a+') as my_file:
                current_url = self.get_current_url()
                my_file.write(f"{current_url}\n")

    def select_random_date_from_calender(self, calender_locator: tuple):
        """Select a new random date from calender, different from the existing date (if any)"""
        calender = self.locate_element(calender_locator)
        self.click(calender)
        all_available_dates = self.locate_all_elements(self.UNSELECTED_DATE_IN_CALENDER)
        new_date = random.choice(all_available_dates)
        self.click(new_date)
        time.sleep(2)

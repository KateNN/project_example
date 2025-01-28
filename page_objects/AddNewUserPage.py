import time
from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import string
import allure
import random

TIMEOUT = 2


class AddNewUserPage(BasePage):
    PATH = "dealers/101590"
    ADD_NEW_USER_FORM_TITLE = (By.CSS_SELECTOR, '.ant-page-header-heading-title')

    # Fields & Values
    FIRST_NAME_INPUT = (By.XPATH, '(//input)[2]')
    LAST_NAME_INPUT = (By.XPATH, '(//input)[3]')
    USERNAME_INPUT = (By.XPATH, '(//input)[4]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    EMAIL_INPUT = (By.XPATH, '(//input)[5]')
    MOBILE_PHONE_INPUT = (By.XPATH, '(//input)[7]')
    EXISTING_USERNAME = '...'

    # Alerts
    FORM_VALIDATION_FAILED_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-alert-message") and contains(., "Form validation failed")]')
    FORM_VALIDATION_FAILED_TEXT = 'Form validation failed. Check fields messages.'
    FIRST_NAME_REQUIRED_ALERT = (By.XPATH,
                                 '//div[contains(@role, "alert") and contains(., "The FirstName field is required.")]')
    FIRST_NAME_REQUIRED_TEXT = 'The FirstName field is required.'
    LAST_NAME_REQUIRED_ALERT = (By.XPATH,
                                '//div[contains(@role, "alert") and contains(., "The LastName field is required.")]')
    LAST_NAME_REQUIRED_TEXT = 'The LastName field is required.'
    USERNAME_REQUIRED_ALERT = (By.XPATH,
                               '//div[contains(@role, "alert") and contains(., "The Login field is required.")]')
    USERNAME_REQUIRED_TEXT = 'The Login field is required.'
    PASSWORD_REQUIRED_ALERT = (By.XPATH,
                               '//div[contains(@role, "alert") and contains(., "The Password field is required.")]')
    PASSWORD_REQUIRED_TEXT = 'The Password field is required.'
    USERNAME_MUST_BE_UNIQUE_ALERT = (By.XPATH,
                                     '//div[contains(@class, "ant-form-item-explain-error") and contains (., "Must be unique")]')
    MUST_BE_UNIQUE_TEXT = 'Must be unique'

    # Buttons
    ADD_NEW_USER_BTN = (By.XPATH, '//button[contains(@class, "ant-btn-default") and contains(.,"New User")]')
    SAVE_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    SUCCESS_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Go to created user")]')

    @allure.step("Generating a new user data")
    def generate_new_user_data(self):
        """Generate test data for a new user"""
        new_user = dict()
        new_user['first_name'] = 'QAtest'
        new_user['last_name'] = 'Auto' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        new_user['username'] = f"{new_user['first_name'].lower()}{new_user['last_name'].lower()}"
        new_user['email'] = f"{new_user['first_name'].lower()}.{new_user['last_name'].lower()}@test.com"
        new_user['password'] = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        new_user['mobile_phone'] = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        return new_user

    @allure.step("Filling 'Add New User' form with the provided data and saving changes")
    def add_new_user(self,
                     first_name: str = '',
                     last_name: str = '',
                     username: str = '',
                     email: str = '',
                     password: str = '',
                     mobile_phone: str = ''):
        """Fill 'Add new user' form with the provided user data and click 'Save' (empty values by default)"""
        # 1. Open "Add New User" form
        add_user_btn = self.locate_element(self.ADD_NEW_USER_BTN)
        self.click(add_user_btn)
        time.sleep(TIMEOUT)
        save_btn = self.locate_element(self.SAVE_BTN)

        # 2. Enter provided user data to the form
        self.type_in_text(self.FIRST_NAME_INPUT, first_name)
        self.type_in_text(self.LAST_NAME_INPUT, last_name)
        self.paste_text(self.USERNAME_INPUT, username)
        self.type_in_text(self.EMAIL_INPUT, email)
        self.paste_text(self.PASSWORD_INPUT, password)
        self.type_in_text(self.MOBILE_PHONE_INPUT, mobile_phone)

        # 3. Click "Save"
        self.click(save_btn)

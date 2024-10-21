from selenium.webdriver.common.by import By
import allure
from page_objects.BasePage import BasePage
import os


class LoginPage(BasePage):
    PATH = ""
    LOGIN_PAGE_TITLE = "MAX Inventory - Login to your account"
    WELCOME_TEXT = 'Welcome to ...'
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    USER_WITH_PITSTOP_ROLE = os.getenv('USER_WITH_PITSTOP_ROLE')
    USER_WITH_NO_PITSTOP_ROLE = os.getenv('USER_WITH_NO_PITSTOP_ROLE')
    PASSWORD = os.getenv('USER_PASSWORD')
    WELCOME_TO_PITSTOP = (By.CSS_SELECTOR, '.ant-page-header-heading-title')
    NOT_AUTHORIZED = (By.CSS_SELECTOR, '.ant-result-title')
    MAX_INVENTORY_URL = 'https://stage'

    LOGIN_BTN = (By.NAME, "submit")

    def log_in(self,
               username: str = '',
               password: str = ''):
        """Log in to PitsTop with the provided username and password (empty values by default)"""
        with allure.step("Logging in to Pitstop/MAX"):
            self.type_in_text(self.USERNAME_INPUT, username)
            self.type_in_text(self.PASSWORD_INPUT, password)
            login_btn = self.locate_element(self.LOGIN_BTN)
            self.click(login_btn)

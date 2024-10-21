from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class UserListPage(BasePage):
    PATH = "users"
    SEARCH_BAR_INPUT = (By.XPATH, '//input[@placeholder = "Enter search terms"]')
    SEARCH_BTN = (By.XPATH, '(//button)[3]')
    ITEMS_IN_SEARCH_RESULTS = (By.XPATH, '//td[contains(@data-label, "User ID")]')

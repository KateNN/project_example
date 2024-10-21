from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class LogoutPage(BasePage):
    PATH = "logout?"
    MAX_INVENTORY_LOGO = (By.XPATH, '//div[@id = "maxInventory_logo"]')

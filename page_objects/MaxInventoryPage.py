from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class MaxInventoryPage(BasePage):
    MAX_INVENTORY_PAGE_TITLE = '... Inventory Management'
    DEALER_NAME_INPUT = (By.XPATH, '//input[1]')

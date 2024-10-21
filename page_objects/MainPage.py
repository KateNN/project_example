from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    # Common elements for all pages
    DEALERS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content")]//a[@href="/dealers"]')
    GROUPS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content")]//a[@href="/groups"]')
    USERS_LEFT_MENU = (By.XPATH, '//span[contains(@class, "ant-menu-title-content")]//a[@href="/users"]')

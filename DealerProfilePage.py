from page_objects.BasePage import BasePage
# from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
# from page_objects.DealerListPage import DealerListPage
import time
from selenium.webdriver.common.by import By

TIMEOUT = 2


class DealerProfilePage(BasePage):
    # Dealer profile common elements
    PROFILE_HEADER = (By.XPATH, '//div[contains(@class, "ant-page-header-content") and contains(.,"is a dealer in")]')
    DEALER_NAME_IN_PROFILE = (By.CSS_SELECTOR, '.ant-page-header-heading-title')
    OPEN_IN_MAX_BTN = (By.XPATH, '//button//a[contains(@title, "Open In MAX")]')
    CLONE_BTN = (By.XPATH, '//button/span[contains(., "Clone")]/..')
    ADD_NEW_USER_BTN = (By.XPATH, '//button[contains(@class, "ant-btn-default") and contains(.,"New User")]')
    DEALER_ID_AND_BU_CODE = (By.XPATH, '//span[contains(., "Dealer ID")]')

    # Dealer profile top-level tabs
    DEALER_TAB = (By.XPATH, '//div[text()="Dealer"]')
    USERS_TAB = (By.XPATH, '//div[text()="Users"]')
    MAX_SETTINGS_TAB = (By.XPATH, '//div[text()="MAX Settings"]')
    SETTINGS_TAB = (By.XPATH, '//div[text()="Settings"]')
    PRICING_TAB = (By.XPATH, '//div[text()="Pricing"]')

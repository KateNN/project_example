from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By
import time
import allure

TIMEOUT = 5


class DealerListPage(BasePage):
    SEARCH_BAR_INPUT = (By.XPATH, '//input[@placeholder = "Enter search terms"]')
    WC_TEST_DEALER = "Windy City Chevrolet"
    WC_TEST_DEALER_LINK = (
        By.XPATH, '//td[contains(@data-label, "Dealer Name")]/a[contains(., "Windy City Chevrolet")]')

    def open_existing_dealer_profile(self, dealer_name):
        """Open existing dealer profile, dealer name is required"""
        with allure.step(f"Opening the '{dealer_name}' dealer profile"):
            dealers_menu = self.locate_element(self.DEALERS_LEFT_MENU)
            self.click(dealers_menu)
            self.locate_element(self.SEARCH_BAR_INPUT)
            self.paste_text(self.SEARCH_BAR_INPUT, dealer_name)
            locator = f"//td[contains(@data-label, 'Dealer Name')]/a[contains(., '{dealer_name}')]"
            link_to_dealer = self.locate_element((By.XPATH, locator))
            self.click(link_to_dealer)
            time.sleep(TIMEOUT)

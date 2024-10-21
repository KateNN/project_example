from page_objects.DealerProfilePage import DealerProfilePage
from selenium.webdriver.common.by import By
import allure
import time

TIMEOUT = 2


class DealerProfileUsersPage(DealerProfilePage):
    # 'Users' tab
    ENTER_USER_NAME = (By.XPATH, '//input[contains(@placeholder, "Enter user name")]')
    SEARCH_BTN = (By.XPATH, '//button[contains(., "Search")]')
    ADD_ACCESS_BTN = (By.XPATH, '//span[@title="Add"]/button')
    FILTER_BY_LOGIN_BTN = (By.XPATH, '//th[2]/div/span/span')
    FILTER_BY_LOGIN_INPUT = (By.XPATH, '//div[2]/input')
    FILTER_BY_LOGIN_OK_BTN = (By.XPATH, '//div[3]/button[3]')
    RESET_FILTER_BY_LOGIN_BTN = (By.XPATH, '//span[contains(., "Reset")]')
    LOGIN_IN_FILTER_RESULTS = (By.XPATH, '//table//td[2]')
    SELECT_GROUP_MODAL_TITLE = (By.XPATH, '(//div[contains(., "Select default group")])[7]')
    SELECT_GROUP_CANCEL_BTN = (By.XPATH, '//button[contains(., "Cancel")]')
    SELECT_GROUP_OK_BTN = (By.XPATH, '//button[contains(., "OK")]')

    @allure.step("Adding access to a dealer for existing user ('Users' tab of a dealer)")
    def add_user_to_dealer(self, user, select_group=False):
        """Add access to a dealer for existing user from 'Users' tab of a Dealer"""
        self.type_in_text(self.ENTER_USER_NAME, user)
        search_btn = self.get_clickable_element(self.SEARCH_BTN)
        self.click(search_btn)
        add_access = self.locate_element(self.ADD_ACCESS_BTN)
        self.click(add_access)
        time.sleep(TIMEOUT)
        try:
            self.locate_element(self.SELECT_GROUP_MODAL_TITLE)
            if select_group:
                ok_btn = self.get_clickable_element(self.SELECT_GROUP_OK_BTN)
                self.click(ok_btn)
            else:
                cancel_btn = self.get_clickable_element(self.SELECT_GROUP_CANCEL_BTN)
                self.click(cancel_btn)
        except AssertionError:
            pass
        time.sleep(TIMEOUT)

    @allure.step("Clearing 'Login' filter in 'Users' tab of dealer")
    def reset_filter_by_login(self):
        """Clear 'Login' filter in 'Users' tab of dealer"""
        filter_by_name = self.get_clickable_element(self.FILTER_BY_LOGIN_BTN)
        self.click(filter_by_name)
        clear_filter = self.locate_element(self.RESET_FILTER_BY_LOGIN_BTN)
        self.click(clear_filter)

    @allure.step("Checking if the user already has access to the dealer")
    def is_user_added_to_dealer(self, user):
        """Check if the user already has access to the dealer. Return True if the user is already added to the dealer"""
        filter_by_name = self.get_clickable_element(self.FILTER_BY_LOGIN_BTN)
        self.click(filter_by_name)
        self.type_in_text(self.FILTER_BY_LOGIN_INPUT, user)
        ok_btn = self.locate_element(self.FILTER_BY_LOGIN_OK_BTN)
        self.click(ok_btn)
        time.sleep(TIMEOUT)
        try:
            login_in_results = self.locate_element(self.LOGIN_IN_FILTER_RESULTS)
            self.reset_filter_by_login()
            return login_in_results.text == user
        except AssertionError:
            self.reset_filter_by_login()
            return False

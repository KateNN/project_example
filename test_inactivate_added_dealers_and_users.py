from page_objects.LoginPage import LoginPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
from page_objects.UserProfilePage import UserProfilePage
import time
import pytest
from pytest_check import check
import allure
import os

TIMEOUT = 4


@pytest.mark.inactivate
@allure.title("Inactivating dealers created during tests (switching to Inactive)")
def test_inactivate_dealers(driver):
    page = LoginPage(driver)
    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    with check:
        if new_dealers_to_inactivate:
            with allure.step("Logging to PitStop as Administrator"):
                page.open()
                page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                            password=page.PASSWORD)
                time.sleep(TIMEOUT)
            for dealer in new_dealers_to_inactivate:
                page.open_url(dealer)
                page = DealerProfileDealerPage(driver)
                time.sleep(TIMEOUT)
                if page.is_button_switched_on(page.SETTING_ACTIVE_BTN):
                    edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
                    page.click(edit_btn)
                    active_button = page.get_clickable_element(page.SETTING_ACTIVE_BTN)
                    with allure.step(f"Inactivating dealer {dealer}"):
                        page.click(active_button)
                        time.sleep(TIMEOUT)
                        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
                        page.click(save_btn)
                        time.sleep(TIMEOUT)
                        with allure.step(f"Verifying that dealer {dealer} is now Inactive"):
                            assert not page.is_button_switched_on(page.SETTING_ACTIVE_BTN), \
                                [f"Dealer {dealer} is still Active!", page.make_screenshot()]
                else:
                    with allure.step(f"Dealer {dealer} is already inactive"):
                        page.make_screenshot()
        else:
            with allure.step("No dealers to inactivate"):
                pass

        with allure.step(f"Removing '{page.NEW_DEALERS_FILE_NAME}' file if exists"):
            try:
                os.remove(page.NEW_DEALERS_FILE_NAME)
                with check:
                    with allure.step(f"Checking that '{page.NEW_DEALERS_FILE_NAME}' file is removed"):
                        assert not os.path.exists(page.NEW_DEALERS_FILE_NAME), \
                            f"File '{page.NEW_DEALERS_FILE_NAME}' is NOT removed"
            except OSError:
                with allure.step(f"File '{page.NEW_DEALERS_FILE_NAME}' doesn't exist"):
                    pass


@pytest.mark.inactivate
@allure.title("Inactivating users created during tests (switching to Inactive)")
def test_inactivate_users(driver):
    page = LoginPage(driver)
    new_users_to_inactivate = page.get_new_objects_list(page.NEW_USERS_FILE_NAME)
    with check:
        if new_users_to_inactivate:
            with allure.step("Logging to PitStop as Administrator"):
                page.open()
                page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                            password=page.PASSWORD)
                time.sleep(TIMEOUT)
            for user in new_users_to_inactivate:
                page.open_url(user)
                page = UserProfilePage(driver)
                time.sleep(6)
                if page.is_button_switched_on(page.GENERAL_ACTIVE_BTN):
                    edit_btn = page.get_clickable_element(page.GENERAL_EDIT_BTN)
                    page.click(edit_btn)
                    active_button = page.get_clickable_element(page.GENERAL_ACTIVE_BTN)
                    with allure.step(f"Inactivating user {user}"):
                        page.click(active_button)
                        time.sleep(TIMEOUT)
                        save_btn = page.get_clickable_element(page.GENERAL_SAVE_BTN)
                        page.click(save_btn)
                        time.sleep(TIMEOUT)
                        with allure.step(f"Verifying that user {user} is now Inactive"):
                            assert not page.is_button_switched_on(page.GENERAL_ACTIVE_BTN), \
                                [f"User {user} is still Active!", page.make_screenshot()]
                else:
                    with allure.step(f"User {user} is already inactive"):
                        page.make_screenshot()
        else:
            with allure.step("No users to inactivate"):
                pass

        with allure.step(f"Removing '{page.NEW_USERS_FILE_NAME}' file if exists"):
            try:
                os.remove(page.NEW_USERS_FILE_NAME)
                with check:
                    with allure.step(f"Checking that '{page.NEW_USERS_FILE_NAME}' file is removed"):
                        assert not os.path.exists(page.NEW_USERS_FILE_NAME), \
                            f"File '{page.NEW_USERS_FILE_NAME}' is NOT removed"
            except OSError:
                with allure.step(f"File '{page.NEW_USERS_FILE_NAME}' doesn't exist"):
                    pass

from page_objects.CreateNewDealerPage import CreateNewDealerPage
from page_objects.LoginPage import LoginPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
from datetime import date
import time
import random
import pytest
from pytest_check import check
import allure

TIMEOUT = 4


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872")
@allure.title("C14337, C14336  Administrator can add/remove Book Two, Book One cannot be removed")
def test_add_and_remove_book_two_and_book_one(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting' tab"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(5)
        element_to_scroll = page.locate_element(page.KBB_CONSUMER_TOOL_TITLE)
        page.scroll_to_element(element_to_scroll)
        time.sleep(TIMEOUT)

    if page.is_element_present(page.GUIDE_BOOK_TWO_TITLE):
        with allure.step("'Guide Book Two' is currently enabled: trying to disable and then enable 'Guide Book Two'"):
            with allure.step("Removing Second Guide Book"):
                remove_guide_book_two_btn = page.get_clickable_element(page.REMOVE_GUIDE_BOOK_TWO_BTN)
                page.click(remove_guide_book_two_btn)
                time.sleep(TIMEOUT)

            with check:
                with allure.step("Checking that 'Second Guide Book' is removed"):
                    assert not page.is_element_present(page.GUIDE_BOOK_TWO_TITLE), [
                        f"'Second Guide Book' is not removed",
                        page.make_screenshot()]

            with allure.step("Enabling 'Guide Book Two'"):
                enable_second_book_btn = page.get_clickable_element(page.ENABLE_SECOND_GUIDE_BOOK_BTN)
                page.click(enable_second_book_btn)
                ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
                page.click(ok_btn)
                time.sleep(TIMEOUT)

            with check:
                with allure.step("Checking that 'Guide Book Two' is now enabled"):
                    assert page.is_element_present(page.GUIDE_BOOK_TWO_TITLE), [f"'Guide Book Two' is not enabled",
                                                                                page.make_screenshot()]
    else:
        with allure.step("'Guide Book Two' is currently disabled: trying to enable and then disable 'Guide Book Two'"):
            with allure.step("Enabling 'Guide Book Two'"):
                enable_second_book_btn = page.get_clickable_element(page.ENABLE_SECOND_GUIDE_BOOK_BTN)
                page.click(enable_second_book_btn)
                time.sleep(TIMEOUT)
                ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
                page.click(ok_btn)
                time.sleep(TIMEOUT)

            with check:
                with allure.step("Checking that 'Guide Book Two' is now enabled"):
                    assert page.is_element_present(page.GUIDE_BOOK_TWO_TITLE), [f"'Guide Book Two' is not enabled",
                                                                                page.make_screenshot()]

            with allure.step("Removing Second Guide Book"):
                remove_guide_book_two_btn = page.get_clickable_element(page.REMOVE_GUIDE_BOOK_TWO_BTN)
                page.click(remove_guide_book_two_btn)
                time.sleep(TIMEOUT)

            with check:
                with allure.step("Checking that 'Second Guide Book' is removed"):
                    assert not page.is_element_present(page.GUIDE_BOOK_TWO_TITLE), \
                        [f"'Second Guide Book' is not removed", page.make_screenshot()]
    with check:
        with allure.step("Checking that 'Guide Book One' cannot be removed"):
            remove_guide_book_one_btn = page.locate_element(page.REMOVE_GUIDE_BOOK_ONE_BTN)
            assert not page.is_button_enabled(remove_guide_book_one_btn), [f"'Remove' button is enabled",
                                                                           page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872")
@allure.title("C13745, C13733, C13735 Administrator can edit book names and book types for book one and two")
def test_edit_book_one_and_book_two(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting' tab"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(5)
        element_to_scroll = page.locate_element(page.KBB_CONSUMER_TOOL_TITLE)
        page.scroll_to_element(element_to_scroll)

        if page.is_element_present(page.GUIDE_BOOK_TWO_TITLE):
            pass
        else:
            with allure.step("Enabling 'Guide Book Two'"):
                enable_second_book_btn = page.get_clickable_element(page.ENABLE_SECOND_GUIDE_BOOK_BTN)
                page.click(enable_second_book_btn)
                time.sleep(TIMEOUT)
                ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
                page.click(ok_btn)
                time.sleep(TIMEOUT)

    with allure.step("Checking that settings for 'Guide Book One' can be modified"):
        with allure.step("Switching to Edit mode"):
            edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
            page.click(edit_book1_btn)
            time.sleep(TIMEOUT)
        book1_name_before = page.get_text(page.GUIDE_BOOK_ONE_NAME)
        with allure.step(f"Modifying Name for 'Guide Book One' from '{book1_name_before}' to another name"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_NAME,
                                                   default_value=book1_name_before)
            time.sleep(2)

        book1_first_type_before = page.get_text(page.GUIDE_BOOK_ONE_1ST_TYPE)
        with allure.step(f"Modifying 1st Type for 'Guide Book One' from '{book1_first_type_before}' to another type"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_1ST_TYPE,
                                                   default_value=book1_first_type_before)
            time.sleep(2)

        book1_second_type_before = page.get_text(page.GUIDE_BOOK_ONE_2D_TYPE)
        with allure.step(f"Modifying 2nd Type for 'Guide Book One' from '{book1_second_type_before}' to another type"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_2ND_TYPE,
                                                   default_value=book1_second_type_before)
            time.sleep(2)

        with allure.step("Saving changes"):
            ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
            page.click(ok_btn)
            time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Guide Book One' name is now different from '{book1_name_before}'"):
                book1_name_after = page.get_text(page.GUIDE_BOOK_ONE_NAME)
                assert book1_name_before != book1_name_after, \
                    ["Guide Book One name was not modified", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that Book One 1st Type is now different from '{book1_first_type_before}'"):
                book1_first_type_after = page.get_text(page.GUIDE_BOOK_ONE_1ST_TYPE)
                assert book1_first_type_before != book1_first_type_after, \
                    ["Guide Book One 1st Type was not modified", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that Book One 2nd Type is now different from '{book1_second_type_before}'"):
                book1_second_type_after = page.get_text(page.GUIDE_BOOK_ONE_2D_TYPE)
                assert book1_second_type_before != book1_second_type_after, \
                    ["Guide Book One 2nd Type was not modified", page.make_screenshot()]

    with allure.step("Checking that settings for 'Guide Book Two' can be modified"):
        with allure.step("Switching to Edit mode"):
            edit_book2_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_TWO_BTN)
            page.click(edit_book2_btn)
            time.sleep(TIMEOUT)
        book2_name_before = page.get_text(page.GUIDE_BOOK_TWO_NAME)
        with allure.step(f"Modifying Name for 'Guide Book Two' from '{book2_name_before}' to another name"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_NAME,
                                                   default_value=book2_name_before)
            time.sleep(2)

        book2_first_type_before = page.get_text(page.GUIDE_BOOK_TWO_1ST_TYPE)
        with allure.step(f"Modifying 1st Type for 'Guide Book Two' from '{book2_first_type_before}' to another type"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_1ST_TYPE,
                                                   default_value=book2_first_type_before)
            time.sleep(2)

        book2_second_type_before = page.get_text(page.GUIDE_BOOK_TWO_2D_TYPE)
        with allure.step(f"Modifying 2nd Type for 'Guide Book Two' from '{book2_second_type_before}' to another type"):
            page.select_random_value_from_dropdown(input_locator=page.SELECT_BOOK_2ND_TYPE,
                                                   default_value=book2_second_type_before)
            time.sleep(2)

        with allure.step("Saving changes"):
            ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
            page.click(ok_btn)
            time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Guide Book Two' name is now different from '{book2_name_before}'"):
                book2_name_after = page.get_text(page.GUIDE_BOOK_TWO_NAME)
                assert book2_name_before != book2_name_after, \
                    ["Guide Book Two name was not modified", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that Book Two 1st Type is now different from '{book2_first_type_before}'"):
                book2_first_type_after = page.get_text(page.GUIDE_BOOK_TWO_1ST_TYPE)
                assert book2_first_type_before != book2_first_type_after, \
                    ["Guide Book Two 1st Type was not modified", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that Book Two 2nd Type is now different from '{book2_second_type_before}'"):
                book2_second_type_after = page.get_text(page.GUIDE_BOOK_TWO_2D_TYPE)
                assert book2_second_type_before != book2_second_type_after, \
                    ["Guide Book Two 2nd Type was not modified", page.make_screenshot()]

    with allure.step("Checking that Book One 2nd Type can be removed (changed to 'None')"):
        with check:
            with allure.step(f"Checking that Book One 2nd Type is not empty, has some value"):
                book1_second_type_before = page.get_text(page.GUIDE_BOOK_ONE_2D_TYPE)
                assert book1_second_type_before != 'None', \
                    ["Guide Book One 2nd Type is currently empty", page.make_screenshot()]
        with allure.step("Editing Book One 2nd Type - clearing the input and saving changes"):
            edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
            page.click(edit_book1_btn)
            time.sleep(TIMEOUT)
            type2_input = page.locate_element(page.SELECT_BOOK_2ND_TYPE)
            page.click(type2_input)
            clear_input = page.get_clickable_element(page.CLEAR_BOOK_2ND_TYPE_INPUT_BTN)
            page.click(clear_input)
            time.sleep(TIMEOUT)
            ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
            page.click(ok_btn)
            time.sleep(TIMEOUT)
        with check:
            with allure.step(f"Checking that Book One 2nd Type is now empty ('None')"):
                book1_second_type_after = page.get_text(page.GUIDE_BOOK_ONE_2D_TYPE)
                assert book1_second_type_after == 'None', \
                    [f"Guide Book One 2nd Type was not removed, it's '{book1_second_type_after}'",
                     page.make_screenshot()]

    with allure.step("Checking that Book Two 2nd Type can be removed (changed to 'None')"):
        with check:
            with allure.step(f"Checking that Book OTwo 2nd Type is not empty, has some value"):
                book2_second_type_before = page.get_text(page.GUIDE_BOOK_TWO_2D_TYPE)
                assert book2_second_type_before != 'None', \
                    ["Guide Book Two 2nd Type is currently empty", page.make_screenshot()]
        with allure.step("Editing Book Two 2nd Type - clearing the input and saving changes"):
            edit_book2_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_TWO_BTN)
            page.click(edit_book2_btn)
            time.sleep(TIMEOUT)
            type2_input = page.locate_element(page.SELECT_BOOK_2ND_TYPE)
            page.click(type2_input)
            clear_input = page.get_clickable_element(page.CLEAR_BOOK_2ND_TYPE_INPUT_BTN)
            page.click(clear_input)
            time.sleep(TIMEOUT)
            ok_btn = page.get_clickable_element(page.BOOK_VALUATIONS_OK_BTN)
            page.click(ok_btn)
            time.sleep(TIMEOUT)
        with check:
            with allure.step(f"Checking that Book Two 2nd Type is now empty ('None')"):
                book2_second_type_after = page.get_text(page.GUIDE_BOOK_TWO_2D_TYPE)
                assert book2_second_type_after == 'None', \
                    [f"Guide Book Two 2nd Type was not removed, it's '{book1_second_type_after}'",
                     page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872, MAX-10527")
@allure.title("C14406, Admin can edit specific settings for Galves, BlackBook, KBB books")
def test_edit_book_specific_settings(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting' tab"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(TIMEOUT)

    with allure.step("Modifying Name for 'Guide Book One' to 'Galves'"):
        edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
        page.click(edit_book1_btn)
        time.sleep(TIMEOUT)
        page.edit_guide_book_name(new_value='Galves')
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'Galves Specific Settings' are displayed"):
            assert page.is_element_present(page.GALVES_SPECIFIC_SETTINGS_TITLE), \
                ["'Galves Specific Settings' are not displayed", page.make_screenshot()]

    with allure.step("Saving 'Galves Specific Settings' setting before it is modified"):
        enable_mobile_galves_before = page.is_button_switched_on(page.ENABLE_MOBILE_GALVES_BTN)

    with allure.step("Modifying 'Galves Specific Settings'"):
        edit_galves_specific_settings_btn = page.get_clickable_element(page.EDIT_GALVES_SPECIFIC_SETTINGS_BTN)
        page.click(edit_galves_specific_settings_btn)
        enable_mobile_galves_btn = page.get_clickable_element(page.ENABLE_MOBILE_GALVES_BTN)
        page.click(enable_mobile_galves_btn)
        save_btn = page.get_clickable_element(page.SAVE_GALVES_SPECIFIC_SETTINGS_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'Galves Specific Settings' were modified"):
            enable_mobile_galves_after = page.is_button_switched_on(page.ENABLE_MOBILE_GALVES_BTN)
            assert enable_mobile_galves_before != enable_mobile_galves_after, \
                ["'Galves Specific Settings' were not modified", page.make_screenshot()]

    with allure.step("Modifying Name for 'Guide Book One' to 'BlackBook'"):
        edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
        page.click(edit_book1_btn)
        time.sleep(TIMEOUT)
        page.edit_guide_book_name(new_value='BlackBook')
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'BlackBook Specific Settings' are displayed"):
            assert page.is_element_present(page.BLACKBOOK_SPECIFIC_SETTINGS_TITLE), \
                ["'BlackBook Specific Settings' are not displayed", page.make_screenshot()]

    with allure.step("Saving 'BlackBook Specific Settings' setting before it is modified"):
        enable_mobile_blackbook_before = page.is_button_switched_on(page.ENABLE_MOBILE_BLACKBOOK_BTN)

    with allure.step("Modifying 'BlackBook Specific Settings'"):
        edit_blackbook_specific_settings_btn = page.get_clickable_element(page.EDIT_BLACKBOOK_SPECIFIC_SETTINGS_BTN)
        page.click(edit_blackbook_specific_settings_btn)
        enable_mobile_blackbook_btn = page.get_clickable_element(page.ENABLE_MOBILE_BLACKBOOK_BTN)
        page.click(enable_mobile_blackbook_btn)
        save_btn = page.get_clickable_element(page.SAVE_BLACKBOOK_SPECIFIC_SETTINGS_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'Blackbook Specific Settings' were modified"):
            enable_mobile_blackbook_after = page.is_button_switched_on(page.ENABLE_MOBILE_BLACKBOOK_BTN)
            assert enable_mobile_blackbook_before != enable_mobile_blackbook_after, \
                ["'Blackbook Specific Settings' were not modified", page.make_screenshot()]

    with allure.step("Modifying Name for 'Guide Book One' to 'KBB'"):
        edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
        page.click(edit_book1_btn)
        time.sleep(TIMEOUT)
        page.edit_guide_book_name(new_value='KBB')
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'KBB Specific Settings' are displayed"):
            assert page.is_element_present(page.KBB_SPECIFIC_SETTINGS_TITLE), \
                ["'KBB Specific Settings' are not displayed", page.make_screenshot()]

    with allure.step(f"Saving 'KBB Specific Settings' before editing"):
        kbb_inventory_dataset = page.get_text(page.KBB_INVENTORY_DATASET)
        kbb_appraisal_dataset = page.get_text(page.KBB_APPRAISAL_DATASET)
        newest_default_inv_condition = page.get_text(page.NEWEST_DEFAULT_INVENTORY_CONDITION)

    with allure.step("Modifying 'KBB Specific Settings' and saving changes"):
        edit_kbb_specific_settings_btn = page.get_clickable_element(page.EDIT_KBB_SPECIFIC_SETTINGS_BTN)
        page.click(edit_kbb_specific_settings_btn)
        with allure.step(f"Changing 'KBB Inventory Dataset:' from '{kbb_inventory_dataset}' to another value"):
            kbb_inventory_dataset_input = page.locate_element(page.KBB_INVENTORY_DATASET)
            page.click(kbb_inventory_dataset_input)
            other_option = page.locate_element(page.KBB_SPECIFIC_SETTINGS_OTHER_DROPDOWN_OPTION)
            page.click(other_option)
        with allure.step(f"Changing 'KBB Appraisal Dataset:' from '{kbb_appraisal_dataset}' to another value"):
            kbb_appraisal_dataset_input = page.locate_element(page.KBB_APPRAISAL_DATASET)
            page.click(kbb_appraisal_dataset_input)
            other_option = page.locate_element(page.KBB_SPECIFIC_SETTINGS_OTHER_DROPDOWN_OPTION)
            page.click(other_option)
        with allure.step(f"Changing 'Newest Default Inventory Condition:' from '{newest_default_inv_condition}' "
                         f"to another value"):
            newest_default_inv_condition_input = page.locate_element(page.NEWEST_DEFAULT_INVENTORY_CONDITION)
            page.click(newest_default_inv_condition_input)
            other_option = page.locate_element(page.KBB_SPECIFIC_SETTINGS_OTHER_DROPDOWN_OPTION)
            page.click(other_option)

        save_btn = page.get_clickable_element(page.SAVE_KBB_SPECIFIC_SETTINGS_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with allure.step(f"Saving 'KBB Specific Settings' after editing"):
        kbb_inventory_dataset_after = page.get_text(page.KBB_INVENTORY_DATASET)
        kbb_appraisal_dataset_after = page.get_text(page.KBB_APPRAISAL_DATASET)
        newest_default_inv_condition_after = page.get_text(page.NEWEST_DEFAULT_INVENTORY_CONDITION)

    with check:
        with allure.step("Checking that 'KBB Inventory Dataset:' setting was modified"):
            assert kbb_inventory_dataset_after != kbb_inventory_dataset, \
                [f"'KBB Inventory Dataset:' was not modified, it's '{kbb_inventory_dataset_after}'",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'KBB Appraisal Dataset:' setting was modified"):
            assert kbb_appraisal_dataset_after != kbb_appraisal_dataset, \
                [f"'KBB Appraisal Dataset:' was not modified, it's '{kbb_appraisal_dataset_after}'",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Newest Default Inventory Condition:' setting was modified"):
            assert newest_default_inv_condition_after != newest_default_inv_condition, \
                [f"'Newest Default Inventory Condition:' was not modified, it's '{newest_default_inv_condition_after}'",
                 page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872")
@allure.title("C13739, Users can toggle KBB Consumer Tool book types to display (Trade-In, Retail, Lending)")
def test_edit_kbb_consumer_tool(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting' tab and scrolling to 'KBB Consumer Tool'"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(TIMEOUT)
        element_to_scroll = page.locate_element(page.BOOKS_EDIT_UPGRADES_BTN)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

    with allure.step("Saving 'KBB Consumer Tool' settings before they are modified"):
        display_tradein_val_before = page.is_button_switched_on(page.DISPLAY_TRAIDIN_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_retail_val_before = page.is_button_switched_on(page.DISPLAY_RETAIL_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_lending_val_before = page.is_button_switched_on(page.DISPLAY_LENDING_VALUES_ON_KBB_CONSUMER_TOOL_BTN)

    with allure.step("Modifying 'KBB Consumer Tool' settings and saving changes"):
        edit_btn = page.get_clickable_element(page.KBB_CONSUMER_TOOL_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(2)
        display_tradein_val = page.get_clickable_element(page.DISPLAY_TRAIDIN_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_retail_val = page.get_clickable_element(page.DISPLAY_RETAIL_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_lending_val = page.get_clickable_element(page.DISPLAY_LENDING_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        page.click(display_tradein_val)
        time.sleep(1)
        page.click(display_retail_val)
        time.sleep(1)
        page.click(display_lending_val)
        time.sleep(1)
        save_btn = page.get_clickable_element(page.KBB_CONSUMER_TOOL_SAVE_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with allure.step(f"Saving 'KBB Consumer Tool' settings after editing"):
        display_tradein_val_after = page.is_button_switched_on(page.DISPLAY_TRAIDIN_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_retail_val_after = page.is_button_switched_on(page.DISPLAY_RETAIL_VALUES_ON_KBB_CONSUMER_TOOL_BTN)
        display_lending_val_after = page.is_button_switched_on(page.DISPLAY_LENDING_VALUES_ON_KBB_CONSUMER_TOOL_BTN)

    with check:
        with allure.step("Verifying that 'Display TradeIn Values on the KBB Consumer Tool:' setting was modified"):
            assert display_tradein_val_before != display_tradein_val_after, \
                [f"'Display TradeIn Values on the KBB Consumer Tool' was not modified, it's "
                 f"'{display_tradein_val_after}'", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Display Retail Values on the KBB Consumer Tool' setting was modified"):
            assert display_retail_val_before != display_retail_val_after, \
                [f"'Display Retail Values on the KBB Consumer Tool' was not modified, it's "
                 f"'{display_retail_val_after}'", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Display Lending Values on the KBB Consumer Tool:' setting was modified"):
            assert display_lending_val_before != display_lending_val_after, \
                [f"'Display Lending Values on the KBB Consumer Tool:' was not modified, it's "
                 f"'{display_lending_val_after}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872")
@allure.title("C13586, Users can edit 'Common' settings")
def test_edit_common_settings(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting'"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(TIMEOUT)

    with allure.step("Saving 'Common' settings before they are modified"):
        bookout_agreed_to_before = page.is_button_switched_on(page.BOOKOUT_AGREED_TO_BTN)
        calc_avg_book_values_before = page.is_button_switched_on(page.CALCULATE_AVG_BOOK_VALUES_BTN)
        set_advertising_status_before = page.is_button_switched_on(page.SET_ADVERTISING_STATUS_BTN)

    with allure.step("Modifying 'Common' settings and saving changes"):
        edit_btn = page.get_clickable_element(page.COMMON_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(2)
        bookout_agreed_to = page.get_clickable_element(page.BOOKOUT_AGREED_TO_BTN)
        calc_avg_book_values = page.get_clickable_element(page.CALCULATE_AVG_BOOK_VALUES_BTN)
        set_advertising_status = page.get_clickable_element(page.SET_ADVERTISING_STATUS_BTN)
        page.click(bookout_agreed_to)
        time.sleep(1)
        page.click(calc_avg_book_values)
        time.sleep(1)
        page.click(set_advertising_status)
        time.sleep(1)
        save_btn = page.get_clickable_element(page.COMMON_SAVE_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with allure.step(f"Saving 'Common' settings after editing"):
        bookout_agreed_to_after = page.is_button_switched_on(page.BOOKOUT_AGREED_TO_BTN)
        calc_avg_book_values_after = page.is_button_switched_on(page.CALCULATE_AVG_BOOK_VALUES_BTN)
        set_advertising_status_after = page.is_button_switched_on(page.SET_ADVERTISING_STATUS_BTN)

    with check:
        with allure.step("Verifying that 'Bookout Agreed To:' setting was modified"):
            assert bookout_agreed_to_before != bookout_agreed_to_after, \
                [f"'Bookout Agreed To:' was not modified, it's '{bookout_agreed_to_after}'", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Calculate Average Book Values:' setting was modified"):
            assert calc_avg_book_values_before != calc_avg_book_values_after, \
                [f"'Calculate Average Book Values:' was not modified, it's "
                 f"'{calc_avg_book_values_after}'", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Set Advertising Status:' setting was modified"):
            assert set_advertising_status_before != set_advertising_status_after, \
                [f"'Set Advertising Status:' was not modified, it's "
                 f"'{set_advertising_status_after}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Book Valuations Settings: MAX-9872, MAX-10527, MAX-10415")
@allure.title("C13750, C16050, C16051 Administrator can enable/disable upgrade settings: 'J.D. Power as 3rd book', "
              "'KBB Trade-In Values', 'Manheim Integration'")
def test_edit_book_upgrade_settings(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    new_dealers_to_inactivate = page.get_new_objects_list(page.NEW_DEALERS_FILE_NAME)
    if new_dealers_to_inactivate:
        dealer_url = new_dealers_to_inactivate[random.randint(0, len(new_dealers_to_inactivate) - 1)]
        page.open_url(dealer_url)
        time.sleep(TIMEOUT)
    else:
        with allure.step(
                "Going to 'Dealers' menu, generating test data, creating new dealer, opening it's profile"):
            dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
            page.click(dealers_menu)
            time.sleep(TIMEOUT)
            page = CreateNewDealerPage(driver)
            new_dealer = page.generate_new_dealer_data()
            page.create_new_dealer(name=new_dealer['name'],
                                   short_name=new_dealer['name'],
                                   website=new_dealer['website'],
                                   google_place_id=new_dealer['google_place_id'],
                                   address=new_dealer['address'],
                                   state=new_dealer['state'],
                                   zip_code=new_dealer['zip_code'])

            open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
            page.click(open_new_dealer_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    page = DealerProfileDealerPage(driver)
    page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)

    with allure.step("Switching to 'Book Valuations Setting' tab"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(5)
        element_to_scroll = page.locate_element(page.BOOKS_PAGE_BOTTOM)
        page.scroll_to_element(element_to_scroll)
        time.sleep(TIMEOUT)

    with allure.step("Checking that all Upgrade buttons are disabled, disabling if enabled"):
        if page.is_button_switched_on(page.BOOKS_JD_POWER_AS_3RD_BOOK_BTN) or page.is_button_switched_on(
                page.BOOKS_KBB_TRADE_IN_VALUES_BTN) or page.is_button_switched_on(page.BOOKS_MANHEIM_INTEGRATION_BTN):
            edit_btn = page.get_clickable_element(page.BOOKS_EDIT_UPGRADES_BTN)
            page.click(edit_btn)
            time.sleep(TIMEOUT)
            with allure.step("Disabling all Upgrade settings and saving changes"):
                disable_all_btn = page.get_clickable_element(page.BOOKS_UPGRADES_DISABLE_ALL_BTN)
                page.click(disable_all_btn)
                confirm_btn = page.get_clickable_element(page.BOOKS_CONFIRM_CHANGES_UPGRADES_BTN)
                page.click(confirm_btn)
                time.sleep(TIMEOUT)

    with check:
        with allure.step("Checking that 'J.D. Power as 3rd book' setting is disabled'"):
            assert not page.is_button_switched_on(page.BOOKS_JD_POWER_AS_3RD_BOOK_BTN), \
                ["'J.D. Power as 3rd book' setting is enabled", page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Start Date' for 'J.D. Power as 3rd book' setting is empty'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == '', \
                [f"'Start Date' for 'J.D. Power as 3rd book' setting is not empty, it's '{start_date}'",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'KBB Trade-In Values' setting is disabled'"):
            assert not page.is_button_switched_on(page.BOOKS_KBB_TRADE_IN_VALUES_BTN), \
                ["'KBB Trade-In Values' setting is enabled", page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Start Date' for 'KBB Trade-In Values' setting is empty'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == '', \
                [f"'Start Date' for 'KBB Trade-In Values' setting is not empty, it's '{start_date}'",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Manheim Integration' setting is disabled'"):
            assert not page.is_button_switched_on(page.BOOKS_MANHEIM_INTEGRATION_BTN), \
                ["'Manheim Integration' setting is enabled", page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Start Date' for 'Manheim Integration' setting is empty'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == '', \
                [f"'Start Date' for 'Manheim Integration' setting is not empty, it's '{start_date}'",
                 page.make_screenshot()]

    with allure.step("Enabling 'J.D. Power as 3rd book', 'KBB Trade-In Values', 'Manheim Integration' settings"
                     " and saving changes"):
        edit_btn = page.get_clickable_element(page.BOOKS_EDIT_UPGRADES_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        jdpower_as_3rd_book_btn = page.get_clickable_element(page.BOOKS_JD_POWER_AS_3RD_BOOK_BTN)
        kbb_trade_in_values_btn = page.get_clickable_element(page.BOOKS_KBB_TRADE_IN_VALUES_BTN)
        manheim_integration_btn = page.get_clickable_element(page.BOOKS_MANHEIM_INTEGRATION_BTN)
        page.click(jdpower_as_3rd_book_btn)
        time.sleep(1)
        page.click(kbb_trade_in_values_btn)
        time.sleep(1)
        page.click(manheim_integration_btn)
        time.sleep(1)
        save_btn = page.get_clickable_element(page.BOOKS_SAVE_UPGRADES_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with allure.step("Getting today's date"):
        today_date = date.today()
        today = today_date.strftime("%B %d, %Y")

    with check:
        with allure.step("Checking that 'J.D. Power as 3rd book' setting is enabled'"):
            assert page.is_button_switched_on(page.BOOKS_JD_POWER_AS_3RD_BOOK_BTN), \
                ["'J.D. Power as 3rd book' setting is disabled", page.make_screenshot()]

    with check:
        with allure.step(f"Checking that 'Start Date' for 'J.D. Power as 3rd book' setting is defaulted to "
                         f"Today: '{today}'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == today, \
                [f"Wrong 'Start Date' for 'J.D. Power as 3rd book': '{start_date}' instead of {today}",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'KBB Trade-In Values' setting is enabled'"):
            assert page.is_button_switched_on(page.BOOKS_KBB_TRADE_IN_VALUES_BTN), \
                ["'KBB Trade-In Values' setting is disabled", page.make_screenshot()]

    with check:
        with allure.step(f"Checking that 'Start Date' for 'KBB Trade-In Values' setting is defaulted to "
                         f"Today: '{today}'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == today, \
                [f"Wrong 'Start Date' for 'KBB Trade-In Values': '{start_date}' instead of {today}",
                 page.make_screenshot()]

    with check:
        with allure.step("Checking that 'Manheim Integration' setting is enabled'"):
            assert page.is_button_switched_on(page.BOOKS_MANHEIM_INTEGRATION_BTN), \
                ["'Manheim Integration' setting is disabled", page.make_screenshot()]

    with check:
        with allure.step(f"Checking that 'Start Date' for 'Manheim Integration' setting is defaulted to "
                         f"Today: '{today}'"):
            start_date = \
                page.get_attribute(page.BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE, 'innerHTML').strip("<!->\n\t ")
            assert start_date == today, \
                [f"Wrong 'Start Date' for 'Manheim Integration': '{start_date}' instead of {today}",
                 page.make_screenshot()]

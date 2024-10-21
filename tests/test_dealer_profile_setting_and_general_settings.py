from page_objects.CreateNewDealerPage import CreateNewDealerPage
from page_objects.LoginPage import LoginPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
from page_objects.DealerListPage import DealerListPage
from page_objects.DealerProfilePage import DealerProfilePage
import time
import pytest
from pytest_check import check
import allure
import random

TIMEOUT = 3


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-11967")
@allure.title("C22833, Dealer ID & BU Code are displayed in Dealer profile")
def test_dealer_id_and_bu_code_displayed_correctly(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the dealer profile for {page.WC_TEST_DEALER}"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step("Getting Dealer ID & BU Code from the dealer profile url and the 'Setting' tab"):
        page = DealerProfileDealerPage(driver)
        current_url = page.get_current_url()
        slash_index = current_url.rfind('/')
        dealer_id_from_url = current_url[slash_index + 1:]
        dealer_code_from_setting = page.get_attribute(page.DEALER_CODE_INPUT, 'value')

    with allure.step("Locating Dealer ID & BU Code in the Dealer profile header"):
        page = DealerProfilePage(driver)
        dealer_id_and_bu_code_in_header = page.get_text(page.DEALER_ID_AND_BU_CODE).split()
        dealer_id_in_header = dealer_id_and_bu_code_in_header[2]
        bu_code_in_header = dealer_id_and_bu_code_in_header[5]

    with check:
        with allure.step(f"Checking that the correct Dealer ID is displayed in the Dealer profile header: "
                         f"{dealer_id_from_url}"):
            assert dealer_id_from_url == dealer_id_in_header, [
                f"Wrong Dealer ID: '{dealer_id_in_header}' instead of '{dealer_id_from_url}'", page.make_screenshot()]

    with check:
        with allure.step(f"Checking that the correct BU Code is displayed in the Dealer profile header: "
                         f"{dealer_code_from_setting}"):
            assert dealer_code_from_setting == bu_code_in_header, [
                f"Wrong BU Code: '{bu_code_in_header}' instead of '{dealer_code_from_setting}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9512")
@allure.title("C13549, Dealer Code field cannot be modified")
def test_dealer_code_is_read_only(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the dealer profile for {page.WC_TEST_DEALER}"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step("Clicking 'Edit' button"):
        page = DealerProfileDealerPage(driver)
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        dealer_code_input = page.locate_element(page.DEALER_CODE_INPUT)

    with check:
        with allure.step("Checking if 'Dealer Code' is read-only"):
            assert page.is_input_readonly(dealer_code_input), ["Dealer Code is not read only!", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9512, MAX-9467, MAX-13494")
@allure.title("C13541, C13545 'Dealer' can be modified (must be unique within Active dealers), 'Dealer Short Name'"
              " can be modified (may match another dealer's Short Name)")
def test_dealer_name_and_short_name_can_be_modified(driver):
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

    with allure.step("Clicking 'Edit' button, modifying 'Dealer' field and saving changes (unique name)"):
        page = DealerProfileDealerPage(driver)
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        page.locate_element(page.DEALER_INPUT)
        current_name = page.get_attribute(page.DEALER_INPUT, 'value')
        modified_name = current_name + '1'
        page.paste_text(page.DEALER_INPUT, modified_name)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
        page.click(save_btn)
        time.sleep(8)

    with check:
        with allure.step(f"Checking if 'Dealer' now displays '{modified_name}'"):
            saved_name = page.get_attribute(page.DEALER_INPUT, 'value')
            assert saved_name == modified_name, [f"Wrong name in 'Dealer' field: '{saved_name}' instead of "
                                                 f"'{modified_name}'", page.make_screenshot()]
    with check:
        with allure.step(f"Checking if '{modified_name}' is displayed in the dealer profile header"):
            name_in_header = page.get_text(page.DEALER_NAME_IN_PROFILE)
            assert name_in_header == modified_name, [f"Wrong name in the header: '{saved_name}' instead of "
                                                     f"'{modified_name}'", page.make_screenshot()]

    with allure.step(f"Clicking 'Edit' button, pasting existing Dealer Name ('{page.EXISTING_DEALER_NAME}') to 'Dealer'"
                     f" field and saving changes"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        page.locate_element(page.DEALER_INPUT)
        page.paste_text(page.DEALER_INPUT, page.EXISTING_DEALER_NAME)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
        page.click(save_btn)
        time.sleep(TIMEOUT)

    with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
        alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
        assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
            [f"Wrong alert text for Form Validation: '{alert1}' instead of "
             f"'{page.FORM_VALIDATION_FAILED_TEXT}'", page.make_screenshot()]

    with allure.step(f"Asserting Name Must Be Unique alert: '{page.NAME_MUST_BE_UNIQUE_TEXT}'"):
        alert2 = page.locate_element(page.NAME_MUST_BE_UNIQUE_ALERT).text
        assert alert2 == page.NAME_MUST_BE_UNIQUE_TEXT, \
            [f"Wrong alert text for the Name field: '{alert2}' instead of "
             f"'{page.NAME_MUST_BE_UNIQUE_TEXT}'", page.make_screenshot()]

    with allure.step("Canceling changes"):
        cancel_btn = page.get_clickable_element(page.SETTING_CANCEL_ADDRESS_BTN)
        page.click(cancel_btn)
        time.sleep(TIMEOUT)

    with allure.step(f"Clicking 'Edit' button, modifying 'Dealer Short Name' (unique) and saving changes"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        page.locate_element(page.DEALER_SHORT_NAME_INPUT)
        current_short_name = page.get_attribute(page.DEALER_SHORT_NAME_INPUT, 'value')
        modified_short_name = current_short_name + '1'
        page.paste_text(page.DEALER_SHORT_NAME_INPUT, modified_short_name)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
        page.click(save_btn)

    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking if 'Dealer Short Name' field displays '{modified_short_name}'"):
            saved_dealer_short_name = page.get_attribute(page.DEALER_SHORT_NAME_INPUT, 'value')
            assert saved_dealer_short_name == modified_short_name, \
                [f"Wrong Dealer Short Name: '{saved_dealer_short_name}' instead of '{modified_short_name}'"
                    , page.make_screenshot()]

    with allure.step(f"Clicking 'Edit' button, modifying 'Dealer Short Name' (matches another dealer's Short Name:"
                     f" '{page.EXISTING_DEALER_SHORT_NAME}') and saving changes"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        page.locate_element(page.DEALER_SHORT_NAME_INPUT)
        page.paste_text(page.DEALER_SHORT_NAME_INPUT, page.EXISTING_DEALER_SHORT_NAME)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
        page.click(save_btn)

    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking if 'Dealer Short Name' field displays '{page.EXISTING_DEALER_SHORT_NAME}'"):
            saved_dealer_short_name = page.get_attribute(page.DEALER_SHORT_NAME_INPUT, 'value')
            assert saved_dealer_short_name == page.EXISTING_DEALER_SHORT_NAME, \
                [f"Wrong Dealer Short Name: '{saved_dealer_short_name}' instead of '{page.EXISTING_DEALER_SHORT_NAME}'"
                    , page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9512, MAX-9467, MAX-17897")
@allure.title("C21699, C55778 - All settings in 'Setting' tab (except of the 'Dealer Code') can be modified")
def test_setting_tab_settings_can_be_modified(driver):
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

    with allure.step("Opening 'Setting' tab"):
        page = DealerProfileDealerPage(driver)
        time.sleep(2)

    with allure.step("Saving initial settings in 'Setting' tab"):
        with allure.step("Saving 'Franchises' setting"):
            if page.is_element_present(page.FRANCHISES):
                franchises = []
                franchises_list = page.locate_all_elements(page.FRANCHISES)
                for item in franchises_list:
                    franchises.append(item.text)
                franchises_before = franchises
            else:
                with allure.step("No Franchises selected yet"):
                    franchises_before = []
            with allure.step(f"Current 'Franchises' are: '{franchises_before}'"):
                pass
        with allure.step("Saving 'Office Phone' setting"):
            office_phone_before = page.get_attribute(page.OFFICE_PHONE_INPUT, 'value')
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
        with allure.step("Saving 'Office Fax' setting"):
            office_fax_before = page.get_attribute(page.OFFICE_FAX_INPUT, 'value')
        with allure.step("Saving 'Address1' setting"):
            address1_before = page.get_attribute(page.ADDRESS1_INPUT, 'value')
        with allure.step("Saving 'Address2' setting"):
            address2_before = page.get_attribute(page.ADDRESS2_INPUT, 'value')
        with allure.step("Saving 'City' setting"):
            city_before = page.get_attribute(page.CITY_INPUT, 'value')
        with allure.step("Saving 'State' setting"):
            if page.is_element_present(page.STATE_CURRENT_VALUE):
                state_before = page.get_text(page.STATE_CURRENT_VALUE)
            else:
                with allure.step("No State selected yet"):
                    state_before = ''
        with allure.step("Saving 'Google Place Id' setting"):
            google_place_id_before = page.get_attribute(page.GOOGLE_PLACE_ID_INPUT, 'value')
        with allure.step("Saving 'Zip Code' setting"):
            zip_code_before = page.get_attribute(page.ZIP_CODE_INPUT, 'value')
        with allure.step("Saving 'Go Live Date (specify value for Go Live):' setting"):
            element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
            go_live_date_before = page.get_attribute(page.GO_LIVE_DATE, 'value')

    with allure.step("Modifying 'Franchises'"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_FRANCHISES_BTN)
        page.click(edit_btn)
        time.sleep(2)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_FRANCHISES_BTN)
        page.select_random_franchise(franchises_before)
        franchises_input = page.locate_element(page.FRANCHISES_INPUT)
        page.click(franchises_input)
        time.sleep(2)
        page.click(save_btn)
    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step("Modifying settings in 'Address' section"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDRESS_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDRESS_BTN)
        with allure.step("Modifying 'Office Phone' setting"):
            office_phone_modified = office_phone_before + '1'
            page.paste_text(page.OFFICE_PHONE_INPUT, office_phone_modified)
            time.sleep(1)
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Modifying 'Office Fax' setting"):
            office_fax_modified = office_fax_before + '1'
            page.paste_text(page.OFFICE_FAX_INPUT, office_fax_modified)
            time.sleep(1)
        with allure.step("Modifying 'Address1' setting"):
            address1_modified = address1_before + '1'
            page.paste_text(page.ADDRESS1_INPUT, address1_modified)
            time.sleep(1)
        with allure.step("Modifying 'Address2' setting"):
            address2_modified = address2_before + '1'
            page.paste_text(page.ADDRESS2_INPUT, address2_modified)
            time.sleep(1)
        with allure.step("Modifying 'City' setting"):
            city_modified = city_before + '1'
            page.paste_text(page.CITY_INPUT, city_modified)
            time.sleep(1)
        with allure.step("Modifying 'State' setting"):
            page.select_random_value_from_dropdown(input_locator=page.STATE_INPUT,
                                                   default_value=state_before)
            element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
        with allure.step("Modifying 'Google Place Id' setting"):
            google_place_id_modified = google_place_id_before + '1'
            page.paste_text(page.GOOGLE_PLACE_ID_INPUT, google_place_id_modified)
            time.sleep(1)
        with allure.step("Modifying 'Zip Code' setting"):
            zip_code_modified = page.get_random_zip_code(zip_code_before)
            page.paste_text(page.ZIP_CODE_INPUT, zip_code_modified)
            time.sleep(1)
        with allure.step("Saving changes"):
            page.click(save_btn)
        with allure.step(f"Checking that success message is displayed"):
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Modifying 'Go Live Date (specify value for Go Live):'"):
        element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_ADDITIONAL_BTN)
        page.click(edit_btn)
        time.sleep(2)
        save_btn = page.get_clickable_element(page.SETTING_SAVE_ADDITIONAL_BTN)
        page.select_random_date_from_calender(calender_locator=page.GO_LIVE_DATE)
        time.sleep(2)
        go_live_date_modified = page.get_attribute(page.GO_LIVE_DATE, 'value')
        page.click(save_btn)
    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step("Checking that settings in 'Setting' were modified"):
        with allure.step("Scrolling the page up"):
            element_to_scroll = page.locate_element(page.FRANCHISES_INPUT)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
        with check:
            with allure.step(f"Checking that 'Franchises' were modified"):
                if page.is_element_present(page.FRANCHISES):
                    franchises = []
                    franchises_list = page.locate_all_elements(page.FRANCHISES)
                    for item in franchises_list:
                        franchises.append(item.text)
                    franchises_after = franchises
                else:
                    franchises_after = []
                with allure.step(f"Current 'Franchises' are: '{franchises_after}', were: '{franchises_before}'"):
                    pass
                assert franchises_after != franchises_before, \
                    [f"'Franchises' were not modified: it's still '{franchises_before}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Office Phone' was modified"):
                office_phone_after = page.get_attribute(page.OFFICE_PHONE_INPUT, 'value')
                with allure.step(f"Current 'Office Phone' is: '{office_phone_after}', was: '{office_phone_before}'"):
                    pass
                assert office_phone_after != office_phone_before and office_phone_after == office_phone_modified, \
                    [f"'Office Phone' was not modified: it's '{office_phone_after}' instead of "
                     f"'{office_phone_modified}'", page.make_screenshot()]
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
        with check:
            with allure.step(f"Checking that 'Office Fax' was modified"):
                office_fax_after = page.get_attribute(page.OFFICE_FAX_INPUT, 'value')
                with allure.step(f"Current 'Office Fax' is: '{office_fax_after}', was: '{office_fax_before}'"):
                    pass
                assert office_fax_after != office_fax_before and office_fax_after == office_fax_modified, \
                    [f"'Office Fax' was not modified: it's '{office_fax_after}' instead of "
                     f"'{office_fax_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Address1' was modified"):
                address1_after = page.get_attribute(page.ADDRESS1_INPUT, 'value')
                with allure.step(f"Current 'Address1' is: '{address1_after}', was: '{address1_before}'"):
                    pass
                assert address1_after != address1_before and address1_after == address1_modified, \
                    [f"'Address1' was not modified: it's '{address1_after}' instead of "
                     f"'{address1_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Address2' was modified"):
                address2_after = page.get_attribute(page.ADDRESS2_INPUT, 'value')
                with allure.step(f"Current 'Address2' is: '{address2_after}', was: '{address2_before}'"):
                    pass
                assert address2_after != address2_before and address2_after == address2_modified, \
                    [f"'Address2' was not modified: it's '{address2_after}' instead of "
                     f"'{address2_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'City' was modified"):
                city_after = page.get_attribute(page.CITY_INPUT, 'value')
                with allure.step(f"Current 'City' is: '{city_after}', was: '{city_before}'"):
                    pass
                assert city_after != city_before and city_after == city_modified, \
                    [f"'City' was not modified: it's '{city_after}' instead of "
                     f"'{city_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'State' was modified"):
                state_after = page.get_text(page.STATE_CURRENT_VALUE)
                with allure.step(f"Current 'State' is: '{state_after}', was: '{state_before}'"):
                    pass
                assert state_after != state_before, \
                    [f"'State' was not modified: it's still '{state_after}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Google Place Id' was modified"):
                google_place_id_after = page.get_attribute(page.GOOGLE_PLACE_ID_INPUT, 'value')
                with allure.step(f"Current 'Google Place Id' is: '{google_place_id_after}', was: "
                                 f"'{google_place_id_before}'"):
                    pass
                assert google_place_id_after != google_place_id_before \
                       and google_place_id_after == google_place_id_modified, \
                    [f"'Google Place Id' was not modified: it's '{google_place_id_after}' instead of "
                     f"'{google_place_id_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Zip Code' was modified"):
                zip_code_after = page.get_attribute(page.ZIP_CODE_INPUT, 'value')
                with allure.step(f"Current 'Zip Code' is: '{zip_code_after}', was: '{zip_code_before}'"):
                    pass
                assert zip_code_after != zip_code_before and zip_code_after == zip_code_modified, \
                    [f"'Zip Code' was not modified: it's '{zip_code_after}' instead of "
                     f"'{zip_code_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Go Live Date (specify value for Go Live):' was modified"):
                element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
                page.scroll_to_element(element_to_scroll)
                time.sleep(2)
                go_live_date_after = page.get_attribute(page.GO_LIVE_DATE, 'value')
                with allure.step(f"Current 'Go Live Date (specify value for Go Live):' is: '{go_live_date_after}', "
                                 f"was: '{go_live_date_before}'"):
                    pass
                assert go_live_date_after != go_live_date_before and go_live_date_after == go_live_date_modified, \
                    [f"'Go Live Date (specify value for Go Live):' was not modified: it's '{go_live_date_after}' "
                     f"instead of '{go_live_date_modified}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9512, MAX-9467")
@allure.title("State field is required")
def test_setting_tab_state_field_is_required(driver):
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

    with allure.step("Opening 'Setting' tab"):
        page = DealerProfileDealerPage(driver)

    with allure.step("Scrolling the page down"):
        element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
        page.scroll_to_element(element_to_scroll)
        time.sleep(1)

    with check:
        with allure.step(f"Checking that 'State' is required"):
            assert page.is_required_field(page.STATE_LABEL), ["'State' field is not required", page.make_screenshot()]

    with allure.step("Switching to 'Edit' mode"):
        edit_btn = page.get_clickable_element(page.SETTING_EDIT_FRANCHISES_BTN)
        page.click(edit_btn)
        time.sleep(1)

    with allure.step("Scrolling the page down"):
        element_to_scroll = page.locate_element(page.ZIP_CODE_INPUT)
        page.scroll_to_element(element_to_scroll)
        time.sleep(1)

    with check:
        with allure.step(f"Checking that 'State' is required in the Edit mode too"):
            assert page.is_required_field(page.STATE_LABEL), ["'State' field is not required in the Edit mode",
                                                              page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-10526")
@allure.title("C13658 - Admin can edit 'Access Groups'")
def test_access_groups_can_be_modified(driver):
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

    with allure.step("Opening 'General Settings' - 'Access Groups' sub-tab"):
        page = DealerProfileDealerPage(driver)
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(TIMEOUT)
        access_groups = page.locate_element(page.GEN_SET_ACCESS_GROUPS)
        page.click(access_groups)
        time.sleep(TIMEOUT)

    with allure.step("Saving the current list of 'Access Groups'"):
        groups = page.locate_all_elements(page.ACCESS_GROUPS)
        access_groups_before = []
        for i in range(len(groups)):
            access_groups_before.append(groups[i].text)
        with allure.step(f"Current Access Groups: {access_groups_before}"):
            pass

    with allure.step("Adding a new group to the list of 'Access Groups'"):
        new_group = page.select_random_access_group(access_groups_before)

    with check:
        with allure.step(f"Checking that '{new_group}' was added to the list of Access Groups"):
            groups = page.locate_all_elements(page.ACCESS_GROUPS)
            access_groups_after = []
            for i in range(len(groups)):
                access_groups_after.append(groups[i].text)
            with allure.step(f"Current Access Groups: {access_groups_after}"):
                pass
            assert new_group in access_groups_after and access_groups_after != access_groups_before, \
                [f"'Access Groups were not modified: '{new_group}' was not added to the list", page.make_screenshot()]

    with allure.step(f"Removing '{new_group}' from the list of 'Access Groups'"):
        page.remove_access_group(new_group)

    with check:
        with allure.step(f"Checking that '{new_group}' was removed from the list of Access Groups"):
            groups = page.locate_all_elements(page.ACCESS_GROUPS)
            access_groups_after = []
            for i in range(len(groups)):
                access_groups_after.append(groups[i].text)
            with allure.step(f"Current Access Groups: {access_groups_after}"):
                pass
            assert new_group not in access_groups_after and access_groups_after == access_groups_before, \
                [f"'{new_group}' was not removed from to the list", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-11834")
@allure.title("C22634 - 'Dealer Appraisal Form Settings' are displayed and can be edited")
def test_edit_dealer_appraisal_form_settings(driver):
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

    with allure.step("Opening 'General Settings' - 'Dealer Appraisal Form Settings' sub-tab"):
        page = DealerProfileDealerPage(driver)
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(TIMEOUT)
        dealer_appraisal_form_settings = page.locate_element(page.GEN_SET_DEALER_APPRAISAL_FORM_SETTINGS)
        page.click(dealer_appraisal_form_settings)
        time.sleep(TIMEOUT)

    with allure.step("Locating the 'Dealer Appraisal Form Settings' section header"):
        page.locate_element(page.DEALER_APPRAISAL_FORM_SETTINGS_HEADER)

    with allure.step("Saving the current values in 'Dealer Appraisal Form Settings' section"):
        with allure.step("Saving 'Appraisal Valid For Days:'"):
            appraisal_valid_for_days_before = page.get_attribute(page.APPRAISAL_VALID_FOR_DAYS_INPUT, 'value')
        with allure.step("Saving 'Appraisal Valid For Miles:'"):
            appraisal_valid_for_miles_before = page.get_attribute(page.APPRAISAL_VALID_FOR_MILES_INPUT, 'value')
        with allure.step("Saving 'Appraisal Form memo:'"):
            appraisal_form_memo_before = page.get_attribute(page.APPRAISAL_FORM_MEMO_INPUT, 'value')
        with allure.step("Saving 'Appraisal Form Disclaimer:'"):
            appraisal_form_disclaimer_before = page.get_attribute(page.APPRAISAL_FORM_DISCLAIMER_INPUT, 'value')
        with allure.step("Saving 'Show Options By Default:'"):
            show_options_by_default_before = page.is_button_switched_on(page.SHOW_OPTIONS_BY_DEFAULT_BTN)
        with allure.step("Saving 'Show Check on Appraisal Form:'"):
            show_check_on_appraisal_form_before = page.is_button_switched_on(page.SHOW_CHECK_ON_APPRAISAL_FORM_BTN)

    with allure.step("Modifying settings in 'Dealer Appraisal Form Settings' section"):
        edit_btn = page.get_clickable_element(page.DEALER_APPRAISAL_FORM_SETTINGS_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.DEALER_APPRAISAL_FORM_SETTINGS_SAVE_BTN)
        with allure.step("Modifying 'Appraisal Valid For Days:' setting"):
            page.modify_numeric_value(page.APPRAISAL_VALID_FOR_DAYS_INPUT, page.APPRAISAL_VALID_FOR_DAYS_INCREASE_BTN)
        with allure.step("Modifying 'Appraisal Valid For Miles:' setting"):
            page.modify_numeric_value(page.APPRAISAL_VALID_FOR_MILES_INPUT, page.APPRAISAL_VALID_FOR_MILES_INCREASE_BTN)
        with allure.step("Modifying 'Appraisal Form memo:' setting"):
            appraisal_form_memo_modified = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            appraisal_form_memo_input = page.locate_element(page.APPRAISAL_FORM_MEMO_INPUT)
            page.click(appraisal_form_memo_input)
            time.sleep(1)
            page.type_in_text(page.APPRAISAL_FORM_MEMO_INPUT, appraisal_form_memo_modified)
            time.sleep(1)
        with allure.step("Modifying 'Appraisal Form Disclaimer:' setting"):
            appraisal_form_disclaimer_modified = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            appraisal_form_disclaimer_input = page.locate_element(page.APPRAISAL_FORM_DISCLAIMER_INPUT)
            page.click(appraisal_form_disclaimer_input)
            time.sleep(1)
            page.type_in_text(page.APPRAISAL_FORM_DISCLAIMER_INPUT, appraisal_form_disclaimer_modified)
            time.sleep(1)
        with allure.step("Modifying 'Show Options By Default:' setting"):
            show_options_by_default_btn = page.get_clickable_element(page.SHOW_OPTIONS_BY_DEFAULT_BTN)
            page.click(show_options_by_default_btn)
            time.sleep(1)
        with allure.step("Modifying 'Show Check on Appraisal Form:' setting"):
            show_check_on_appraisal_form_btn = page.get_clickable_element(page.SHOW_CHECK_ON_APPRAISAL_FORM_BTN)
            page.click(show_check_on_appraisal_form_btn)
            time.sleep(1)
        with allure.step("Saving changes"):
            page.click(save_btn)
        with allure.step(f"Checking that success message is displayed"):
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Checking that all settings in 'Dealer Appraisal Form Settings' were modified"):
        with check:
            with allure.step(f"Checking that 'Appraisal Valid For Days:' is modified correctly "
                             f"(was '{appraisal_valid_for_days_before}')"):
                appraisal_valid_for_days_after = page.get_attribute(page.APPRAISAL_VALID_FOR_DAYS_INPUT, 'value')
                assert appraisal_valid_for_days_after == str(int(appraisal_valid_for_days_before) + 1), \
                    [f"'Appraisal Valid For Days:' is not modified correctly: it's '{appraisal_valid_for_days_after}'"
                     f" instead of '{str(int(appraisal_valid_for_days_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Valid For Miles:' is modified correctly "
                             f"(was '{appraisal_valid_for_miles_before}')"):
                appraisal_valid_for_miles_after = page.get_attribute(page.APPRAISAL_VALID_FOR_MILES_INPUT, 'value')
                assert appraisal_valid_for_miles_after == str(int(appraisal_valid_for_miles_before) + 1), \
                    [f"'Appraisal Valid For Miles:' is not modified correctly: it's '{appraisal_valid_for_miles_after}'"
                     f" instead of '{str(int(appraisal_valid_for_miles_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Form memo:' is modified correctly "
                             f"(was '{appraisal_form_memo_before}')"):
                appraisal_form_memo_after = page.get_attribute(page.APPRAISAL_FORM_MEMO_INPUT, 'value')
                assert appraisal_form_memo_after != appraisal_form_memo_before and \
                       appraisal_form_memo_after == appraisal_form_memo_modified, \
                    [f"'Appraisal Form memo:' is not modified correctly: it's '{appraisal_form_memo_after}' "
                     f"instead of '{appraisal_form_memo_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Form Disclaimer:' is modified correctly "
                             f"(was '{appraisal_form_disclaimer_before}')"):
                with allure.step("Saving 'Appraisal Form Disclaimer:'"):
                    appraisal_form_disclaimer_after = page.get_attribute(page.APPRAISAL_FORM_DISCLAIMER_INPUT, 'value')
                assert appraisal_form_disclaimer_after != appraisal_form_disclaimer_before and \
                       appraisal_form_disclaimer_after == appraisal_form_disclaimer_modified, \
                    [f"'Appraisal Form Disclaimer:' is not modified correctly: it's '{appraisal_form_disclaimer_after}'"
                     f" instead of '{appraisal_form_disclaimer_modified}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Options By Default:' is modified "
                             f"(was '{show_options_by_default_before}')"):
                show_options_by_default_after = page.is_button_switched_on(page.SHOW_OPTIONS_BY_DEFAULT_BTN)
                assert show_options_by_default_after != show_options_by_default_before, \
                    [f"'Show Options By Default:' is not modified", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Check on Appraisal Form:' is modified "
                             f" (was '{show_check_on_appraisal_form_before}')"):
                show_check_on_appraisal_form_after = page.is_button_switched_on(page.SHOW_CHECK_ON_APPRAISAL_FORM_BTN)
                assert show_check_on_appraisal_form_after != show_check_on_appraisal_form_before, \
                    [f"'Show Check on Appraisal Form:' is not modified", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-16543")
@allure.title("C53109 - 'General Settings Scorecard' setting is displayed and it can be edited")
def test_scorecard_is_displayed_and_can_be_modified(driver):
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

    with allure.step("Opening 'General Settings' - 'Scorecard - Units Sold Thresholds' sub-tab"):
        page = DealerProfileDealerPage(driver)
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(TIMEOUT)
        scorecard = page.locate_element(page.GEN_SET_SCORECARD)
        page.click(scorecard)
        time.sleep(TIMEOUT)

    with allure.step("Locating the 'Scorecard - Units Sold Thresholds' header"):
        page.locate_element(page.SCORECARD_HEADER)

    with allure.step("Saving the current values in 'Scorecard - Units Sold Thresholds'"):
        with allure.step("Saving 'Threshold for 4 Weeks:'"):
            threshold_4_weeks_before = page.get_attribute(page.THRESHOLD_4_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 8 Weeks:'"):
            threshold_8_weeks_before = page.get_attribute(page.THRESHOLD_8_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 12 Weeks:'"):
            threshold_12_weeks_before = page.get_attribute(page.THRESHOLD_12_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 13 Weeks:'"):
            threshold_13_weeks_before = page.get_attribute(page.THRESHOLD_13_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 26 Weeks:'"):
            threshold_26_weeks_before = page.get_attribute(page.THRESHOLD_26_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 52 Weeks:'"):
            threshold_52_weeks_before = page.get_attribute(page.THRESHOLD_52_WEEKS_INPUT, 'value')

    with allure.step("Modifying settings in 'Scorecard - Units Sold Thresholds' and saving the changes"):
        edit_btn = page.get_clickable_element(page.SCORECARD_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)
        save_btn = page.get_clickable_element(page.SCORECARD_SAVE_BTN)
        with allure.step("Modifying 'Threshold for 4 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_4_WEEKS_INPUT, page.THRESHOLD_4_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Threshold for 8 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_8_WEEKS_INPUT, page.THRESHOLD_8_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Threshold for 12 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_12_WEEKS_INPUT, page.THRESHOLD_12_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Threshold for 13 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_13_WEEKS_INPUT, page.THRESHOLD_13_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Threshold for 26 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_26_WEEKS_INPUT, page.THRESHOLD_26_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Threshold for 52 Weeks:' setting"):
            page.modify_numeric_value(page.THRESHOLD_52_WEEKS_INPUT, page.THRESHOLD_52_WEEKS_INCREASE_BTN)
        with allure.step("Saving changes"):
            page.click(save_btn)
        with allure.step(f"Checking that success message is displayed"):
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Checking that all settings in 'Scorecard - Units Sold Thresholds' were modified"):
        with check:
            with allure.step(f"Checking that 'Threshold for 4 Weeks:' is modified correctly "
                             f"(was '{threshold_4_weeks_before}')"):
                threshold_4_weeks_after = page.get_attribute(page.THRESHOLD_4_WEEKS_INPUT, 'value')
                assert threshold_4_weeks_after == str(int(threshold_4_weeks_before) + 1), \
                    [f"'Threshold for 4 Weeks:' is not modified correctly: it's '{threshold_4_weeks_after}'"
                     f" instead of '{str(int(threshold_4_weeks_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Threshold for 8 Weeks:' is modified correctly "
                             f"(was '{threshold_8_weeks_before}')"):
                threshold_8_weeks_after = page.get_attribute(page.THRESHOLD_8_WEEKS_INPUT, 'value')
                assert threshold_8_weeks_after == str(int(threshold_8_weeks_before) + 1), \
                    [f"'Threshold for 8 Weeks:' is not modified correctly: it's '{threshold_8_weeks_after}'"
                     f" instead of '{str(int(threshold_8_weeks_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Threshold for 12 Weeks:' is modified correctly "
                             f"(was '{threshold_12_weeks_before}')"):
                threshold_12_weeks_after = page.get_attribute(page.THRESHOLD_12_WEEKS_INPUT, 'value')
                assert threshold_12_weeks_after == str(int(threshold_12_weeks_before) + 1), \
                    [f"'Threshold for 12 Weeks:' is not modified correctly: it's '{threshold_12_weeks_after}'"
                     f" instead of '{str(int(threshold_12_weeks_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Threshold for 13 Weeks:' is modified correctly "
                             f"(was '{threshold_13_weeks_before}')"):
                threshold_13_weeks_after = page.get_attribute(page.THRESHOLD_13_WEEKS_INPUT, 'value')
                assert threshold_13_weeks_after == str(int(threshold_13_weeks_before) + 1), \
                    [f"'Threshold for 13 Weeks:' is not modified correctly: it's '{threshold_13_weeks_after}'"
                     f" instead of '{str(int(threshold_13_weeks_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Threshold for 26 Weeks:' is modified correctly "
                             f"(was '{threshold_26_weeks_before}')"):
                threshold_26_weeks_after = page.get_attribute(page.THRESHOLD_26_WEEKS_INPUT, 'value')
                assert threshold_26_weeks_after == str(int(threshold_26_weeks_before) + 1), \
                    [f"'Threshold for 26 Weeks:' is not modified correctly: it's '{threshold_26_weeks_after}'"
                     f" instead of '{str(int(threshold_26_weeks_before) + 1)}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Threshold for 52 Weeks:' is modified correctly "
                             f"(was '{threshold_52_weeks_before}')"):
                threshold_52_weeks_after = page.get_attribute(page.THRESHOLD_52_WEEKS_INPUT, 'value')
                assert threshold_52_weeks_after == str(int(threshold_52_weeks_before) + 1), \
                    [f"'Threshold for 52 Weeks:' is not modified correctly: it's '{threshold_52_weeks_after}'"
                     f" instead of '{str(int(threshold_52_weeks_before) + 1)}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9512")
@allure.title("C13632 - All settings in 'Dealer General' can be modified")
def test_all_settings_in_dealer_general_can_be_modified(driver):
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

    with allure.step("Opening 'General Settings' - 'Dealer General' sub-tab"):
        page = DealerProfileDealerPage(driver)
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(TIMEOUT)
        dealer_general = page.locate_element(page.GEN_SET_DEALER_GENERAL)
        page.click(dealer_general)
        time.sleep(TIMEOUT)

    with allure.step("Saving the current values in 'Dealer General'"):
        dealer_general_before = dict()
        with allure.step("Saving 'Show Recall:' setting"):
            dealer_general_before['show_recall'] = page.is_button_switched_on(page.SHOW_RECALL_BTN)
        with allure.step("Saving 'Trade-In Offer Auto Calculate:' setting"):
            dealer_general_before['trade_in_offer_auto_calc'] = \
                page.is_button_switched_on(page.TRADE_IN_OFFER_AUTO_CALCULATE)
        with allure.step("Saving 'Appraisal Value Requirement on Trade Analyzer:' setting"):
            dealer_general_before['appraisal_value_requirement'] = page.get_text(page.APPRAISAL_VALUE_REQUIREMENT)
        with allure.step("Saving 'Inventory Days Back Threshold:' setting"):
            dealer_general_before['inventory_days_back_threshold'] = \
                page.get_attribute(page.INVENTORY_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Unwind Days Threshold:' setting"):
            dealer_general_before['unwind_days_threshold'] = page.get_attribute(page.UNWIND_DAYS_THRESHOLD, 'value')
        with allure.step("Saving 'Search Appraisal Days Back Threshold:' setting"):
            dealer_general_before['search_appraisal_days_back_threshold'] = \
                page.get_attribute(page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Appraisal Look Back Period:' setting"):
            dealer_general_before['appraisal_look_back_period'] = \
                page.get_attribute(page.APPRAISAL_LOOK_BACK_PERIOD, 'value')
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Appraisal Look Forward Period:' setting"):
            dealer_general_before['appraisal_look_forward_period'] = \
                page.get_attribute(page.APPRAISAL_LOOK_FORWARD_PERIOD, 'value')
        with allure.step("Saving 'Showroom Days Filter:' setting"):
            dealer_general_before['showroom_days_filter'] = page.get_attribute(page.SHOWROOM_DAYS_FILTER, 'value')
        with allure.step("Saving 'Trade Manager Days Filter:' setting"):
            dealer_general_before['trade_manager_days_filter'] = page.get_text(page.TRADE_MANAGER_DAYS_FILTER)
        with allure.step("Saving 'Run Day Of Week:' setting"):
            dealer_general_before['run_day_of_week'] = page.get_text(page.RUN_DAY_OF_WEEK)
        with allure.step("Saving 'Program Type:' setting"):
            dealer_general_before['program_type'] = page.get_text(page.PROGRAM_TYPE)
        with allure.step("Saving 'Pack Amount:' setting"):
            dealer_general_before['pack_amount'] = page.get_attribute(page.PACK_AMOUNT, 'value')
        with allure.step("Saving 'Group Appraisal Search Weeks:' setting"):
            dealer_general_before['group_appraisal_search_weeks'] = \
                page.get_attribute(page.GROUP_APPRAISAL_SEARCH_WEEKS, 'value')
        with allure.step("Saving 'Twix Url:' setting"):
            dealer_general_before['twix_url'] = page.get_attribute(page.TWIX_URL, 'value')
        with allure.step("Saving 'Auction Area:' setting"):
            dealer_general_before['auction_area'] = page.get_text(page.AUCTION_AREA)
        with allure.step("Saving 'Live Auction Distance From Dealer:' setting"):
            dealer_general_before['live_auction_distance'] = page.get_text(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Dashboard Display:' setting"):
            dealer_general_before['dashboard_display'] = page.get_text(page.DASHBOARD_DISPLAY)
        with allure.step("Saving 'Forecaster Weeks:' setting"):
            dealer_general_before['forecaster_weeks'] = page.get_text(page.FORECASTER_WEEKS)
        with allure.step("Saving 'PerfAnalyzer Weeks:' setting"):
            dealer_general_before['perfanalyzer_weeks'] = page.get_text(page.PERFANALYZER_WEEKS)
        with allure.step("Saving 'PerfAnalyzer View:' setting"):
            dealer_general_before['perfanalyzer_view'] = page.get_text(page.PERFANALYZER_VIEW)
        with allure.step("Scrolling the page up"):
            element_to_scroll = page.locate_element(page.RECALL_REPORT_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Recall Report:' setting"):
            dealer_general_before['recall_report'] = page.is_button_switched_on(page.RECALL_REPORT_BTN)
        with allure.step("Saving 'Show Lot Location Status:' setting"):
            dealer_general_before['show_lot_location_status'] = \
                page.is_button_switched_on(page.SHOW_LOT_LOCATION_STATUS_BTN)
        with allure.step("Saving 'Show Inactive Appraisals:' setting"):
            dealer_general_before['show_inactive_appraisal'] = \
                page.is_button_switched_on(page.SHOW_INACTIVE_APPRAISALS_BTN)
        with allure.step("Saving 'Require Name On Appraisals:' setting"):
            dealer_general_before['require_name_on_appraisals'] = \
                page.is_button_switched_on(page.REQUIRE_NAME_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Est Recon Cost On Appraisals:' setting"):
            dealer_general_before['require_est_recon_cost'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Recon Notes On Appraisals:' setting"):
            dealer_general_before['require_recon_notes_on_appraisals'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Show Casey And Casey:' setting"):
            dealer_general_before['show_casey_and_casey'] = page.is_button_switched_on(
                page.SHOW_CASEY_AND_CASEY_BTN)
        with allure.step("Saving 'Show Appraisal Form Offer Group:' setting"):
            dealer_general_before['show_appraisal_form_offer_group'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN)
        with allure.step("Saving 'Show Appraisal Value Group:' setting"):
            dealer_general_before['show_appraisal_value_group'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_VALUE_GROUP_BTN)
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Use Lot Price:' setting"):
            dealer_general_before['use_lot_price'] = page.is_button_switched_on(page.USE_LOT_PRICE_BTN)
        with allure.step("Saving 'Exclude Wholesale From Days Supply:' setting"):
            dealer_general_before['exclude_wholesale_from_days_supply'] = page.is_button_switched_on(
                page.EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN)
        with allure.step("Saving 'Atc Enabled:' setting"):
            dealer_general_before['atc_enabled'] = page.is_button_switched_on(page.ATC_ENABLED_BTN)
        with allure.step("Saving 'Gmac Enabled:' setting"):
            dealer_general_before['gmac_enabled'] = page.is_button_switched_on(page.GMAC_ENABLED_BTN)
        with allure.step("Saving 'Tfs Enabled:' setting"):
            dealer_general_before['tfs_enabled'] = page.is_button_switched_on(page.TFS_ENABLED_BTN)
        with allure.step("Saving 'Visible To Dealer Group:' setting"):
            dealer_general_before['visible_to_dealer_group'] = page.is_button_switched_on(
                page.VISIBLE_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'Enable Auto Match:' setting"):
            dealer_general_before['enable_auto_match'] = page.is_button_switched_on(page.ENABLE_AUTO_MATCH_BTN)
        with allure.step("Saving 'Display Unit Cost To Dealer Group:' setting"):
            dealer_general_before['display_unit_cost_to_dealer_group'] = page.is_button_switched_on(
                page.DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'In-Transit Inventory:' setting"):
            dealer_general_before['in_transit_inventory'] = page.is_button_switched_on(
                page.IN_TRANSIT_INVENTORY_BTN)
        with allure.step("Saving 'Display Recalls Lookup By VIN Link on Appraisals:' setting"):
            dealer_general_before['display_recalls_lookup_by_vin'] = page.is_button_switched_on(
                page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
        with allure.step("Scrolling the page up"):
            element_to_scroll = page.locate_element(page.RECALL_REPORT_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)

    with allure.step("Clicking 'Edit' button"):
        page = DealerProfileDealerPage(driver)
        edit_btn = page.get_clickable_element(page.DEALER_GENERAL_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)

    with allure.step("Modifying all values in 'Dealer General'"):
        with allure.step("Modifying 'Show Recall:' setting"):
            show_recall_btn = page.get_clickable_element(page.SHOW_RECALL_BTN)
            page.click(show_recall_btn)
            time.sleep(1)

        with allure.step("Modifying 'Trade-In Offer Auto Calculate:' setting"):
            trade_in_offer_auto_calculate_btn = page.get_clickable_element(page.TRADE_IN_OFFER_AUTO_CALCULATE)
            page.click(trade_in_offer_auto_calculate_btn)
            time.sleep(1)

        with allure.step("Modifying 'Appraisal Value Requirement on Trade Analyzer:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.APPRAISAL_VALUE_REQUIREMENT,
                                                   default_value=dealer_general_before['appraisal_value_requirement'])
            time.sleep(2)
        with allure.step("Modifying 'Inventory Days Back Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.INVENTORY_DAYS_BACK_THRESHOLD,
                                      action_button_locator=page.INVENTORY_DAYS_BACK_THRESHOLD_INCREASE_BTN)

        with allure.step("Modifying 'Unwind Days Threshold:' setting"):
            if dealer_general_before['unwind_days_threshold'] == '255':
                page.modify_numeric_value(input_locator=page.UNWIND_DAYS_THRESHOLD,
                                          action_button_locator=page.UNWIND_DAYS_THRESHOLD_DECREASE_BTN)
            else:
                page.modify_numeric_value(input_locator=page.UNWIND_DAYS_THRESHOLD,
                                          action_button_locator=page.UNWIND_DAYS_THRESHOLD_INCREASE_BTN)

        with allure.step("Modifying 'Search Appraisal Days Back Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD,
                                      action_button_locator=page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD_INCREASE_BTN)

        with allure.step("Modifying 'Appraisal Look Back Period:' setting"):
            page.modify_numeric_value(input_locator=page.APPRAISAL_LOOK_BACK_PERIOD,
                                      action_button_locator=page.APPRAISAL_LOOK_BACK_PERIOD_INCREASE_BTN)

        with allure.step("Modifying 'Appraisal Look Forward Period:' setting"):
            page.modify_numeric_value(input_locator=page.APPRAISAL_LOOK_FORWARD_PERIOD,
                                      action_button_locator=page.APPRAISAL_LOOK_FORWARD_PERIOD_INCREASE_BTN)

        with allure.step("Modifying 'Showroom Days Filter:' setting"):
            page.modify_numeric_value(input_locator=page.SHOWROOM_DAYS_FILTER,
                                      action_button_locator=page.SHOWROOM_DAYS_FILTER_INCREASE_BTN)

        with allure.step("Modifying 'Trade Manager Days Filter:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.TRADE_MANAGER_DAYS_FILTER,
                                                   default_value=dealer_general_before['trade_manager_days_filter'])

        with allure.step("Modifying 'Run Day Of Week:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.RUN_DAY_OF_WEEK,
                                                   default_value=dealer_general_before['run_day_of_week'])

        with allure.step("Modifying 'Program Type:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.PROGRAM_TYPE,
                                                   default_value=dealer_general_before['program_type'])

        with allure.step("Modifying 'Pack Amount:' setting"):
            page.modify_numeric_value(input_locator=page.PACK_AMOUNT,
                                      action_button_locator=page.PACK_AMOUNT_INCREASE_BTN)

        with allure.step("Modifying 'Group Appraisal Search Weeks:' setting"):
            page.modify_numeric_value(input_locator=page.GROUP_APPRAISAL_SEARCH_WEEKS,
                                      action_button_locator=page.GROUP_APPRAISAL_SEARCH_WEEKS_INCREASE_BTN)

        with allure.step("Modifying 'Twix Url:' setting"):
            modified_twix_url = dealer_general_before['twix_url'] + '1'
            page.paste_text(page.TWIX_URL, modified_twix_url)
            time.sleep(TIMEOUT)

        with allure.step("Modifying 'Auction Area:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.AUCTION_AREA,
                                                   default_value=dealer_general_before['auction_area'])
        with allure.step("Modifying 'Live Auction Distance From Dealer:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.LIVE_AUCTION_DISTANCE_FROM_DEALER,
                                                   default_value=dealer_general_before['live_auction_distance'])
        with allure.step("Modifying 'Dashboard Display:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.DASHBOARD_DISPLAY,
                                                   default_value=dealer_general_before['dashboard_display'])
        with allure.step("Modifying 'Forecaster Weeks:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.FORECASTER_WEEKS,
                                                   default_value=dealer_general_before['forecaster_weeks'])
        with allure.step("Modifying 'PerfAnalyzer Weeks:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.PERFANALYZER_WEEKS,
                                                   default_value=dealer_general_before['perfanalyzer_weeks'])
        with allure.step("Modifying 'PerfAnalyzer View:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.PERFANALYZER_VIEW,
                                                   default_value=dealer_general_before['perfanalyzer_view'])
        with allure.step("Modifying 'Recall Report:' setting"):
            recall_report_btn = page.get_clickable_element(page.RECALL_REPORT_BTN)
            page.click(recall_report_btn)
            time.sleep(1)
        with allure.step("Modifying 'Show Lot Location Status:' setting"):
            show_lot_location_status_btn = page.get_clickable_element(page.SHOW_LOT_LOCATION_STATUS_BTN)
            page.click(show_lot_location_status_btn)
            time.sleep(1)
        with allure.step("Modifying 'Show Inactive Appraisals:' setting"):
            show_inactive_appraisal = page.get_clickable_element(page.SHOW_INACTIVE_APPRAISALS_BTN)
            page.click(show_inactive_appraisal)
            time.sleep(1)
        with allure.step("Modifying 'Require Name On Appraisals:' setting"):
            require_name_on_appraisals = page.get_clickable_element(page.REQUIRE_NAME_ON_APPRAISALS_BTN)
            page.click(require_name_on_appraisals)
            time.sleep(1)
        with allure.step("Modifying 'Require Est Recon Cost On Appraisals:' setting"):
            require_est_recon_cost = page.get_clickable_element(page.REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN)
            page.click(require_est_recon_cost)
            time.sleep(1)
        with allure.step("Modifying 'Require Recon Notes On Appraisals:' setting"):
            require_recon_notes_on_appraisals = \
                page.get_clickable_element(page.REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN)
            page.click(require_recon_notes_on_appraisals)
            time.sleep(1)
        with allure.step("Modifying 'Show Casey And Casey:' setting"):
            show_casey_and_casey = page.get_clickable_element(page.SHOW_CASEY_AND_CASEY_BTN)
            page.click(show_casey_and_casey)
            time.sleep(1)
        with allure.step("Modifying 'Show Appraisal Form Offer Group:' setting"):
            show_appraisal_form_offer_group = page.get_clickable_element(page.SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN)
            page.click(show_appraisal_form_offer_group)
            time.sleep(1)
        with allure.step("Modifying 'Show Appraisal Value Group:' setting"):
            show_appraisal_value_group = page.get_clickable_element(page.SHOW_APPRAISAL_VALUE_GROUP_BTN)
            page.click(show_appraisal_value_group)
            time.sleep(1)
        with allure.step("Modifying 'Use Lot Price:' setting"):
            use_lot_price = page.get_clickable_element(page.USE_LOT_PRICE_BTN)
            page.click(use_lot_price)
            time.sleep(1)
        with allure.step("Modifying 'Exclude Wholesale From Days Supply:' setting"):
            exclude_wholesale_from_days_supply = page.get_clickable_element(page.EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN)
            page.click(exclude_wholesale_from_days_supply)
            time.sleep(1)
        with allure.step("Modifying 'Atc Enabled:' setting"):
            atc_enabled = page.get_clickable_element(page.ATC_ENABLED_BTN)
            page.click(atc_enabled)
            time.sleep(1)
        with allure.step("Modifying 'Gmac Enabled:' setting"):
            gmac_enabled = page.get_clickable_element(page.GMAC_ENABLED_BTN)
            page.click(gmac_enabled)
            time.sleep(1)
        with allure.step("Modifying 'Tfs Enabled:' setting"):
            tfs_enabled = page.get_clickable_element(page.TFS_ENABLED_BTN)
            page.click(tfs_enabled)
            time.sleep(1)
        with allure.step("Modifying 'Visible To Dealer Group:' setting"):
            visible_to_dealer_group = page.get_clickable_element(page.VISIBLE_TO_DEALER_GROUP_BTN)
            page.click(visible_to_dealer_group)
            time.sleep(1)
        with allure.step("Modifying 'Enable Auto Match:' setting"):
            enable_auto_match = page.get_clickable_element(page.ENABLE_AUTO_MATCH_BTN)
            page.click(enable_auto_match)
            time.sleep(1)
        with allure.step("Modifying 'Display Unit Cost To Dealer Group:' setting"):
            display_unit_cost_to_dealer_group = page.get_clickable_element(page.DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN)
            page.click(display_unit_cost_to_dealer_group)
            time.sleep(1)
        with allure.step("Modifying 'In-Transit Inventory:' setting"):
            in_transit_inventory = page.get_clickable_element(page.IN_TRANSIT_INVENTORY_BTN)
            page.click(in_transit_inventory)
            time.sleep(1)
        with allure.step("Modifying 'Display Recalls Lookup By VIN Link on Appraisals:' setting"):
            display_recalls_lookup_by_vin = page.get_clickable_element(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
            page.click(display_recalls_lookup_by_vin)
            time.sleep(1)

    with allure.step("Saving the changes"):
        save_btn = page.get_clickable_element(page.DEALER_GENERAL_SAVE_BTN)
        page.click(save_btn)
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step("Saving new values in 'Dealer General'"):
        dealer_general_after = dict()
        with allure.step("Saving 'Show Recall:' setting"):
            dealer_general_after['show_recall'] = page.is_button_switched_on(page.SHOW_RECALL_BTN)
        with allure.step("Saving 'Trade-In Offer Auto Calculate:' setting"):
            dealer_general_after['trade_in_offer_auto_calc'] = \
                page.is_button_switched_on(page.TRADE_IN_OFFER_AUTO_CALCULATE)
        with allure.step("Saving 'Appraisal Value Requirement on Trade Analyzer:' setting"):
            dealer_general_after['appraisal_value_requirement'] = page.get_text(page.APPRAISAL_VALUE_REQUIREMENT)
        with allure.step("Saving 'Inventory Days Back Threshold:' setting"):
            dealer_general_after['inventory_days_back_threshold'] = \
                page.get_attribute(page.INVENTORY_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Unwind Days Threshold:' setting"):
            dealer_general_after['unwind_days_threshold'] = page.get_attribute(page.UNWIND_DAYS_THRESHOLD, 'value')
        with allure.step("Saving 'Search Appraisal Days Back Threshold:' setting"):
            dealer_general_after['search_appraisal_days_back_threshold'] = \
                page.get_attribute(page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Appraisal Look Back Period:' setting"):
            dealer_general_after['appraisal_look_back_period'] = \
                page.get_attribute(page.APPRAISAL_LOOK_BACK_PERIOD, 'value')
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Appraisal Look Forward Period:' setting"):
            dealer_general_after['appraisal_look_forward_period'] = \
                page.get_attribute(page.APPRAISAL_LOOK_FORWARD_PERIOD, 'value')
        with allure.step("Saving 'Showroom Days Filter:' setting"):
            dealer_general_after['showroom_days_filter'] = page.get_attribute(page.SHOWROOM_DAYS_FILTER, 'value')
        with allure.step("Saving 'Trade Manager Days Filter:' setting"):
            dealer_general_after['trade_manager_days_filter'] = page.get_text(page.TRADE_MANAGER_DAYS_FILTER)
        with allure.step("Saving 'Run Day Of Week:' setting"):
            dealer_general_after['run_day_of_week'] = page.get_text(page.RUN_DAY_OF_WEEK)
        with allure.step("Saving 'Program Type:' setting"):
            dealer_general_after['program_type'] = page.get_text(page.PROGRAM_TYPE)
        with allure.step("Saving 'Pack Amount:' setting"):
            dealer_general_after['pack_amount'] = page.get_attribute(page.PACK_AMOUNT, 'value')
        with allure.step("Saving 'Group Appraisal Search Weeks:' setting"):
            dealer_general_after['group_appraisal_search_weeks'] = \
                page.get_attribute(page.GROUP_APPRAISAL_SEARCH_WEEKS, 'value')
        with allure.step("Saving 'Twix Url:' setting"):
            dealer_general_after['twix_url'] = page.get_attribute(page.TWIX_URL, 'value')
        with allure.step("Saving 'Auction Area:' setting"):
            dealer_general_after['auction_area'] = page.get_text(page.AUCTION_AREA)
        with allure.step("Saving 'Live Auction Distance From Dealer:' setting"):
            dealer_general_after['live_auction_distance'] = page.get_text(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Dashboard Display:' setting"):
            dealer_general_after['dashboard_display'] = page.get_text(page.DASHBOARD_DISPLAY)
        with allure.step("Saving 'Forecaster Weeks:' setting"):
            dealer_general_after['forecaster_weeks'] = page.get_text(page.FORECASTER_WEEKS)
        with allure.step("Saving 'PerfAnalyzer Weeks:' setting"):
            dealer_general_after['perfanalyzer_weeks'] = page.get_text(page.PERFANALYZER_WEEKS)
        with allure.step("Saving 'PerfAnalyzer View:' setting"):
            dealer_general_after['perfanalyzer_view'] = page.get_text(page.PERFANALYZER_VIEW)
        with allure.step("Scrolling the page up"):
            element_to_scroll = page.locate_element(page.RECALL_REPORT_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Recall Report:' setting"):
            dealer_general_after['recall_report'] = page.is_button_switched_on(page.RECALL_REPORT_BTN)
        with allure.step("Saving 'Show Lot Location Status:' setting"):
            dealer_general_after['show_lot_location_status'] = \
                page.is_button_switched_on(page.SHOW_LOT_LOCATION_STATUS_BTN)
        with allure.step("Saving 'Show Inactive Appraisals:' setting"):
            dealer_general_after['show_inactive_appraisal'] = \
                page.is_button_switched_on(page.SHOW_INACTIVE_APPRAISALS_BTN)
        with allure.step("Saving 'Require Name On Appraisals:' setting"):
            dealer_general_after['require_name_on_appraisals'] = \
                page.is_button_switched_on(page.REQUIRE_NAME_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Est Recon Cost On Appraisals:' setting"):
            dealer_general_after['require_est_recon_cost'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Recon Notes On Appraisals:' setting"):
            dealer_general_after['require_recon_notes_on_appraisals'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Show Casey And Casey:' setting"):
            dealer_general_after['show_casey_and_casey'] = page.is_button_switched_on(
                page.SHOW_CASEY_AND_CASEY_BTN)
        with allure.step("Saving 'Show Appraisal Form Offer Group:' setting"):
            dealer_general_after['show_appraisal_form_offer_group'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN)
        with allure.step("Saving 'Show Appraisal Value Group:' setting"):
            dealer_general_after['show_appraisal_value_group'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_VALUE_GROUP_BTN)
        with allure.step("Scrolling the page down"):
            element_to_scroll = page.locate_element(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)
        with allure.step("Saving 'Use Lot Price:' setting"):
            dealer_general_after['use_lot_price'] = page.is_button_switched_on(page.USE_LOT_PRICE_BTN)
        with allure.step("Saving 'Exclude Wholesale From Days Supply:' setting"):
            dealer_general_after['exclude_wholesale_from_days_supply'] = page.is_button_switched_on(
                page.EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN)
        with allure.step("Saving 'Atc Enabled:' setting"):
            dealer_general_after['atc_enabled'] = page.is_button_switched_on(page.ATC_ENABLED_BTN)
        with allure.step("Saving 'Gmac Enabled:' setting"):
            dealer_general_after['gmac_enabled'] = page.is_button_switched_on(page.GMAC_ENABLED_BTN)
        with allure.step("Saving 'Tfs Enabled:' setting"):
            dealer_general_after['tfs_enabled'] = page.is_button_switched_on(page.TFS_ENABLED_BTN)
        with allure.step("Saving 'Visible To Dealer Group:' setting"):
            dealer_general_after['visible_to_dealer_group'] = page.is_button_switched_on(
                page.VISIBLE_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'Enable Auto Match:' setting"):
            dealer_general_after['enable_auto_match'] = page.is_button_switched_on(page.ENABLE_AUTO_MATCH_BTN)
        with allure.step("Saving 'Display Unit Cost To Dealer Group:' setting"):
            dealer_general_after['display_unit_cost_to_dealer_group'] = page.is_button_switched_on(
                page.DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'In-Transit Inventory:' setting"):
            dealer_general_after['in_transit_inventory'] = page.is_button_switched_on(
                page.IN_TRANSIT_INVENTORY_BTN)
        with allure.step("Saving 'Display Recalls Lookup By VIN Link on Appraisals:' setting"):
            dealer_general_after['display_recalls_lookup_by_vin'] = page.is_button_switched_on(
                page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
        with allure.step("Scrolling the page up"):
            element_to_scroll = page.locate_element(page.RECALL_REPORT_BTN)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)

    with allure.step("Checking that settings in 'Dealer General' were modified"):
        for key in dealer_general_before.keys():
            with check:
                with allure.step(f"Checking that '{key}' setting was modified"):
                    with allure.step(f"Current '{key}' value is: '{dealer_general_after[key]}', was: "
                                     f"'{dealer_general_before[key]}'"):
                        pass
                    assert dealer_general_after[key] != dealer_general_before[key], \
                        [f"'{key}' setting was not modified", page.make_screenshot()]

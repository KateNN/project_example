from page_objects.CreateNewDealerPage import CreateNewDealerPage
from page_objects.LoginPage import LoginPage
from page_objects.MaxInventoryPage import MaxInventoryPage
from page_objects.DealerProfilePage import DealerProfilePage
from page_objects.DealerProfileUsersPage import DealerProfileUsersPage
from page_objects.DealerProfileMaxSettingsPage import DealerProfileMaxSettingsPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
from page_objects.DealerProfilePricingPage import DealerProfilePricingPage
from datetime import date
import time
import random
import pytest
from pytest_check import check
import allure

TIMEOUT = 4


@pytest.mark.regression
@allure.feature("Add New Dealer: MAX-9467")
@allure.title("Authorized PitStop users with Admin role can create new dealers (required fields only). Basic scenario."
              "C13740 - Latitude and Longitude are calculated automatically by Zip Code")
def test_create_new_dealer_required_fields_only(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Generating test data, creating new dealer"):
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
                               zip_code=new_dealer['zip_code'],
                               calc_lat_long_by='zip_code')

    with allure.step("Opening the new dealer's profile"):
        open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
        page.click(open_new_dealer_btn)
        time.sleep(TIMEOUT)
        page = DealerProfilePage(driver)
        page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    with allure.step(f"Asserting that the new dealer name '{new_dealer['name']}' is in the dealer profile header"):
        assert new_dealer['name'] in page.locate_element(page.PROFILE_HEADER).text, \
            [f"Dealer name '{new_dealer['name']}' is not in the header", page.make_screenshot()]


@pytest.mark.regression
@pytest.mark.xfail(reason="MAX Inventory UI in staging works unstable")
@allure.feature("Create New Dealer: MAX-9467")
@allure.title("C13701 Positive case: all required fields have valid values, all non-mandatory fields empty, "
              "new dealer can be opened in MAX. C13740 - Latitude and Longitude are calculated automatically by"
              " Google Place ID")
def test_new_dealer_can_be_opened_in_max(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        user = page.USER_WITH_PITSTOP_ROLE

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

    with allure.step("Saving the new dealer's name displayed in Profile"):
        page = DealerProfileDealerPage(driver)
        dealer_name_in_profile = page.get_attribute(page.DEALER_INPUT, 'value')

    with allure.step(f"Adding access for the user '{user}' to the new dealer '{dealer_name_in_profile}'"):
        page = DealerProfilePage(driver)
        users_tab = page.locate_element(page.USERS_TAB)
        page.click(users_tab)
        time.sleep(TIMEOUT)
        page = DealerProfileUsersPage(driver)
        page.add_user_to_dealer(user)
        page.refresh_page()
        time.sleep(TIMEOUT)

    with allure.step(f"Opening '{dealer_name_in_profile}' dealer in MAX Inventory"):
        open_in_max = page.locate_element(page.OPEN_IN_MAX_BTN)
        page.click(open_in_max)
        driver.switch_to.window(driver.window_handles[1])
        page = MaxInventoryPage(driver)
        time.sleep(TIMEOUT)
        page.check_page_title(page.MAX_INVENTORY_PAGE_TITLE)
        dealer_name = page.get_attribute(page.DEALER_NAME_INPUT, 'value')

    with allure.step(f"Asserting that the new dealer '{dealer_name_in_profile}' is opened in MAX Inventory"):
        assert dealer_name == dealer_name_in_profile, \
            [f"Dealer {dealer_name_in_profile} is not present on the page", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-9467")
@allure.title("C13668 Required fields are empty")
def test_create_dealer_required_fields_empty(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Clicking 'Create New Dealer' button, leaving all required fields empty, "
                     "trying to save the changes"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)
        page.create_new_dealer(dealer_group='',
                               calc_lat_long_by='')

    with check:
        with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
            alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
            assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
                [f"Wrong alert text for Form Validation: {alert1} instead of "
                 f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Group Required alert: '{page.GROUP_REQUIRED_TEXT}'"):
            alert2 = page.locate_element(page.GROUP_REQUIRED_ALERT).text
            assert alert2 == page.GROUP_REQUIRED_TEXT, \
                [f"Wrong alert text for Group field: {alert2} instead of "
                 f"{page.GROUP_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Name Required alert: '{page.NAME_REQUIRED_TEXT}'"):
            alert3 = page.locate_element(page.NAME_REQUIRED_ALERT).text
            assert alert3 == page.NAME_REQUIRED_TEXT, \
                [f"Wrong alert text for Name field: {alert3} instead of"
                 f"{page.NAME_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Short Name Required alert: '{page.SHORT_NAME_REQUIRED_TEXT}'"):
            alert4 = page.locate_element(page.SHORT_NAME_REQUIRED_ALERT).text
            assert alert4 == page.SHORT_NAME_REQUIRED_TEXT, \
                [f"Wrong alert text for Short Name field: {alert4} instead of "
                 f"{page.SHORT_NAME_REQUIRED_TEXT}", page.make_screenshot()]

    element_to_scroll = page.locate_element(page.LONGITUDE_REQUIRED_ALERT)
    page.scroll_to_element(element_to_scroll)
    time.sleep(2)

    with check:
        with allure.step(f"Asserting ZipCode Required alert: '{page.ZIPCODE_REQUIRED_TEXT}'"):
            alert5 = page.locate_element(page.ZIPCODE_REQUIRED_ALERT).text
            assert alert5 == page.ZIPCODE_REQUIRED_TEXT, \
                [f"Wrong alert text for the ZipCode field: {alert5} instead of "
                 f"{page.ZIPCODE_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Latitude Required alert: '{page.LATITUDE_REQUIRED_TEXT}'"):
            alert6 = page.locate_element(page.LATITUDE_REQUIRED_ALERT).text
            assert alert6 == page.LATITUDE_REQUIRED_TEXT, \
                [f"Wrong alert text for the Latitude field: {alert6} instead of "
                 f"{page.LATITUDE_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Longitude Required alert: '{page.LONGITUDE_REQUIRED_TEXT}'"):
            alert7 = page.locate_element(page.LONGITUDE_REQUIRED_ALERT).text
            assert alert7 == page.LONGITUDE_REQUIRED_TEXT, \
                [f"Wrong alert text for the Longitude field: {alert7} instead of "
                 f"{page.LONGITUDE_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting State Required alert: '{page.STATE_REQUIRED_TEXT}'"):
            alert8 = page.locate_element(page.STATE_REQUIRED_ALERT).text
            assert alert8 == page.STATE_REQUIRED_TEXT, \
                [f"Wrong alert text for the State field: {alert8} instead of "
                 f"{page.STATE_REQUIRED_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-9467")
@allure.title("C13703 Required field Name must be unique within active dealerships")
def test_create_dealer_name_must_be_unique(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Generating test data, filling required fields of the Create New Dealer form. "
                     "Entering existing active Dealer name to 'Name' and trying to save changes"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)
        new_dealer = page.generate_new_dealer_data()
        page.create_new_dealer(name=page.EXISTING_DEALER_NAME,
                               short_name=new_dealer['name'],
                               website=new_dealer['website'],
                               google_place_id=new_dealer['google_place_id'],
                               address=new_dealer['address'],
                               state=new_dealer['state'],
                               zip_code=new_dealer['zip_code'])

    with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
        alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
        assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
            [f"Wrong alert text for Form Validation: {alert1} instead of "
             f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]
    with allure.step(f"Asserting Name Must Be Unique alert: '{page.NAME_MUST_BE_UNIQUE_TEXT}'"):
        alert2 = page.locate_element(page.NAME_MUST_BE_UNIQUE_ALERT).text
        assert alert2 == page.NAME_MUST_BE_UNIQUE_TEXT, \
            [f"Wrong alert text for the Name field: {alert2} instead of "
             f"{page.NAME_MUST_BE_UNIQUE_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-9467, MAX-10515")
@allure.title("C13717 'Go Live Date' is defaulted for Today's date, making 'Google Place ID', "
              "'Website' and 'Address' required if not empty")
def test_create_dealer_go_live_date(driver):
    with allure.step("Logging to PitStop as Administrator and going to 'Dealers' menu"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)

    with allure.step("Clicking the 'Create New Dealer' button"):
        create_new_dealer_btn = page.get_clickable_element(page.ADD_NEW_DEALER_BTN)
        page.click(create_new_dealer_btn)
        page.get_clickable_element(page.SAVE_BTN)

    with allure.step("Getting 'Go Live Date' and today's date"):
        default_go_live_date = page.get_attribute(page.GO_LIVE_DATE, 'value')
        today_date = date.today()
        today = today_date.strftime("%B %d, %Y")

    with check:
        with allure.step(f"Asserting that Go Live Date '{default_go_live_date}' is defaulted for Today: '{today}'"):
            assert default_go_live_date == today, \
                [f"Wrong Go Live Date: {default_go_live_date} instead of {today}", page.make_screenshot()]

    with allure.step("Scrolling the page down"):
        element_to_scroll = page.locate_element(page.CITY)
        page.scroll_to_element(element_to_scroll)
        time.sleep(1)

    with check:
        with allure.step('Verifying that Website field is required'):
            assert page.is_required_field(page.WEBSITE_LABEL), \
                ["Website field is not required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Google Place ID field is required'):
            assert page.is_required_field(page.GOOGLE_PLACE_ID_LABEL), \
                ["Google Place ID field is not required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Address field is required'):
            assert page.is_required_field(page.ADDRESS_LABEL), \
                ["Address field is not required", page.make_screenshot()]

    with allure.step("Changing 'Go Live Date' to another date"):
        go_live_date_input = page.locate_element(page.GO_LIVE_DATE)
        page.select_random_date_from_calender(calender_locator=page.GO_LIVE_DATE)
        time.sleep(2)
        new_date = page.get_attribute(page.GO_LIVE_DATE, 'value')
    with check:
        with allure.step(f"Asserting that Go Live Date is set to another date: '{new_date}' instead of "
                         f"'{default_go_live_date}'"):
            assert new_date != default_go_live_date, \
                [f"Go Live Date haven't changed", page.make_screenshot()]

    with allure.step("Scrolling the page down"):
        element_to_scroll = page.locate_element(page.CITY)
        page.scroll_to_element(element_to_scroll)
        time.sleep(1)

    with check:
        with allure.step('Verifying that Website field is still required'):
            assert page.is_required_field(page.WEBSITE_LABEL), \
                ["Website field is not required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Google Place ID field is still required'):
            assert page.is_required_field(page.GOOGLE_PLACE_ID_LABEL), \
                ["Google Place ID field is not required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Address field is still required'):
            assert page.is_required_field(page.ADDRESS_LABEL), \
                ["Address field is not required", page.make_screenshot()]

    with allure.step("Clearing 'Go Live Date' field and getting current value for 'Go Live Date'"):
        page.click(go_live_date_input)
        clear_btn = page.locate_element(page.CLEAR_GO_LIVE_DATE_BTN)
        page.click(clear_btn)
        time.sleep(2)
        go_live_date = page.get_attribute(page.GO_LIVE_DATE, 'value')
    with check:
        with allure.step("Asserting that Go Live Date is empty"):
            assert go_live_date == '', ["Go Live Date is not empty", page.make_screenshot()]

    with allure.step("Scrolling the page down"):
        element_to_scroll = page.locate_element(page.CITY)
        page.scroll_to_element(element_to_scroll)
        time.sleep(1)

    with check:
        with allure.step('Verifying that Website field is non-mandatory'):
            assert not page.is_required_field(page.WEBSITE_LABEL), ["Website field is required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Google Place ID field is non-mandatory'):
            assert not page.is_required_field(page.GOOGLE_PLACE_ID_LABEL), \
                ["Google Place ID field is required", page.make_screenshot()]
    with check:
        with allure.step('Verifying that Address field is non-mandatory'):
            assert not page.is_required_field(page.ADDRESS_LABEL), \
                ["Address field is required", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Add New Dealer: MAX-9467, MAX-9837")
@allure.title("C13713 Required field Short Name can be auto-filled")
def test_create_new_dealer_short_name_can_be_auto_filled(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
    with allure.step("Opening 'Create New Dealer' form"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)
        create_new_dealer_btn = page.get_clickable_element(page.ADD_NEW_DEALER_BTN)
        page.click(create_new_dealer_btn)

    with allure.step("Generating test data, filling the Name and clicking auto-fill button for the Short Name"):
        new_dealer = page.generate_new_dealer_data()
        page.paste_text(page.NAME, new_dealer['name'])
        autofill_btn = page.get_clickable_element(page.AUTOFILL_BTN)
        page.click(autofill_btn)
        time.sleep(TIMEOUT)
        my_text = page.get_attribute(page.SHORT_NAME, 'value')

    with allure.step(f"Asserting that Short Name is auto-filled with the Name value: '{new_dealer['name']}'"):
        assert my_text == new_dealer['name'], \
            [f"Wrong Short Name: {my_text} instead of {new_dealer['name']}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-9467")
@allure.title("C13704, C13711, C13744, C13746, C13742, C13743 Verify that 'Create New Dealer' form has default "
              "values for 'Active', 'Run Day Of Week', 'Appraisal Form Memo', 'Appraisal Form Disclaimer', "
              "'Guide Book One', 'Guide Book One 1st Type'")
def test_create_dealer_fields_default_values(driver):
    with allure.step("Logging to PitStop as Administrator and going to 'Dealers' menu"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)

    with allure.step("Clicking the 'Create New Dealer' button to open the form and check defaults"):
        create_new_dealer_btn = page.get_clickable_element(page.ADD_NEW_DEALER_BTN)
        page.click(create_new_dealer_btn)
        page.get_clickable_element(page.SAVE_BTN)
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Asserting 'Active' button is On"):
            page.locate_element(page.ACTIVE_BTN)
            assert page.get_attribute(page.ACTIVE_BTN, 'aria-checked') == 'true', \
                ["'Active' button is Off", page.make_screenshot()]

    with check:
        with allure.step(f"Checking defaults for 'Run Day Of Week' - {page.RUN_DAY_OF_WEEK_VALUE}"):
            page.locate_element(page.RUN_DAY_OF_WEEK)
            day_of_week = page.get_text(page.RUN_DAY_OF_WEEK)
            assert day_of_week == page.RUN_DAY_OF_WEEK_VALUE, \
                [f"Wrong Run Day of Week: {day_of_week} instead of "
                 f"{page.RUN_DAY_OF_WEEK_VALUE}", page.make_screenshot()]

    with check:
        with allure.step("Verifying that 'Appraisal Form Memo' is required"):
            page.locate_element(page.APPRAISAL_FORM_MEMO_LABEL)
            assert page.is_required_field(page.APPRAISAL_FORM_MEMO_LABEL), \
                ["'Appraisal Form Memo' field is not required", page.make_screenshot()]

    with check:
        with allure.step("Checking defaults for 'Appraisal Form Memo'"):
            page.locate_element(page.APPRAISAL_FORM_MEMO)
            memo_text = page.get_attribute(page.APPRAISAL_FORM_MEMO, 'value')
            assert memo_text == page.APPRAISAL_FORM_MEMO_TEXT, \
                [f"Wrong text for 'Appraisal Form Memo': '{memo_text}' instead of "
                 f"'{page.APPRAISAL_FORM_MEMO_TEXT}'", page.make_screenshot()]

    with check:
        with allure.step("Verifying that 'Appraisal Form Disclaimer' is required"):
            page.locate_element(page.APPRAISAL_FORM_DISCLAIMER_LABEL)
            assert page.is_required_field(page.APPRAISAL_FORM_DISCLAIMER_LABEL), \
                ["'Appraisal Form Disclaimer' field is not required", page.make_screenshot()]

    with check:
        with allure.step("Checking defaults for 'Appraisal Form Disclaimer'"):
            page.locate_element(page.APPRAISAL_FORM_DISCLAIMER)
            disclaimer_text = page.get_attribute(page.APPRAISAL_FORM_DISCLAIMER, 'value')
            assert disclaimer_text == page.APPRAISAL_FORM_DISCLAIMER_TEXT, \
                [f"Wrong text for 'Appraisal Form Disclaimer': '{disclaimer_text}' instead of "
                 f"'{page.APPRAISAL_FORM_DISCLAIMER_TEXT}'", page.make_screenshot()]

    with check:
        with allure.step("Verifying that 'Guide Book One' is required"):
            page.locate_element(page.GUIDE_BOOK_ONE_LABEL)
            assert page.is_required_field(page.GUIDE_BOOK_ONE_LABEL), \
                ["'Guide Book One' field is not required", page.make_screenshot()]

    with check:
        with allure.step(f"Verifying that 'Guide Book One' is defaulted to {page.GUIDE_BOOK_ONE_VALUE}"):
            page.locate_element(page.GUIDE_BOOK_ONE)
            guide_book1 = page.get_text(page.GUIDE_BOOK_ONE)
            assert guide_book1 == page.GUIDE_BOOK_ONE_VALUE, \
                [f"Wrong value for 'Guide Book One': {guide_book1} instead of "
                 f"{page.GUIDE_BOOK_ONE_VALUE}", page.make_screenshot()]

    with check:
        with allure.step("Verifying that 'Guide Book One 1st Type' is required"):
            page.locate_element(page.GUIDE_BOOK_ONE_1ST_TYPE_LABEL)
            assert page.is_required_field(page.GUIDE_BOOK_ONE_1ST_TYPE_LABEL), \
                ["'Guide Book One 1st Type' field is not required", page.make_screenshot()]

    with check:
        with allure.step(
                f"Verifying that 'Guide Book One 1st Type' is defaulted to {page.GUIDE_BOOK_ONE_1ST_TYPE_VALUE}"):
            page.locate_element(page.GUIDE_BOOK_ONE_1ST_TYPE)
            book1_first_type = page.get_text(page.GUIDE_BOOK_ONE_1ST_TYPE)
            assert book1_first_type == page.GUIDE_BOOK_ONE_1ST_TYPE_VALUE, \
                [f"Wrong 'Guide Book One 1st Type': {book1_first_type} instead of "
                 f"{page.GUIDE_BOOK_ONE_1ST_TYPE_VALUE}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-9467, MAX-14027, MAX-13965")
@allure.title("C22304, C13719, C13594, C16063, C22619, C30952, C16080, C22816, C22817, C22818 C16056, C22835, "
              "C22855, C16049, C16800, C16490, C16498, C13741, C39548, C35448, C39552, C50684, C53110, C33343 "
              "Check New Dealer's defaults")
def test_new_dealer_defaults(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        time.sleep(TIMEOUT)

    with allure.step("Generating test data, creating new dealer"):
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
                               zip_code=new_dealer['zip_code'],
                               calc_lat_long_by='zip_code')

        open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
        page.click(open_new_dealer_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)

    # "General Settings" defaults: TCs C22304, C13719, C22619, C22816, C22817, C22818, C16080, C39552, C53110
    with allure.step("Switching to 'General Settings' tab"):
        page = DealerProfileDealerPage(driver)
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(TIMEOUT)

    with allure.step("Switching to 'General Settings' - 'Access Groups' sub-tab"):
        access_groups = page.locate_element(page.GEN_SET_ACCESS_GROUPS)
        page.click(access_groups)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Access Groups' number is equal to {len(page.ACCESS_GROUPS_DEFAULTS)}"):
                groups = page.locate_all_elements(page.ACCESS_GROUPS)
                assert len(groups) == len(page.ACCESS_GROUPS_DEFAULTS), \
                    [f"Wrong number of Access Groups - {len(groups)}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Access Groups' list matches the {page.ACCESS_GROUPS_DEFAULTS}"):
                access_groups_names = []
                for i in range(len(groups)):
                    access_groups_names.append(groups[i].text)
                assert access_groups_names == page.ACCESS_GROUPS_DEFAULTS, \
                    [f"Wrong Access Groups: {access_groups_names}", page.make_screenshot()]

    with allure.step("Switching to 'General Settings' - 'Dealer General' sub-tab"):
        dealer_general = page.locate_element(page.GEN_SET_DEALER_GENERAL)
        page.click(dealer_general)
        time.sleep(TIMEOUT)

        with check:
            with allure.step("Checking that 'Trade-In Offer Auto Calculate' is defaulted to OFF"):
                assert not page.is_button_switched_on(page.TRADE_IN_OFFER_AUTO_CALCULATE), \
                    ["'Trade-In Offer Auto Calculate' button is On", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        with check:
            with allure.step("Checking that 'In-Transit Inventory' is defaulted to ON"):
                assert page.is_button_switched_on(page.IN_TRANSIT_INVENTORY_BTN), \
                    ["'In-Transit Inventory' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Display Recalls Lookup By VIN Link on Appraisals' is defaulted to ON"):
                assert page.is_button_switched_on(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN), \
                    ["'Display Recalls Lookup By VIN Link on Appraisals' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Atc Enabled' is defaulted to ON"):
                assert page.is_button_switched_on(page.ATC_ENABLED_BTN), \
                    ["'Atc Enabled' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Gmac Enabled' is defaulted to ON"):
                assert page.is_button_switched_on(page.GMAC_ENABLED_BTN), \
                    ["'Gmac Enabled' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Tfs Enabled' is defaulted to ON"):
                assert page.is_button_switched_on(page.TFS_ENABLED_BTN), \
                    ["'Tfs Enabled' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Enable Auto Match' is defaulted to ON"):
                assert page.is_button_switched_on(page.ENABLE_AUTO_MATCH_BTN), \
                    ["'Enable Auto Match' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Use Lot Price' is defaulted to OFF"):
                assert not page.is_button_switched_on(page.USE_LOT_PRICE_BTN), \
                    ["'Use Lot Price' button is On", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Program Type' is defaulted to '{page.PROGRAM_TYPE_DEFAULT}'"):
                program_type = page.get_text(page.PROGRAM_TYPE)
                assert program_type == page.PROGRAM_TYPE_DEFAULT, \
                    [f"Wrong default value for 'Program Type': {program_type} instead of "
                     f"{page.PROGRAM_TYPE_DEFAULT}", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.PERFANALYZER_VIEW)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        with check:
            with allure.step(f"Checking that 'Dashboard Display' is defaulted to '{page.DASHBOARD_DISPLAY_DEFAULT}'"):
                dashboard_display = page.get_text(page.DASHBOARD_DISPLAY)
                assert dashboard_display == page.DASHBOARD_DISPLAY_DEFAULT, \
                    [f"Wrong default value for 'Dashboard Display': {dashboard_display} instead of "
                     f"{page.DASHBOARD_DISPLAY_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Forecaster Weeks' is defaulted to '{page.FORECASTER_WEEKS_DEFAULT}'"):
                forecaster_weeks = page.get_text(page.FORECASTER_WEEKS)
                assert forecaster_weeks == page.FORECASTER_WEEKS_DEFAULT, \
                    [f"Wrong default value for 'Forecaster Weeks': {forecaster_weeks} instead of "
                     f"{page.FORECASTER_WEEKS_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'PerfAnalyzer Weeks' is defaulted to '{page.PERFANALYZER_WEEKS_DEFAULT}'"):
                perf_weeks = page.get_text(page.PERFANALYZER_WEEKS)
                assert perf_weeks == page.PERFANALYZER_WEEKS_DEFAULT, \
                    [f"Wrong default value for 'PerfAnalyzer Weeks': {perf_weeks} instead of "
                     f"{page.PERFANALYZER_WEEKS_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'PerfAnalyzer View' is defaulted to '{page.PERFANALYZER_VIEW_DEFAULT}'"):
                perf_view = page.get_text(page.PERFANALYZER_VIEW)
                assert perf_view == page.PERFANALYZER_VIEW_DEFAULT, \
                    [f"Wrong default value for 'PerfAnalyzer View': {perf_view} instead of "
                     f"{page.PERFANALYZER_VIEW_DEFAULT}", page.make_screenshot()]

    with allure.step("Switching to 'General Settings' - 'Scorecard - Units Sold Thresholds' sub-tab"):
        scorecard = page.locate_element(page.GEN_SET_SCORECARD)
        page.click(scorecard)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking 'Threshold for 4 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[0]}')"):
                threshold_4_weeks = page.get_attribute(page.THRESHOLD_4_WEEKS_INPUT, 'value')
                assert threshold_4_weeks == str(page.SCORECARD_DEFAULTS[0]), \
                    [f"Wrong default for 'Threshold for 4 Weeks:' '{threshold_4_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[0])}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking 'Threshold for 8 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[1]}')"):
                threshold_8_weeks = page.get_attribute(page.THRESHOLD_8_WEEKS_INPUT, 'value')
                assert threshold_8_weeks == str(page.SCORECARD_DEFAULTS[1]), \
                    [f"Wrong default for 'Threshold for 8 Weeks:' '{threshold_8_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[1])}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking 'Threshold for 12 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[2]}')"):
                threshold_12_weeks = page.get_attribute(page.THRESHOLD_12_WEEKS_INPUT, 'value')
                assert threshold_12_weeks == str(page.SCORECARD_DEFAULTS[2]), \
                    [f"Wrong default for 'Threshold for 12 Weeks:' '{threshold_12_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[2])}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking 'Threshold for 13 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[3]}')"):
                threshold_13_weeks = page.get_attribute(page.THRESHOLD_13_WEEKS_INPUT, 'value')
                assert threshold_13_weeks == str(page.SCORECARD_DEFAULTS[3]), \
                    [f"Wrong default for 'Threshold for 13 Weeks:' '{threshold_13_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[3])}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking 'Threshold for 26 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[4]}')"):
                threshold_26_weeks = page.get_attribute(page.THRESHOLD_26_WEEKS_INPUT, 'value')
                assert threshold_26_weeks == str(page.SCORECARD_DEFAULTS[4]), \
                    [f"Wrong default for 'Threshold for 26 Weeks:' '{threshold_26_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[4])}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking 'Threshold for 52 Weeks:' is defaulted to '{page.SCORECARD_DEFAULTS[5]}')"):
                threshold_52_weeks = page.get_attribute(page.THRESHOLD_52_WEEKS_INPUT, 'value')
                assert threshold_52_weeks == str(page.SCORECARD_DEFAULTS[5]), \
                    [f"Wrong default for 'Threshold for 52 Weeks:' '{threshold_52_weeks}'"
                     f" instead of '{str(page.SCORECARD_DEFAULTS[5])}'", page.make_screenshot()]

    # "Inventory Settings" defaults: TCs C16056, C22835, C30952, C39548
    with allure.step("Switching to 'Inventory Settings' tab"):
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step("Checking that 'Enable New Ping On FL and MAX' is defaulted to ON"):
                assert page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN), \
                    ["'Enable New Ping On FL and MAX' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Is New Ping' is defaulted to ON"):
                assert page.is_button_switched_on(page.IS_NEW_PING_BTN), \
                    ["'Is New Ping' button is Off", page.make_screenshot()]
        with check:
            with allure.step("Checking that 'Market Listing VDP Link' is defaulted to ON"):
                assert page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN), \
                    ["'Market Listing VDP Link' button is Off", page.make_screenshot()]
        with check:
            with allure.step(
                    f"Checking that 'Default Search Radius' is defaulted to '{page.DEFAULT_SEARCH_RADIUS_DEFAULT}'"):
                radius = page.get_text(page.DEFAULT_SEARCH_RADIUS)
                assert radius == page.DEFAULT_SEARCH_RADIUS_DEFAULT, \
                    [f"Wrong default value for 'Default Search Radius':{radius} instead of "
                     f"{page.DEFAULT_SEARCH_RADIUS_DEFAULT}", page.make_screenshot()]

        with allure.step("Scrolling down to 'New Ping Pricing Indicator Settings'"):
            new_ping_pricing_indicator_settings_bottom = page.locate_element(page.NEW_PING_PRICING_GREEN_TO)
            page.scroll_to_element(new_ping_pricing_indicator_settings_bottom)
            time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Above:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_RED_ABOVE_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_RED_ABOVE)
                red_above = page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
                assert red_above == page.NEW_PING_PRICING_RED_ABOVE_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Red Above:': '{red_above}' instead of "
                     f"'{page.NEW_PING_PRICING_RED_ABOVE_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Below:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_RED_BELOW_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_RED_BELOW)
                red_below = page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
                assert red_below == page.NEW_PING_PRICING_RED_BELOW_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Red Below:': '{red_below}' instead of "
                     f"'{page.NEW_PING_PRICING_RED_BELOW_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow From:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_YELLOW_FROM)
                yellow_from = page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
                assert yellow_from == page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Yellow From:': '{yellow_from}' instead "
                     f"of '{page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow To:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_YELLOW_TO_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_YELLOW_TO)
                yellow_to = page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
                assert yellow_to == page.NEW_PING_PRICING_YELLOW_TO_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Yellow To:': '{yellow_to}' instead of "
                     f"'{page.NEW_PING_PRICING_YELLOW_TO_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow From:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_AND_YELLOW_FROM)
                and_yellow_from = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
                assert and_yellow_from == page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - & Yellow From:': '{and_yellow_from}' "
                     f"instead of '{page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow To:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_AND_YELLOW_TO)
                and_yellow_to = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
                assert and_yellow_to == page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - & Yellow To:': '{and_yellow_to}' instead"
                     f" of '{page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green From:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_GREEN_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_GREEN_FROM)
                green_from = page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
                assert green_from == page.NEW_PING_PRICING_GREEN_FROM_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Green From:': '{green_from}' instead of "
                     f"'{page.NEW_PING_PRICING_GREEN_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green To:' is defaulted to "
                             f"'{page.NEW_PING_PRICING_GREEN_TO_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_GREEN_TO)
                green_to = page.get_attribute(page.NEW_PING_PRICING_GREEN_TO, 'value')
                assert green_to == page.NEW_PING_PRICING_GREEN_TO_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Green To:': '{green_to}' instead of "
                     f"'{page.NEW_PING_PRICING_GREEN_TO_DEFAULT}'", page.make_screenshot()]

    with allure.step("Switching to 'Age Buckets' sub-tab"):
        age_buckets_sub_tab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_sub_tab)
        time.sleep(5)
        page.locate_element(page.BUCKET_ELEMENT)

        with check:
            with allure.step(f"Checking that number of Age Buckets is {len(page.AGE_BUCKETS_DEFAULT_VALUES)}"):
                age_buckets = page.locate_all_elements(page.AGE_BUCKETS_ROW)
                assert len(age_buckets) == len(page.AGE_BUCKETS_DEFAULT_VALUES), \
                    [f"Wrong number of Age buckets:{len(age_buckets)} instead of "
                     f"{len(page.AGE_BUCKETS_DEFAULT_VALUES)}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking default values for Age Bucket sizes: {page.AGE_BUCKETS_DEFAULT_VALUES}"):
                age_bucket_sizes = []
                for i in range(1, len(age_buckets) + 1):
                    age_bucket_sizes.append(page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, i, 2))
                assert age_bucket_sizes == page.AGE_BUCKETS_DEFAULT_VALUES, \
                    [f"Wrong Default Sizes: {age_bucket_sizes}", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        with check:
            with allure.step(f"Checking that number of FirstLook Age Buckets is "
                             f"{len(page.FL_AGE_BUCKETS_DEFAULT_VALUES)}"):
                fl_age_buckets = page.locate_all_elements(page.FL_AGE_BUCKETS_ROW)
                assert len(fl_age_buckets) == len(page.FL_AGE_BUCKETS_DEFAULT_VALUES), \
                    [f"Wrong number of Firstlook buckets: {len(fl_age_buckets)} instead of "
                     f"{len(page.FL_AGE_BUCKETS_DEFAULT_VALUES)}", page.make_screenshot()]
        with check:
            with allure.step(
                    f"Checking default values for FirstLook Age Bucket sizes: {page.FL_AGE_BUCKETS_DEFAULT_VALUES}"):
                fl_age_bucket_sizes = []
                for i in range(1, len(fl_age_buckets) + 1):
                    fl_age_bucket_sizes.append(page.get_table_cell_value_from_input(page.FL_AGE_BUCKET_TABLE, i, 2))
                assert fl_age_bucket_sizes == page.FL_AGE_BUCKETS_DEFAULT_VALUES, \
                    [f"Wrong Default Sizes: {fl_age_bucket_sizes}", page.make_screenshot()]

    # "Book Valuation Settings" defaults: TCs C13594, C33343
    with allure.step("Switching to 'Book Valuations Settings' tab"):
        book_valuations_tab = page.locate_element(page.BOOK_VALUATIONS_TAB)
        page.click(book_valuations_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Guide Book One' is defaulted to '{page.GUIDE_BOOK_ONE_DEFAULT}'"):
                book1 = page.get_text(page.GUIDE_BOOK_ONE_NAME)
                assert book1 == page.GUIDE_BOOK_ONE_DEFAULT, \
                    [f"Wrong Guide Book One name: {book1} instead of {page.GUIDE_BOOK_ONE_DEFAULT}",
                     page.make_screenshot()]
        with check:
            with allure.step(f"Checking that Book One 1st type is defaulted to "
                             f"'{page.GUIDE_BOOK_ONE_1ST_TYPE_DEFAULT}'"):
                book1_first_type = page.get_text(page.GUIDE_BOOK_ONE_1ST_TYPE)
                assert book1_first_type == page.GUIDE_BOOK_ONE_1ST_TYPE_DEFAULT, \
                    [f"Wrong Guide Book One 1st type: {book1_first_type} instead of "
                     f"{page.GUIDE_BOOK_ONE_1ST_TYPE_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that Book One 2d type is defaulted to {page.GUIDE_BOOK_ONE_2D_TYPE_DEFAULT}"):
                book1_second_type = page.get_text(page.GUIDE_BOOK_ONE_2D_TYPE)
                assert book1_second_type == page.GUIDE_BOOK_ONE_2D_TYPE_DEFAULT, \
                    [f"Wrong Guide Book One 2d type: {book1_second_type} instead of "
                     f"{page.GUIDE_BOOK_ONE_2D_TYPE_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable Second Guide Book' button is present and is clickable"):
                page.get_clickable_element(page.ENABLE_SECOND_GUIDE_BOOK_BTN)

        with allure.step("Modifying Name for 'Guide Book One' to 'KBB'"):
            edit_book1_btn = page.get_clickable_element(page.EDIT_GUIDE_BOOK_ONE_BTN)
            page.click(edit_book1_btn)
            time.sleep(TIMEOUT)
            page.edit_guide_book_name(new_value='KBB')
            time.sleep(TIMEOUT)
            element_to_scroll = page.locate_element(page.KBB_CONSUMER_TOOL_TITLE)
            page.scroll_to_element(element_to_scroll)
            time.sleep(1)

        with check:
            with allure.step("Checking that 'KBB Specific Settings' are displayed"):
                assert page.is_element_present(page.KBB_SPECIFIC_SETTINGS_TITLE), \
                    ["'KBB Specific Settings' are not displayed", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'Newest Default Inventory Condition' setting is defaulted to "
                             f"'{page.NEWEST_DEFAULT_INVENTORY_CONDITION_DEFAULT_VALUE}'"):
                newest_default_inv_condition = page.get_text(page.NEWEST_DEFAULT_INVENTORY_CONDITION)
                assert newest_default_inv_condition == page.NEWEST_DEFAULT_INVENTORY_CONDITION_DEFAULT_VALUE, \
                    [f"Wrong default for 'Newest Default Inventory Condition': '{newest_default_inv_condition} "
                        f"instead of '{page.NEWEST_DEFAULT_INVENTORY_CONDITION_DEFAULT_VALUE}'", page.make_screenshot()]

    # "Decoding" tab defaults: TC C16063
    with allure.step("Switching to 'Decoding' tab"):
        decoding_tab = page.locate_element(page.DECODING_TAB)
        page.click(decoding_tab)
        time.sleep(TIMEOUT)

        with allure.step(f"Checking that all checkboxes for Manufacturers are defaulted to On"):
            manufacturers = page.locate_all_elements(page.DECODING_CHECKBOX_STATUS)
        for i in range(1, len(manufacturers) + 1):
            with check:
                checkbox_name = page.get_checkbox_name_decoding(page.DECODING_CHECKBOX_STATUS, i)
                with allure.step(f"Checking that checkbox '{checkbox_name}' is On"):
                    assert page.is_checkbox_checked(page.DECODING_CHECKBOX_STATUS, i, checkbox_name), \
                        [f"Checkbox '{checkbox_name}' is unchecked", page.make_screenshot()]

    # Pricing > Syndication Price defaults: TC C35448
    with allure.step("Switching to 'Pricing' tab"):
        pricing_tab = page.locate_element(page.PRICING_TAB)
        page.click(pricing_tab)
        page = DealerProfilePricingPage(driver)
        time.sleep(TIMEOUT)

        with allure.step("Checking 'Syndication Price Showroom' defaults"):
            syndication_price_showroom = page.locate_element(page.SYNDICATION_PRICE_SHOWROOM)
            page.click(syndication_price_showroom)
            time.sleep(TIMEOUT)
            with check:
                with allure.step(f"Checking that the price for 'New Vehicles' in 'Syndication Price Showroom' is "
                                 f"defaulted to '{page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_SHOWROOM_NEW_VEHICLES)
                    assert price == page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'New Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Used Vehicles' in 'Syndication Price Showroom' is "
                                 f"defaulted to '{page.SYND_PRICE_SHOWROOM_USED_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_SHOWROOM_USED_VEHICLES)
                    assert price == page.SYND_PRICE_SHOWROOM_USED_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Used Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_SHOWROOM_USED_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Unknown Vehicles' in 'Syndication Price Showroom' is "
                                 f"defaulted to '{page.SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES)
                    assert price == page.SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Unknown Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES_DEFAULT}'", page.make_screenshot()]

        with allure.step("Checking 'Syndication Price 1' defaults"):
            syndication_price_1 = page.locate_element(page.SYNDICATION_PRICE_1)
            page.click(syndication_price_1)
            time.sleep(TIMEOUT)
            with check:
                with allure.step(f"Checking that the price for 'New Vehicles' in 'Syndication Price 1' is defaulted "
                                 f"to '{page.SYND_PRICE_1_NEW_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_1_NEW_VEHICLES)
                    assert price == page.SYND_PRICE_1_NEW_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'New Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_1_NEW_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Used Vehicles' in 'Syndication Price 1' is defaulted"
                                 f" to '{page.SYND_PRICE_1_USED_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_1_USED_VEHICLES)
                    assert price == page.SYND_PRICE_1_USED_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Used Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_1_USED_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Unknown Vehicles' in 'Syndication Price 1' is "
                                 f"defaulted to '{page.SYND_PRICE_1_UNKNOWN_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.SYND_PRICE_1_UNKNOWN_VEHICLES)
                    assert price == page.SYND_PRICE_1_UNKNOWN_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Unknown Vehicles': '{price}' instead of "
                         f"'{page.SYND_PRICE_1_UNKNOWN_VEHICLES_DEFAULT}'", page.make_screenshot()]

        with allure.step("Checking 'Writeback Price' defaults"):
            element_to_scroll = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element_to_scroll)
            time.sleep(2)
            writeback_price = page.locate_element(page.WRITEBACK_PRICE)
            page.click(writeback_price)
            time.sleep(TIMEOUT)
            with check:
                with allure.step(f"Checking that the price for 'New Vehicles' in 'Writeback Price' is defaulted "
                                 f"to '{page.WRITEBACK_PRICE_NEW_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.WRITEBACK_PRICE_NEW_VEHICLES)
                    assert price == page.WRITEBACK_PRICE_NEW_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'New Vehicles': '{price}' instead of "
                         f"'{page.WRITEBACK_PRICE_NEW_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Used Vehicles' in 'Writeback Price' is defaulted"
                                 f" to '{page.WRITEBACK_PRICE_USED_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.WRITEBACK_PRICE_USED_VEHICLES)
                    assert price == page.WRITEBACK_PRICE_USED_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Used Vehicles': '{price}' instead of "
                         f"'{page.WRITEBACK_PRICE_USED_VEHICLES_DEFAULT}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that the price for 'Unknown Vehicles' in 'Writeback Price' is "
                                 f"defaulted to '{page.WRITEBACK_PRICE_UNKNOWN_VEHICLES_DEFAULT}'"):
                    price = page.get_text(page.WRITEBACK_PRICE_UNKNOWN_VEHICLES)
                    assert price == page.WRITEBACK_PRICE_UNKNOWN_VEHICLES_DEFAULT, \
                        [f"Wrong default value for 'Unknown Vehicles': '{price}' instead of "
                         f"'{page.WRITEBACK_PRICE_UNKNOWN_VEHICLES_DEFAULT}'", page.make_screenshot()]

    # MAX Settings > Ad Settings defaults: TC C22855
    with allure.step("Switching to 'MAX Settings' / 'Ad Settings' tab"):
        max_settings_tab = page.locate_element(page.MAX_SETTINGS_TAB)
        page.click(max_settings_tab)
        page = DealerProfileMaxSettingsPage(driver)
        ad_settings_sub_tab = page.locate_element(page.AD_SETTINGS_SUB_TAB)
        page.click(ad_settings_sub_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking default values for Tier 0, Tier 1, Tier 2, Tier 3: {page.TIER_DEFAULTS}"):
                tiers = list()
                tiers.append(page.get_attribute(page.TIER_0_INPUT, 'value'))
                tiers.append(page.get_attribute(page.TIER_1_INPUT, 'value'))
                tiers.append(page.get_attribute(page.TIER_2_INPUT, 'value'))
                tiers.append(page.get_attribute(page.TIER_3_INPUT, 'value'))
                assert tiers == page.TIER_DEFAULTS, [f"Wrong Tier Defaults: {tiers}", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'How long is your listing site preview text?' length is defaulted "
                             f"to '{page.PREVIEW_TEXT_LENGTH_DEFAULT}'"):
                text_len = page.get_attribute(page.PREVIEW_TEXT_LENGTH, 'value')
                assert text_len == page.PREVIEW_TEXT_LENGTH_DEFAULT, \
                    [f"Wrong default value for preview text length: {text_len} instead of "
                     f"{page.PREVIEW_TEXT_LENGTH_DEFAULT}", page.make_screenshot()]

        with check:
            with allure.step("Checking that 'Do you want to use more verbose descriptions by default?' is defaulted "
                             "to ON"):
                assert page.is_checkbox_checked(page.MORE_VERBOSE_DESCRIPTIONS_STATUS), \
                    ["Checkbox 'Do you want to use more verbose descriptions by default?' is "
                     "unchecked", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'What Symbol should break up your descriptions' is defaulted to "
                             f"'{page.BREAK_UP_SYMBOL_DEFAULT}'"):
                symbol = page.get_attribute(page.BREAK_UP_SYMBOL, 'value')
                assert symbol == page.BREAK_UP_SYMBOL_DEFAULT, \
                    [f"Wrong default value for 'What Symbol should break up your descriptions': '{symbol}' instead of "
                     f"'{page.BREAK_UP_SYMBOL_DEFAULT}'", page.make_screenshot()]

    # MAX Settings > Setup Wizard: C16049
    with allure.step("Switching to 'MAX Settings' / 'Setup Wizard' tab"):
        setup_wizard_tab = page.locate_element(page.SETUP_WIZARD_TAB)
        page.click(setup_wizard_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(
                    f"Checking that 'What's the minimum mileage remaining you would advertise?' is defaulted to "
                    f"'{page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT}'"):
                minimum_mileage = page.get_attribute(page.SETUP_WIZARD_MIN_MILEAGE_INPUT, 'value')
                assert minimum_mileage == page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT, \
                    [f"Wrong Default for Minimum mileage: {minimum_mileage} instead of "
                     f"{page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'How many characters long is your 'preview' on the web?' is defaulted to "
                             f"'{page.SETUP_WIZARD_CHARACTERS_DEFAULT}'"):
                characters = page.get_attribute(page.SETUP_WIZARD_CHARACTERS_INPUT, 'value')
                assert characters == page.SETUP_WIZARD_CHARACTERS_DEFAULT, \
                    [f"Wrong Default for preview length: {characters} instead of "
                     f"{page.SETUP_WIZARD_CHARACTERS_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Low Photo Threshold' is defaulted to "
                             f"'{page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT}'"):
                low_photo = page.get_attribute(page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_INPUT, 'value')
                assert low_photo == page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT, \
                    [f"Wrong Default for 'Low Photo Threshold': {low_photo} instead of "
                     f"{page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT}", page.make_screenshot()]

    # MAX Settings > Miscellaneous Settings: C16800, C13741
    with allure.step("Switching to 'MAX Settings' / 'Miscellaneous Settings' tab"):
        miscellaneous_sub_tab = page.locate_element(page.MISC_SETTINGS_SUB_TAB)
        page.click(miscellaneous_sub_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step("Checking that checkbox for 'MAX 3.0 Upgrade' is On"):
                assert page.is_checkbox_checked(page.MISC_MAX_3_0_UPGRADE_STATUS), \
                    ["Checkbox 'MAX 3.0 Upgrade' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Webloader' is On"):
                assert page.is_checkbox_checked(page.MISC_WEBLOADER_STATUS), \
                    ["Checkbox 'Webloader' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Batch Autoload' is Off"):
                assert not page.is_checkbox_checked(page.MISC_BATCH_AUTOLOAD_STATUS), \
                    ["Checkbox 'Batch Autoload' is checked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Dashboard' is On"):
                assert page.is_checkbox_checked(page.MISC_DASHBOARD_STATUS), \
                    ["Checkbox 'Dashboard' is unchecked", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that checkbox for 'Show Online Classified Overview' is On"):
                assert page.is_checkbox_checked(page.MISC_SHOW_ONLINE_CLASSIFIED_OVERVIEW_STATUS), \
                    ["Checkbox 'Show Online Classified Overview' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Show Time to Market' is On"):
                assert page.is_checkbox_checked(page.MISC_SHOW_TIME_TO_MARKET_STATUS), \
                    ["Checkbox 'Show Time to Market' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Group Level Dashboard' is On"):
                assert page.is_checkbox_checked(page.MISC_GROUP_LEVEL_DASHBOARD_STATUS), \
                    ["Checkbox 'Group Level Dashboard' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Send Optimal Format' is On"):
                assert page.is_checkbox_checked(page.MISC_SEND_OPTIMAL_FORMAT_STATUS), \
                    ["Checkbox 'Send Optimal Format' is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Move Vehicles Offline that have a Wholesale plan in IMP' "
                             "is On"):
                assert page.is_checkbox_checked(page.MISC_MOVE_VEHICLES_OFFLINE_STATUS), \
                    ["Checkbox 'Move Vehicles Offline that have a Wholesale plan in IMP' "
                     "is unchecked", page.make_screenshot()]
        with check:
            with allure.step("Checking that checkbox for 'Show CTR Graph' is On"):
                assert page.is_checkbox_checked(page.MISC_SHOW_CTR_GRAPH_STATUS), \
                    ["Checkbox 'Show CTR Graph' is unchecked", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'GID Provider - Used' is defaulted to '{page.MISC_GID_PROVIDER_DEFAULT}'"):
                assert page.get_text(page.MISC_GID_PROVIDER_USED_INPUT) == page.MISC_GID_PROVIDER_DEFAULT, \
                    [f"Wrong Default for GID Provider - Used: "
                     f"{page.get_text(page.MISC_GID_PROVIDER_USED_INPUT)}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'GID Provider - New' is defaulted to '{page.MISC_GID_PROVIDER_DEFAULT}'"):
                assert page.get_text(page.MISC_GID_PROVIDER_NEW_INPUT) == page.MISC_GID_PROVIDER_DEFAULT, \
                    [f"Wrong Default for GID Provider - New: "
                     f"{page.get_text(page.MISC_GID_PROVIDER_NEW_INPUT)}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Report Data Source - Used' is defaulted to "
                             f"'{page.MISC_REPORT_DATA_SOURCE_DEFAULT}'"):
                assert page.get_text(page.MISC_REPORT_DATA_SOURCE_USED_INPUT) == page.MISC_GID_PROVIDER_DEFAULT, \
                    [f"Wrong Default for Report Data Source - Used: "
                     f"{page.get_text(page.MISC_REPORT_DATA_SOURCE_USED_INPUT)}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Report Data Source - New' is defaulted to "
                             f"'{page.MISC_REPORT_DATA_SOURCE_DEFAULT}'"):
                assert page.get_text(page.MISC_REPORT_DATA_SOURCE_NEW_INPUT) == page.MISC_GID_PROVIDER_DEFAULT, \
                    [f"Wrong Default for Report Data Source - New: "
                     f"{page.get_text(page.MISC_REPORT_DATA_SOURCE_NEW_INPUT)}", page.make_screenshot()]

    # MAX Settings > Auto-Approve: TC C16490
    with allure.step("Switching to 'MAX Settings'/'Auto-Approve' tab"):
        auto_approve_sub_tab = page.locate_element(page.AUTO_APPROVE_SUB_TAB)
        page.click(auto_approve_sub_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'First Name' is defaulted to '{page.AUTO_APPROVE_FIRST_NAME_DEFAULT}'"):
                first_name = page.get_attribute(page.AUTO_APPROVE_FIRST_NAME, 'value')
                assert first_name == page.AUTO_APPROVE_FIRST_NAME_DEFAULT, \
                    [f"Wrong Default for 'First Name': {first_name} instead of "
                     f"{page.AUTO_APPROVE_FIRST_NAME_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Last Name' is defaulted to '{page.AUTO_APPROVE_LAST_NAME_DEFAULT}'"):
                last_name = page.get_attribute(page.AUTO_APPROVE_LAST_NAME, 'value')
                assert last_name == page.AUTO_APPROVE_LAST_NAME_DEFAULT, \
                    [f"Wrong Default for 'Last Name': {last_name} instead of "
                     f"{page.AUTO_APPROVE_LAST_NAME_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Email' is defaulted to '{page.AUTO_APPROVE_EMAIL_DEFAULT}'"):
                email_default = page.get_attribute(page.AUTO_APPROVE_EMAIL, 'value')
                assert email_default == page.AUTO_APPROVE_EMAIL_DEFAULT, \
                    [f"Wrong Default for 'Email': {email_default} instead of "
                     f"{page.AUTO_APPROVE_EMAIL_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Auto-Approve is' is defaulted to '{page.AUTO_APPROVE_IS_DEFAULT}'"):
                auto_approve = page.get_text(page.AUTO_APPROVE_IS)
                assert auto_approve == page.AUTO_APPROVE_IS_DEFAULT, \
                    [f"Wrong Default for 'Auto-Approve is': '{auto_approve}' instead of "
                     f"'{page.AUTO_APPROVE_IS_DEFAULT}'", page.make_screenshot()]

    # MAX Settings > Alerts defaults: TC C16498
    with allure.step("Switching to 'MAX Settings'/'Alerts' tab"):
        alerts_sub_tab = page.locate_element(page.ALERTS_SUB_TAB)
        page.click(alerts_sub_tab)
        time.sleep(TIMEOUT)

        with allure.step(f"Checking 'Display on Dashboard' and 'Alert in E-mail' checkboxes defaults"):
            for i in page.ALERTS_CHECKBOXES_DEFAULTED_ON:
                with check:
                    checkbox_names = page.get_checkbox_name_alerts_tab(page.ALERTS_CHECKBOX_NAME, i)
                    with allure.step(f"Checking that checkbox '{checkbox_names[0]}' - '{checkbox_names[1]}' is On"):
                        assert page.is_checkbox_checked(page.ALERTS_CHECKBOX_STATUS, i), \
                            [f"Checkbox '{checkbox_names[0]}' - {checkbox_names[1]} is unchecked",
                             page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Create New Dealer: MAX-11759, MAX-13264")
@allure.title("C27235 Spaces are trimmed for text fields when creating a new dealer")
def test_create_dealer_spaces_trimmed(driver):
    with allure.step("Logging to PitStop as Administrator, going to 'Dealers' menu, generating test data"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = CreateNewDealerPage(driver)
        new_dealer = page.generate_new_dealer_data()

    with allure.step("Clicking 'Create New Dealer' button"):
        create_new_dealer_btn = page.get_clickable_element(page.ADD_NEW_DEALER_BTN)
        page.click(create_new_dealer_btn)
        page.get_clickable_element(page.SAVE_BTN)

    with allure.step("Entering values with spaces before and after the value to text fields Name, Short Name, Website,"
                     " Google Place ID, Address, then clicking another field"):
        page.paste_text(page.NAME, f"  {new_dealer['name']}  ")
        page.paste_text(page.SHORT_NAME, f"  {new_dealer['name']}  ")
        page.paste_text(page.WEBSITE, f"  {new_dealer['website']}  ")
        page.paste_text(page.GOOGLE_PLACE_ID, f"  {new_dealer['google_place_id']}  ")
        page.paste_text(page.ADDRESS, f"  {new_dealer['address']}  ")
        phone = page.locate_element(page.OFFICE_PHONE)
        page.click(phone)
        time.sleep(TIMEOUT)

    with check:
        with allure.step("Asserting that spaces are trimmed in the 'Name' field"):
            name_value = page.get_attribute(page.NAME, 'value')
            assert name_value == new_dealer['name'], \
                ["Spaces are not trimmed in the 'Name' field", page.make_screenshot()]
    with check:
        with allure.step("Asserting that spaces are trimmed in the 'Short Name' field"):
            short_name_value = page.get_attribute(page.SHORT_NAME, 'value')
            assert short_name_value == new_dealer['name'], \
                ["Spaces are not trimmed in the 'Short Name' field", page.make_screenshot()]
    with check:
        with allure.step("Asserting that spaces are trimmed in the 'Website' field"):
            website_value = page.get_attribute(page.WEBSITE, 'value')
            assert website_value == new_dealer['website'], \
                ["Spaces are not trimmed in the 'Website' field", page.make_screenshot()]
    with check:
        with allure.step("Asserting that spaces are trimmed in the 'Google Place ID' field"):
            google_place_id_value = page.get_attribute(page.GOOGLE_PLACE_ID, 'value')
            assert google_place_id_value == new_dealer['google_place_id'], \
                ["Spaces are not trimmed in the 'Google Place ID' field", page.make_screenshot()]
    with check:
        with allure.step("Asserting that spaces are trimmed in the 'Address' field"):
            address_value = page.get_attribute(page.ADDRESS, 'value')
            assert address_value == new_dealer['address'], \
                ["Spaces are not trimmed in the 'Address' field", page.make_screenshot()]

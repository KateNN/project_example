import time

from page_objects.AddNewUserPage import AddNewUserPage
from page_objects.LoginPage import LoginPage
from page_objects.LogoutPage import LogoutPage
from page_objects.UserProfilePage import UserProfilePage
from page_objects.MaxInventoryPage import MaxInventoryPage
from page_objects.DealerListPage import DealerListPage
from page_objects.UserListPage import UserListPage
import pytest
from pytest_check import check
import allure

TIMEOUT = 3


@pytest.mark.regression
@allure.feature("Add New User: MAX-9511, MAX-12629, MAX-11612")
@allure.title("Authorized PitStop users can add new users (required fields only). Basic scenario,  "
              "C21695 A unique 6-digit ID is assigned to new users (generated automatically)")
def test_new_user_can_be_added_required_fields_only(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE, password=page.PASSWORD)

    with allure.step("Opening dealer's profile (Windy City Chevrolet) and clicking 'Add New User' button"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)

        add_user_btn = page.locate_element(page.ADD_NEW_USER_BTN)
        page.click(add_user_btn)
        save_btn = page.locate_element(page.SAVE_BTN)
        form_title = page.get_text(page.ADD_NEW_USER_FORM_TITLE)
    with check:
        with allure.step("Asserting that the form title is 'New User"):
            assert form_title == "New User", \
                [f"Wrong form title - {form_title} instead of 'New User'", page.make_screenshot()]

    with allure.step("Generating test data for a new user, filling required fields and saving changes"):
        new_user = page.generate_new_user_data()
        page.type_in_text(page.FIRST_NAME_INPUT, new_user['first_name'])
        page.type_in_text(page.LAST_NAME_INPUT, new_user['last_name'])
        page.paste_text(page.USERNAME_INPUT, new_user['username'])
        page.paste_text(page.PASSWORD_INPUT, new_user['password'])
        page.click(save_btn)

    with allure.step("Verifying that the new user's profile can be opened"):
        open_new_user_btn = page.locate_element(page.SUCCESS_BTN)
        page.click(open_new_user_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_USERS_FILE_NAME)
        page = UserProfilePage(driver)
        user_name_in_profile = page.get_text(page.NEW_USERNAME_IN_PROFILE)
    with check:
        with allure.step("Asserting that the User name in profile is the new user's name"):
            assert user_name_in_profile == new_user['username'], \
                [f"Wrong username in the user profile - {user_name_in_profile}", page.make_screenshot()]

    with allure.step("Getting Member ID"):
        page.locate_element(page.MEMBER_ID)
        member_id = page.get_text(page.MEMBER_ID).split()[-1]
    with check:
        with allure.step(f"Asserting that Member ID '{member_id}' consists of 6 characters"):
            assert len(member_id) == 6, \
                [f"Wrong Member ID length: {len(member_id)} instead of 6", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting that Member ID '{member_id}' consists of digits only"):
            assert member_id.isdigit(), [f"Member ID includes not only digits: {member_id}", page.make_screenshot()]
    with allure.step(f"Switching to 'Users' list and searching for users by new user's Member ID {member_id}"):
        page = UserListPage(driver)
        page.open()
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, member_id)
        search_btn = page.get_clickable_element(page.SEARCH_BTN)
        page.click(search_btn)
        time.sleep(TIMEOUT)
    with check:
        with allure.step(f"Checking that Member ID {member_id} is unique (a single search result)"):
            items_in_results = page.locate_all_elements(page.ITEMS_IN_SEARCH_RESULTS)
            assert len(items_in_results) == 1, [f"Member ID {member_id} is not unique!", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Add New User: MAX-9511, MAX-12629, MAX-11612")
@allure.title("C13588 Positive case: all required fields have valid values, new user can login to MAX Inventory")
def test_new_user_can_login_to_max_inventory_all_fields(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Going to Windy City Chevrolet page, generating test data and creating a new user"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)

        new_user = page.generate_new_user_data()
        page.add_new_user(first_name=new_user['first_name'],
                          last_name=new_user['last_name'],
                          username=new_user['username'],
                          email=new_user['email'],
                          password=new_user['password'],
                          mobile_phone=new_user['mobile_phone'])

    with allure.step(f"Verifying that the new user's '{new_user['username']}' profile can be opened"):
        open_new_user_btn = page.locate_element(page.SUCCESS_BTN)
        page.click(open_new_user_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_USERS_FILE_NAME)
        page = UserProfilePage(driver)
        user_name_in_profile = page.get_text(page.NEW_USERNAME_IN_PROFILE)
        with allure.step("Asserting that the User name in profile is the new user's name"):
            assert user_name_in_profile == new_user['username'], \
                [f"Wrong username in the user profile - {user_name_in_profile}", page.make_screenshot()]
        time.sleep(TIMEOUT)

    with allure.step("Logging out from PitStop"):
        page = LogoutPage(driver)
        page.open()
        page.locate_element(page.MAX_INVENTORY_LOGO)

    with allure.step("Going to MAX Inventory and logging in with the new user credentials"):
        page = LoginPage(driver)
        page.open_url(page.MAX_INVENTORY_URL)
        page.log_in(username=new_user['username'],
                    password=new_user['password'])
        page = MaxInventoryPage(driver)
        page.check_page_title(page.MAX_INVENTORY_PAGE_TITLE)


@pytest.mark.regression
@allure.feature("Add New User: MAX-9511")
@allure.title("C13589 All required fields are empty")
def test_add_new_user_empty_required_fields(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Going to Windy City Chevrolet, clicking 'Add New User' button, leaving all required fields empty."
                     " Saving changes"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)
        page.add_new_user()

    with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
        alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
        assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
            [f"Wrong alert text for Form Validation: {alert1} instead of "
             f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]
    with allure.step(f"Asserting First Name Required alert: '{page.FIRST_NAME_REQUIRED_TEXT}'"):
        alert2 = page.locate_element(page.FIRST_NAME_REQUIRED_ALERT).text
        assert alert2 == page.FIRST_NAME_REQUIRED_TEXT, \
            [f"Wrong alert text for the First Name field: {alert2} instead of "
             f"{page.FIRST_NAME_REQUIRED_TEXT}", page.make_screenshot()]
    with allure.step(f"Asserting Last Name Required alert: '{page.LAST_NAME_REQUIRED_TEXT}'"):
        alert3 = page.locate_element(page.LAST_NAME_REQUIRED_ALERT).text
        assert alert3 == page.LAST_NAME_REQUIRED_TEXT, \
            [f"Wrong alert text the Last Name field: {alert3} instead of "
             f"{page.LAST_NAME_REQUIRED_TEXT}", page.make_screenshot()]
    with allure.step(f"Asserting Username Required alert: '{page.USERNAME_REQUIRED_TEXT}'"):
        alert4 = page.locate_element(page.USERNAME_REQUIRED_ALERT).text
        assert alert4 == page.USERNAME_REQUIRED_TEXT, \
            [f"Wrong alert text the Username field: {alert4} instead of "
             f"{page.USERNAME_REQUIRED_TEXT}", page.make_screenshot()]
    with allure.step(f"Asserting Password Required alert: '{page.PASSWORD_REQUIRED_TEXT}'"):
        alert5 = page.locate_element(page.PASSWORD_REQUIRED_ALERT).text
        assert alert5 == page.PASSWORD_REQUIRED_TEXT, \
            [f"Wrong alert text for the Password field: {alert5} instead of"
             f" {page.PASSWORD_REQUIRED_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Add New User: MAX-9511")
@allure.title("C13678 Required field Username must be unique")
def test_add_new_user_username_must_be_unique(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

    with allure.step("Going to Windy City Chevrolet, generating test data. Clicking 'Add New User' button, filling all"
                     " required fields. Entering existing login to the Username field and trying to save the changes"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)
        new_user = page.generate_new_user_data()
        page.add_new_user(first_name=new_user['first_name'],
                          last_name=new_user['last_name'],
                          username=page.EXISTING_USERNAME,
                          password=new_user['password'])

    with allure.step(f"Checking Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
        alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
        assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
            [f"Wrong alert text for Form Validation: {alert1} instead of "
             f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]

    with allure.step(f"Checking Username Must Be Unique alert: '{page.MUST_BE_UNIQUE_TEXT}'"):
        alert2 = page.locate_element(page.USERNAME_MUST_BE_UNIQUE_ALERT).text
        assert alert2 == page.MUST_BE_UNIQUE_TEXT, \
            [f"Wrong alert text for Username must be unique: {alert2} instead of "
             f"{page.MUST_BE_UNIQUE_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("User Profile Settings: MAX-16334, MAX-11553, MAX-9884, MAX-12052")
@allure.title("C53103, C22841, C16039, C13760 - Dashboard Row Display defaults, Default Dealer Group display, "
              "Merchandising roles defaults, Login field is view-only")
def test_new_user_defaults_and_settings(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE, password=page.PASSWORD)
        time.sleep(TIMEOUT)

    with allure.step("Opening dealer's profile (Windy City Chevrolet) and clicking 'Add New User' button"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)

        new_user = page.generate_new_user_data()
        page.add_new_user(first_name=new_user['first_name'],
                          last_name=new_user['last_name'],
                          username=new_user['username'],
                          email=new_user['email'],
                          password=new_user['password'],
                          mobile_phone=new_user['mobile_phone'])

    with allure.step(f"Opening '{new_user['username']}' profile"):
        open_new_user_btn = page.locate_element(page.SUCCESS_BTN)
        page.click(open_new_user_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_USERS_FILE_NAME)

    page = UserProfilePage(driver)
    page.get_clickable_element(page.GENERAL_EDIT_BTN)

    with allure.step("Switching to 'Edit' mode"):
        edit_btn = page.get_clickable_element(page.GENERAL_EDIT_BTN)
        page.click(edit_btn)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that 'Login' field contains the User's username"):
            user_name_in_profile = page.get_text(page.NEW_USERNAME_IN_PROFILE)
            login_text = page.get_text(page.LOGIN_FIELD)
            assert login_text == user_name_in_profile, [f"'Login' is not' {user_name_in_profile}', "
                                                        f"it's '{login_text}'", page.make_screenshot()]
    with check:
        with allure.step("Checking that 'Login' field cannot be modified (not an input or a textarea)"):
            login_field_tag = page.get_tag_name(page.LOGIN_FIELD)
            assert login_field_tag not in ['input', 'textarea'], \
                [f"'Login' field can be modified, it's '{login_field_tag}'", page.make_screenshot()]

    with allure.step("Switching back to 'View' mode"):
        cancel_btn = page.get_clickable_element(page.GENERAL_CANCEL_BTN)
        page.click(cancel_btn)
        time.sleep(TIMEOUT)

    with allure.step("Switching to 'Other' tab"):
        other_tab = page.locate_element(page.OTHER_TAB)
        page.click(other_tab)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that 'Dashboard Row Display' is defaulted to "
                         f"{page.DASHBOARD_ROW_DISPLAY_DEFAULT}"):
            dashboard_row_display = page.get_attribute(page.DASHBOARD_ROW_DISPLAY, 'value')
            assert dashboard_row_display == page.DASHBOARD_ROW_DISPLAY_DEFAULT, \
                [f"'Dashboard Row Display' is not defaulted to '{page.DASHBOARD_ROW_DISPLAY_DEFAULT}', "
                 f"it's '{dashboard_row_display}'", page.make_screenshot()]

    with check:
        with allure.step(f"Checking that 'Default Dealer Group' displays '{page.DEFAULT_GROUP_NAME}'"):
            default_dealer_group = page.get_text(page.DEFAULT_DEALER_GROUP)
            assert default_dealer_group == page.DEFAULT_GROUP_NAME, \
                [f"Wrong value for 'Default Dealer Group': '{default_dealer_group}' instead of "
                 f"'{page.DEFAULT_GROUP_NAME}'", page.make_screenshot()]

    with allure.step("Switching to 'Roles - Merchandising' tab"):
        roles_tab = page.locate_element(page.ROLES_TAB)
        page.click(roles_tab)
        time.sleep(TIMEOUT)
        merchandising_tab = page.locate_element(page.ROLES_MERCHANDISING_TAB)
        page.click(merchandising_tab)
        time.sleep(TIMEOUT)

    with allure.step(f"Verifying that {page.USER_MERCHANDISING_ROLES_DEFAULTS} roles are checked by default"):
        roles = page.locate_all_elements(page.MERCHANDISING_CHECKBOX_STATUS)
    for i in range(1, len(roles) + 1):
        with check:
            checkbox_name = page.get_checkbox_name_merchandising(page.MERCHANDISING_CHECKBOX_STATUS, i)
            if checkbox_name in page.USER_MERCHANDISING_ROLES_DEFAULTS:
                with allure.step(f"Checking that checkbox '{checkbox_name}' is checked"):
                    assert page.is_checkbox_checked(page.MERCHANDISING_CHECKBOX_STATUS, i, checkbox_name), \
                        [f"Checkbox '{checkbox_name}' is unchecked", page.make_screenshot()]
            else:
                with allure.step(f"Checking that checkbox '{checkbox_name}' is NOT checked"):
                    assert not page.is_checkbox_checked(page.MERCHANDISING_CHECKBOX_STATUS, i, checkbox_name), \
                        [f"Checkbox '{checkbox_name}' is unchecked", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("User Profile Settings: MAX-12269")
@allure.title("C24212 - 'Manager (Without Pricing)' role set in 'Roles' unchecks the 'Pricer' setting within "
              "'Merchandising Roles'")
def test_manager_without_pricing_unchecks_pricer(driver):
    with allure.step("Logging to PitStop as Administrator"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE, password=page.PASSWORD)
        time.sleep(TIMEOUT)

    new_users_to_inactivate = page.get_new_objects_list(page.NEW_USERS_FILE_NAME)
    if new_users_to_inactivate:
        user_url = new_users_to_inactivate[0]
        page.open_url(user_url)
        time.sleep(TIMEOUT)
    else:
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        page = AddNewUserPage(driver)

        new_user = page.generate_new_user_data()
        page.add_new_user(first_name=new_user['first_name'],
                          last_name=new_user['last_name'],
                          username=new_user['username'],
                          email=new_user['email'],
                          password=new_user['password'],
                          mobile_phone=new_user['mobile_phone'])

        with allure.step(f"Opening '{new_user['username']}' profile"):
            open_new_user_btn = page.locate_element(page.SUCCESS_BTN)
            page.click(open_new_user_btn)
            time.sleep(TIMEOUT)
            page.add_new_objects_to_list(page.NEW_USERS_FILE_NAME)

    page = UserProfilePage(driver)
    page.get_clickable_element(page.GENERAL_EDIT_BTN)

    with allure.step("Switching to 'Roles' tab"):
        roles_tab = page.locate_element(page.ROLES_TAB)
        page.click(roles_tab)
        time.sleep(TIMEOUT)

    with allure.step("Checking the current 'Used Car Role' and changing it to 'Manager' if it's "
                     "'Manager (without pricing)'"):
        current_used_car_role = page.get_text(page.USED_CAR_ROLE_VALUE)
        if current_used_car_role == 'Manager (without pricing)':
            with allure.step("Selecting 'Manager' for 'Used Car Role'"):
                used_car_role = page.locate_element(page.USED_CAR_ROLE)
                page.click(used_car_role)
                time.sleep(TIMEOUT)
                manager_without_pricing = page.locate_element(page.MANAGER_OPTION)
                page.click(manager_without_pricing)
                time.sleep(TIMEOUT)

    with allure.step("Switching to 'Roles - Merchandising' sub-tab"):
        merchandising_tab = page.locate_element(page.ROLES_MERCHANDISING_TAB)
        page.click(merchandising_tab)
        time.sleep(TIMEOUT)

    with allure.step("Checking 'Pricer' if is it unchecked"):
        checkbox_name = page.get_checkbox_name_merchandising(page.MERCHANDISING_CHECKBOX_STATUS, 10)
        is_pricer_checked = page.is_checkbox_checked(page.MERCHANDISING_CHECKBOX_STATUS, 10, checkbox_name)
        if not is_pricer_checked:
            with allure.step("Checking 'Pricer' checkbox and saving changes"):
                pricer = page.locate_element(page.PRICER_CHECKBOX)
                page.click(pricer)
                time.sleep(TIMEOUT)
                save_btn = page.get_clickable_element(page.MERCH_ROLES_SAVE_BTN)
                page.click(save_btn)
                time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that 'Pricer' is checked now"):
            assert page.is_checkbox_checked(page.MERCHANDISING_CHECKBOX_STATUS, 10, checkbox_name), \
                [f"'Pricer' is not checked!", page.make_screenshot()]

    with allure.step("Switching to 'Roles - Roles' sub-tab"):
        roles_tab = page.locate_element(page.ROLES_ROLES_SUBTAB)
        page.click(roles_tab)
        time.sleep(TIMEOUT)

    with allure.step("Selecting 'Manager (without pricing)' for 'Used Car Role'"):
        used_car_role = page.locate_element(page.USED_CAR_ROLE)
        page.click(used_car_role)
        time.sleep(TIMEOUT)
        manager_without_pricing = page.locate_element(page.MANAGER_WITHOUT_PRICING_OPTION)
        page.click(manager_without_pricing)

    with check:
        with allure.step(f"Checking that alert '{page.PRICER_REMOVED_ALERT_TEXT}' is displayed"):
            alert = page.get_text(page.PRICER_REMOVED_ALERT)
            assert alert == page.PRICER_REMOVED_ALERT_TEXT, \
                [f"Wrong alert text: '{alert}' instead of '{page.PRICER_REMOVED_ALERT_TEXT}'", page.make_screenshot()]
        time.sleep(TIMEOUT)

    with allure.step("Switching to 'Roles - Merchandising' sub-tab"):
        merchandising_tab = page.locate_element(page.ROLES_MERCHANDISING_TAB)
        page.click(merchandising_tab)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that 'Pricer' is unchecked now"):
            checkbox_name = page.get_checkbox_name_merchandising(page.MERCHANDISING_CHECKBOX_STATUS, 10)
            assert not page.is_checkbox_checked(page.MERCHANDISING_CHECKBOX_STATUS, 10, checkbox_name), \
                [f"'Pricer' is sill checked!", page.make_screenshot()]

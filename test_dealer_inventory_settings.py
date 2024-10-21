from page_objects.CreateNewDealerPage import CreateNewDealerPage
from page_objects.LoginPage import LoginPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
import time
import random
import pytest
from pytest_check import check
import allure

TIMEOUT = 3


@pytest.mark.regression
@allure.feature("Inventory Settings: MAX-9522")
@allure.title("C21700, C34679, C27237, C13666, C22606, C39549, C34679 All settings in the 'Inventory Settings' tab "
              "can be edited . 'Restore Defaults' button")
def test_edit_inventory_settings_and_restore_defaults(driver):
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

    with allure.step("Switching to 'Inventory Settings' / 'Pin II' tab"):
        page = DealerProfileDealerPage(driver)
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)

    with allure.step("Saving initial settings in 'Ping II' tab, 'Ping II / Market' section"):
        ping2_before = dict()
        ping2_before['supress_seller_name'] = page.is_button_switched_on(page.SUPRESS_SELLER_NAME_BTN)
        ping2_before['exclude_no_price_from_calc'] = page.is_button_switched_on(page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
        ping2_before['enable_new_car_pricing'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_before['enable_lithia_new_car_view'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_before['enable_chrome_incentives'] = page.is_button_switched_on(page.ENABLE_CHROME_INCENTIVES_BTN)
        ping2_before['is_new_ping'] = page.is_button_switched_on(page.IS_NEW_PING_BTN)
        ping2_before['enable_new_ping_on_fl_and_max'] = \
            page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
        ping2_before['market_listing_vdp_link'] = page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN)
        ping2_before['default_search_radius'] = page.get_text(page.DEFAULT_SEARCH_RADIUS)
        ping2_before['default_stock_type'] = page.get_text(page.DEFAULT_STOCK_TYPE)

    with allure.step("Clicking 'Edit' button, modifying all settings"):
        edit_button = page.get_clickable_element(page.PING_II_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        save_button = page.get_clickable_element(page.PING_II_SAVE_BTN)
        supress_seller_name = page.get_clickable_element(page.SUPRESS_SELLER_NAME_BTN)
        page.click(supress_seller_name)
        exclude_no_price_from_calc = page.get_clickable_element(page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
        page.click(exclude_no_price_from_calc)
        enable_new_car_pricing = page.get_clickable_element(page.ENABLE_NEW_CAR_PRICING_BTN)
        page.click(enable_new_car_pricing)
        enable_lithia_new_car_view = page.get_clickable_element(page.ENABLE_LITHIA_NEW_CAR_VIEW_BTN)
        page.click(enable_lithia_new_car_view)
        enable_chrome_incentives = page.get_clickable_element(page.ENABLE_CHROME_INCENTIVES_BTN)
        page.click(enable_chrome_incentives)
        is_new_ping = page.get_clickable_element(page.IS_NEW_PING_BTN)
        page.click(is_new_ping)
        enable_new_ping_on_fl_and_max = page.get_clickable_element(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
        page.click(enable_new_ping_on_fl_and_max)
        market_listing_vdp_link = page.get_clickable_element(page.MARKET_LISTING_VDP_LINK_BTN)
        page.click(market_listing_vdp_link)
        default_search_radius = page.locate_element(page.DEFAULT_SEARCH_RADIUS)
        page.click(default_search_radius)
        time.sleep(TIMEOUT)
        new_radius_path = page.get_other_value_for_ping_2_dropdowns(ping2_before['default_search_radius'],
                                                                    page.DEFAULT_SEARCH_RADIUS_VALUES)
        new_radius = page.locate_element(new_radius_path)
        page.click(new_radius)
        default_stock_type = page.locate_element(page.DEFAULT_STOCK_TYPE)
        page.click(default_stock_type)
        time.sleep(TIMEOUT)
        new_stock_type_path = page.get_other_value_for_ping_2_dropdowns(ping2_before['default_stock_type'],
                                                                        page.DEFAULT_STOCK_TYPE_VALUES)
        new_stock_type = page.locate_element(new_stock_type_path)
        page.click(new_stock_type)
        time.sleep(TIMEOUT)

    with allure.step("Collecting modified values and saving changes"):
        ping2_modified = dict()
        ping2_modified['supress_seller_name'] = page.is_button_switched_on(page.SUPRESS_SELLER_NAME_BTN)
        ping2_modified['exclude_no_price_from_calc'] = page.is_button_switched_on(page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
        ping2_modified['enable_new_car_pricing'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_modified['enable_lithia_new_car_view'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_modified['enable_chrome_incentives'] = page.is_button_switched_on(page.ENABLE_CHROME_INCENTIVES_BTN)
        ping2_modified['is_new_ping'] = page.is_button_switched_on(page.IS_NEW_PING_BTN)
        ping2_modified['enable_new_ping_on_fl_and_max'] = \
            page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
        ping2_modified['market_listing_vdp_link'] = page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN)
        ping2_modified['default_search_radius'] = page.get_text(page.DEFAULT_SEARCH_RADIUS)
        ping2_modified['default_stock_type'] = page.get_text(page.DEFAULT_STOCK_TYPE)
        page.click(save_button)

    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.PING_II_SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step("Collecting values in 'Ping II' tab 'Ping II / Market' section after changes are saved"):
        ping2_after = dict()
        ping2_after['supress_seller_name'] = page.is_button_switched_on(page.SUPRESS_SELLER_NAME_BTN)
        ping2_after['exclude_no_price_from_calc'] = page.is_button_switched_on(page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
        ping2_after['enable_new_car_pricing'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_after['enable_lithia_new_car_view'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_after['enable_lithia_new_car_view'] = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        ping2_after['enable_chrome_incentives'] = page.is_button_switched_on(page.ENABLE_CHROME_INCENTIVES_BTN)
        ping2_after['is_new_ping'] = page.is_button_switched_on(page.IS_NEW_PING_BTN)
        ping2_after['enable_new_ping_on_fl_and_max'] = \
            page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
        ping2_after['market_listing_vdp_link'] = page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN)
        ping2_after['default_search_radius'] = page.get_text(page.DEFAULT_SEARCH_RADIUS)
        ping2_after['default_stock_type'] = page.get_text(page.DEFAULT_STOCK_TYPE)

    with allure.step("Checking that all changes were saved"):
        for key in ping2_after.keys():
            with check:
                with allure.step(f"Checking that '{key}' was modified from '{ping2_before[key]}' to "
                                 f"'{ping2_modified[key]}'"):
                    assert ping2_after[key] == ping2_modified[key] and ping2_after[key] != ping2_before[key], \
                        [f"{key}' setting not edited, it has old value: '{ping2_before[key]}'",
                         page.make_screenshot()]

    with allure.step("Scrolling down to 'New Ping Pricing Indicator Settings'"):
        new_ping_pricing_indicator_settings_bottom = page.locate_element(page.NEW_PING_PRICING_GREEN_TO)
        page.scroll_to_element(new_ping_pricing_indicator_settings_bottom)
        time.sleep(TIMEOUT)

    with allure.step("Saving initial settings in 'Ping II' tab, 'New Ping Pricing Indicator Settings' section"):
        new_ping_pricing_before = dict()
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Above' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_red_above'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Below' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_red_below'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow From' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow To' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow From' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_and_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow To' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_and_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green From' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_green_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green To' setting"):
            new_ping_pricing_before['new_ping_pricing_indicator_green_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_TO, 'value')

    with allure.step("Clicking 'Edit' button, modifying all settings and saving the changes"):
        edit_button = page.get_clickable_element(page.EDIT_NEW_PING_PRICING_INDICATOR_SETTINGS_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        save_button = page.get_clickable_element(page.SAVE_NEW_PING_PRICING_INDICATOR_SETTINGS_BTN)
        with allure.step("Modifying all 'New Ping Pricing Indicator Settings'"):
            for item in page.NEW_PING_PRICING_INDICATOR_SETTINGS_TITLES:
                page.edit_new_ping_pricing_indicator_settings(item)
        time.sleep(TIMEOUT)
        page.click(save_button)

    with allure.step(f"Checking that success message is displayed"):
        page.locate_element(page.PING_II_SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step("Collecting values in 'New Ping Pricing Indicator Settings' section after the changes are saved"):
        new_ping_pricing_after = dict()
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Above' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_red_above'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Below' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_red_below'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow From' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow To' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow From' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_and_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow To' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_and_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green From' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_green_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green To' setting"):
            new_ping_pricing_after['new_ping_pricing_indicator_green_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_TO, 'value')

    with allure.step("Checking that all changes were saved"):
        for key in new_ping_pricing_after.keys():
            with check:
                with allure.step(f"Checking that '{key}' was modified from '{new_ping_pricing_before[key]}' to "
                                 f"'{new_ping_pricing_after[key]}'"):
                    assert new_ping_pricing_after[key] != new_ping_pricing_before[key], \
                        [f"{key}' setting not edited, it has old value: '{new_ping_pricing_before[key]}'",
                         page.make_screenshot()]

    with allure.step("Switching to 'Inventory Settings' / 'Age Buckets' tab"):
        age_buckets_tab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_tab)
        time.sleep(TIMEOUT)

    with allure.step("Saving initial settings in 'Age Buckets' tab"):
        age_buckets_before = dict()
        age_buckets_after = dict()
        age_buckets = page.locate_all_elements(page.AGE_BUCKETS_ROW)
        age_buckets_before['number_of_age_buckets'] = len(age_buckets)
        age_bucket_sizes = []
        for i in range(1, len(age_buckets) + 1):
            age_bucket_sizes.append(page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, i, 2))
        age_buckets_before['age_bucket_sizes'] = age_bucket_sizes
        fl_age_buckets = page.locate_all_elements(page.FL_AGE_BUCKETS_ROW)
        fl_age_bucket_sizes = []
        for i in range(1, len(fl_age_buckets) + 1):
            fl_age_bucket_sizes.append(page.get_table_cell_value_from_input(page.FL_AGE_BUCKET_TABLE, i, 2))
        age_buckets_before['fl_age_bucket_sizes'] = fl_age_bucket_sizes

    with allure.step("Clicking 'Edit' button, modifying Age Bucket settings"):
        edit_button = page.get_clickable_element(page.AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        with allure.step("Modifying Age Bucket sizes "):
            for i in range(1, len(age_buckets)):
                page.change_size_of_age_bucket(i, 'up')

    with allure.step("Adding 7th and 8th Age Buckets and saving changed"):
        new_button = page.locate_element(page.AGE_BUCKETS_NEW_BTN)
        for _ in range(2):
            page.click(new_button)
            time.sleep(5)
        page.click(save_button)
        time.sleep(TIMEOUT)

    with allure.step("Collecting 1-6th Age Buckets settings after changes are saved, and values for new 7-8th Buckets"):
        age_buckets = page.locate_all_elements(page.AGE_BUCKETS_ROW)
        age_buckets_after['number_of_age_buckets'] = len(age_buckets)
        age_bucket_sizes = []
        for i in range(1, len(age_buckets) + 1):
            age_bucket_sizes.append(page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, i, 2))
        age_buckets_after['age_bucket_sizes'] = age_bucket_sizes
        min_market_7th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 7, 4)
        max_market_7th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 7, 5)
        min_gross_7th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 7, 6)
        min_market_8th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 8, 4)
        max_market_8th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 8, 5)
        min_gross_8th_bucket = page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, 8, 6)
        age_buckets_after['age_bucket7_values'] = [min_market_7th_bucket, max_market_7th_bucket, min_gross_7th_bucket]
        age_buckets_after['age_bucket8_values'] = [min_market_8th_bucket, max_market_8th_bucket, min_gross_8th_bucket]

    with allure.step("Clicking 'Edit' button, modifying FirstLook Age Bucket settings"):
        edit_button = page.get_clickable_element(page.FL_AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        with allure.step("Modifying Firstlook Age Bucket sizes and saving changes"):
            for i in range(1, len(fl_age_buckets)):
                page.change_size_of_firstlook_age_bucket(i, 'up')
            page.click(save_button)

    with allure.step("Collecting Firstlook Age Buckets settings after changes are saved"):
        fl_age_bucket_sizes = []
        for i in range(1, len(fl_age_buckets) + 1):
            fl_age_bucket_sizes.append(page.get_table_cell_value_from_input(page.FL_AGE_BUCKET_TABLE, i, 2))
        age_buckets_after['fl_age_bucket_sizes'] = fl_age_bucket_sizes

    with allure.step("Checking that sizes of Age Buckets 1-5 were modified"):
        for i in range(5):
            with check:
                with allure.step(f"Checking that Age Bucket {i + 1} was modified"):
                    assert age_buckets_before['age_bucket_sizes'][i] != age_buckets_after['age_bucket_sizes'][i], \
                        [f"Age Bucket {i + 1} was not modified, it has old size: "
                         f"'{age_buckets_before['age_bucket_sizes'][i]}'", page.make_screenshot()]

    with allure.step("Checking defaults for 7th and 8th Age Buckets"):
        with check:
            with allure.step(f"Checking that 7th and 8th buckets were added"):
                assert len(age_buckets_after['age_bucket_sizes']) == 8, \
                    [f"Wrong Age Bucket number: {len(age_buckets_after['age_bucket_sizes'])} instead of 8",
                     page.make_screenshot()]

        with check:
            with allure.step(f"Checking 7th Age Bucket defaults for 'Min Market%', 'Max Market%', 'Min Gross': "
                             f"'{page.AGE_BUCKETS_7TH_BUCKET_DEFAULTS}'"):
                assert age_buckets_after['age_bucket7_values'] == page.AGE_BUCKETS_7TH_BUCKET_DEFAULTS, \
                    [f"Wrong Age Bucket 7 defaults: {age_buckets_after['age_bucket7_values']} instead of "
                     f"{page.AGE_BUCKETS_7TH_BUCKET_DEFAULTS}", page.make_screenshot()]

        with check:
            with allure.step(f"Checking 8th Age Bucket defaults for 'Min Market%', 'Max Market%', 'Min Gross': "
                             f"'{page.AGE_BUCKETS_8TH_BUCKET_DEFAULTS}'"):
                assert age_buckets_after['age_bucket8_values'] == page.AGE_BUCKETS_8TH_BUCKET_DEFAULTS, \
                    [f"Wrong Age Bucket 8 defaults: {age_buckets_after['age_bucket8_values']} instead of "
                     f"{page.AGE_BUCKETS_8TH_BUCKET_DEFAULTS}", page.make_screenshot()]

    with allure.step("Checking that sizes of FirstLook Age Buckets were modified"):
        for i in range(4):
            with check:
                with allure.step(f"Checking that FirstLook Age Bucket {i + 1} was modified"):
                    assert age_buckets_before['fl_age_bucket_sizes'][i] != age_buckets_after['fl_age_bucket_sizes'][i], \
                        [f"FirstLook Age Bucket {i + 1} was not modified,it has old size: "
                         f"'{age_buckets_before['fl_age_bucket_sizes'][i]}'", page.make_screenshot()]

    with allure.step("Switching to 'Inventory Settings' / 'Pin II' tab"):
        ping2_tab = page.locate_element(page.PING_II_SUB_TAB)
        page.click(ping2_tab)
        time.sleep(TIMEOUT)

    with allure.step("Clicking 'Restore Defaults' button, checking 'Restore Age Buckets' check-box  and confirming"):
        restore_defaults = page.locate_element(page.PING_II_RESTORE_DEFAULTS_BTN)
        page.click(restore_defaults)
        time.sleep(TIMEOUT)
        restore_age_bucket_checkbox = page.locate_element(page.RESTORE_AGE_BUCKETS_CHECKBOX)
        page.click(restore_age_bucket_checkbox)
        confirm_button = page.locate_element(page.RESTORE_DEFAULTS_CONFIRM_BTN)
        page.click(confirm_button)
        time.sleep(TIMEOUT)

    with allure.step("Checking that Ping II settings, 'Ping II / Market' section, are restored to defaults"):
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

    with allure.step("Checking that Ping II settings, 'New Ping Pricing Indicator Settings' section, are restored to "
                     "defaults"):
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Above:' is restored to "
                             f"'{page.NEW_PING_PRICING_RED_ABOVE_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_RED_ABOVE)
                red_above = page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
                assert red_above == page.NEW_PING_PRICING_RED_ABOVE_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Red Above:': '{red_above}' instead of "
                     f"'{page.NEW_PING_PRICING_RED_ABOVE_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Below:' is restored to "
                             f"'{page.NEW_PING_PRICING_RED_BELOW_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_RED_BELOW)
                red_below = page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
                assert red_below == page.NEW_PING_PRICING_RED_BELOW_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Red Below:': '{red_below}' instead of "
                     f"'{page.NEW_PING_PRICING_RED_BELOW_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow From:' is restored to "
                             f"'{page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_YELLOW_FROM)
                yellow_from = page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
                assert yellow_from == page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT, \
                    [
                        f"Wrong value for 'New Ping Pricing Indicator Settings - Yellow From:': '{yellow_from}' "
                        f"instead of '{page.NEW_PING_PRICING_YELLOW_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow To:' is restored to "
                             f"'{page.NEW_PING_PRICING_YELLOW_TO_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_YELLOW_TO)
                yellow_to = page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
                assert yellow_to == page.NEW_PING_PRICING_YELLOW_TO_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Yellow To:': '{yellow_to}' instead of "
                     f"'{page.NEW_PING_PRICING_YELLOW_TO_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow From:' is restored to "
                             f"'{page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_AND_YELLOW_FROM)
                and_yellow_from = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
                assert and_yellow_from == page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT, \
                    [
                        f"Wrong value for 'New Ping Pricing Indicator Settings - & Yellow From:': '{and_yellow_from}' "
                        f"instead of '{page.NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow To:' is restored to "
                             f"'{page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_AND_YELLOW_TO)
                and_yellow_to = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
                assert and_yellow_to == page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT, \
                    [
                        f"Wrong value for 'New Ping Pricing Indicator Settings - & Yellow To:': '{and_yellow_to}' "
                        f"instead of '{page.NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green From:' is restored to "
                             f"'{page.NEW_PING_PRICING_GREEN_FROM_DEFAULT}'"):
                page.locate_element(page.NEW_PING_PRICING_GREEN_FROM)
                green_from = page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
                assert green_from == page.NEW_PING_PRICING_GREEN_FROM_DEFAULT, \
                    [f"Wrong value for 'New Ping Pricing Indicator Settings - Green From:': '{green_from}' instead of "
                     f"'{page.NEW_PING_PRICING_GREEN_FROM_DEFAULT}'", page.make_screenshot()]

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green To:' is restored to "
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

    with check:
        with allure.step(
                f"Checking that number of FirstLook Age Buckets is {len(page.FL_AGE_BUCKETS_DEFAULT_VALUES)}"):
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


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9870, MAX-11610")
@allure.title("C13540, C22607 Users can edit values of Max Market %, Min Market % and Min Gross "
              "and toggle 'Watch List' On and Off")
def test_edit_buckets_max_min_and_watchlist(driver):
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

    with allure.step("Switching to 'Inventory Settings' / 'Age Buckets' tab"):
        page = DealerProfileDealerPage(driver)
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)
        age_buckets_tab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_tab)
        time.sleep(TIMEOUT)

    with allure.step("Saving 'Min Market %', 'Max Market %', 'Min Gross' settings for the 1st Age Bucket"):
        min_market_before = page.get_attribute(page.AGE_BUCKET1_MIN_MARKET_VALUE, 'value')
        max_market_before = page.get_attribute(page.AGE_BUCKET1_MAX_MARKET_VALUE, 'value')
        min_gross_before = page.get_attribute(page.AGE_BUCKET1_MIN_GROSS_VALUE, 'value')
        with allure.step(f"Found values: 'Min Market %': '{min_market_before}', 'Max Market %': '{max_market_before}', "
                         f"'Min Gross': '{min_gross_before}'"):
            pass

    with allure.step("Clicking 'Edit' button, modifying 'Min Market %', 'Max Market %', 'Min Gross' settings"):
        edit_button = page.get_clickable_element(page.AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(1)

        with allure.step("Modifying 'Min Market %', increasing value"):
            page.modify_numeric_value(page.AGE_BUCKET1_MIN_MARKET_INPUT, page.AGE_BUCKET1_MIN_MARKET_MORE_BTN)
        with allure.step("Modifying 'Max Market %', increasing value"):
            page.modify_numeric_value(page.AGE_BUCKET1_MAX_MARKET_INPUT, page.AGE_BUCKET1_MAX_MARKET_MORE_BTN)
        with allure.step("Modifying 'Min Gross', increasing value"):
            page.modify_numeric_value(page.AGE_BUCKET1_MIN_GROSS_INPUT, page.AGE_BUCKET1_MIN_GROSS_MORE_BTN)

        with allure.step("Saving changes"):
            save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
            page.click(save_button)
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Checking that 'Min Market %', 'Max Market %', 'Min Gross' settings were modified correctly"):
        with check:
            with allure.step(f"Checking that 'Min Market %' was modified to '{int(min_market_before) + 1}'"):
                min_market_after = page.get_attribute(page.AGE_BUCKET1_MIN_MARKET_VALUE, 'value')
                assert int(min_market_after) == int(min_market_before) + 1, \
                    [f"Wrong value for 'Min Market %': '{int(min_market_after)}' instead of "
                     f"'{int(min_market_before) + 1}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Max Market %' was modified to '{int(max_market_before) + 1}'"):
                max_market_after = page.get_attribute(page.AGE_BUCKET1_MAX_MARKET_VALUE, 'value')
                assert int(max_market_after) == int(max_market_before) + 1, \
                    [f"Wrong value for 'Max Market %': '{int(max_market_after)}' instead of "
                     f"'{int(max_market_before) + 1}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Min Gross' was modified to '{int(min_gross_before) + 1}'"):
                min_gross_after = page.get_attribute(page.AGE_BUCKET1_MIN_GROSS_VALUE, 'value')
                assert int(min_gross_after) == int(min_gross_before) + 1, \
                    [f"Wrong value for 'Min Gross': '{int(min_gross_after)}' instead of "
                     f"'{int(min_gross_before) + 1}'", page.make_screenshot()]

    with allure.step("Scrolling down to 'FirstLook Age Buckets'"):
        fl_age_buckets = page.locate_element(page.FL_AGE_BUCKET_TABLE)
        page.scroll_to_element(fl_age_buckets)
        time.sleep(1)

    with allure.step("Saving 'Watch List' status"):
        watchlist_before = page.is_button_switched_on(page.FL_AGE_BUCKETS_WATCHLIST_BTN)
        with allure.step(f"The current 'Watchlist' status: '{watchlist_before}'"):
            pass

    with allure.step("Clicking 'Edit', clicking 'Watch List' button and saving changes"):
        edit_button = page.get_clickable_element(page.FL_AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(1)
        watch_list_btn = page.get_clickable_element(page.FL_AGE_BUCKETS_WATCHLIST_BTN)
        page.click(watch_list_btn)
        time.sleep(1)
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        page.click(save_button)
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that 'Watch List' was modified, not '{watchlist_before}' any more"):
            watchlist_after = page.is_button_switched_on(page.FL_AGE_BUCKETS_WATCHLIST_BTN)
            assert watchlist_after != watchlist_before, \
                [f"'Watch List' status wasn't modified. It is still'{watchlist_after}'", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-9870, MAX-11179")
@allure.title("C13650, C13605 Users can add up to 8 age buckets to a dealer and remove Age Buckets from dealer")
def test_max_number_of_buckets_and_delete_buckets(driver):
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

    with allure.step("Switching to 'Inventory Settings' / 'Age Buckets' tab"):
        page = DealerProfileDealerPage(driver)
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)
        age_buckets_tab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_tab)
        time.sleep(TIMEOUT)

    with allure.step(f"Clicking 'Edit' button and increasing the number of buckets to '{page.AGE_BUCKETS_MAX_NUMBER}'"):
        edit_button = page.get_clickable_element(page.AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(1)
        new_button = page.locate_element(page.AGE_BUCKETS_NEW_BTN)
        num_of_buckets = len(page.locate_all_elements(page.AGE_BUCKETS_ROW))
        while num_of_buckets < page.AGE_BUCKETS_MAX_NUMBER:
            page.click(new_button)
            time.sleep(1)
            num_of_buckets = len(page.locate_all_elements(page.AGE_BUCKETS_ROW))

    with allure.step(f"Trying to add one more Age Bucket above the '{page.AGE_BUCKETS_MAX_NUMBER}'"):
        page.click(new_button)

    with allure.step(f"Locating '{page.AGE_BUCKETS_MAX_NUMBER_NOTIFICATION}' notification"):
        page.locate_element(page.AGE_BUCKETS_MAX_NUMBER_NOTIFICATION)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that the number of Age Buckets is still equal to '{page.AGE_BUCKETS_MAX_NUMBER}'"):
            num_of_buckets = len(page.locate_all_elements(page.AGE_BUCKETS_ROW))
            assert num_of_buckets == page.AGE_BUCKETS_MAX_NUMBER, \
                [f"Wrong number of Age Buckets, '{num_of_buckets}' instead of '{page.AGE_BUCKETS_MAX_NUMBER}'",
                 page.make_screenshot()]

    with allure.step("Saving changes"):
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        page.click(save_button)
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with allure.step(f"Clicking 'Edit' button and removing a single Age Bucket. The current number "
                     f"is '{num_of_buckets}'"):
        edit_button = page.get_clickable_element(page.AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(1)
        age_bucket_one_checkbox = page.locate_element(page.AGE_BUCKETS_BUCKET_ONE_CHECKBOX)
        page.click(age_bucket_one_checkbox)
        time.sleep(1)
        delete_btn = page.get_clickable_element(page.AGE_BUCKETS_DELETE_BTN)
        page.click(delete_btn)
        time.sleep(1)
        ok_btn = page.get_clickable_element(page.AGE_BUCKETS_OK_CONFIRM_BTN)
        page.click(ok_btn)
        time.sleep(1)

    with allure.step("Saving changes"):
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        page.click(save_button)
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that the number of Age Buckets is now equal to '{num_of_buckets - 1}'"):
            new_num_of_buckets = len(page.locate_all_elements(page.AGE_BUCKETS_ROW))
            assert new_num_of_buckets == num_of_buckets - 1, \
                [f"Wrong number of Age Buckets, '{new_num_of_buckets}' instead of '{num_of_buckets - 1}'",
                 page.make_screenshot()]

    with allure.step(f"Clicking 'Edit' button and removing all Age Buckets. The current number is "
                     f"'{new_num_of_buckets}'"):
        edit_button = page.get_clickable_element(page.AGE_BUCKETS_EDIT_BTN)
        page.click(edit_button)
        time.sleep(1)
        all_buckets_checkbox = page.locate_element(page.AGE_BUCKETS_ALL_BUCKETS_CHECKBOX)
        page.click(all_buckets_checkbox)
        time.sleep(1)
        delete_btn = page.get_clickable_element(page.AGE_BUCKETS_DELETE_BTN)
        page.click(delete_btn)
        time.sleep(1)
        ok_btn = page.get_clickable_element(page.AGE_BUCKETS_OK_CONFIRM_BTN)
        page.click(ok_btn)
        time.sleep(1)

    with allure.step("Saving changes"):
        save_button = page.get_clickable_element(page.AGE_BUCKETS_SAVE_BTN)
        page.click(save_button)
        page.locate_element(page.SUCCESS_MESSAGE)
        time.sleep(TIMEOUT)

    with check:
        with allure.step(f"Checking that all Age Buckets were removed - '{page.AGE_BUCKETS_NO_BUCKETS}' is displayed"):
            page.locate_element(page.AGE_BUCKETS_NO_BUCKETS)


@pytest.mark.regression
@allure.feature("Dealer Profile: MAX-12207")
@allure.title("C26962, C26963 Lights/Risk sub-tab can be edited, Light Targets total must be 100%")
def test_edit_lights_risk_tab(driver):
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

    with allure.step("Switching to 'Inventory Settings' / 'Lights/Risk' tab"):
        page = DealerProfileDealerPage(driver)
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)
        lights_risk_tab = page.locate_element(page.LIGHTS_RISK_SUB_TAB)
        page.click(lights_risk_tab)
        time.sleep(TIMEOUT)

    with allure.step("Scrolling the page down"):
        element = page.locate_element(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN)
        page.scroll_to_element(element)
        time.sleep(1)

    with check:
        with allure.step(f"Checking that the 'Light Targets' total is 100%"):
            red_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_RED, "value"))
            yellow_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_YELLOW, "value"))
            green_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN, "value"))
            total_value = red_value + yellow_value + green_value
            assert total_value == 100, \
                [f"Wrong total for 'Light Targets', {total_value}% instead of 100%", page.make_screenshot()]

    with allure.step("Clicking 'Edit' and modifying 'Green %:' so that the total is not 100% anymore"):
        edit_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_RISK_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        green_input = page.locate_element(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN)
        page.click(green_input)
        green_increase_btn = page.get_clickable_element(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN_INCREASE_BTN)
        page.click(green_increase_btn)
        time.sleep(2)

    with check:
        with allure.step(f"Checking that the 'Light Targets' total is NOT 100% now"):
            red_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_RED, "value"))
            yellow_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_YELLOW, "value"))
            green_value = int(page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN, "value"))
            total_value = red_value + yellow_value + green_value
            assert total_value != 100, \
                [f"Wrong total for 'Light Targets' - 100%", page.make_screenshot()]

    with allure.step("Trying to save the changes and checking the form validation messages/alerts"):
        save_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_RISK_SAVE_BTN)
        page.click(save_button)
        page.locate_element(page.LIGHTS_RISK_FORM_VALIDATION_FAILED_ALERT)
        page.locate_element(page.LIGHTS_RISK_LIGHT_TARGETS_ALERT)
        time.sleep(2)

    with allure.step("Discarding changes"):
        cancel_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_RISK_CANCEL_BTN)
        page.click(cancel_button)
        time.sleep(TIMEOUT)

    with allure.step("Scrolling the page up"):
        element = page.locate_element(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN)
        page.scroll_to_element(element)
        time.sleep(1)

    with allure.step("Saving the current values in 'Lights/Risk'"):
        lights_risk_before = dict()
        with allure.step("Saving 'Target Days Supply:' setting"):
            lights_risk_before['target_days_supply'] = page.get_attribute(page.LIGHTS_RISK_TARGET_DAYS_SUPPLY, 'value')
        with allure.step("Saving 'Unit Cost Buckets - Creation Threshold:' setting"):
            lights_risk_before['unit_cost_buckets_creation_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD, 'value')
        with allure.step("Saving 'Unit Cost Buckets - Allocation Threshold:' setting"):
            lights_risk_before['unit_cost_buckets_allocation_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD, 'value')

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION_VALUE)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Market Performers - Display Threshold:' setting"):
            lights_risk_before['market_performers_display_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - In Stock Threshold:' setting"):
            lights_risk_before['market_performers_in_stock_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - Zip Code Threshold:' setting"):
            lights_risk_before['market_performers_zip_code_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - Units Threshold:' setting"):
            lights_risk_before['market_performers_units_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD, 'value')
        with allure.step("Saving 'Basis Periods - Lights Determination:' setting"):
            lights_risk_before['basis_periods_lights_determination'] = \
                page.get_text(page.LIGHTS_RISK_BASIS_PERIODS_LIGHTS_DETERMINATION_VALUE)
        with allure.step("Saving 'Basis Periods - Sales History:' setting"):
            lights_risk_before['basis_periods_sales_history'] = \
                page.get_text(page.LIGHTS_RISK_BASIS_PERIODS_SALES_HISTORY_VALUE)

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'CIA Basis Periods - Store Target Inventory:' setting"):
            lights_risk_before['cia_basis_periods_store_target_inventory'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_STORE_TARGET_INVENTORY_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Core Model Determination:' setting"):
            lights_risk_before['cia_basis_periods_core_model_determination'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Powerzone Target Inventory:' setting"):
            lights_risk_before['cia_basis_periods_powerzone_target_inventory'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_POWERZONE_TARGET_INVENTORY_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Core Model Year Allocation:' setting"):
            lights_risk_before['cia_basis_periods_core_model_year_allocation'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_YEAR_ALLOCATION_VALUE)

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Light Targets - Red %:' setting"):
            lights_risk_before['light_targets_red'] = page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_RED, 'value')
        with allure.step("Saving 'Light Targets - Yellow %:' setting"):
            lights_risk_before['light_targets_yellow'] = \
                page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_YELLOW, 'value')
        with allure.step("Saving 'Light Targets - Green %:' setting"):
            lights_risk_before['light_targets_green'] = \
                page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN, 'value')
        with allure.step("Saving 'Year Thresholds - Initial Time Period Year Offset:' setting"):
            lights_risk_before['year_thresholds_initial_time_period_year_offset'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET, 'value')
        with allure.step("Saving 'Year Thresholds - Secondary Time Period Year Offset:' setting"):
            lights_risk_before['year_thresholds_secondary_time_period_year_offset'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET, 'value')
        with allure.step("Saving 'Year Thresholds - Roll Over Month:' setting"):
            lights_risk_before['year_thresholds_roll_over_month'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # Weeks:' setting"):
            lights_risk_before['risk_level_thresholds_num_weeks'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # Deals:' setting"):
            lights_risk_before['risk_level_thresholds_num_deals'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # of Contributors:' setting"):
            lights_risk_before['risk_level_thresholds_num_of_contributors'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS, 'value')
        with allure.step("Saving 'Red Light Thresholds - No Sale >:' setting"):
            lights_risk_before['red_light_thresholds_no_sale_more'] = \
                page.get_attribute(page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE, 'value')
        with allure.step("Saving 'Red Light Thresholds - Gross Profit <=:' setting"):
            lights_risk_before['red_light_thresholds_gross_profit_less'] = \
                page.get_attribute(page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS, 'value')

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Green Light Thresholds - No Sale <:' setting"):
            lights_risk_before['green_light_thresholds_no_sale_less'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS, 'value')
        with allure.step("Saving 'Green Light Thresholds - Gross Profit >=:' setting"):
            lights_risk_before['green_light_thresholds_gross_profit_more'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE, 'value')
        with allure.step("Saving 'Green Light Thresholds - Margin >=:' setting"):
            lights_risk_before['green_light_thresholds_margin_more'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE, 'value')
        with allure.step("Saving 'Green Light Thresholds - Days % <=:' setting"):
            lights_risk_before['green_light_thresholds_days_percentage_less'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS, 'value')
        with allure.step("Saving 'Age Band Targets - Year >=:' setting"):
            lights_risk_before['age_band_targets_year_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE, 'value')
        with allure.step("Saving 'Age Band Targets - Overall >=:' setting"):
            lights_risk_before['age_band_targets_overall_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE, 'value')
        with allure.step("Saving 'Age Band Targets - Red Light >=:' setting"):
            lights_risk_before['age_band_targets_red_light_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE, 'value')

    with allure.step("Clicking 'Edit' and modifying all settings in 'Dealer C I A Preference' section"):
        edit_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_CIA_PREFERENCE_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        with allure.step("Modifying 'Target Days Supply:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_TARGET_DAYS_SUPPLY,
                                      action_button_locator=page.LIGHTS_RISK_TARGET_DAYS_SUPPLY_INCREASE_BTN)
        with allure.step("Modifying 'Unit Cost Buckets - Creation Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Unit Cost Buckets - Allocation Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Market Performers - Display Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Market Performers - In Stock Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Market Performers - Zip Code Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Market Performers - Units Threshold:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD,
                                      action_button_locator=
                                      page.LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD_INCREASE_BTN)
        with allure.step("Modifying 'Basis Periods - Lights Determination:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.LIGHTS_RISK_BASIS_PERIODS_LIGHTS_DETERMINATION,
                                                   default_value=lights_risk_before[
                                                       'basis_periods_lights_determination'])
        with allure.step("Modifying 'Basis Periods - Sales History:' setting"):
            page.select_random_value_from_dropdown(input_locator=page.LIGHTS_RISK_BASIS_PERIODS_SALES_HISTORY,
                                                   default_value=lights_risk_before['basis_periods_sales_history'])
        with allure.step("Modifying 'CIA Basis Periods - Store Target Inventory:' setting"):
            page.select_random_value_from_dropdown(
                input_locator=page.LIGHTS_RISK_CIA_BASIS_PERIODS_STORE_TARGET_INVENTORY,
                default_value=lights_risk_before['cia_basis_periods_store_target_inventory'])
        with allure.step("Modifying 'CIA Basis Periods - Core Model Determination:' setting"):
            page.select_random_value_from_dropdown(
                input_locator=page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION,
                default_value=lights_risk_before['cia_basis_periods_core_model_determination'])
        with allure.step("Modifying 'CIA Basis Periods - Powerzone Target Inventory:' setting"):
            page.select_random_value_from_dropdown(
                input_locator=page.LIGHTS_RISK_CIA_BASIS_PERIODS_POWERZONE_TARGET_INVENTORY,
                default_value=lights_risk_before['cia_basis_periods_powerzone_target_inventory'])
        with allure.step("Modifying 'CIA Basis Periods - Core Model Year Allocation:' setting"):
            page.select_random_value_from_dropdown(
                input_locator=page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_YEAR_ALLOCATION,
                default_value=lights_risk_before['cia_basis_periods_core_model_year_allocation'])

        with allure.step("Saving changes in 'Dealer C I A Preference' section"):
            save_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_CIA_PREFERENCE_SAVE_BTN)
            page.click(save_button)
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Clicking 'Edit' and modifying all settings in 'Dealer Risk' section"):
        edit_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_RISK_EDIT_BTN)
        page.click(edit_button)
        time.sleep(TIMEOUT)
        with allure.step("Modifying 'Light Targets - Red %:' setting"):
            page.paste_text(page.LIGHTS_RISK_LIGHT_TARGETS_RED, str(int(lights_risk_before['light_targets_red']) + 1))
            time.sleep(2)
        with allure.step("Modifying 'Light Targets - Yellow %:' setting"):
            page.paste_text(page.LIGHTS_RISK_LIGHT_TARGETS_YELLOW,
                            str(int(lights_risk_before['light_targets_yellow']) + 1))
            time.sleep(2)
        with allure.step("Modifying 'Light Targets - Green %:' setting"):
            page.paste_text(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN,
                            str(int(lights_risk_before['light_targets_green']) - 2))
            time.sleep(2)
        with allure.step("Modifying 'Year Thresholds - Initial Time Period Year Offset:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET,
                                      action_button_locator=
                                      page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET_INCREASE_BTN)
        with allure.step("Modifying 'Year Thresholds - Secondary Time Period Year Offset:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET,
                                      action_button_locator=page.
                                      LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET_INCREASE_BTN)
        with allure.step("Modifying 'Year Thresholds - Roll Over Month:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH,
                                      action_button_locator=page.
                                      LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH_INCREASE_BTN)
        with allure.step("Modifying 'Risk Level Thresholds - # Weeks:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS_INCREASE_BTN)
        with allure.step("Modifying 'Risk Level Thresholds - # Deals' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS_INCREASE_BTN)
        with allure.step("Modifying 'Risk Level Thresholds - # of Contributors' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS_INCREASE_BTN)
        with allure.step("Modifying 'Red Light Thresholds - No Sale >:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE_INCREASE_BTN)
        with allure.step("Modifying 'Red Light Thresholds - Gross Profit <=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS_INCREASE_BTN)
        with allure.step("Modifying 'Green Light Thresholds - No Sale <:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS_INCREASE_BTN)
        with allure.step("Modifying 'Green Light Thresholds - Gross Profit >=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE_INCREASE_BTN)
        with allure.step("Modifying 'Green Light Thresholds - Margin >=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE_INCREASE_BTN)
        with allure.step("Modifying 'Green Light Thresholds - Days % <=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS,
                                      action_button_locator=page.
                                      LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS_INCREASE_BTN)
        with allure.step("Modifying 'Age Band Targets - Year >=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE_INCREASE_BTN)
        with allure.step("Modifying 'Age Band Targets - Overall >=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE_INCREASE_BTN)
        with allure.step("Modifying 'Age Band Targets - Red Light >=:' setting"):
            page.modify_numeric_value(input_locator=page.LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE,
                                      action_button_locator=page.
                                      LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE_INCREASE_BTN)

        with allure.step("Saving changes in 'Dealer Risk' section"):
            save_button = page.get_clickable_element(page.LIGHTS_RISK_DEALER_RISK_SAVE_BTN)
            page.click(save_button)
            page.locate_element(page.SUCCESS_MESSAGE)
            time.sleep(TIMEOUT)

    with allure.step("Saving new values in 'Lights/Risk'"):
        lights_risk_after = dict()
        with allure.step("Saving 'Target Days Supply:' setting"):
            lights_risk_after['target_days_supply'] = page.get_attribute(page.LIGHTS_RISK_TARGET_DAYS_SUPPLY, 'value')
        with allure.step("Saving 'Unit Cost Buckets - Creation Threshold:' setting"):
            lights_risk_after['unit_cost_buckets_creation_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD, 'value')
        with allure.step("Saving 'Unit Cost Buckets - Allocation Threshold:' setting"):
            lights_risk_after['unit_cost_buckets_allocation_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD, 'value')

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION_VALUE)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Market Performers - Display Threshold:' setting"):
            lights_risk_after['market_performers_display_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - In Stock Threshold:' setting"):
            lights_risk_after['market_performers_in_stock_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - Zip Code Threshold:' setting"):
            lights_risk_after['market_performers_zip_code_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD, 'value')
        with allure.step("Saving 'Market Performers - Units Threshold:' setting"):
            lights_risk_after['market_performers_units_threshold'] = \
                page.get_attribute(page.LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD, 'value')
        with allure.step("Saving 'Basis Periods - Lights Determination:' setting"):
            lights_risk_after['basis_periods_lights_determination'] = \
                page.get_text(page.LIGHTS_RISK_BASIS_PERIODS_LIGHTS_DETERMINATION_VALUE)
        with allure.step("Saving 'Basis Periods - Sales History:' setting"):
            lights_risk_after['basis_periods_sales_history'] = \
                page.get_text(page.LIGHTS_RISK_BASIS_PERIODS_SALES_HISTORY_VALUE)

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'CIA Basis Periods - Store Target Inventory:' setting"):
            lights_risk_after['cia_basis_periods_store_target_inventory'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_STORE_TARGET_INVENTORY_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Core Model Determination:' setting"):
            lights_risk_after['cia_basis_periods_core_model_determination'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Powerzone Target Inventory:' setting"):
            lights_risk_after['cia_basis_periods_powerzone_target_inventory'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_POWERZONE_TARGET_INVENTORY_VALUE)
        with allure.step("Saving 'CIA Basis Periods - Core Model Year Allocation:' setting"):
            lights_risk_after['cia_basis_periods_core_model_year_allocation'] = \
                page.get_text(page.LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_YEAR_ALLOCATION_VALUE)

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Light Targets - Red %:' setting"):
            lights_risk_after['light_targets_red'] = page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_RED, 'value')
        with allure.step("Saving 'Light Targets - Yellow %:' setting"):
            lights_risk_after['light_targets_yellow'] = \
                page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_YELLOW, 'value')
        with allure.step("Saving 'Light Targets - Green %:' setting"):
            lights_risk_after['light_targets_green'] = \
                page.get_attribute(page.LIGHTS_RISK_LIGHT_TARGETS_GREEN, 'value')
        with allure.step("Saving 'Year Thresholds - Initial Time Period Year Offset:' setting"):
            lights_risk_after['year_thresholds_initial_time_period_year_offset'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET, 'value')
        with allure.step("Saving 'Year Thresholds - Secondary Time Period Year Offset:' setting"):
            lights_risk_after['year_thresholds_secondary_time_period_year_offset'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET, 'value')
        with allure.step("Saving 'Year Thresholds - Roll Over Month:' setting"):
            lights_risk_after['year_thresholds_roll_over_month'] = \
                page.get_attribute(page.LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # Weeks:' setting"):
            lights_risk_after['risk_level_thresholds_num_weeks'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # Deals:' setting"):
            lights_risk_after['risk_level_thresholds_num_deals'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS, 'value')
        with allure.step("Saving 'Risk Level Thresholds - # of Contributors:' setting"):
            lights_risk_after['risk_level_thresholds_num_of_contributors'] = \
                page.get_attribute(page.LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS, 'value')
        with allure.step("Saving 'Red Light Thresholds - No Sale >:' setting"):
            lights_risk_after['red_light_thresholds_no_sale_more'] = \
                page.get_attribute(page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE, 'value')
        with allure.step("Saving 'Red Light Thresholds - Gross Profit <=:' setting"):
            lights_risk_after['red_light_thresholds_gross_profit_less'] = \
                page.get_attribute(page.LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS, 'value')

        with allure.step("Scrolling the page down"):
            element = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(element)
            time.sleep(1)

        with allure.step("Saving 'Green Light Thresholds - No Sale <:' setting"):
            lights_risk_after['green_light_thresholds_no_sale_less'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS, 'value')
        with allure.step("Saving 'Green Light Thresholds - Gross Profit >=:' setting"):
            lights_risk_after['green_light_thresholds_gross_profit_more'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE, 'value')
        with allure.step("Saving 'Green Light Thresholds - Margin >=:' setting"):
            lights_risk_after['green_light_thresholds_margin_more'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE, 'value')
        with allure.step("Saving 'Green Light Thresholds - Days % <=:' setting"):
            lights_risk_after['green_light_thresholds_days_percentage_less'] = \
                page.get_attribute(page.LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS, 'value')
        with allure.step("Saving 'Age Band Targets - Year >=:' setting"):
            lights_risk_after['age_band_targets_year_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE, 'value')
        with allure.step("Saving 'Age Band Targets - Overall >=:' setting"):
            lights_risk_after['age_band_targets_overall_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE, 'value')
        with allure.step("Saving 'Age Band Targets - Red Light >=:' setting"):
            lights_risk_after['age_band_targets_red_light_more'] = \
                page.get_attribute(page.LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE, 'value')

    with allure.step("Checking that settings in 'Lights/Risk' were modified"):
        for key in lights_risk_before.keys():
            with check:
                with allure.step(f"Checking that '{key}' setting was modified"):
                    with allure.step(f"Current '{key}' value is: '{lights_risk_after[key]}', was: "
                                     f"'{lights_risk_before[key]}'"):
                        pass
                    assert lights_risk_after[key] != lights_risk_before[key], \
                        [f"'{key}' setting was not modified", page.make_screenshot()]

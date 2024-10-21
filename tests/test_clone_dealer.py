from page_objects.LoginPage import LoginPage
from page_objects.DealerProfilePage import DealerProfilePage
from page_objects.DealerProfileMaxSettingsPage import DealerProfileMaxSettingsPage
from page_objects.DealerProfileDealerPage import DealerProfileDealerPage
from page_objects.DealerListPage import DealerListPage
from page_objects.DealerProfileSettingsPage import DealerProfileSettingsPage
from page_objects.DealerProfilePricingPage import DealerProfilePricingPage
from page_objects.CloneDealerPage import CloneDealerPage
import time
import pytest
from pytest_check import check
import allure

TIMEOUT = 6


@pytest.mark.regression
@allure.feature("Clone Dealer: MAX-9170, MAX-13479, MAX-13480, MAX-13477, MAX-14027, MAX-13965, MAX-16543")
@allure.title("C13723, C33773, C38176, C38177, C39550, C53114, C53111 Positive case: all required fields have valid "
              "values, all non-mandatory fields empty (check cloned settings and defaults)")
def test_clone_dealer_default_settings(driver):
    with allure.step("Logging to PitStop as Administrator and opening dealer list page"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)

        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the original dealer {page.WC_TEST_DEALER} first to save its settings"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step("Saving settings of the original dealer - 'Setting' tab"):
        page = DealerProfileDealerPage(driver)
        original_dealer = dict()
        with allure.step("Saving Franchises"):
            franchises = []
            franchises_list = page.locate_all_elements(page.FRANCHISES)
            for item in franchises_list:
                franchises.append(item.text)
            original_dealer['setting_franchises'] = franchises

    with allure.step("Saving settings of the original dealer - 'General Settings' - 'Dealer General' sub-tab"):
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(3)
        dealer_general = page.locate_element(page.GEN_SET_DEALER_GENERAL)
        page.click(dealer_general)
        time.sleep(TIMEOUT)
        # Toggles
        with allure.step("Saving 'Show Recall:' setting"):
            original_dealer['gen_set_show_recall'] = page.is_button_switched_on(page.SHOW_RECALL_BTN)
        with allure.step("Saving 'Recall Report:' setting"):
            original_dealer['gen_set_recall_report'] = page.is_button_switched_on(page.RECALL_REPORT_BTN)
        with allure.step("Saving 'Show Lot Location Status:' setting"):
            original_dealer['gen_set_lot_location'] = page.is_button_switched_on(page.SHOW_LOT_LOCATION_STATUS_BTN)
        with allure.step("Saving 'Show Inactive Appraisals:' setting"):
            original_dealer['gen_set_inactive_appraisal'] = page.is_button_switched_on(
                page.SHOW_INACTIVE_APPRAISALS_BTN)
        with allure.step("Saving 'Require Name On Appraisals:' setting"):
            original_dealer['gen_set_require_name'] = page.is_button_switched_on(page.REQUIRE_NAME_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Est Recon Cost On Appraisals:' setting"):
            original_dealer['gen_set_est_recon_cost'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Require Recon Notes On Appraisals:' setting"):
            original_dealer['gen_set_recon_notes'] = page.is_button_switched_on(
                page.REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN)
        with allure.step("Saving 'Show Casey And Casey:' setting"):
            original_dealer['gen_set_show_casey'] = page.is_button_switched_on(
                page.SHOW_CASEY_AND_CASEY_BTN)
        with allure.step("Saving 'Show Appraisal Form Offer Group:' setting"):
            original_dealer['gen_set_show_appraisal_form'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN)
        with allure.step("Saving 'Show Appraisal Value Group:' setting"):
            original_dealer['gen_set_show_appraisal_value_group'] = page.is_button_switched_on(
                page.SHOW_APPRAISAL_VALUE_GROUP_BTN)
        with allure.step("Saving 'Use Lot Price:' setting"):
            original_dealer['gen_set_use_lot_price'] = page.is_button_switched_on(
                page.USE_LOT_PRICE_BTN)
        with allure.step("Saving 'Exclude Wholesale From Days Supply:' setting"):
            original_dealer['gen_set_exclude_wholesale'] = page.is_button_switched_on(
                page.EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN)
        with allure.step("Saving 'Atc Enabled:' setting"):
            original_dealer['gen_set_atc_enabled'] = page.is_button_switched_on(
                page.ATC_ENABLED_BTN)
        with allure.step("Saving 'Gmac Enabled:' setting"):
            original_dealer['gen_set_gmac_enabled'] = page.is_button_switched_on(
                page.GMAC_ENABLED_BTN)
        with allure.step("Saving 'Tfs Enabled:' setting"):
            original_dealer['gen_set_tfs_enabled'] = page.is_button_switched_on(
                page.TFS_ENABLED_BTN)
        with allure.step("Saving 'Visible To Dealer Group:' setting"):
            original_dealer['gen_set_visible_to_dealer_group'] = page.is_button_switched_on(
                page.VISIBLE_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'Enable Auto Match:' setting"):
            original_dealer['gen_set_enable_auto_match'] = page.is_button_switched_on(
                page.ENABLE_AUTO_MATCH_BTN)
        with allure.step("Saving 'Display Unit Cost To Dealer Group:' setting"):
            original_dealer['gen_set_display_unit_cost'] = page.is_button_switched_on(
                page.DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN)
        with allure.step("Saving 'In-Transit Inventory:' setting"):
            original_dealer['gen_set_in_transit_inventory'] = page.is_button_switched_on(
                page.IN_TRANSIT_INVENTORY_BTN)
        with allure.step("Saving 'Display Recalls Lookup By VIN Link on Appraisals:' setting"):
            original_dealer['gen_set_display_recalls_lookup'] = page.is_button_switched_on(
                page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
        # Inputs & dropdowns
        with allure.step("Saving 'Recall Provider:' setting"):
            original_dealer['gen_set_recall_provider'] = page.get_text(page.RECALL_PROVIDER)
        with allure.step("Saving 'Appraisal Value Requirement on Trade Analyzer:' setting"):
            original_dealer['gen_set_appraisal_value_requirement'] = page.get_text(page.APPRAISAL_VALUE_REQUIREMENT)
        with allure.step("Saving 'Inventory Days Back Threshold:' setting"):
            original_dealer['gen_set_inventory_days_back_threshold'] = \
                page.get_attribute(page.INVENTORY_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Unwind Days Threshold:' setting"):
            original_dealer['gen_set_unwind_days_threshold'] = page.get_attribute(page.UNWIND_DAYS_THRESHOLD, 'value')
        with allure.step("Saving 'Search Appraisal Days Back Threshold:' setting"):
            original_dealer['gen_set_search_appraisal_days'] = \
                page.get_attribute(page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD, 'value')
        with allure.step("Saving 'Appraisal Look Back Period:' setting"):
            original_dealer['gen_set_appraisal_look_back'] = \
                page.get_attribute(page.APPRAISAL_LOOK_BACK_PERIOD, 'value')
        with allure.step("Saving 'Appraisal Look Forward Period:' setting"):
            original_dealer['gen_set_appraisal_look_forward'] = \
                page.get_attribute(page.APPRAISAL_LOOK_FORWARD_PERIOD, 'value')
        with allure.step("Saving 'Showroom Days Filter:' setting"):
            original_dealer['gen_set_showroom_days_filter'] = page.get_attribute(page.SHOWROOM_DAYS_FILTER, 'value')
        with allure.step("Saving 'Trade Manager Days Filter:' setting"):
            original_dealer['gen_set_trade_manager_days'] = page.get_text(page.TRADE_MANAGER_DAYS_FILTER)
        with allure.step("Saving 'Run Day Of Week:' setting"):
            original_dealer['gen_set_run_day_of_week'] = page.get_text(page.RUN_DAY_OF_WEEK)
        with allure.step("Saving 'Program Type:' setting"):
            original_dealer['gen_set_program_type'] = page.get_text(page.PROGRAM_TYPE)
        with allure.step("Saving 'Pack Amount:' setting"):
            original_dealer['gen_set_pack_amount'] = page.get_attribute(page.PACK_AMOUNT, 'value')
        with allure.step("Saving 'Group Appraisal Search Weeks:' setting"):
            original_dealer['gen_set_group_appraisal_search_weeks'] = \
                page.get_attribute(page.GROUP_APPRAISAL_SEARCH_WEEKS, 'value')
        with allure.step("Saving 'Twix Url:' setting"):
            original_dealer['gen_set_twix_url'] = page.get_attribute(page.TWIX_URL, 'value')
        with allure.step("Saving 'Auction Area:' setting"):
            original_dealer['gen_set_auction_area'] = page.get_text(page.AUCTION_AREA)
        with allure.step("Saving 'Live Auction Distance From Dealer:' setting"):
            original_dealer['gen_set_live_auction_distance'] = page.get_text(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
        with allure.step("Saving 'Dashboard Display:' setting"):
            original_dealer['gen_set_dashboard_display'] = page.get_text(page.DASHBOARD_DISPLAY)
        with allure.step("Saving 'Forecaster Weeks:' setting"):
            original_dealer['gen_set_forecaster_weeks'] = page.get_text(page.FORECASTER_WEEKS)
        with allure.step("Saving 'PerfAnalyzer Weeks:' setting"):
            original_dealer['gen_set_perfanalyzer_weeks'] = page.get_text(page.PERFANALYZER_WEEKS)

    with allure.step("Saving settings of the original dealer - 'General Settings' - 'Scorecard - "
                     "Units Sold Thresholds' sub-tab"):
        scorecard = page.locate_element(page.GEN_SET_SCORECARD)
        page.click(scorecard)
        time.sleep(TIMEOUT)
        with allure.step("Saving 'Threshold for 4 Weeks:'"):
            original_dealer['scorecard_4_weeks'] = page.get_attribute(page.THRESHOLD_4_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 8 Weeks:'"):
            original_dealer['scorecard_8_weeks'] = page.get_attribute(page.THRESHOLD_8_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 12 Weeks:'"):
            original_dealer['scorecard_12_weeks'] = page.get_attribute(page.THRESHOLD_12_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 13 Weeks:'"):
            original_dealer['scorecard_13_weeks'] = page.get_attribute(page.THRESHOLD_13_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 26 Weeks:'"):
            original_dealer['scorecard_26_weeks'] = page.get_attribute(page.THRESHOLD_26_WEEKS_INPUT, 'value')
        with allure.step("Saving 'Threshold for 52 Weeks:'"):
            original_dealer['scorecard_52_weeks'] = page.get_attribute(page.THRESHOLD_52_WEEKS_INPUT, 'value')

    with allure.step("Saving settings of the original dealer - 'Inventory Settings' tab"):
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)
        with allure.step("Saving 'Default Search Radius:' setting"):
            original_dealer['inv_set_default_search_radius'] = page.get_text(page.DEFAULT_SEARCH_RADIUS)
        with allure.step("Saving 'Default Stock Type:' setting"):
            original_dealer['inv_set_default_stock_type'] = page.get_text(page.DEFAULT_STOCK_TYPE)
        with allure.step("Saving 'Supress Seller Name:' setting"):
            original_dealer['inv_set_supress_seller_name'] = page.is_button_switched_on(page.SUPRESS_SELLER_NAME_BTN)
        with allure.step("Saving 'Exclude No Price From Calc:' setting"):
            original_dealer['inv_set_exclude_no_price'] = page.is_button_switched_on(
                page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
        with allure.step("Saving 'Enable New Car Pricing:' setting"):
            original_dealer['inv_set_enable_new_car_pricing'] = \
                page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
        with allure.step("Saving 'Enable Lithia New Car View:' setting"):
            original_dealer['inv_set_enable_lithia_new_car_view'] = \
                page.is_button_switched_on(page.ENABLE_LITHIA_NEW_CAR_VIEW_BTN)
        with allure.step("Saving 'Enable Chrome Incentives:' setting"):
            original_dealer['inv_set_enable_chrome_incentives'] = \
                page.is_button_switched_on(page.ENABLE_CHROME_INCENTIVES_BTN)
        with allure.step("Saving 'Is New Ping:' setting"):
            original_dealer['inv_set_is_new_ping'] = page.is_button_switched_on(page.IS_NEW_PING_BTN)
        with allure.step("Saving 'Enable New Ping On FL and MAX:' setting"):
            original_dealer['inv_set_new_ping_on_fl_and_max'] = \
                page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
        with allure.step("Saving 'Market Listing VDP Link:' setting"):
            original_dealer['inv_set_market_listing_vdp_link'] = \
                page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN)

        with allure.step("Scrolling down to 'New Ping Pricing Indicator Settings'"):
            new_ping_pricing_indicator_settings_bottom = page.locate_element(page.NEW_PING_PRICING_GREEN_TO)
            page.scroll_to_element(new_ping_pricing_indicator_settings_bottom)
            time.sleep(2)

        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Above' setting"):
            original_dealer['new_ping_pricing_indicator_red_above'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Red Below' setting"):
            original_dealer['new_ping_pricing_indicator_red_below'] = \
                page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow From' setting"):
            original_dealer['new_ping_pricing_indicator_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Yellow To' setting"):
            original_dealer['new_ping_pricing_indicator_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow From' setting"):
            original_dealer['new_ping_pricing_indicator_and_yellow_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - & Yellow To' setting"):
            original_dealer['new_ping_pricing_indicator_and_yellow_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green From' setting"):
            original_dealer['new_ping_pricing_indicator_green_from'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
        with allure.step("Saving 'New Ping Pricing Indicator Settings - Green To' setting"):
            original_dealer['new_ping_pricing_indicator_green_to'] = \
                page.get_attribute(page.NEW_PING_PRICING_GREEN_TO, 'value')

    with allure.step("Switching to 'Age Buckets' sub-tab"):
        age_buckets_subtab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_subtab)
        time.sleep(TIMEOUT)
        page.locate_element(page.BUCKET_ELEMENT)
        with allure.step("Saving the number of Age Buckets"):
            age_buckets = page.locate_all_elements(page.AGE_BUCKETS_ROW)
            original_dealer['age_buckets_num'] = len(age_buckets)

        with allure.step("Saving Age Bucket sizes"):
            age_bucket_sizes = []
            for i in range(1, len(age_buckets) + 1):
                age_bucket_sizes.append(page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, i, 2))
            original_dealer['age_buckets_values'] = age_bucket_sizes

        # FirstLook Age Buckets
        with allure.step("Saving FirstLook Age Bucket sizes"):
            page_bottom = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(page_bottom)
            time.sleep(2)
            fl_age_buckets = page.locate_all_elements(page.FL_AGE_BUCKETS_ROW)
            fl_age_bucket_sizes = []
            for i in range(1, len(fl_age_buckets) + 1):
                fl_age_bucket_sizes.append(page.get_table_cell_value_from_input(page.FL_AGE_BUCKET_TABLE, i, 2))
            original_dealer['firstlook_age_buckets_values'] = fl_age_bucket_sizes

    with allure.step("Saving settings of the original dealer - 'Settings' tab - 'Upgrades'"):
        settings_tab = page.locate_element(page.SETTINGS_TAB)
        page.click(settings_tab)
        page = DealerProfileSettingsPage(driver)
        time.sleep(8)

        all_upgrades = page.get_all_upgrades_names()

        for i in range(len(all_upgrades)):
            key_name, locator = page.get_upgrade_key_name_and_locator(all_upgrades[i])
            with allure.step(f"Saving '{all_upgrades[i]}' setting"):
                original_dealer[key_name] = page.is_button_switched_on(locator)
        print(original_dealer)

    with allure.step("Switching to 'MAX Settings' / 'Ad Settings' tab"):
        max_settings_tab = page.locate_element(page.MAX_SETTINGS_TAB)
        page.click(max_settings_tab)
        time.sleep(TIMEOUT)
        page = DealerProfileMaxSettingsPage(driver)
        ad_settings_sub_tab = page.locate_element(page.AD_SETTINGS_SUB_TAB)
        page.click(ad_settings_sub_tab)
        time.sleep(TIMEOUT)
        with allure.step("Saving 'Which book value should be used in descriptions?' setting"):
            original_dealer['max_set_book_value_in_description'] = page.get_text(page.WHICH_BOOK_VALUE_SHOULD_BE_USED)

    with allure.step("Cloning the dealer"):
        page = CloneDealerPage(driver)
        new_dealer = page.generate_new_dealer_data()
        page.clone_dealer(name=new_dealer['name'],
                          short_name=new_dealer['name'],
                          website=new_dealer['website'],
                          google_place_id=new_dealer['google_place_id'],
                          address=new_dealer['address'],
                          zip_code=new_dealer['zip_code'],
                          calc_lat_long_by='zip_code')
        time.sleep(TIMEOUT)
        open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
        page.click(open_new_dealer_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)
        page = DealerProfilePage(driver)

    with check:
        with allure.step(f"Asserting that the new dealer name {new_dealer['name']} is in the dealer profile header"):
            assert new_dealer['name'] in page.locate_element(page.PROFILE_HEADER).text, \
                f"Dealer name '{new_dealer['name']}' is not in the header"

    with allure.step("Switching to 'Setting' tab"):
        page = DealerProfileDealerPage(driver)
        with check:
            with allure.step(f"Checking that Franchises are cloned: {original_dealer['setting_franchises']}"):
                franchises = []
                franchises_list = page.locate_all_elements(page.FRANCHISES)
                for item in franchises_list:
                    franchises.append(item.text)
                assert original_dealer['setting_franchises'] == franchises, [
                    f"Wrong Franchises: {franchises} instead of {original_dealer['setting_franchises']}",
                    page.make_screenshot()]

    with allure.step("Switching to 'General Settings' - 'Dealer General' sub-tab"):
        general_settings_tab = page.locate_element(page.GENERAL_SETTINGS_TAB)
        page.click(general_settings_tab)
        time.sleep(3)
        dealer_general = page.locate_element(page.GEN_SET_DEALER_GENERAL)
        page.click(dealer_general)
        time.sleep(TIMEOUT)

        element_to_scroll = page.locate_element(page.ATC_ENABLED_BTN)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        # Toggles
        with check:
            with allure.step(f"Checking that 'Show Recall:' is cloned: {original_dealer['gen_set_show_recall']}"):
                show_recall = page.is_button_switched_on(page.SHOW_RECALL_BTN)
                assert original_dealer['gen_set_show_recall'] == show_recall, [
                    f"Wrong 'Show Recall' value: {show_recall} instead of {original_dealer['gen_set_show_recall']}",
                    page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Lot Location Status:' "
                             f"is cloned: {original_dealer['gen_set_lot_location']}"):
                lot_location = page.is_button_switched_on(page.SHOW_LOT_LOCATION_STATUS_BTN)
                assert original_dealer['gen_set_lot_location'] == lot_location, [
                    f"Wrong 'Show Lot Location Status:' value: {lot_location} instead of "
                    f"{original_dealer['gen_set_lot_location']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Inactive Appraisals:' "
                             f"is cloned: {original_dealer['gen_set_inactive_appraisal']}"):
                inactive_appraisals = page.is_button_switched_on(page.SHOW_INACTIVE_APPRAISALS_BTN)
                assert original_dealer['gen_set_inactive_appraisal'] == inactive_appraisals, [
                    f"Wrong 'Show Inactive Appraisals:' value: {inactive_appraisals} instead of "
                    f"{original_dealer['gen_set_inactive_appraisal']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Require Name On Appraisals:' "
                             f"is cloned: {original_dealer['gen_set_require_name']}"):
                require_name = page.is_button_switched_on(page.REQUIRE_NAME_ON_APPRAISALS_BTN)
                assert original_dealer['gen_set_require_name'] == require_name, [
                    f"Wrong 'Require Name On Appraisals:' value: {require_name} instead of "
                    f"{original_dealer['gen_set_require_name']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Require Est Recon Cost On Appraisals:' "
                             f"is cloned: {original_dealer['gen_set_est_recon_cost']}"):
                est_recon_cost = page.is_button_switched_on(page.REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN)
                assert original_dealer['gen_set_est_recon_cost'] == est_recon_cost, [
                    f"Wrong 'Require Est Recon Cost On Appraisals:' value: {est_recon_cost} instead of "
                    f"{original_dealer['gen_set_est_recon_cost']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Require Recon Notes On Appraisals:' "
                             f"is cloned: {original_dealer['gen_set_recon_notes']}"):
                recon_notes = page.is_button_switched_on(page.REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN)
                assert original_dealer['gen_set_recon_notes'] == recon_notes, [
                    f"Wrong 'Require Recon Notes On Appraisals:' value: {recon_notes} instead of "
                    f"{original_dealer['gen_set_recon_notes']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Casey And Casey:' "
                             f"is cloned: {original_dealer['gen_set_show_casey']}"):
                show_casey = page.is_button_switched_on(page.SHOW_CASEY_AND_CASEY_BTN)
                assert original_dealer['gen_set_show_casey'] == show_casey, [
                    f"Wrong 'Show Casey And Casey:' value: {show_casey} instead of "
                    f"{original_dealer['gen_set_show_casey']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Appraisal Form Offer Group:' "
                             f"is cloned: {original_dealer['gen_set_show_appraisal_form']}"):
                show_appraisal_form = page.is_button_switched_on(page.SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN)
                assert original_dealer['gen_set_show_appraisal_form'] == show_appraisal_form, [
                    f"Wrong 'Show Appraisal Form Offer Group:' value: {show_appraisal_form} instead of "
                    f"{original_dealer['gen_set_show_appraisal_form']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Show Appraisal Value Group:' "
                             f"is cloned: {original_dealer['gen_set_show_appraisal_value_group']}"):
                show_appraisal_value_group = page.is_button_switched_on(page.SHOW_APPRAISAL_VALUE_GROUP_BTN)
                assert original_dealer['gen_set_show_appraisal_value_group'] == show_appraisal_value_group, [
                    f"Wrong 'Show Appraisal Value Group:' value: {show_appraisal_value_group} instead of "
                    f"{original_dealer['gen_set_show_appraisal_value_group']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Use Lot Price:' is cloned: {original_dealer['gen_set_use_lot_price']}"):
                use_lot_price = page.is_button_switched_on(page.USE_LOT_PRICE_BTN)
                assert original_dealer['gen_set_use_lot_price'] == use_lot_price, [
                    f"Wrong 'Use Lot Price:' value: {use_lot_price} instead of "
                    f"{original_dealer['gen_set_use_lot_price']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Exclude Wholesale From Days Supply:' "
                             f"is cloned: {original_dealer['gen_set_exclude_wholesale']}"):
                exclude_wholesale = page.is_button_switched_on(page.EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN)
                assert original_dealer['gen_set_exclude_wholesale'] == exclude_wholesale, [
                    f"Wrong 'Exclude Wholesale From Days Supply:' value: {exclude_wholesale} instead of "
                    f"{original_dealer['gen_set_exclude_wholesale']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Atc Enabled:' is cloned: {original_dealer['gen_set_atc_enabled']}"):
                atc_enabled = page.is_button_switched_on(page.ATC_ENABLED_BTN)
                assert original_dealer['gen_set_atc_enabled'] == atc_enabled, [
                    f"Wrong 'Atc Enabled:' value: {atc_enabled} instead of "
                    f"{original_dealer['gen_set_atc_enabled']}", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        with check:
            with allure.step(f"Checking that 'Gmac Enabled:' is cloned: {original_dealer['gen_set_gmac_enabled']}"):
                gmac_enabled = page.is_button_switched_on(page.GMAC_ENABLED_BTN)
                assert original_dealer['gen_set_gmac_enabled'] == gmac_enabled, [
                    f"Wrong 'Gmac Enabled:' value: {gmac_enabled} instead of "
                    f"{original_dealer['gen_set_gmac_enabled']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Tfs Enabled:' is cloned: {original_dealer['gen_set_tfs_enabled']}"):
                tfs_enabled = page.is_button_switched_on(page.TFS_ENABLED_BTN)
                assert original_dealer['gen_set_tfs_enabled'] == tfs_enabled, [
                    f"Wrong 'Tfs Enabled:' value: {tfs_enabled} instead of "
                    f"{original_dealer['gen_set_tfs_enabled']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Visible To Dealer Group:' "
                             f"is cloned: {original_dealer['gen_set_visible_to_dealer_group']}"):
                visible_to_dealer_group = page.is_button_switched_on(page.VISIBLE_TO_DEALER_GROUP_BTN)
                assert original_dealer['gen_set_visible_to_dealer_group'] == visible_to_dealer_group, [
                    f"Wrong 'Visible To Dealer Group:' value: {visible_to_dealer_group} instead of "
                    f"{original_dealer['gen_set_visible_to_dealer_group']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable Auto Match:' "
                             f"is cloned: {original_dealer['gen_set_enable_auto_match']}"):
                enable_auto_match = page.is_button_switched_on(page.ENABLE_AUTO_MATCH_BTN)
                assert original_dealer['gen_set_enable_auto_match'] == enable_auto_match, [
                    f"Wrong 'Enable Auto Match:' value: {enable_auto_match} instead of "
                    f"{original_dealer['gen_set_enable_auto_match']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Display Unit Cost To Dealer Group:' "
                             f"is cloned: {original_dealer['gen_set_display_unit_cost']}"):
                display_unit_cost = page.is_button_switched_on(page.DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN)
                assert original_dealer['gen_set_display_unit_cost'] == display_unit_cost, [
                    f"Wrong 'Display Unit Cost To Dealer Group:' value: {display_unit_cost} instead of "
                    f"{original_dealer['gen_set_display_unit_cost']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'In-Transit Inventory:' "
                             f"is cloned: {original_dealer['gen_set_in_transit_inventory']}"):
                in_transit_inventory = page.is_button_switched_on(page.IN_TRANSIT_INVENTORY_BTN)
                assert original_dealer['gen_set_in_transit_inventory'] == in_transit_inventory, [
                    f"Wrong 'In-Transit Inventory:' value: {in_transit_inventory} instead of "
                    f"{original_dealer['gen_set_in_transit_inventory']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Display Recalls Lookup By VIN Link on Appraisals:' "
                             f"is cloned: {original_dealer['gen_set_display_recalls_lookup']}"):
                display_recalls_lookup = page.is_button_switched_on(page.DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN)
                assert original_dealer['gen_set_display_recalls_lookup'] == display_recalls_lookup, [
                    f"Wrong 'Display Recalls Lookup By VIN Link on Appraisals:' value: {display_recalls_lookup} "
                    f"instead of {original_dealer['gen_set_display_recalls_lookup']}", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.TRADE_MANAGER_DAYS_FILTER)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        # Inputs & dropdowns
        with check:
            with allure.step(f"Checking that 'Recall Provider:' "
                             f"is cloned: {original_dealer['gen_set_recall_provider']}"):
                recall_provider = page.get_text(page.RECALL_PROVIDER)
                assert original_dealer['gen_set_recall_provider'] == recall_provider, [
                    f"Wrong 'Recall Provider:' value: {recall_provider} instead of "
                    f"{original_dealer['gen_set_recall_provider']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Value Requirement on Trade Analyzer:' "
                             f"is cloned: {original_dealer['gen_set_appraisal_value_requirement']}"):
                appraisal_value_req = page.get_text(page.APPRAISAL_VALUE_REQUIREMENT)
                assert original_dealer['gen_set_appraisal_value_requirement'] == appraisal_value_req, [
                    f"Wrong 'Appraisal Value Requirement on Trade Analyzer:' value: {appraisal_value_req} instead of "
                    f"{original_dealer['gen_set_appraisal_value_requirement']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Inventory Days Back Threshold:' "
                             f"is cloned: {original_dealer['gen_set_inventory_days_back_threshold']}"):
                inventory_back_days = page.get_attribute(page.INVENTORY_DAYS_BACK_THRESHOLD, 'value')
                assert original_dealer['gen_set_inventory_days_back_threshold'] == inventory_back_days, [
                    f"Wrong 'Inventory Days Back Threshold:' value: {inventory_back_days} instead of "
                    f"{original_dealer['gen_set_inventory_days_back_threshold']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Unwind Days Threshold:' "
                             f"is cloned: {original_dealer['gen_set_unwind_days_threshold']}"):
                unwind_days_threshold = page.get_attribute(page.UNWIND_DAYS_THRESHOLD, 'value')
                assert original_dealer['gen_set_unwind_days_threshold'] == unwind_days_threshold, [
                    f"Wrong 'Unwind Days Threshold:' value: {unwind_days_threshold} instead of "
                    f"{original_dealer['gen_set_unwind_days_threshold']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Search Appraisal Days Back Threshold:' "
                             f"is cloned: {original_dealer['gen_set_search_appraisal_days']}"):
                search_appraisal_days = page.get_attribute(page.SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD, 'value')
                assert original_dealer['gen_set_search_appraisal_days'] == search_appraisal_days, [
                    f"Wrong 'Search Appraisal Days Back Threshold:' value: {search_appraisal_days} instead of "
                    f"{original_dealer['gen_set_search_appraisal_days']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Look Back Period:' "
                             f"is cloned: {original_dealer['gen_set_appraisal_look_back']}"):
                appraisal_look_back = page.get_attribute(page.APPRAISAL_LOOK_BACK_PERIOD, 'value')
                assert original_dealer['gen_set_appraisal_look_back'] == appraisal_look_back, [
                    f"Wrong 'Appraisal Look Back Period:' value: {appraisal_look_back} instead of "
                    f"{original_dealer['gen_set_appraisal_look_back']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Appraisal Look Forward Period:' "
                             f"is cloned: {original_dealer['gen_set_appraisal_look_forward']}"):
                appraisal_look_forward = page.get_attribute(page.APPRAISAL_LOOK_FORWARD_PERIOD, 'value')
                assert original_dealer['gen_set_appraisal_look_forward'] == appraisal_look_forward, [
                    f"Wrong 'Appraisal Look Forward Period:' value: {appraisal_look_forward} instead of "
                    f"{original_dealer['gen_set_appraisal_look_forward']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Showroom Days Filter:' "
                             f"is cloned: {original_dealer['gen_set_showroom_days_filter']}"):
                showroom_days_filter = page.get_attribute(page.SHOWROOM_DAYS_FILTER, 'value')
                assert original_dealer['gen_set_showroom_days_filter'] == showroom_days_filter, [
                    f"Wrong 'Showroom Days Filter:' value: {showroom_days_filter} instead of "
                    f"{original_dealer['gen_set_showroom_days_filter']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Trade Manager Days Filter:' "
                             f"is cloned: {original_dealer['gen_set_trade_manager_days']}"):
                trade_manager_days = page.get_text(page.TRADE_MANAGER_DAYS_FILTER)
                assert original_dealer['gen_set_trade_manager_days'] == trade_manager_days, [
                    f"Wrong 'Trade Manager Days Filter:' value: {trade_manager_days} instead of "
                    f"{original_dealer['gen_set_trade_manager_days']}", page.make_screenshot()]

        element_to_scroll = page.locate_element(page.PERFANALYZER_VIEW)
        page.scroll_to_element(element_to_scroll)
        time.sleep(2)

        with check:
            with allure.step(f"Checking that 'Run Day Of Week:' "
                             f"is cloned: {original_dealer['gen_set_run_day_of_week']}"):
                run_day_of_week = page.get_text(page.RUN_DAY_OF_WEEK)
                assert original_dealer['gen_set_run_day_of_week'] == run_day_of_week, [
                    f"Wrong 'Run Day Of Week:' value: {run_day_of_week} instead of "
                    f"{original_dealer['gen_set_run_day_of_week']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Program Type:' is cloned: {original_dealer['gen_set_program_type']}"):
                program_type = page.get_text(page.PROGRAM_TYPE)
                assert original_dealer['gen_set_program_type'] == program_type, [
                    f"Wrong 'Program Type:' value: {program_type} instead of "
                    f"{original_dealer['gen_set_program_type']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Pack Amount:' is cloned: {original_dealer['gen_set_pack_amount']}"):
                pack_amount = page.get_attribute(page.PACK_AMOUNT, 'value')
                assert original_dealer['gen_set_pack_amount'] == pack_amount, [
                    f"Wrong 'Pack Amount:' value: {pack_amount} instead of "
                    f"{original_dealer['gen_set_pack_amount']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Group Appraisal Search Weeks:' "
                             f"is cloned: {original_dealer['gen_set_group_appraisal_search_weeks']}"):
                group_appraisal_search_weeks = page.get_attribute(page.GROUP_APPRAISAL_SEARCH_WEEKS, 'value')
                assert original_dealer['gen_set_group_appraisal_search_weeks'] == group_appraisal_search_weeks, [
                    f"Wrong 'Group Appraisal Search Weeks:' value: {group_appraisal_search_weeks} instead of "
                    f"{original_dealer['gen_set_group_appraisal_search_weeks']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Twix Url:' is cloned: {original_dealer['gen_set_twix_url']}"):
                twix_url = page.get_attribute(page.TWIX_URL, 'value')
                assert original_dealer['gen_set_twix_url'] == twix_url, [
                    f"Wrong 'Twix Url:' value: {twix_url} instead of "
                    f"{original_dealer['gen_set_twix_url']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Auction Area:' is cloned: {original_dealer['gen_set_auction_area']}"):
                auction_area = page.get_text(page.AUCTION_AREA)
                assert original_dealer['gen_set_auction_area'] == auction_area, [
                    f"Wrong 'Auction Area:' value: {auction_area} instead of "
                    f"{original_dealer['gen_set_auction_area']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Live Auction Distance From Dealer:' "
                             f"is cloned: {original_dealer['gen_set_live_auction_distance']}"):
                live_auction_distance = page.get_text(page.LIVE_AUCTION_DISTANCE_FROM_DEALER)
                assert original_dealer['gen_set_live_auction_distance'] == live_auction_distance, [
                    f"Wrong 'Live Auction Distance From Dealer:' value: {live_auction_distance} instead of "
                    f"{original_dealer['gen_set_live_auction_distance']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Dashboard Display:' "
                             f"is cloned: {original_dealer['gen_set_dashboard_display']}"):
                dashboard_display = page.get_text(page.DASHBOARD_DISPLAY)
                assert original_dealer['gen_set_dashboard_display'] == dashboard_display, [
                    f"Wrong 'Dashboard Display:' value: {dashboard_display} instead of "
                    f"{original_dealer['gen_set_dashboard_display']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Forecaster Weeks:' "
                             f"is cloned: {original_dealer['gen_set_forecaster_weeks']}"):
                forecaster_weeks = page.get_text(page.FORECASTER_WEEKS)
                assert original_dealer['gen_set_forecaster_weeks'] == forecaster_weeks, [
                    f"Wrong 'Forecaster Weeks:' value: {forecaster_weeks} instead of "
                    f"{original_dealer['gen_set_forecaster_weeks']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'PerfAnalyzer Weeks:' "
                             f"is cloned: {original_dealer['gen_set_perfanalyzer_weeks']}"):
                perfanalyzer_weeks = page.get_text(page.PERFANALYZER_WEEKS)
                assert original_dealer['gen_set_perfanalyzer_weeks'] == perfanalyzer_weeks, [
                    f"Wrong 'PerfAnalyzer Weeks:' value: {perfanalyzer_weeks} instead of "
                    f"{original_dealer['gen_set_perfanalyzer_weeks']}", page.make_screenshot()]
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
            with allure.step(f"Checking that 'Threshold for 4 Weeks:' is cloned: "
                             f"'{original_dealer['scorecard_4_weeks']}'"):
                scorecard_4_weeks = page.get_attribute(page.THRESHOLD_4_WEEKS_INPUT, 'value')
                assert original_dealer['scorecard_4_weeks'] == scorecard_4_weeks, \
                    [f"'Threshold for 4 Weeks:' is not cloned: '{scorecard_4_weeks}' instead of "
                     f"'{original_dealer['scorecard_4_weeks']}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that 'Threshold for 8 Weeks:' is cloned: "
                                 f"'{original_dealer['scorecard_8_weeks']}'"):
                    scorecard_8_weeks = page.get_attribute(page.THRESHOLD_8_WEEKS_INPUT, 'value')
                    assert original_dealer['scorecard_8_weeks'] == scorecard_8_weeks, \
                        [f"'Threshold for 8 Weeks:' is not cloned: '{scorecard_8_weeks}' instead of "
                         f"'{original_dealer['scorecard_8_weeks']}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that 'Threshold for 12 Weeks:' is cloned: "
                                 f"'{original_dealer['scorecard_12_weeks']}'"):
                    scorecard_12_weeks = page.get_attribute(page.THRESHOLD_12_WEEKS_INPUT, 'value')
                    assert original_dealer['scorecard_12_weeks'] == scorecard_12_weeks, \
                        [f"'Threshold for 12 Weeks:' is not cloned: '{scorecard_12_weeks}' instead of "
                         f"'{original_dealer['scorecard_12_weeks']}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that 'Threshold for 13 Weeks:' is cloned: "
                                 f"'{original_dealer['scorecard_13_weeks']}'"):
                    scorecard_13_weeks = page.get_attribute(page.THRESHOLD_13_WEEKS_INPUT, 'value')
                    assert original_dealer['scorecard_13_weeks'] == scorecard_13_weeks, \
                        [f"'Threshold for 13 Weeks:' is not cloned: '{scorecard_13_weeks}' instead of "
                         f"'{original_dealer['scorecard_13_weeks']}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that 'Threshold for 26 Weeks:' is cloned: "
                                 f"'{original_dealer['scorecard_26_weeks']}'"):
                    scorecard_26_weeks = page.get_attribute(page.THRESHOLD_26_WEEKS_INPUT, 'value')
                    assert original_dealer['scorecard_26_weeks'] == scorecard_26_weeks, \
                        [f"'Threshold for 26 Weeks:' is not cloned: '{scorecard_26_weeks}' instead of "
                         f"'{original_dealer['scorecard_26_weeks']}'", page.make_screenshot()]
            with check:
                with allure.step(f"Checking that 'Threshold for 52 Weeks:' is cloned: "
                                 f"'{original_dealer['scorecard_52_weeks']}'"):
                    scorecard_52_weeks = page.get_attribute(page.THRESHOLD_52_WEEKS_INPUT, 'value')
                    assert original_dealer['scorecard_52_weeks'] == scorecard_52_weeks, \
                        [f"'Threshold for 52 Weeks:' is not cloned: '{scorecard_52_weeks}' instead of "
                         f"'{original_dealer['scorecard_52_weeks']}'", page.make_screenshot()]

    with allure.step("Switching to 'Inventory Settings' tab"):
        inventory_settings_tab = page.locate_element(page.INVENTORY_SETTINGS_TAB)
        page.click(inventory_settings_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Default Search Radius:' "
                             f"is cloned: {original_dealer['inv_set_default_search_radius']}"):
                default_search_radius = page.get_text(page.DEFAULT_SEARCH_RADIUS)
                assert original_dealer['inv_set_default_search_radius'] == default_search_radius, [
                    f"Wrong 'Default Search Radius:' value: {default_search_radius} instead of "
                    f"{original_dealer['inv_set_default_search_radius']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Default Stock Type:' "
                             f"is cloned: {original_dealer['inv_set_default_stock_type']}"):
                default_stock_type = page.get_text(page.DEFAULT_STOCK_TYPE)
                assert original_dealer['inv_set_default_stock_type'] == default_stock_type, [
                    f"Wrong 'Default Stock Type:' value: {default_stock_type} instead of "
                    f"{original_dealer['inv_set_default_stock_type']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Supress Seller Name:' "
                             f"is cloned: {original_dealer['inv_set_supress_seller_name']}"):
                supress_seller_name = page.is_button_switched_on(page.SUPRESS_SELLER_NAME_BTN)
                assert original_dealer['inv_set_supress_seller_name'] == supress_seller_name, [
                    f"Wrong 'Supress Seller Name:' value: {supress_seller_name} instead of "
                    f"{original_dealer['inv_set_supress_seller_name']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Exclude No Price From Calc:' "
                             f"is cloned: {original_dealer['inv_set_exclude_no_price']}"):
                exclude_no_price = page.is_button_switched_on(page.EXCLUDE_NO_PRICE_FROM_CALC_BTN)
                assert original_dealer['inv_set_exclude_no_price'] == exclude_no_price, [
                    f"Wrong 'Exclude No Price From Calc:' value: {exclude_no_price} instead of "
                    f"{original_dealer['inv_set_exclude_no_price']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable New Car Pricing:' "
                             f"is cloned: {original_dealer['inv_set_enable_new_car_pricing']}"):
                enable_new_car_pricing = page.is_button_switched_on(page.ENABLE_NEW_CAR_PRICING_BTN)
                assert original_dealer['inv_set_enable_new_car_pricing'] == enable_new_car_pricing, [
                    f"Wrong 'Enable New Car Pricing:' value: {enable_new_car_pricing} instead of "
                    f"{original_dealer['inv_set_enable_new_car_pricing']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable Lithia New Car View:' "
                             f"is cloned: {original_dealer['inv_set_enable_lithia_new_car_view']}"):
                enable_lithia_new_car_view = page.is_button_switched_on(page.ENABLE_LITHIA_NEW_CAR_VIEW_BTN)
                assert original_dealer['inv_set_enable_lithia_new_car_view'] == enable_lithia_new_car_view, [
                    f"Wrong 'Enable Lithia New Car View:' value: {enable_lithia_new_car_view} instead of "
                    f"{original_dealer['inv_set_enable_lithia_new_car_view']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable Chrome Incentives:' "
                             f"is cloned: {original_dealer['inv_set_enable_chrome_incentives']}"):
                enable_chrome_incentives = page.is_button_switched_on(page.ENABLE_CHROME_INCENTIVES_BTN)
                assert original_dealer['inv_set_enable_chrome_incentives'] == enable_chrome_incentives, [
                    f"Wrong 'Enable Chrome Incentives:' value: {enable_chrome_incentives} instead of "
                    f"{original_dealer['inv_set_enable_chrome_incentives']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Is New Ping:' "
                             f"is cloned: {original_dealer['inv_set_is_new_ping']}"):
                is_new_ping = page.is_button_switched_on(page.IS_NEW_PING_BTN)
                assert original_dealer['inv_set_is_new_ping'] == is_new_ping, [
                    f"Wrong 'Is New Ping:' value: {is_new_ping} instead of "
                    f"{original_dealer['inv_set_is_new_ping']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Enable New Ping On FL and MAX:' "
                             f"is cloned: {original_dealer['inv_set_new_ping_on_fl_and_max']}"):
                new_ping_on_fl_and_max = page.is_button_switched_on(page.ENABLE_NEW_PING_ON_FL_AND_MAX_BTN)
                assert original_dealer['inv_set_new_ping_on_fl_and_max'] == new_ping_on_fl_and_max, [
                    f"Wrong 'Enable New Ping On FL and MAX:' value: {new_ping_on_fl_and_max} instead of "
                    f"{original_dealer['inv_set_new_ping_on_fl_and_max']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Market Listing VDP Link:' "
                             f"is cloned: {original_dealer['inv_set_market_listing_vdp_link']}"):
                market_listing_vdp_link = page.is_button_switched_on(page.MARKET_LISTING_VDP_LINK_BTN)
                assert original_dealer['inv_set_market_listing_vdp_link'] == market_listing_vdp_link, [
                    f"Wrong 'Market Listing VDP Link:' value: {market_listing_vdp_link} instead of "
                    f"{original_dealer['inv_set_market_listing_vdp_link']}", page.make_screenshot()]

        with allure.step("Scrolling down to 'New Ping Pricing Indicator Settings'"):
            new_ping_pricing_indicator_settings_bottom = page.locate_element(page.NEW_PING_PRICING_GREEN_TO)
            page.scroll_to_element(new_ping_pricing_indicator_settings_bottom)
            time.sleep(2)

        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Above:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_red_above']}"):
                red_above = page.get_attribute(page.NEW_PING_PRICING_RED_ABOVE, 'value')
                assert red_above == original_dealer['new_ping_pricing_indicator_red_above'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Red Above:' value: {red_above} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_red_above']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Red Below:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_red_below']}"):
                red_below = page.get_attribute(page.NEW_PING_PRICING_RED_BELOW, 'value')
                assert red_below == original_dealer['new_ping_pricing_indicator_red_below'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Red Below:' value: {red_below} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_red_below']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow From:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_yellow_from']}"):
                yellow_from = page.get_attribute(page.NEW_PING_PRICING_YELLOW_FROM, 'value')
                assert yellow_from == original_dealer['new_ping_pricing_indicator_yellow_from'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Yellow From:' value: {yellow_from} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_yellow_from']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Yellow To:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_yellow_to']}"):
                yellow_to = page.get_attribute(page.NEW_PING_PRICING_YELLOW_TO, 'value')
                assert yellow_to == original_dealer['new_ping_pricing_indicator_yellow_to'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Yellow To:' value: {yellow_to} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_yellow_to']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow From:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_and_yellow_from']}"):
                and_yellow_from = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_FROM, 'value')
                assert and_yellow_from == original_dealer['new_ping_pricing_indicator_and_yellow_from'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - & Yellow From:' value: {and_yellow_from} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_and_yellow_from']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - & Yellow To:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_and_yellow_to']}"):
                and_yellow_to = page.get_attribute(page.NEW_PING_PRICING_AND_YELLOW_TO, 'value')
                assert and_yellow_to == original_dealer['new_ping_pricing_indicator_and_yellow_to'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - & Yellow To:' value: {and_yellow_to} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_and_yellow_to']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green From:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_green_from']}"):
                green_from = page.get_attribute(page.NEW_PING_PRICING_GREEN_FROM, 'value')
                assert green_from == original_dealer['new_ping_pricing_indicator_green_from'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Green From:' value: {green_from} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_green_from']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'New Ping Pricing Indicator Settings - Green To:' is cloned: "
                             f"{original_dealer['new_ping_pricing_indicator_green_to']}"):
                green_to = page.get_attribute(page.NEW_PING_PRICING_GREEN_TO, 'value')
                assert green_to == original_dealer['new_ping_pricing_indicator_green_to'], [
                    f"Wrong 'New Ping Pricing Indicator Settings - Green To:' value: {green_to} instead of "
                    f"{original_dealer['new_ping_pricing_indicator_green_to']}", page.make_screenshot()]

    with allure.step("Switching to 'Age Buckets' sub-tab"):
        age_buckets_subtab = page.locate_element(page.AGE_BUCKETS_SUB_TAB)
        page.click(age_buckets_subtab)
        time.sleep(TIMEOUT)
        page.locate_element(page.BUCKET_ELEMENT)

        # Age Buckets
        with allure.step("Finding the number and values for Age Buckets of the cloned dealer"):
            age_buckets_cloned_num = len(page.locate_all_elements(page.AGE_BUCKETS_ROW))
            age_bucket_cloned_sizes = []
            for i in range(1, age_buckets_cloned_num + 1):
                age_bucket_cloned_sizes.append(page.get_table_cell_value_from_input(page.AGE_BUCKET_TABLE, i, 2))
        with check:
            with allure.step(f"Checking that number of Age Buckets is correct: {original_dealer['age_buckets_num']}"):
                assert original_dealer['age_buckets_num'] == age_buckets_cloned_num, [
                    f"Wrong number of Age Buckets: {age_buckets_cloned_num} instead of "
                    f"{original_dealer['age_buckets_num']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that Age Buckets sizes are correct: {original_dealer['age_buckets_values']}"):
                assert original_dealer['age_buckets_values'] == age_bucket_cloned_sizes, [
                    f"Wrong sizes of Age Buckets: {age_bucket_cloned_sizes} instead of "
                    f"{original_dealer['age_buckets_values']}", page.make_screenshot()]

        with allure.step("Scrolling down to 'FirstLook Age Buckets'"):
            page_bottom = page.locate_element(page.PAGE_BOTTOM)
            page.scroll_to_element(page_bottom)
            time.sleep(2)

        # FirstLook Age Buckets
        with allure.step("Finding FirstLook Age Bucket sizes for the cloned dealer"):

            fl_age_buckets_cloned = page.locate_all_elements(page.FL_AGE_BUCKETS_ROW)
            fl_age_bucket_sizes_cloned = []
            for i in range(1, len(fl_age_buckets_cloned) + 1):
                fl_age_bucket_sizes_cloned.append(page.get_table_cell_value_from_input(page.FL_AGE_BUCKET_TABLE, i, 2))
        with check:
            with allure.step(f"Checking that FirstLook Age Buckets sizes are correct: "
                             f"{original_dealer['firstlook_age_buckets_values']}"):
                assert original_dealer['firstlook_age_buckets_values'] == fl_age_bucket_sizes_cloned, [
                    f"Wrong sizes of FirstLook Age Buckets: {fl_age_bucket_sizes_cloned} instead of "
                    f"{original_dealer['firstlook_age_buckets_values']}", page.make_screenshot()]

    with allure.step("Switching to 'Settings' tab - 'Upgrades'"):
        settings_tab = page.locate_element(page.SETTINGS_TAB)
        page.click(settings_tab)
        page = DealerProfileSettingsPage(driver)
        time.sleep(8)

    all_upgrades_cloned = page.get_all_upgrades_names()

    with check:
        with allure.step(f"Checking that the list of Upgrades is correct for the cloned dealer"):
            assert all_upgrades == all_upgrades_cloned, [
                f"Wrong list of Upgrades: {all_upgrades_cloned} instead of {all_upgrades}", page.make_screenshot()]

    with allure.step(f"Checking that all Upgrades settings has correct value for the cloned dealer"):
        for i in range(len(all_upgrades_cloned)):
            key_name, locator = page.get_upgrade_key_name_and_locator(all_upgrades_cloned[i])
            cloned_setting_status = page.is_button_switched_on(locator)
            with check:
                with allure.step(f"Checking that '{all_upgrades_cloned[i]}' setting is cloned (set to "
                                 f"{original_dealer[key_name]})"):
                    assert original_dealer[key_name] == cloned_setting_status, [
                        f"Wrong value for {all_upgrades_cloned[i]}: {cloned_setting_status} instead of "
                        f"{original_dealer[key_name]}", page.make_screenshot()]

    # Pricing > Syndication Price Showroom defaults: TC C38177
    with allure.step("Switching to 'Pricing' tab"):
        pricing_tab = page.locate_element(page.PRICING_TAB)
        page.click(pricing_tab)
        page = DealerProfilePricingPage(driver)
        time.sleep(TIMEOUT)
        syndication_price_showroom = page.locate_element(page.SYNDICATION_PRICE_SHOWROOM)
        page.click(syndication_price_showroom)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that the price for 'New Vehicles' in 'Syndication Price Showroom' is defaulted"
                             f" to '{page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT}'"):
                price = page.get_text(page.SYND_PRICE_SHOWROOM_NEW_VEHICLES)
                assert price == page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT, \
                    [f"Wrong default value for 'New Vehicles': '{price}' instead of "
                     f"'{page.SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT}'", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that the price for 'Used Vehicles' in 'Syndication Price Showroom' is defaulted"
                             f" to '{page.SYND_PRICE_SHOWROOM_USED_VEHICLES_DEFAULT}'"):
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

    with allure.step("Switching to 'MAX Settings' / 'Ad Settings' tab"):
        max_settings_tab = page.locate_element(page.MAX_SETTINGS_TAB)
        page.click(max_settings_tab)
        time.sleep(TIMEOUT)
        page = DealerProfileMaxSettingsPage(driver)
        ad_settings_sub_tab = page.locate_element(page.AD_SETTINGS_SUB_TAB)
        page.click(ad_settings_sub_tab)
        time.sleep(TIMEOUT)

        with check:
            with allure.step(f"Checking that 'Which book value should be used in descriptions?' "
                             f"is cloned: {original_dealer['max_set_book_value_in_description']}"):
                book_value_in_description = page.get_text(page.WHICH_BOOK_VALUE_SHOULD_BE_USED)
                assert original_dealer['max_set_book_value_in_description'] == book_value_in_description, [
                    f"Wrong 'Which book value should be used in descriptions?' value: {book_value_in_description} "
                    f"instead of {original_dealer['max_set_book_value_in_description']}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Do you want to show a call to action in previews' is OFF by default"):
                assert not page.is_checkbox_checked(page.CALL_TO_ACTION_IN_PREVIEWS_STATUS), [
                    "'Do you want to show a call to action in previews' is ON", page.make_screenshot()]

        with allure.step("Switching to 'MAX Settings' / 'Setup Wizard' tab"):
            setup_wizard_tab = page.locate_element(page.SETUP_WIZARD_TAB)
            page.click(setup_wizard_tab)
            time.sleep(TIMEOUT)

        with check:
            with allure.step(
                    f"Checking that 'What's the minimum mileage remaining you would advertise?' is defaulted to "
                    f"'{page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT}' for the cloned dealer"):
                minimum_mileage = page.get_attribute(page.SETUP_WIZARD_MIN_MILEAGE_INPUT, 'value')
                assert minimum_mileage == page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT, \
                    [f"Wrong Default for Minimum mileage: {minimum_mileage} instead of "
                     f"{page.SETUP_WIZARD_MIN_MILEAGE_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'How many characters long is your 'preview' on the web?' is defaulted to "
                             f"'{page.SETUP_WIZARD_CHARACTERS_DEFAULT}' for the cloned dealer"):
                characters = page.get_attribute(page.SETUP_WIZARD_CHARACTERS_INPUT, 'value')
                assert characters == page.SETUP_WIZARD_CHARACTERS_DEFAULT, \
                    [f"Wrong Default for preview length: {characters} instead of "
                     f"{page.SETUP_WIZARD_CHARACTERS_DEFAULT}", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that 'Low Photo Threshold' is defaulted to "
                             f"'{page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT}' for the cloned dealer"):
                low_photo = page.get_attribute(page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_INPUT, 'value')
                assert low_photo == page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT, \
                    [f"Wrong Default for 'Low Photo Threshold': {low_photo} instead of "
                     f"{page.SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT}", page.make_screenshot()]

        with allure.step("Switching to 'MAX Settings' / 'Miscellaneous Settings' tab"):
            miscellaneous_sub_tab = page.locate_element(page.MISC_SETTINGS_SUB_TAB)
            page.click(miscellaneous_sub_tab)
            time.sleep(TIMEOUT)

        with check:
            with allure.step("Checking that checkbox for 'Webloader' is On"):
                assert page.is_checkbox_checked(page.MISC_WEBLOADER_STATUS), \
                    ["Checkbox 'Webloader' is unchecked", page.make_screenshot()]
        with check:
            with allure.step(f"Checking that checkbox for 'Batch Autoload' is Off for the cloned dealer"):
                assert not page.is_checkbox_checked(page.MISC_BATCH_AUTOLOAD_STATUS), \
                    ["Checkbox 'Batch Autoload' is checked", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Clone Dealer: MAX-9170")
@allure.title("C13755 Cloning with required fields empty")
def test_clone_dealer_required_fields_empty(driver):
    with allure.step("Logging to PitStop as Administrator and opening dealer list page"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the original dealer {page.WC_TEST_DEALER}"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)
        page = CloneDealerPage(driver)
        page.clone_dealer(calc_lat_long_by='')

    with check:
        with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
            alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
            assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
                [f"Wrong alert text for Form Validation: {alert1} instead of "
                 f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Name Required alert: '{page.NAME_REQUIRED_TEXT}'"):
            alert2 = page.locate_element(page.NAME_REQUIRED_ALERT).text
            assert alert2 == page.NAME_REQUIRED_TEXT, \
                [f"Wrong alert text for Name field: {alert2} instead of"
                 f"{page.NAME_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Short Name Required alert: '{page.SHORT_NAME_REQUIRED_TEXT}'"):
            alert3 = page.locate_element(page.SHORT_NAME_REQUIRED_ALERT).text
            assert alert3 == page.SHORT_NAME_REQUIRED_TEXT, \
                [f"Wrong alert text for Short Name field: {alert3} instead of "
                 f"{page.SHORT_NAME_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting ZipCode Required alert: '{page.ZIPCODE_REQUIRED_TEXT}'"):
            alert4 = page.locate_element(page.ZIPCODE_REQUIRED_ALERT).text
            assert alert4 == page.ZIPCODE_REQUIRED_TEXT, \
                [f"Wrong alert text for the ZipCode field: {alert4} instead of "
                 f"{page.ZIPCODE_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Latitude Required alert: '{page.LATITUDE_REQUIRED_TEXT}'"):
            alert5 = page.locate_element(page.LATITUDE_REQUIRED_ALERT).text
            assert alert5 == page.LATITUDE_REQUIRED_TEXT, \
                [f"Wrong alert text for the Latitude field: {alert5} instead of "
                 f"{page.LATITUDE_REQUIRED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Longitude Required alert: '{page.LONGITUDE_REQUIRED_TEXT}'"):
            alert6 = page.locate_element(page.LONGITUDE_REQUIRED_ALERT).text
            assert alert6 == page.LONGITUDE_REQUIRED_TEXT, \
                [f"Wrong alert text for the Longitude field: {alert6} instead of "
                 f"{page.LONGITUDE_REQUIRED_TEXT}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Clone Dealer: MAX-9170")
@allure.title("C13725, C13756, C13738, C13757 Clone Dealer form values and defaults")
def test_clone_dealer_form_values_and_defaults(driver):
    with allure.step("Logging to PitStop as Administrator and opening dealer list page"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the original dealer {page.WC_TEST_DEALER}"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step("Saving settings of the original dealer - 'Franchises' and 'State'"):
        page = DealerProfileDealerPage(driver)
        original_dealer = dict()
        with allure.step("Saving 'Franchises'"):
            franchises = []
            franchises_list = page.locate_all_elements(page.FRANCHISES)
            for item in franchises_list:
                franchises.append(item.text)
            with allure.step(f"Found Franchises: {franchises}"):
                original_dealer['franchises'] = franchises
        with allure.step("Saving 'State'"):
            original_dealer['state'] = page.get_text(page.STATE_VALUE)

    with allure.step("Cloning the dealer"):
        page = CloneDealerPage(driver)
        clone_btn = page.get_clickable_element(page.CLONE_BTN)
        page.click(clone_btn)
        time.sleep(7)

    # Check that Dealer Group field has a pre-defined value and cannot be edited, read-only (C13725)
    with check:
        with allure.step(f"Asserting that Dealer Group field has a pre-defined value - {page.GROUP_NAME}"):
            dealer_group = page.get_text(page.GROUP_CONTENT)
            assert dealer_group == page.GROUP_NAME, \
                [f"Wrong Group Name: {dealer_group} instead of {page.GROUP_NAME}", page.make_screenshot()]
    with check:
        with allure.step("Asserting that Dealer Group field is read-only (cannot be edited)"):
            group_input = page.locate_element(page.GROUP_INPUT)
            assert page.is_input_readonly(group_input), \
                ["Dealer Group field is active, not read-only", page.make_screenshot()]

    # Franchises and State fields have pre-defined values matching the original dealer (C13756)
    with check:
        with allure.step(f"Checking that 'Franchises' field has pre-defined value: {original_dealer['franchises']}"):
            cloned_franchises = []
            cloned_franchises_list = page.locate_all_elements(page.FRANCHISES_VALUES)
            for item in cloned_franchises_list:
                cloned_franchises.append(item.text)
            with allure.step(f"Found Franchises: {cloned_franchises}"):
                assert original_dealer['franchises'] == franchises, [
                    f"Wrong Franchises: {franchises} instead of {original_dealer['franchises']}",
                    page.make_screenshot()]
    with check:
        with allure.step(f"Checking that 'State' field has pre-defined value: {original_dealer['state']}"):
            state_name = page.get_text(page.STATE_VALUE)
            assert original_dealer['state'] == state_name, \
                [f"Wrong State: {state_name} instead of {original_dealer['state']}", page.make_screenshot()]

    # Checking that ZipCode field is empty and is required (C13738)
    with check:
        with allure.step("Checking that 'ZipCode' field is empty"):
            zipcode_value = page.get_attribute(page.ZIP_CODE, 'value')
            assert zipcode_value == '', [f"'ZipCode' is not empty: {zipcode_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'ZipCode' field is required"):
            page.locate_element(page.ZIP_CODE_LABEL)
            time.sleep(TIMEOUT)
            assert page.is_required_field(page.ZIP_CODE_LABEL), \
                ["'ZipCode' field is not required", page.make_screenshot()]

    # Checking that  'Name', 'Short Name', 'Website', 'Google Place ID', 'Office Phone', 'Address' and 'City' fields
    # are empty, no pre-defined values (C13757)
    with check:
        with allure.step("Verifying that 'Name' field is empty"):
            name_value = page.get_attribute(page.NAME, 'value')
            assert name_value == '', [f"'Name' field is not empty: {name_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Short Name' field is empty"):
            short_name_value = page.get_attribute(page.SHORT_NAME, 'value')
            assert short_name_value == '', \
                [f"'Short Name' field is not empty: {short_name_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Website' field is empty"):
            website_value = page.get_attribute(page.WEBSITE, 'value')
            assert website_value == '', [f"'Website' field is not empty: {website_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Google Place ID' field is empty"):
            google_place_id_value = page.get_attribute(page.GOOGLE_PLACE_ID, 'value')
            assert google_place_id_value == '', \
                [f"'Google Place ID' field is not empty: {google_place_id_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Office Phone' field is empty"):
            phone_value = page.get_attribute(page.OFFICE_PHONE, 'value')
            assert phone_value == '', [f"'Office Phone' field is not empty: {phone_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'Address' field is empty"):
            address_value = page.get_attribute(page.ADDRESS, 'value')
            assert address_value == '', [f"'Address' field is not empty: {address_value}", page.make_screenshot()]
    with check:
        with allure.step("Verifying that 'City' field is empty"):
            city_value = page.get_attribute(page.CITY, 'value')
            assert city_value == '', [f"'City' field is not empty: {city_value}", page.make_screenshot()]


@pytest.mark.regression
@allure.feature("Clone Dealer: MAX-9170, MAX-13494")
@allure.title("C13714, C13730 Clone dealer: Name must be unique for Active dealers, Short Name may match another Active"
              " dealer's Short Name")
def test_clone_dealer_with_existing_name_and_short_name(driver):
    with allure.step("Logging to PitStop as Administrator and opening dealer list page"):
        page = LoginPage(driver)
        page.open()
        page.log_in(username=page.USER_WITH_PITSTOP_ROLE,
                    password=page.PASSWORD)
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)

    with allure.step(f"Opening the original dealer {page.WC_TEST_DEALER}"):
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step(f"Generating data and trying to clone the dealer with existing Active dealer's name - "
                     f"'{page.EXISTING_DEALER_NAME}'"):
        page = CloneDealerPage(driver)
        new_dealer = page.generate_new_dealer_data()
        page.clone_dealer(name=page.EXISTING_DEALER_NAME,
                          short_name=new_dealer['name'],
                          website=new_dealer['website'],
                          google_place_id=new_dealer['google_place_id'],
                          address=new_dealer['address'],
                          zip_code=new_dealer['zip_code'],
                          calc_lat_long_by='zip_code')

    with check:
        with allure.step(f"Asserting Form Validation Failed alert: '{page.FORM_VALIDATION_FAILED_TEXT}'"):
            alert1 = page.locate_element(page.FORM_VALIDATION_FAILED_ALERT).text
            assert alert1 == page.FORM_VALIDATION_FAILED_TEXT, \
                [f"Wrong alert text for Form Validation: {alert1} instead of "
                 f"{page.FORM_VALIDATION_FAILED_TEXT}", page.make_screenshot()]
    with check:
        with allure.step(f"Asserting Name must be unique alert: '{page.NAME_MUST_BE_UNIQUE_TEXT}'"):
            alert2 = page.locate_element(page.NAME_MUST_BE_UNIQUE_ALERT).text
            assert alert2 == page.NAME_MUST_BE_UNIQUE_TEXT, \
                [f"Wrong alert text for Name field: {alert2} instead of"
                 f"{page.NAME_MUST_BE_UNIQUE_TEXT}", page.make_screenshot()]

    with allure.step(f"Opening the original dealer '{page.WC_TEST_DEALER}'"):
        dealers_menu = page.locate_element(page.DEALERS_LEFT_MENU)
        page.click(dealers_menu)
        time.sleep(TIMEOUT)
        page = DealerListPage(driver)
        page.locate_element(page.SEARCH_BAR_INPUT)
        page.paste_text(page.SEARCH_BAR_INPUT, page.WC_TEST_DEALER)
        link_to_dealer = page.locate_element(page.WC_TEST_DEALER_LINK)
        page.click(link_to_dealer)
        time.sleep(TIMEOUT)

    with allure.step(f"Trying to clone the dealer with existing Active dealer's Short Name - "
                     f"'{page.EXISTING_DEALER_SHORT_NAME}'"):
        page = CloneDealerPage(driver)
        page.clone_dealer(name=new_dealer['name'],
                          short_name=page.EXISTING_DEALER_NAME,
                          website=new_dealer['website'],
                          google_place_id=new_dealer['google_place_id'],
                          address=new_dealer['address'],
                          zip_code=new_dealer['zip_code'],
                          calc_lat_long_by='zip_code')
        time.sleep(TIMEOUT)
        open_new_dealer_btn = page.get_clickable_element(page.SUCCESS_BTN)
        page.click(open_new_dealer_btn)
        time.sleep(TIMEOUT)
        page.add_new_objects_to_list(page.NEW_DEALERS_FILE_NAME)
        page = DealerProfileDealerPage(driver)

    with check:
        with allure.step(f"Asserting that the cloned dealer's Short Name is '{page.EXISTING_DEALER_SHORT_NAME}'"):
            short_name = page.get_attribute(page.DEALER_SHORT_NAME_INPUT, 'value')
            assert short_name == page.EXISTING_DEALER_SHORT_NAME, \
                [f"Wrong Dealer Short Name: '{short_name}' instead of '{page.EXISTING_DEALER_SHORT_NAME}'"
                    , page.make_screenshot()]

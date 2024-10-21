import time
from page_objects.DealerProfilePage import DealerProfilePage
from selenium.webdriver.common.by import By
import allure
import random

TIMEOUT = 2


class DealerProfileDealerPage(DealerProfilePage):
    # 'Setting' tab
    SETTING_TAB = (By.XPATH, '//div[text()="Setting"]')
    SETTING_EDIT_ADDRESS_BTN = (By.XPATH, '(//button[contains(., "Edit")])[2]')
    SETTING_EDIT_FRANCHISES_BTN = (By.XPATH, '(//button[contains(., "Edit")])[1]')
    SETTING_SAVE_FRANCHISES_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    SETTING_ACTIVE_BTN = (By.XPATH, '//div[label[contains(., "Active:")]]/following-sibling::div//button')
    SETTING_SAVE_ADDRESS_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    SETTING_CANCEL_ADDRESS_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Cancel")]')
    FRANCHISES = (By.XPATH, '//span[contains(@class, "ant-select-selection-item-content")]')
    STATE_VALUE = (By.XPATH, '(//div[label[contains(., "State")]]/following-sibling::div//span)[2]')
    STATE_LABEL = (By.XPATH, '//label[contains(., "State:")]')
    DEALER_CODE_INPUT = (By.XPATH, '//div/label[text()="Dealer Code:"]/../following-sibling::div//input')
    DEALER_INPUT = (By.XPATH, '//div/label[text()="Dealer:"]/../following-sibling::div//input')
    DEALER_SHORT_NAME_INPUT = (By.XPATH, '//div/label[text()="Dealer Short Name:"]/../following-sibling::div//input')
    FRANCHISES_OPTION = (By.XPATH, '(//div[@role="listbox"])[3]//div[@class="ant-select-item-option-content"]')
    FRANCHISES_INPUT = \
        (By.XPATH, '//div/label[text()="Franchises:"]/../following-sibling::div//div[@class="ant-select-selector"]')
    FRANCHISES_SEARCH_INPUT = (By.XPATH, '//input[@placeholder="Enter search value and press Enter"]')
    FRANCHISES_SEARCH_BTN = \
        (By.XPATH, '//input[@placeholder="Enter search value and press Enter"]/../following-sibling::span//button')
    OFFICE_PHONE_INPUT = (By.XPATH, '//div/label[text()="Office Phone:"]/../following-sibling::div//input')
    OFFICE_FAX_INPUT = (By.XPATH, '//div/label[text()="Office Fax:"]/../following-sibling::div//input')
    ADDRESS1_INPUT = (By.XPATH, '//div/label[text()="Address1:"]/../following-sibling::div//input')
    ADDRESS2_INPUT = (By.XPATH, '//div/label[text()="Address2:"]/../following-sibling::div//input')
    CITY_INPUT = (By.XPATH, '//div/label[text()="City:"]/../following-sibling::div//input')
    STATE_INPUT = (By.XPATH, '//div/label[text()="State:"]/../following-sibling::div//input')
    STATE_CURRENT_VALUE = \
        (By.XPATH, '//div/label[text()="State:"]/../following-sibling::div//span[@class="ant-select-selection-item"]')
    STATE_OPTION = (By.XPATH, '(//div[@role="listbox"])[3]//div[@class="ant-select-item-option-content"]')
    GOOGLE_PLACE_ID_INPUT = (By.XPATH, '//div/label[text()="Google Place Id:"]/../following-sibling::div//input')
    ZIP_CODE_INPUT = (By.XPATH, '//div/label[text()="Zip Code:"]/../following-sibling::div//input')
    GO_LIVE_DATE = (By.XPATH, '//input[contains(@placeholder, "Select date")]')
    SETTING_EDIT_ADDITIONAL_BTN = (By.XPATH, '(//button[contains(., "Edit")])[3]')
    SETTING_SAVE_ADDITIONAL_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    SUCCESS_MESSAGE = (By.XPATH, '//span//span[contains(., "Saved successfully")]')
    FORM_VALIDATION_FAILED_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-alert-message") and contains(., "Form validation failed")]')
    FORM_VALIDATION_FAILED_TEXT = 'Form validation failed. Check fields messages.'
    NAME_MUST_BE_UNIQUE_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-form-item-explain-error") and contains (., "Must be unique")]')
    NAME_MUST_BE_UNIQUE_TEXT = 'Must be unique for active dealer'

    # 'General Settings' tab
    GENERAL_SETTINGS_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"General Settings")]')
    GEN_SET_LOGO = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Logo")]')
    GEN_SET_ACCESS_GROUPS = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Access Groups")]')
    GEN_SET_DEALER_GENERAL = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Dealer General")]')
    GEN_SET_DEALER_APPRAISAL_FORM_SETTINGS = \
        (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Dealer Appraisal Form Settings")]')
    GEN_SET_SCORECARD = \
        (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Scorecard - Units Sold Thresholds")]')
    GEN_SET_BOOKOUT_LOCK = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Bookout Lock")]')
    RECALL_PROVIDER = (By.XPATH, '//div[label[contains(., "Recall Provider")]]/following-sibling::div//span[2]')
    APPRAISAL_VALUE_REQUIREMENT = \
        (By.XPATH, '//div[label[contains(., "Appraisal Value Requirement")]]/following-sibling::div//span[2]')
    INVENTORY_DAYS_BACK_THRESHOLD = \
        (By.XPATH, '//div[label[contains(., "Inventory Days Back")]]/following-sibling::div//input')
    INVENTORY_DAYS_BACK_THRESHOLD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Inventory Days Back Threshold:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    UNWIND_DAYS_THRESHOLD = (By.XPATH, '//div[label[contains(., "Unwind Days")]]/following-sibling::div//input')
    UNWIND_DAYS_THRESHOLD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Unwind Days Threshold:"]/../following-sibling::div'
                   '//span[@aria-label="Increase Value"]')
    UNWIND_DAYS_THRESHOLD_DECREASE_BTN = \
        (By.XPATH, '//label[text()="Unwind Days Threshold:"]/../following-sibling::div'
                   '//span[@aria-label="Decrease Value"]')
    SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD = \
        (By.XPATH, '//div[label[contains(., "Search Appraisal Days")]]/following-sibling::div//input')
    SEARCH_APPRAISAL_DAYS_BACK_THRESHOLD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Search Appraisal Days Back Threshold:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    APPRAISAL_LOOK_BACK_PERIOD = \
        (By.XPATH, '//div[label[contains(., "Appraisal Look Back")]]/following-sibling::div//input')
    APPRAISAL_LOOK_BACK_PERIOD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Appraisal Look Back Period:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    APPRAISAL_LOOK_FORWARD_PERIOD = \
        (By.XPATH, '//div[label[contains(., "Appraisal Look Forward")]]/following-sibling::div//input')
    APPRAISAL_LOOK_FORWARD_PERIOD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Appraisal Look Forward Period:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    SHOWROOM_DAYS_FILTER = (By.XPATH, '//div[label[contains(., "Showroom Days Filter")]]/following-sibling::div//input')
    SHOWROOM_DAYS_FILTER_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Showroom Days Filter:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    TRADE_MANAGER_DAYS_FILTER = \
        (By.XPATH, '//div[label[contains(., "Trade Manager Days")]]/following-sibling::div//span[2]')
    RUN_DAY_OF_WEEK = (By.XPATH, '//div[label[contains(., "Run Day")]]/following-sibling::div//span[2]')
    PROGRAM_TYPE = (By.XPATH, '//div[label[contains(., "Program Type")]]/following-sibling::div//span[2]')
    PROGRAM_TYPE_DEFAULT = 'Insight'
    PACK_AMOUNT = (By.XPATH, '//div[label[contains(., "Pack Amount")]]/following-sibling::div//input')
    PACK_AMOUNT_INCREASE_BTN = (By.XPATH, '//label[text()="Pack Amount:"]/../following-sibling::div//'
                                          'span[@aria-label="Increase Value"]')
    GROUP_APPRAISAL_SEARCH_WEEKS = \
        (By.XPATH, '//div[label[contains(., "Group Appraisal Search Weeks")]]/following-sibling::div//input')
    GROUP_APPRAISAL_SEARCH_WEEKS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Group Appraisal Search Weeks:"]/../following-sibling::div//'
                   'span[@aria-label="Increase Value"]')
    TWIX_URL = (By.XPATH, '//div[label[contains(., "Twix Url")]]/following-sibling::div//input')
    AUCTION_AREA = (By.XPATH, '//div[label[contains(., "Auction Area")]]/following-sibling::div//span[2]')
    LIVE_AUCTION_DISTANCE_FROM_DEALER = \
        (By.XPATH, '//div[label[contains(., "Live Auction Distance")]]/following-sibling::div//span[2]')
    DASHBOARD_DISPLAY = (By.XPATH, '//div[label[contains(., "Dashboard Display")]]/following-sibling::div//span[2]')
    DASHBOARD_DISPLAY_DEFAULT = 'UNITS_IN_STOCK'
    FORECASTER_WEEKS = (By.XPATH, '//div[label[contains(., "Forecaster Weeks")]]/following-sibling::div//span[2]')
    FORECASTER_WEEKS_DEFAULT = '13 Weeks'
    PERFANALYZER_WEEKS = (By.XPATH, '//div[label[contains(., "PerfAnalyzer Weeks")]]/following-sibling::div//span[2]')
    PERFANALYZER_WEEKS_DEFAULT = '13 Weeks'
    PERFANALYZER_VIEW = (By.XPATH, '//div[label[contains(., "PerfAnalyzer View")]]/following-sibling::div//span[2]')
    PERFANALYZER_VIEW_DEFAULT = 'Top Seller'
    # Toggles & Buttons
    SHOW_RECALL_BTN = (By.XPATH, '//div[label[contains(., "Show Recall")]]/following-sibling::div//button')
    RECALL_REPORT_BTN = (By.XPATH, '//div[label[contains(., "Recall Report")]]/following-sibling::div//button')
    SHOW_LOT_LOCATION_STATUS_BTN = \
        (By.XPATH, '//div[label[contains(., "Show Lot Location Status")]]/following-sibling::div//button')
    SHOW_INACTIVE_APPRAISALS_BTN = \
        (By.XPATH, '//div[label[contains(., "Show Inactive Appraisals")]]/following-sibling::div//button')
    REQUIRE_NAME_ON_APPRAISALS_BTN = \
        (By.XPATH, '//div[label[contains(., "Require Name On Appraisals")]]/following-sibling::div//button')
    REQUIRE_EST_RECON_COST_ON_APPRAISALS_BTN = \
        (By.XPATH, '//div[label[contains(., "Recon Cost On Appraisals")]]/following-sibling::div//button')
    REQUIRE_EST_RECON_NOTES_ON_APPRAISALS_BTN = \
        (By.XPATH, '//div[label[contains(., "Recon Notes On Appraisals")]]/following-sibling::div//button')
    SHOW_CASEY_AND_CASEY_BTN = \
        (By.XPATH, '//div[label[contains(., "Show Casey")]]/following-sibling::div//button')
    SHOW_APPRAISAL_FROM_OFFER_GROUP_BTN = \
        (By.XPATH, '//div[label[contains(., "Appraisal Form Offer Group")]]/following-sibling::div//button')
    SHOW_APPRAISAL_VALUE_GROUP_BTN = \
        (By.XPATH, '//div[label[contains(., "Appraisal Value Group")]]/following-sibling::div//button')
    USE_LOT_PRICE_BTN = (By.XPATH, '//div[label[contains(., "Use Lot Price")]]/following-sibling::div//button')
    EXCLUDE_WHOLESALE_FROM_DAYS_SUPPLY_BTN = \
        (By.XPATH, '//div[label[contains(., "Wholesale From Days")]]/following-sibling::div//button')
    ATC_ENABLED_BTN = (By.XPATH, '//div[label[contains(., "Atc Enabled")]]/following-sibling::div//button')
    GMAC_ENABLED_BTN = (By.XPATH, '//div[label[contains(., "Gmac Enabled")]]/following-sibling::div//button')
    TFS_ENABLED_BTN = (By.XPATH, '//div[label[contains(., "Tfs Enabled")]]/following-sibling::div//button')
    VISIBLE_TO_DEALER_GROUP_BTN = \
        (By.XPATH, '//div[label[contains(., "Visible To Dealer Group")]]/following-sibling::div//button')
    ENABLE_AUTO_MATCH_BTN = (By.XPATH, '//div[label[contains(., "Enable Auto Match")]]/following-sibling::div//button')
    DISPLAY_UNIT_COST_TO_DEALER_GROUP_BTN = (
        By.XPATH, '//div[label[contains(., "Unit Cost To Dealer Group")]]/following-sibling::div//button')
    IN_TRANSIT_INVENTORY_BTN = (
        By.XPATH, '//div[label[contains(., "In-Transit Inventory")]]/following-sibling::div//button')
    DISPLAY_RECALLS_LOOKUP_BY_VIN_BTN = (
        By.XPATH, '//div[label[contains(., "Display Recalls Lookup By VIN")]]/following-sibling::div//button')
    TRADE_IN_OFFER_AUTO_CALCULATE = (
        By.XPATH, '//div[label[contains(., "Trade-In Offer Auto Calculate:")]]/following-sibling::div//button')
    DEALER_GENERAL_EDIT_BTN = (
        By.XPATH, '//div[text()="Dealer General"]/following-sibling::div//button[contains(., "Edit")]')
    DEALER_GENERAL_SAVE_BTN = \
        (By.XPATH, '//div[text()="Dealer General"]/following-sibling::div//button[contains(., "Save")]')

    # Access Groups
    ACCESS_GROUPS = (By.XPATH, '//table//td/div/div[1]')
    ACCESS_GROUPS_DEFAULTS = ['ADESA - All Dealers', 'Dealer Direct - Open', 'GMAC SmartAuction - Open', 'OVE - Open']
    SELECT_ACCESS_GROUP_INPUT = (By.XPATH, '//div[text()="AccessGroups"]/following-sibling::div//input')
    ADD_ACCESS_GROUP_BTN = (By.XPATH, '//span[text()="Add"]/..')
    ACCESS_GROUPS_OK_BTN = (By.XPATH, '//span[text()="OK"]/..')
    # Dealer Appraisal Form Settings
    DEALER_APPRAISAL_FORM_SETTINGS_HEADER = (By.XPATH, '//div[text()="Dealer Appraisal Form Settings"]')
    APPRAISAL_VALID_FOR_DAYS_INPUT = \
        (By.XPATH, '//label[text()="Appraisal Valid For Days:"]/../following-sibling::div//input')
    APPRAISAL_VALID_FOR_DAYS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Appraisal Valid For Days:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    APPRAISAL_VALID_FOR_MILES_INPUT = \
        (By.XPATH, '//label[text()="Appraisal Valid For Miles:"]/../following-sibling::div//input')
    APPRAISAL_VALID_FOR_MILES_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Appraisal Valid For Miles:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    APPRAISAL_FORM_MEMO_INPUT = \
        (By.XPATH, '//label[text()="Appraisal Form memo:"]/../following-sibling::div//input')
    APPRAISAL_FORM_DISCLAIMER_INPUT = \
        (By.XPATH, '//label[text()="Appraisal Form Disclaimer:"]/../following-sibling::div//input')
    SHOW_OPTIONS_BY_DEFAULT_BTN = \
        (By.XPATH, '//label[text()="Show Options By Default:"]/../following-sibling::div//button')
    SHOW_CHECK_ON_APPRAISAL_FORM_BTN = \
        (By.XPATH, '//label[text()="Show Check on Appraisal Form:"]/../following-sibling::div//button')
    DEALER_APPRAISAL_FORM_SETTINGS_EDIT_BTN = \
        (By.XPATH, '//div[text()="Dealer Appraisal Form Settings"]/following-sibling::div//button[contains(., "Edit")]')
    DEALER_APPRAISAL_FORM_SETTINGS_SAVE_BTN = (By.XPATH, '//button[contains(., "Save")]')
    # Scorecard - Units Sold Thresholds
    SCORECARD_HEADER = \
        (By.XPATH, '//div[contains(@class, "ant-card-head-title") and text()="Scorecard - Units Sold Thresholds"]')
    THRESHOLD_4_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 4 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_4_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 4 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    THRESHOLD_8_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 8 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_8_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 8 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    THRESHOLD_12_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 12 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_12_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 12 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    THRESHOLD_13_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 13 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_13_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 13 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    THRESHOLD_26_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 26 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_26_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 26 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    THRESHOLD_52_WEEKS_INPUT = (By.XPATH, '//label[text()="Threshold for 52 Weeks:"]/../following-sibling::div//input')
    THRESHOLD_52_WEEKS_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Threshold for 52 Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    SCORECARD_EDIT_BTN = \
        (By.XPATH,
         '//div[text()="Scorecard - Units Sold Thresholds"]/following-sibling::div//button[contains(., "Edit")]')
    SCORECARD_SAVE_BTN = (By.XPATH, '//button[contains(., "Save")]')
    SCORECARD_WEEKS = ['4', '8', '12', '13', '26', '52']
    SCORECARD_DEFAULTS = [1, 1, 1, 1, 2, 4]

    # 'Inventory Settings' tab
    INVENTORY_SETTINGS_TAB = (
        By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Inventory Settings")]')
    PING_II_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Ping II")]')
    AGE_BUCKETS_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Age Buckets")]')
    LIGHTS_RISK_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Lights/Risk")]')

    # Ping II - Toggles and buttons
    SUPRESS_SELLER_NAME_BTN = (
        By.XPATH, '//div[label[contains(., "Supress Seller Name")]]/following-sibling::div//button')
    EXCLUDE_NO_PRICE_FROM_CALC_BTN = \
        (By.XPATH, '//div[label[contains(., "Exclude No Price")]]/following-sibling::div//button')
    ENABLE_NEW_CAR_PRICING_BTN = (
        By.XPATH, '//div[label[contains(., "New Car Pricing")]]/following-sibling::div//button')
    ENABLE_LITHIA_NEW_CAR_VIEW_BTN = \
        (By.XPATH, '//div[label[contains(., "Lithia New Car View")]]/following-sibling::div//button')
    ENABLE_CHROME_INCENTIVES_BTN = \
        (By.XPATH, '//div[label[contains(., "Chrome Incentives")]]/following-sibling::div//button')
    IS_NEW_PING_BTN = (By.XPATH, '//div[label[contains(., "Is New Ping")]]/following-sibling::div//button')
    ENABLE_NEW_PING_ON_FL_AND_MAX_BTN = (
        By.XPATH, '//div[label[contains(., "Enable New Ping On FL and MAX")]]/following-sibling::div//button')
    MARKET_LISTING_VDP_LINK_BTN = (
        By.XPATH, '//div[label[contains(., "Market Listing VDP")]]/following-sibling::div//button')
    # Ping II - Other settings
    DEFAULT_SEARCH_RADIUS = (
        By.XPATH, '//div[label[contains(., "Default Search Radius")]]/following-sibling::div//span[2]')
    DEFAULT_SEARCH_RADIUS_VALUES = ['10', '25', '50', '75', '100', '150', '250', '500', '750', '1000', '5000']
    DEFAULT_SEARCH_RADIUS_DEFAULT = '150'
    DEFAULT_STOCK_TYPE = (By.XPATH, '//div[label[contains(., "Default Stock Type")]]/following-sibling::div//span[2]')
    DEFAULT_STOCK_TYPE_VALUES = ['All', 'New', 'Used']
    NEW_PING_PRICING_RED_ABOVE = (By.XPATH, '//label[text()="Red Above:"]/../following-sibling::div//input')
    NEW_PING_PRICING_RED_ABOVE_DEFAULT = '108%'
    NEW_PING_PRICING_RED_BELOW = (By.XPATH, '//label[text()="Red Below:"]/../following-sibling::div//input')
    NEW_PING_PRICING_RED_BELOW_DEFAULT = '92%'
    NEW_PING_PRICING_YELLOW_FROM = (By.XPATH, '//label[text()="Yellow From:"]/../following-sibling::div//input')
    NEW_PING_PRICING_YELLOW_FROM_DEFAULT = '104%'
    NEW_PING_PRICING_YELLOW_TO = (By.XPATH, '//label[text()="Yellow To:"]/../following-sibling::div//input')
    NEW_PING_PRICING_YELLOW_TO_DEFAULT = '107%'
    NEW_PING_PRICING_AND_YELLOW_FROM = (By.XPATH, '//label[text()="& Yellow From:"]/../following-sibling::div//input')
    NEW_PING_PRICING_AND_YELLOW_FROM_DEFAULT = '92%'
    NEW_PING_PRICING_AND_YELLOW_TO = (By.XPATH, '//label[text()="& Yellow To:"]/../following-sibling::div//input')
    NEW_PING_PRICING_AND_YELLOW_TO_DEFAULT = '95%'
    NEW_PING_PRICING_GREEN_FROM = (By.XPATH, '//label[text()="Green From:"]/../following-sibling::div//input')
    NEW_PING_PRICING_GREEN_FROM_DEFAULT = '96%'
    NEW_PING_PRICING_GREEN_TO = (By.XPATH, '//label[text()="Green To:"]/../following-sibling::div//input')
    NEW_PING_PRICING_GREEN_TO_DEFAULT = '103%'
    NEW_PING_PRICING_INDICATOR_SETTINGS_TITLES = ['Red Above:', 'Red Below:', 'Yellow From:', 'Yellow To:',
                                                  '& Yellow From:', '& Yellow To:', 'Green From:', 'Green To:']
    PING_II_EDIT_BTN = (By.XPATH, '//div[contains(@class, "ant-card-head-title") and contains(., "Ping II / Market")]/'
                                  'following-sibling::div//button')
    PING_II_SAVE_BTN = (By.XPATH, '//button[contains(., "Save")]')
    PING_II_SUCCESS_MESSAGE = (By.XPATH, '//span//span[contains(., "Saved successfully")]')
    EDIT_NEW_PING_PRICING_INDICATOR_SETTINGS_BTN = \
        (By.XPATH, '//div[contains(@class, "ant-card-head-title") and contains'
                   '(., "New Ping Pricing Indicator Settings")]/following-sibling::div//button')
    SAVE_NEW_PING_PRICING_INDICATOR_SETTINGS_BTN = (By.XPATH, '//button[contains(., "Save")]')
    PING_II_RESTORE_DEFAULTS_BTN = (By.XPATH, '//button[contains(., "Restore Defaults")]')
    RESTORE_AGE_BUCKETS_CHECKBOX = \
        (By.XPATH, '//span[contains(., "Restore Age Buckets?")]/following-sibling::label/span')
    RESTORE_DEFAULTS_CONFIRM_BTN = (By.XPATH, "//button[contains(., 'Yes')]")
    # Age Buckets
    BUCKET_ELEMENT = (By.XPATH, '//td[contains (., "+ Days")]')
    AGE_BUCKETS_ROW = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr')
    AGE_BUCKET_TABLE = (By.XPATH, '//table[contains(., "Min Market %")]/tbody')
    AGE_BUCKET1_SIZE_INPUT = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[3]//input')
    AGE_BUCKET1_SIZE_INCREASE_BUTTON = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[3]//span')
    AGE_BUCKET1_MIN_MARKET_VALUE = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[4]//input')
    AGE_BUCKET1_MIN_MARKET_INPUT = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[5]//input')
    AGE_BUCKET1_MIN_MARKET_MORE_BTN = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[5]//'
                                                 'span[@class="ant-input-number-handler-up-inner anticon anticon-up"]')
    AGE_BUCKET1_MAX_MARKET_VALUE = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[5]//input')
    AGE_BUCKET1_MAX_MARKET_INPUT = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[6]//input')
    AGE_BUCKET1_MAX_MARKET_MORE_BTN = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[6]//'
                                                 'span[@class="ant-input-number-handler-up-inner anticon anticon-up"]')
    AGE_BUCKET1_MIN_GROSS_VALUE = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[6]//input')
    AGE_BUCKET1_MIN_GROSS_INPUT = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[7]//input')
    AGE_BUCKET1_MIN_GROSS_MORE_BTN = (By.XPATH, '//table[contains(., "Min Market %")]/tbody/tr[1]/td[7]//'
                                                'span[@class="ant-input-number-handler-up-inner anticon anticon-up"]')
    AGE_BUCKETS_DEFAULT_VALUES = ['15', '15', '15', '15', '15', '0']
    AGE_BUCKETS_7TH_BUCKET_DEFAULTS = ['84', '87', '0']
    AGE_BUCKETS_8TH_BUCKET_DEFAULTS = ['80', '83', '0']
    AGE_BUCKETS_EDIT_BTN = (By.XPATH, '(//div[contains(@class, "ant-card-head-title") and contains(., "Age Buckets")]'
                                      '/following-sibling::div//button)[1]')
    AGE_BUCKETS_NEW_BTN = (By.XPATH, '(//button[contains (., "New")])[2]')
    AGE_BUCKETS_DELETE_BTN = (By.XPATH, '//button[contains(., "Delete")]')
    AGE_BUCKETS_OK_CONFIRM_BTN = (By.XPATH, '//button[contains(., "OK")]')
    AGE_BUCKETS_SAVE_BTN = (By.XPATH, '//button[contains(., "Save")]')
    AGE_BUCKETS_MAX_NUMBER = 8
    AGE_BUCKETS_MAX_NUMBER_NOTIFICATION = (By.XPATH, '//span//span[contains(., "Maximum items added")]')
    AGE_BUCKETS_NO_BUCKETS = (By.XPATH, '//p[text()="No Data"]')
    AGE_BUCKETS_BUCKET_ONE_CHECKBOX = (By.XPATH, '(//span[@class="ant-checkbox"])[2]')
    AGE_BUCKETS_ALL_BUCKETS_CHECKBOX = (By.XPATH, '(//span[@class="ant-checkbox"])[1]')
    FL_AGE_BUCKETS_ROW = (
        By.XPATH, '//div[contains(@class, "ant-space-item") and contains(., " FirstLook Age Buckets")]//table/tbody/tr')
    FL_AGE_BUCKET_TABLE = (
        By.XPATH, '//div[contains(@class, "ant-space-item") and contains(., " FirstLook Age Buckets")]//table/tbody')
    FL_AGE_BUCKETS_DEFAULT_VALUES = ['30', '10', '10', '10', '0']
    FL_AGE_BUCKETS_EDIT_BTN = (By.XPATH, '//div[contains(@class, "ant-card-head-title") and contains'
                                         '(., "FirstLook Age Buckets")]/following-sibling::div//button')
    FL_AGE_BUCKETS_WATCHLIST_BTN = (By.XPATH, '//button//span[contains(., "Watch List")]/..')
    # Lights/Risk
    LIGHTS_RISK_DEALER_CIA_PREFERENCE_EDIT_BTN = \
        (By.XPATH, '//div[text()="Dealer C I A Preference"]/following-sibling::div//button[contains(., "Edit")]')
    LIGHTS_RISK_DEALER_CIA_PREFERENCE_SAVE_BTN = \
        (By.XPATH, '//div[text()="Dealer C I A Preference"]/following-sibling::div//button[contains(., "Save")]')
    LIGHTS_RISK_DEALER_RISK_EDIT_BTN = \
        (By.XPATH, '//div[text()="Dealer Risk"]/following-sibling::div//button[contains(., "Edit")]')
    LIGHTS_RISK_DEALER_RISK_SAVE_BTN = \
        (By.XPATH, '//div[text()="Dealer Risk"]/following-sibling::div//button[contains(., "Save")]')
    LIGHTS_RISK_DEALER_RISK_CANCEL_BTN = \
        (By.XPATH, '//div[text()="Dealer Risk"]/following-sibling::div//button[contains(., "Cancel")]')
    LIGHTS_RISK_FORM_VALIDATION_FAILED_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-alert-message") and contains(., "Form validation failed")]')
    LIGHTS_RISK_LIGHT_TARGETS_ALERT = (By.XPATH, '//span//span[contains(., "Total of Light Targets should be 100%")] ')
    LIGHTS_RISK_TARGET_DAYS_SUPPLY = \
        (By.XPATH, '//label[text()="Target Days Supply:"]/../following-sibling::div//input')
    LIGHTS_RISK_TARGET_DAYS_SUPPLY_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Target Days Supply:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD = \
        (By.XPATH, '//label[text()="Creation Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_UNIT_COST_BUCKETS_CREATION_THRESHOLD_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Creation Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD = \
        (By.XPATH, '//label[text()="Allocation Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_UNIT_COST_BUCKETS_ALLOCATION_THRESHOLD_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Allocation Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD = \
        (By.XPATH, '//label[text()="Display Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_MARKET_PERFORMERS_DISPLAY_THRESHOLD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Display Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD = \
        (By.XPATH, '//label[text()="In Stock Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_MARKET_PERFORMERS_IN_STOCK_THRESHOLD_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="In Stock Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD = \
        (By.XPATH, '//label[text()="Zip Code Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_MARKET_PERFORMERS_ZIP_CODE_THRESHOLD_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Zip Code Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD = \
        (By.XPATH, '//label[text()="Units Threshold:"]/../following-sibling::div//input')
    LIGHTS_RISK_MARKET_PERFORMERS_UNITS_THRESHOLD_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Units Threshold:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_BASIS_PERIODS_LIGHTS_DETERMINATION = \
        (By.XPATH, '//label[text()="Lights Determination:"]/../following-sibling::div//span')
    LIGHTS_RISK_BASIS_PERIODS_LIGHTS_DETERMINATION_VALUE = \
        (By.XPATH, '//label[text()="Lights Determination:"]/../following-sibling::div')
    LIGHTS_RISK_BASIS_PERIODS_SALES_HISTORY = \
        (By.XPATH, '//label[text()="Sales History:"]/../following-sibling::div//span')
    LIGHTS_RISK_BASIS_PERIODS_SALES_HISTORY_VALUE = \
        (By.XPATH, '//label[text()="Sales History:"]/../following-sibling::div')
    LIGHTS_RISK_CIA_BASIS_PERIODS_STORE_TARGET_INVENTORY = \
        (By.XPATH, '//label[text()="Store Target Inventory:"]/../following-sibling::div//span')
    LIGHTS_RISK_CIA_BASIS_PERIODS_STORE_TARGET_INVENTORY_VALUE = \
        (By.XPATH, '//label[text()="Store Target Inventory:"]/../following-sibling::div')
    LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION = \
        (By.XPATH, '//label[text()="Core Model Determination:"]/../following-sibling::div//span')
    LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_DETERMINATION_VALUE = \
        (By.XPATH, '//label[text()="Core Model Determination:"]/../following-sibling::div')
    LIGHTS_RISK_CIA_BASIS_PERIODS_POWERZONE_TARGET_INVENTORY = \
        (By.XPATH, '//label[text()="Powerzone Target Inventory:"]/../following-sibling::div//span')
    LIGHTS_RISK_CIA_BASIS_PERIODS_POWERZONE_TARGET_INVENTORY_VALUE = \
        (By.XPATH, '//label[text()="Powerzone Target Inventory:"]/../following-sibling::div')
    LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_YEAR_ALLOCATION = \
        (By.XPATH, '//label[text()="Core Model Year Allocation:"]/../following-sibling::div//span')
    LIGHTS_RISK_CIA_BASIS_PERIODS_CORE_MODEL_YEAR_ALLOCATION_VALUE = \
        (By.XPATH, '//label[text()="Core Model Year Allocation:"]/../following-sibling::div')
    LIGHTS_RISK_LIGHT_TARGETS_RED = (By.XPATH, '//label[text()="Red %:"]/../following-sibling::div//input')
    LIGHTS_RISK_LIGHT_TARGETS_YELLOW = (By.XPATH, '//label[text()="Yellow %:"]/../following-sibling::div//input')
    LIGHTS_RISK_LIGHT_TARGETS_GREEN = (By.XPATH, '//label[text()="Green %:"]/../following-sibling::div//input')
    LIGHTS_RISK_LIGHT_TARGETS_GREEN_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Green %:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_LIGHT_TARGETS_GREEN_DECREASE_BTN = \
        (By.XPATH, '//label[text()="Green %:"]/../following-sibling::div//span[@aria-label="Decrease Value"]')
    LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET = \
        (By.XPATH, '//label[text()="Initial Time Period Year Offset:"]/../following-sibling::div//input')
    LIGHTS_RISK_YEAR_THRESHOLDS_INITIAL_TIME_PERIOD_YEAR_OFFSET_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Initial Time Period Year Offset:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET = \
        (By.XPATH, '//label[text()="Secondary Time Period Year Offset:"]/../following-sibling::div//input')
    LIGHTS_RISK_YEAR_THRESHOLDS_SECONDARY_TIME_PERIOD_YEAR_OFFSET_INCREASE_BTN = \
        (By.XPATH,
         '//label[text()="Secondary Time Period Year Offset:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH = \
        (By.XPATH, '//label[text()="Roll Over Month:"]/../following-sibling::div//input')
    LIGHTS_RISK_YEAR_THRESHOLDS_ROLL_OVER_MONTH_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Roll Over Month:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS = \
        (By.XPATH, '//label[text()="# Weeks:"]/../following-sibling::div//input')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_WEEKS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="# Weeks:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS = \
        (By.XPATH, '//label[text()="# Deals:"]/../following-sibling::div//input')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_DEALS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="# Deals:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS = \
        (By.XPATH, '//label[text()="# of Contributors:"]/../following-sibling::div//input')
    LIGHTS_RISK_RISK_LEVEL_THRESHOLDS_NUM_OF_CONTRIBUTORS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="# of Contributors:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE = \
        (By.XPATH, '//label[text()="No Sale >:"]/../following-sibling::div//input')
    LIGHTS_RISK_RED_LIGHT_THRESHOLDS_NO_SALE_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="No Sale >:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS = \
        (By.XPATH, '//label[text()="Gross Profit <=:"]/../following-sibling::div//input')
    LIGHTS_RISK_RED_LIGHT_THRESHOLDS_GROSS_PROFIT_LESS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Gross Profit <=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS = \
        (By.XPATH, '//label[text()="No Sale <:"]/../following-sibling::div//input')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_NO_SALE_LESS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="No Sale <:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE = \
        (By.XPATH, '//label[text()="Gross Profit >=:"]/../following-sibling::div//input')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_GROSS_PROFIT_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Gross Profit >=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE = \
        (By.XPATH, '//label[text()="Margin >=:"]/../following-sibling::div//input')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_MARGIN_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Margin >=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS = \
        (By.XPATH, '//label[text()="Days % <=:"]/../following-sibling::div//input')
    LIGHTS_RISK_GREEN_LIGHT_THRESHOLDS_DAYS_PERCENTAGE_LESS_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Days % <=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE = \
        (By.XPATH, '//label[text()="Year >=:"]/../following-sibling::div//input')
    LIGHTS_RISK_AGE_BAND_TARGETS_YEAR_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Year >=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE = \
        (By.XPATH, '//label[text()="Overall >=:"]/../following-sibling::div//input')
    LIGHTS_RISK_AGE_BAND_TARGETS_OVERALL_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Overall >=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')
    LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE = \
        (By.XPATH, '//label[text()="Red Light >=:"]/../following-sibling::div//input')
    LIGHTS_RISK_AGE_BAND_TARGETS_RED_LIGHT_MORE_INCREASE_BTN = \
        (By.XPATH, '//label[text()="Red Light >=:"]/../following-sibling::div//span[@aria-label="Increase Value"]')

    # 'Book Valuations Settings' tab
    BOOK_VALUATIONS_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Book Valuations")]')
    GUIDE_BOOK_ONE_NAME = \
        (By.XPATH, '//div[contains(., "Guide Book One") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[1]//span')
    GUIDE_BOOK_ONE_DEFAULT = 'Galves'
    GUIDE_BOOK_ONE_1ST_TYPE = \
        (By.XPATH, '//div[contains(., "Guide Book One") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[2]//span')
    GUIDE_BOOK_ONE_1ST_TYPE_DEFAULT = 'Trade-In'
    GUIDE_BOOK_ONE_2D_TYPE = \
        (By.XPATH, '//div[contains(., "Guide Book One") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[3]//span')
    GUIDE_BOOK_ONE_2D_TYPE_DEFAULT = 'None'
    GUIDE_BOOK_TWO_NAME = \
        (By.XPATH, '//div[contains(., "Guide Book Two") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[1]//span')
    GUIDE_BOOK_TWO_1ST_TYPE = \
        (By.XPATH, '//div[contains(., "Guide Book Two") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[2]//span')
    GUIDE_BOOK_TWO_2D_TYPE = \
        (By.XPATH, '//div[contains(., "Guide Book Two") and contains(@class, "ant-card-small")]//table//tr[contains'
                   '(., "Guide book name")]/following-sibling::tr[1]/td[3]//span')
    ENABLE_SECOND_GUIDE_BOOK_BTN = \
        (By.XPATH, '//button[contains(., " Enable ") and contains(., "Second") and contains(., " Guide Book")]')
    REMOVE_GUIDE_BOOK_ONE_BTN = (By.XPATH, '(//button[contains(., "Remove")])[1]')
    REMOVE_GUIDE_BOOK_TWO_BTN = (By.XPATH, '(//button[contains(., "Remove")])[2]')
    BOOK_VALUATIONS_OK_BTN = (By.XPATH, '//button[contains(., "OK")]')
    GUIDE_BOOK_TWO_TITLE = (By.XPATH, '//div[text()="Guide Book Two"]')
    KBB_CONSUMER_TOOL_TITLE = (By.XPATH, '//div[text()="KBB Consumer Tool"]')
    GALVES_SPECIFIC_SETTINGS_TITLE = (By.XPATH, '//div[text()="Galves Specific Settings"]')
    EDIT_GALVES_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="Galves Specific Settings"]/following-sibling::div//button[contains(., "Edit")]')
    SAVE_GALVES_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="Galves Specific Settings"]/following-sibling::div//button[contains(., "Save")]')
    ENABLE_MOBILE_GALVES_BTN = (By.XPATH, '//label[text()="Enable Mobile Galves:"]/../following-sibling::div//button')
    BLACKBOOK_SPECIFIC_SETTINGS_TITLE = (By.XPATH, '//div[text()="BlackBook Specific Settings"]')
    EDIT_BLACKBOOK_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="BlackBook Specific Settings"]/following-sibling::div//button[contains(., "Edit")]')
    SAVE_BLACKBOOK_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="BlackBook Specific Settings"]/following-sibling::div//button[contains(., "Save")]')
    ENABLE_MOBILE_BLACKBOOK_BTN = \
        (By.XPATH, '//label[text()="Enable Mobile BlackBook:"]/../following-sibling::div//button')
    KBB_SPECIFIC_SETTINGS_TITLE = (By.XPATH, '//div[text()="KBB Specific Settings"]')
    EDIT_KBB_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="KBB Specific Settings"]/following-sibling::div//button[contains(., "Edit")]')
    SAVE_KBB_SPECIFIC_SETTINGS_BTN = \
        (By.XPATH, '//div[text()="KBB Specific Settings"]/following-sibling::div//button[contains(., "Save")]')
    KBB_SPECIFIC_SETTINGS_OTHER_DROPDOWN_OPTION = \
        (By.XPATH, '//div[contains(@class, "ant-slide-up-enter-active")]//div[not(@aria-selected) '
                   'and (@role="option")]')
    NEWEST_DEFAULT_INVENTORY_CONDITION = \
        (By.XPATH, '//label[text()="Newest Default Inventory Condition:"]/../following-sibling::div//span[2]')
    KBB_INVENTORY_DATASET = \
        (By.XPATH, '//label[text()="KBB Inventory Dataset:"]/../following-sibling::div//span[2]')
    KBB_APPRAISAL_DATASET = \
        (By.XPATH, '//label[text()="KBB Appraisal Dataset:"]/../following-sibling::div//span[2]')
    NEWEST_DEFAULT_INVENTORY_CONDITION_DEFAULT_VALUE = 'Fair'
    EDIT_GUIDE_BOOK_ONE_BTN = \
        (By.XPATH, '//div[text()="Guide Book One"]/following-sibling::div//button[contains(., "Edit")]')
    EDIT_GUIDE_BOOK_TWO_BTN = \
        (By.XPATH, '//div[text()="Guide Book Two"]/following-sibling::div//button[contains(., "Edit")]')
    SELECT_BOOK_NAME = (By.XPATH, '//label[text()="Guide Book"]/../following-sibling::div')
    BOOK_NAME_VALUE_IN_INPUT = (By.XPATH, '//label[text()="Guide Book"]/../following-sibling::div//span[2]')
    SELECT_BOOK_1ST_TYPE = (By.XPATH, '//label[text()="1st Type"]/../following-sibling::div')
    BOOK_1ST_TYPE_VALUE_IN_INPUT = (By.XPATH, '//label[text()="1st Type"]/../following-sibling::div//span[2]')
    SELECT_BOOK_2ND_TYPE = (By.XPATH, '//label[text()="2nd Type"]/../following-sibling::div')
    BOOK_2ND_TYPE_VALUE_IN_INPUT = (By.XPATH, '//label[text()="2nd Type"]/../following-sibling::div//span[2]')
    BOOK_DROPDOWN_LIST_OPTIONS = \
        (By.XPATH, '//div[contains(@class, "ant-modal-footer")]/following-sibling::div//div[@role="listbox"]/div')
    CLEAR_BOOK_2ND_TYPE_INPUT_BTN = (By.CLASS_NAME, 'ant-select-clear')
    BOOKS_JD_POWER_AS_3RD_BOOK_BTN = (By.XPATH,
                                      '//td/h4[text()="J.D. Power as 3rd book"]/../following-sibling::td/button')
    BOOKS_KBB_TRADE_IN_VALUES_BTN = (By.XPATH, '//td/h4[text()="KBB Trade-In Values"]/../following-sibling::td/button')
    BOOKS_MANHEIM_INTEGRATION_BTN = (By.XPATH, '//td/h4[text()="Manheim Integration"]/../following-sibling::td/button')
    BOOKS_JD_POWER_AS_3RD_BOOK_START_DATE = \
        (By.XPATH, '//td/h4[text()="J.D. Power as 3rd book"]/../following-sibling::td[2]')
    BOOKS_KBB_TRADE_IN_VALUES_START_DATE = \
        (By.XPATH, '//td[text()="KBB Trade-In Values"]/following-sibling::td[3]//input')
    BOOKS_MANHEIM_INTEGRATION_START_DATE = \
        (By.XPATH, '//td[text()="Manheim Integration"]/following-sibling::td[3]//input')
    BOOKS_EDIT_UPGRADES_BTN = \
        (By.XPATH, '//div[text()="Dealer Upgrades"]/following-sibling::div//button[contains(., "Edit")]')
    BOOKS_SAVE_UPGRADES_BTN = \
        (By.XPATH, '//div[text()="Dealer Upgrades"]/following-sibling::div//button[contains(., "Save")]')
    BOOKS_CONFIRM_CHANGES_UPGRADES_BTN = (By.XPATH, '//button[contains(., "OK")]')
    BOOKS_UPGRADES_DISABLE_ALL_BTN = (By.XPATH, '//button[contains(., "Disable All")]')
    BOOKS_UPGRADES_ENABLE_ALL_BTN = (By.XPATH, '//button[contains(., "Enable All")]')
    BOOKS_PAGE_BOTTOM = (By.XPATH, '//h4[text()="Applications"]')
    DISPLAY_TRAIDIN_VALUES_ON_KBB_CONSUMER_TOOL_BTN = \
        (By.XPATH,
         '//label[text()="Display TradeIn Values on the KBB Consumer Tool:"]/../following-sibling::div//button')
    DISPLAY_RETAIL_VALUES_ON_KBB_CONSUMER_TOOL_BTN = \
        (By.XPATH,
         '//label[text()="Display Retail Values on the KBB Consumer Tool:"]/../following-sibling::div//button')
    DISPLAY_LENDING_VALUES_ON_KBB_CONSUMER_TOOL_BTN = \
        (By.XPATH,
         '//label[text()="Display Lending Values on the KBB Consumer Tool:"]/../following-sibling::div//button')
    KBB_CONSUMER_TOOL_EDIT_BTN = \
        (By.XPATH, '//div[text()="KBB Consumer Tool"]/following-sibling::div//button[contains(., "Edit")]')
    KBB_CONSUMER_TOOL_SAVE_BTN = \
        (By.XPATH, '//div[text()="KBB Consumer Tool"]/following-sibling::div//button[contains(., "Save")]')
    BOOKOUT_AGREED_TO_BTN = (By.XPATH, '//label[text()="Bookout Agreed To:"]/../following-sibling::div//button')
    CALCULATE_AVG_BOOK_VALUES_BTN = \
        (By.XPATH, '//label[text()="Calculate Average Book Values:"]/../following-sibling::div//button')
    SET_ADVERTISING_STATUS_BTN = \
        (By.XPATH, '//label[text()="Set Advertising Status:"]/../following-sibling::div//button')
    COMMON_EDIT_BTN = \
        (By.XPATH, '//div[text()="Common"]/following-sibling::div//button[contains(., "Edit")]')
    COMMON_SAVE_BTN = \
        (By.XPATH, '//div[text()="Common"]/following-sibling::div//button[contains(., "Save")]')

    # 'Decoding' tab
    DECODING_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(.,"Decoding")]')
    DECODING_CHECKBOX_STATUS = (By.XPATH, '//input[@type="checkbox"]/..')

    # Drop-downs
    ACTIVE_DROPDOWN_OPTION = (By.XPATH, '//div[contains(@class, "ant-slide-up-enter-active")]//div[@role="option"]/div')
    CURRENT_DATE_IN_CALENDER = \
        (By.XPATH, '//table[@class="ant-picker-content"]//td[contains(@class, "ant-picker-cell-selected")]/div')

    @allure.step("Getting check-box names")
    def get_checkbox_name_decoding(self, checkbox_status_locator: tuple, checkbox_num=1):
        """Works for 'Decoding' and 'Miscellaneous Settings' tab"""
        checkbox_name_path = f'({checkbox_status_locator[1]}/following-sibling::span)[{checkbox_num}]'
        name_locator = (By.XPATH, checkbox_name_path)
        return self.get_text(name_locator)

    @allure.step("Getting check-box names for 'Alerts'")
    def get_checkbox_name_alerts_tab(self, checkbox_name_locator: tuple, checkbox_num=1):
        """Works for 'Alerts' tab"""
        if checkbox_num % 2 == 0:
            row_num = checkbox_num // 2
            column_name = 'Alert in E-mail'
        else:
            row_num = (checkbox_num + 1) // 2
            column_name = 'Display on Dashboard'
        checkbox_name_path = f'({checkbox_name_locator[1]})[{row_num}]'
        name_locator = (By.XPATH, checkbox_name_path)
        return column_name, self.get_text(name_locator)

    @allure.step("Getting locator for a new value from dropdown in 'Ping II'")
    def get_other_value_for_ping_2_dropdowns(self, current_value, all_values):
        values_to_select = [i for i in all_values if i != current_value]
        new_value = random.choice(values_to_select)
        new_value_path = \
            f'(//div[contains(@role, "listbox")])[5]/div[{all_values.index(new_value) + 1}]'
        new_value_locator = (By.XPATH, new_value_path)
        with allure.step(f"New value selected from '{all_values}': '{new_value}'. Old value was: {current_value}. "
                         f"Locator: {new_value_locator}"):
            return new_value_locator

    @allure.step("Editing 'New Ping Pricing Indicator Settings'")
    def edit_new_ping_pricing_indicator_settings(self, setting_name: str, action='up', num_clicks=1):
        """Increase or decrease the value of the provided New Ping Pricing Indicator setting.
        Action options: 'up' (by default) or 'down'"""
        setting_input_path = f'//div/label[text()="{setting_name}"]/../following-sibling::div//input'
        setting_input_locator = (By.XPATH, setting_input_path)
        setting_input = self.locate_element(setting_input_locator)
        self.click(setting_input)
        time.sleep(1)
        if action != 'up':
            action_button_path = f'(//div/label[text()="{setting_name}"]/../following-sibling::div//span)[3]'
        else:
            action_button_path = f'(//div/label[text()="{setting_name}"]/../following-sibling::div//span)[1]'
        action_button_locator = (By.XPATH, action_button_path)
        action_button = self.get_clickable_element(action_button_locator)
        with allure.step(f"Modifying '{setting_name}', clicking '{action}' button {num_clicks} times"):
            for _ in range(num_clicks):
                self.click(action_button)
        time.sleep(TIMEOUT)

    @allure.step("Changing size of Age Bucket")
    def change_size_of_age_bucket(self, bucket_num: int, action='up', num_clicks=1):
        """Increase or decrease the size of the provided Age Bucket. Action options: 'up' (by default) or 'down'"""
        age_bucket_input_path = f'{self.AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[3]//input'
        age_bucket_input_locator = (By.XPATH, age_bucket_input_path)
        age_bucket_input = self.locate_element(age_bucket_input_locator)
        self.click(age_bucket_input)
        time.sleep(1)
        if action != 'up':
            action_button_path = f'({self.AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[3]//span)[3]'
        else:
            action_button_path = f'({self.AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[3]//span)[1]'
        action_button_locator = (By.XPATH, action_button_path)
        action_button = self.get_clickable_element(action_button_locator)
        with allure.step(f"Modifying Age Bucket '{bucket_num}' size, clicking '{action}' button {num_clicks} times"):
            for _ in range(num_clicks):
                self.click(action_button)
            time.sleep(TIMEOUT)

    @allure.step("Changing size of Firstlook Age Bucket")
    def change_size_of_firstlook_age_bucket(self, bucket_num: int, action='up', num_clicks=1):
        """Increase or decrease the size of the provided Firstlook Age Bucket.
        Action options: 'up' (by default) or 'down'"""
        fl_age_bucket_input_path = f'{self.FL_AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[2]//input'
        fl_age_bucket_input_locator = (By.XPATH, fl_age_bucket_input_path)
        fl_age_bucket_input = self.locate_element(fl_age_bucket_input_locator)
        self.click(fl_age_bucket_input)
        time.sleep(1)
        if action != 'up':
            action_button_path = f'({self.FL_AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[2]//span)[3]'
        else:
            action_button_path = f'({self.FL_AGE_BUCKET_TABLE[1]}/tr[{bucket_num}]/td[2]//span)[1]'
        action_button_locator = (By.XPATH, action_button_path)
        action_button = self.get_clickable_element(action_button_locator)
        with allure.step(f"Modifying FirstLook Age Bucket '{bucket_num}' size, clicking '{action}' button "
                         f"{num_clicks} times"):
            for _ in range(num_clicks):
                self.click(action_button)
            time.sleep(TIMEOUT)

    @allure.step("Editing Guide Book Name")
    def edit_guide_book_name(self, new_value):
        """Edit Guide Book One or Two Name to a new vale."""
        field_input = self.locate_element(self.SELECT_BOOK_NAME)
        self.click(field_input)
        time.sleep(TIMEOUT)
        options = self.locate_all_elements(self.ACTIVE_DROPDOWN_OPTION)
        all_options_list = []
        for option in options:
            all_options_list.append(option.text)
        if new_value in all_options_list:
            with allure.step(f"Selecting '{new_value}' as the new Book Name and saving the changes"):
                new_option_path = f'//div[contains(@class, "ant-slide-up-enter-active")]//div[text()="{new_value}"]'
                new_value_locator = (By.XPATH, new_option_path)
                new_option = self.locate_element(new_value_locator)
                self.click(new_option)
                ok_btn = self.get_clickable_element(self.BOOK_VALUATIONS_OK_BTN)
                self.click(ok_btn)
        else:
            with allure.step(f"'{new_value}' is not a valid Book Name!"):
                pass

    @allure.step("Getting a new random Franchise in 'Setting'")
    def select_random_franchise(self, current_values=None):
        franchises_input = self.locate_element(self.FRANCHISES_INPUT)
        self.click(franchises_input)
        time.sleep(TIMEOUT)
        franchise_search_input = self.locate_element(self.FRANCHISES_SEARCH_INPUT)
        self.click(franchise_search_input)
        time.sleep(TIMEOUT)
        options = self.locate_all_elements(self.FRANCHISES_OPTION)
        all_franchises = []
        for option in options:
            all_franchises.append(option.text)
        if current_values:
            all_franchises = [i for i in all_franchises if i not in current_values]
        new_value = random.choice(all_franchises)
        with allure.step(f"Selecting new value from 'Franchises': '{new_value}' additionally to the current values: "
                         f"'{current_values}'"):
            self.paste_text(self.FRANCHISES_SEARCH_INPUT, new_value)
            time.sleep(TIMEOUT)
            search_btn = self.get_clickable_element(self.FRANCHISES_SEARCH_BTN)
            self.click(search_btn)
            time.sleep(TIMEOUT)
            new_value_path = f'//div[text()="{new_value}"]'
            new_value_locator = (By.XPATH, new_value_path)
            new_value_option = self.locate_element(new_value_locator)
            self.click(new_value_option)
            time.sleep(TIMEOUT)

    @allure.step("Getting a random valid Zip Code")
    def get_random_zip_code(self, current_zip_code=None):
        zip_codes = ['14067', '14080', '14112', '14427', '14516', '14568', '14611', '14625', '14708', '14742']
        if current_zip_code:
            zip_codes = [i for i in zip_codes if i != current_zip_code]
        new_zip_code = random.choice(zip_codes)
        with allure.step(f"New value for 'Zip Code': '{new_zip_code}'"):
            return new_zip_code

    @allure.step("Selecting and adding a random Access Group in 'General Settings'")
    def select_random_access_group(self, current_groups=None):
        group_examples = ['ADESA', 'ADESA - Acura', 'ADESA - Alfa Romeo', 'ADESA - Aston Martin', 'ADESA - Audi',
                          'ADESA - Bentley', 'ADESA - BMW', 'ADESA - Bugatti']
        select_input = self.locate_element(self.SELECT_ACCESS_GROUP_INPUT)
        self.click(select_input)
        time.sleep(TIMEOUT)
        if current_groups:
            group_examples = [i for i in group_examples if i not in current_groups]
        new_access_group = random.choice(group_examples)
        with allure.step(f"Adding a new Access Group: '{new_access_group}' to the list of groups"):
            new_group_path = f'//div[text()="{new_access_group}"]'
            new_group_locator = (By.XPATH, new_group_path)
            new_group_option = self.locate_element(new_group_locator)
            self.click(new_group_option)
            time.sleep(TIMEOUT)
            add_btn = self.get_clickable_element(self.ADD_ACCESS_GROUP_BTN)
            self.click(add_btn)
            time.sleep(TIMEOUT)
            return new_access_group

    @allure.step("Removing Access Group in 'General Settings'")
    def remove_access_group(self, access_group):
        remove_btn_path = f'//div[@class="ant-space-item" and text()="{access_group}"]/following-sibling::div//button'
        remove_btn = self.locate_element((By.XPATH, remove_btn_path))
        self.click(remove_btn)
        time.sleep(TIMEOUT)
        ok_btn = self.get_clickable_element(self.ACCESS_GROUPS_OK_BTN)
        self.click(ok_btn)
        time.sleep(TIMEOUT)

    @allure.step("Selecting a new random option from drop-down")
    def select_random_value_from_dropdown(self, input_locator, default_value=None):
        dropdown_input = self.locate_element(input_locator)
        self.click(dropdown_input)
        time.sleep(TIMEOUT)
        options = self.locate_all_elements(self.ACTIVE_DROPDOWN_OPTION)
        all_options_list = []
        for option in options:
            all_options_list.append(option.text)
        if default_value:
            all_options_list = [i for i in all_options_list if i != default_value]
        new_option = random.choice(all_options_list)
        with allure.step(f"Selecting new value from '{input_locator}': '{new_option}' instead of '{default_value}'"):
            new_option_path = f'//div[contains(@class, "ant-slide-up-enter-active")]//div[text()="{new_option}"]'
            new_value_locator = (By.XPATH, new_option_path)
            new_option = self.locate_element(new_value_locator)
            self.click(new_option)
            time.sleep(TIMEOUT)

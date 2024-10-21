import time

from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import allure
import string
import random

TIMEOUT = 4


class CreateNewDealerPage(BasePage):
    PATH = "dealers"
    CREATE_NEW_DEALER_FORM_TITLE = (By.CSS_SELECTOR, '.ant-page-header-heading-title')
    FORM_TITLE_TEXT = "Create New Dealer"

    # Fields & Values
    GROUP_INPUT = (By.XPATH, '//div[div[label[contains(.,"Dealer Group")]]]//input')
    GROUP_NAME = "Windy City Demo Auto Group (101589)"
    SELECT_GROUP_NAME = (
        By.XPATH, '//div[contains(@class, "ant-select-item-option-content") and contains(., "Windy City Demo")]')
    NAME = (By.XPATH, '(//form//div[2]//input)[2]')
    SHORT_NAME = (By.XPATH, '//form//div[4]//input')
    GO_LIVE_DATE = (By.XPATH, '//input[contains(@placeholder, "Select date")]')
    FRANCHISES = (By.XPATH, '//div[contains(@class, "ant-select-selection-search")]/input')
    RUN_DAY_OF_WEEK = (By.XPATH, '//form//div[7]//span[2]')
    RUN_DAY_OF_WEEK_VALUE = 'Sunday'
    PACK_AMOUNT = (By.XPATH, '//form//div[8]//input')
    APPRAISAL_FORM_MEMO = (By.XPATH, '//form//div[9]//input')
    APPRAISAL_FORM_MEMO_LABEL = (By.XPATH, '//label[contains(., "Appraisal Form Memo")]')
    APPRAISAL_FORM_MEMO_TEXT = 'Trade in value for purchase of a vehicle.'
    APPRAISAL_FORM_DISCLAIMER = (By.XPATH, '//form//div[10]//input')
    APPRAISAL_FORM_DISCLAIMER_LABEL = (By.XPATH, '//label[contains(., "Appraisal Form Disclaimer")]')
    APPRAISAL_FORM_DISCLAIMER_TEXT = \
        'The owner of this vehicle hereby affirms that it has not been damaged by flood or had frame damage.'
    GUIDE_BOOK_ONE = (By.XPATH, '//form//div[11]//span[2]')
    GUIDE_BOOK_ONE_LABEL = (By.XPATH, '//label[contains(., "Guide Book One")]')
    GUIDE_BOOK_ONE_VALUE = 'Galves'
    GUIDE_BOOK_ONE_1ST_TYPE = (By.XPATH, '//form//div[12]//span[2]')
    GUIDE_BOOK_ONE_1ST_TYPE_LABEL = (By.XPATH, '//label[contains(., "Guide Book One 1st Type")]')
    GUIDE_BOOK_ONE_1ST_TYPE_VALUE = 'Trade-In'
    GUIDE_BOOK_ONE_2ND_TYPE = (By.XPATH, '//form//div[13]//span[2]')
    GUIDE_BOOK_TWO = (By.XPATH, '//form//div[14]//input')
    GUIDE_BOOK_TWO_1ST_TYPE = (By.XPATH, '//form//div[15]//input')
    GUIDE_BOOK_TWO_2ND_TYPE = (By.XPATH, '//form//div[16]//input')
    WEBSITE_PREFIX = (By.XPATH, '//form//div[17]//input')
    WEBSITE = (By.XPATH, '//input[@name="Model.Website"]')
    WEBSITE_LABEL = (By.XPATH, '//label[contains(., "Website")]')
    GOOGLE_PLACE_ID = (By.XPATH, '//form//div[18]//input')
    GOOGLE_PLACE_ID_LABEL = (By.XPATH, '//label[contains(., "Google Place Id")]')
    OFFICE_PHONE = (By.XPATH, '//form//div[19]//input')
    ADDRESS = (By.XPATH, '//form//div[20]//input')
    ADDRESS_LABEL = (By.XPATH, '//label[contains(., "Address")]')
    CITY = (By.XPATH, '//form//div[21]//input')
    STATE = (By.XPATH, '//form//div[22]//input')
    STATE_LABEL = (By.XPATH, '//label[contains(., "State:")]')
    SELECT_SAMPLE_STATE = (By.XPATH, '//div[contains(@class, "ant-select-item-option-content") and text()="IL"]')

    ZIP_CODE = (By.XPATH, '//form//div[23]//input')
    SAMPLE_VALID_GOOGLE_PLACE_ID = 'ChIJl24c2LAY9ocR7gd7CpefUrY'
    SAMPLE_VALID_ZIP_CODE = "60606"
    LAT_LONG_MODAL = (By.XPATH, '//div[contains(@class, "ant-modal-body")]')

    # Alerts
    FORM_VALIDATION_FAILED_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-alert-message") and contains(., "Form validation failed")]')
    FORM_VALIDATION_FAILED_TEXT = 'Form validation failed. Check fields messages.'
    GROUP_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "GroupId")]')
    GROUP_REQUIRED_TEXT = 'The GroupId field is required.'
    NAME_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "The Name")]')
    NAME_REQUIRED_TEXT = 'The Name field is required.'
    SHORT_NAME_REQUIRED_ALERT = (By.XPATH,
                                 '//div[contains(@role, "alert") and contains(., "The ShortName")]')
    SHORT_NAME_REQUIRED_TEXT = 'The ShortName field is required.'
    STATE_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "State")]')
    STATE_REQUIRED_TEXT = 'Please select State before saving'
    ZIPCODE_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "ZipCode")]')
    ZIPCODE_REQUIRED_TEXT = 'The ZipCode field is required.'
    LATITUDE_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "Latitude")]')
    LATITUDE_REQUIRED_TEXT = 'The Latitude field is required.'
    LONGITUDE_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "Longitude")]')
    LONGITUDE_REQUIRED_TEXT = 'The Longitude field is required.'
    NAME_MUST_BE_UNIQUE_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-form-item-explain-error") and contains (., "Must be unique")]')
    NAME_MUST_BE_UNIQUE_TEXT = 'Must be unique for active dealer'
    MUST_BE_UNIQUE_TEXT = 'Must be unique'
    OTHER_DATE = None

    # Buttons
    ADD_NEW_DEALER_BTN = (By.XPATH, '//button[contains(@class, "ant-btn-default") and contains(.,"New Dealer")]')
    BY_ZIP_CODE_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"ZipCode")]')
    By_GOOGLE_PLACE_ID = (By.XPATH,
                          '//button[contains(@class, "ant-btn") and contains(.,"GooglePlaceId")]')
    SAVE_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    SUCCESS_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Go to created dealer")]')
    ADD_LAT_LONG_ONLY_LOCATION_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Only location")]')
    AUTOFILL_BTN = (By.XPATH, '//button[contains(@class, "ant-btn-text ant-btn-circle ant-btn-sm ant-btn-icon-only")]')
    CLEAR_GO_LIVE_DATE_BTN = (By.CLASS_NAME, 'ant-picker-clear')
    ACTIVE_BTN = (By.XPATH, '//button[contains(@role, "switch")]')

    @allure.step("Generating a new dealership data")
    def generate_new_dealer_data(self):
        """Generate test data for a new dealership"""
        new_dealer = dict()
        new_dealer['name'] = 'Test' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        new_dealer['website'] = f"{new_dealer['name'].lower()}.com"
        new_dealer['google_place_id'] = self.SAMPLE_VALID_GOOGLE_PLACE_ID
        new_dealer['office_phone'] = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        new_dealer['address'] = f"{''.join([str(random.randint(1, 9)) for _ in range(4)])} Sunrise Ave."
        new_dealer['city'] = "Chicago"
        new_dealer['state'] = 'IL'
        new_dealer['zip_code'] = self.SAMPLE_VALID_ZIP_CODE

        return new_dealer

    @allure.step("Filling 'Create New Dealer' form with the provided data and saving changes")
    def create_new_dealer(self,
                          dealer_group: str = GROUP_NAME,
                          name: str = '',
                          short_name: str = '',
                          website: str = '',
                          google_place_id: str = '',
                          address: str = '',
                          state: str = '',
                          zip_code: str = '',
                          calc_lat_long_by: str = 'zip_code'):
        """Fill 'Create new dealer' form with the provided data and click 'Save' (empty values by default)
        Options for calc_lat_long_by: zip_code, google_place_id. If no valid option provided, the step is skipped"""

        # 1. Open "Create New Dealer" form
        create_new_dealer_btn = self.get_clickable_element(self.ADD_NEW_DEALER_BTN)
        self.click(create_new_dealer_btn)
        time.sleep(TIMEOUT)
        self.get_clickable_element(self.SAVE_BTN)

        # 2. Enter provided data to the form
        if dealer_group == self.GROUP_NAME:
            self.paste_text(self.GROUP_INPUT, dealer_group)
            time.sleep(2)
            my_group = self.locate_element(self.SELECT_GROUP_NAME)
            self.click(my_group)
            time.sleep(1)
        else:
            pass
        self.paste_text(self.NAME, name)
        self.paste_text(self.SHORT_NAME, short_name)
        self.type_in_text(self.WEBSITE, website)
        self.paste_text(self.GOOGLE_PLACE_ID, google_place_id)
        self.type_in_text(self.ADDRESS, address)
        if state:
            self.paste_text(self.STATE, state)
            time.sleep(2)
            select_state = self.locate_element(self.SELECT_SAMPLE_STATE)
            self.click(select_state)
            time.sleep(1)
        self.paste_text(self.ZIP_CODE, zip_code)
        name_field = self.locate_element(self.NAME)
        self.click(name_field)

        # 3. Calculate Latitude & Longitude by Zip Code or by Google Place ID.
        if calc_lat_long_by == 'zip_code':
            lat_long_by_zipcode = self.get_clickable_element(self.BY_ZIP_CODE_BTN)
            self.click(lat_long_by_zipcode)
            self.locate_element(self.LAT_LONG_MODAL)
            time.sleep(TIMEOUT)
            add_location_only = self.get_clickable_element(self.ADD_LAT_LONG_ONLY_LOCATION_BTN)
            self.click(add_location_only)
            self.wait_for_element_to_disappear(self.LAT_LONG_MODAL)
        elif calc_lat_long_by == 'google_place_id':
            lat_long_by_google_place_id = self.get_clickable_element(self.By_GOOGLE_PLACE_ID)
            self.click(lat_long_by_google_place_id)
            self.locate_element(self.LAT_LONG_MODAL)
            time.sleep(TIMEOUT)
            add_location_only = self.get_clickable_element(self.ADD_LAT_LONG_ONLY_LOCATION_BTN)
            self.click(add_location_only)
            self.wait_for_element_to_disappear(self.LAT_LONG_MODAL)
        else:
            pass
        time.sleep(TIMEOUT)
        # 4. Click "Save"
        save_btn = self.get_clickable_element(self.SAVE_BTN)
        self.click(save_btn)

    @allure.step("Getting a different from Today's date")
    def get_other_date(self, current_date):
        other_dates = [x for x in range(1, 28) if x != current_date.day]
        other_day = '{:02}'.format(random.choice(other_dates))
        other_date = current_date.strftime("%Y-%m") + "-" + other_day
        other_date_in_calendar = f'//td[contains(@title, "{other_date}")]/div'
        other_day_in_input = f'{current_date.strftime("%B")} {other_day}, {current_date.strftime("%Y")}'
        self.OTHER_DATE = (By.XPATH, other_date_in_calendar)
        with allure.step(f"New date: {other_day_in_input}"):
            return other_day_in_input

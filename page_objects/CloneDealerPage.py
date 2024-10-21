import time

from selenium.webdriver.common.by import By
from page_objects.BasePage import BasePage
import allure
import string
import random

TIMEOUT = 6


class CloneDealerPage(BasePage):
    CLONE_DEALER_FORM_TITLE = (By.CSS_SELECTOR, '.ant-page-header-heading-title')
    FORM_TITLE_TEXT = "Clone Dealer"

    # Fields & Values
    GROUP_INPUT = (By.XPATH, '//div[div[label[contains(.,"Dealer Group")]]]//input')
    GROUP_CONTENT = (By.XPATH, '(//div[div[label[contains(.,"Dealer Group")]]]//span)[2]')
    GROUP_NAME = "Windy City Demo Auto Group (101589)"
    SELECT_GROUP_NAME = (
        By.XPATH, '//div[contains(@class, "ant-select-item-option-content") and contains(., "Windy City Demo")]')
    NAME = (By.XPATH, '(//form//div[2]//input)[2]')
    SHORT_NAME = (By.XPATH, '//form//div[4]//input')
    GO_LIVE_DATE = (By.XPATH, '//input[contains(@placeholder, "Select date")]')
    FRANCHISES = (By.XPATH, '//div[contains(@class, "ant-select-selection-search")]/input')
    FRANCHISES_VALUES = (By.XPATH, '//span[contains(@class, "ant-select-selection-item-content")]')
    WEBSITE_PREFIX = (By.XPATH, '//form//div[7]//input')
    WEBSITE = (By.XPATH, '//input[@name="Model.Website"]')
    WEBSITE_LABEL = (By.XPATH, '//label[contains(., "Website")]')
    GOOGLE_PLACE_ID = (By.XPATH, '//form//div[8]//input')
    GOOGLE_PLACE_ID_LABEL = (By.XPATH, '//label[contains(., "Google Place Id")]')
    OFFICE_PHONE = (By.XPATH, '//form//div[9]//input')
    ADDRESS = (By.XPATH, '//form//div[10]//input')
    ADDRESS_LABEL = (By.XPATH, '//label[contains(., "Address")]')
    CITY = (By.XPATH, '//form//div[11]//input')
    STATE = (By.XPATH, '//form//div[12]//input')
    STATE_VALUE = (By.XPATH, '//form//div[12]//input/../following-sibling::span')
    ZIP_CODE = (By.XPATH, '//form//div[13]//input')
    ZIP_CODE_LABEL = (By.XPATH, '//label[contains(., "Zip Code")]')
    SAMPLE_VALID_GOOGLE_PLACE_ID = 'ChIJl24c2LAY9ocR7gd7CpefUrY'
    SAMPLE_VALID_ZIP_CODE = "60606"
    EXISTING_DEALER_NAME = "Windy City BMW"
    EXISTING_DEALER_SHORT_NAME = "Windy City BMW"
    LAT_LONG_MODAL = (By.XPATH, '//div[contains(@class, "ant-modal-body")]')

    # Alerts
    FORM_VALIDATION_FAILED_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-alert-message") and contains(., "Form validation failed")]')
    FORM_VALIDATION_FAILED_TEXT = 'Form validation failed. Check fields messages.'
    NAME_REQUIRED_ALERT = (By.XPATH, '//div[contains(@role, "alert") and contains(., "The Name field is required.")]')
    NAME_REQUIRED_TEXT = 'The Name field is required.'
    SHORT_NAME_REQUIRED_ALERT = (By.XPATH,
                                 '//div[contains(@role, "alert") and contains(., "The ShortName field is required.")]')
    SHORT_NAME_REQUIRED_TEXT = 'The ShortName field is required.'
    ZIPCODE_REQUIRED_ALERT = (By.XPATH,
                              '//div[contains(@role, "alert") and contains(., "The ZipCode field is required.")]')
    ZIPCODE_REQUIRED_TEXT = 'The ZipCode field is required.'
    LATITUDE_REQUIRED_ALERT = (By.XPATH,
                               '//div[contains(@role, "alert") and contains(., "The Latitude field is required.")]')
    LATITUDE_REQUIRED_TEXT = 'The Latitude field is required.'
    LONGITUDE_REQUIRED_ALERT = (By.XPATH,
                                '//div[contains(@role, "alert") and contains(., "The Longitude field is required.")]')
    LONGITUDE_REQUIRED_TEXT = 'The Longitude field is required.'
    NAME_MUST_BE_UNIQUE_ALERT = \
        (By.XPATH, '//div[contains(@class, "ant-form-item-explain-error") and contains (., "Must be unique")]')
    NAME_MUST_BE_UNIQUE_TEXT = 'Must be unique for active dealer'
    MUST_BE_UNIQUE_TEXT = 'Must be unique'
    OTHER_DATE = None

    # Buttons
    CLONE_BTN = (By.XPATH, '//button/span[contains(., "Clone")]/..')
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

    @allure.step("Filling 'Clone Dealer' form with the provided data and saving changes")
    def clone_dealer(self,
                     name: str = '',
                     short_name: str = '',
                     website: str = '',
                     google_place_id: str = '',
                     address: str = '',
                     zip_code: str = '',
                     calc_lat_long_by: str = 'zip_code'):
        """Fill 'Clone Dealer' form with the provided data and click 'Save' (empty values by default)
        Options for calc_lat_long_by: zip_code, google_place_id. If no valid option provided, the step is skipped"""

        # 1. Open "Clone Dealer" form
        clone_btn = self.get_clickable_element(self.CLONE_BTN)
        self.click(clone_btn)
        time.sleep(TIMEOUT)
        self.get_clickable_element(self.SAVE_BTN)

        # 2. Enter provided data to the form
        self.paste_text(self.NAME, name)
        self.paste_text(self.SHORT_NAME, short_name)
        self.type_in_text(self.WEBSITE, website)
        self.paste_text(self.GOOGLE_PLACE_ID, google_place_id)
        self.type_in_text(self.ADDRESS, address)
        self.paste_text(self.ZIP_CODE, zip_code)
        name_field = self.locate_element(self.NAME)
        self.click(name_field)
        time.sleep(TIMEOUT)

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

    @allure.step("Checking if the form element is required")
    def is_required_field(self, label_locator):
        return self.get_attribute(label_locator, 'class') == "ant-form-item-required"

    @allure.step("Getting a different from Today's date")
    def get_other_date(self, current_date):
        other_dates = [x for x in range(1, 28) if x != current_date.day]
        other_day = '{:02}'.format(random.choice(other_dates))
        other_date = current_date.strftime("%Y-%m") + "-" + other_day
        other_date_in_calendar = f'//td[contains(@title, "{other_date}")]/div'
        other_day_in_input = f'{current_date.strftime("%B")} {other_day}, {current_date.strftime("%Y")}'
        self.OTHER_DATE = (By.XPATH, other_date_in_calendar)
        return other_day_in_input

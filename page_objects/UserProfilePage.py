from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By
import allure


class UserProfilePage(BasePage):
    NEW_USERNAME_IN_PROFILE = (By.CSS_SELECTOR, '.ant-page-header-heading-title')
    MEMBER_ID = (By.XPATH, '//span[contains(., "Member ID")]')

    # 'User-General' tab
    GENERAL_TAB = (By.XPATH, '//div[text()="General"]')
    GENERAL_ACTIVE_BTN = (By.XPATH, '//div/button[(@role = "switch")]')
    GENERAL_EDIT_BTN = (By.XPATH, '//button[contains(., "Edit")]')
    GENERAL_SAVE_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')
    GENERAL_CANCEL_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Cancel")]')
    LOGIN_FIELD = (By.XPATH, '//label[text()="Login"]/../following-sibling::div/div/*[contains (text(), "")]')
    # 'User-Notes' tab
    OTHER_NOTES = (By.XPATH, '//div[text()="Notes"]')
    # 'User-Other' tab
    OTHER_TAB = (By.XPATH, '//div[text()="Other"]')
    DASHBOARD_ROW_DISPLAY = (By.XPATH, '//div/label[text()="Dashboard Row Display"]/../following-sibling::div//input')
    DASHBOARD_ROW_DISPLAY_DEFAULT = '10'
    DEFAULT_DEALER_GROUP = (By.XPATH, '//div/label[text()="Default Dealer Group"]/../following-sibling::div//span')

    # 'Roles' tab
    ROLES_TAB = (By.XPATH, '//div[text()="Roles"]')
    # Roles-Roles' sub-tab
    ROLES_ROLES_SUBTAB = (By.XPATH, '(//div[text()="Roles"])[2]')
    USED_CAR_ROLE = (By.XPATH, '//label[text()="Used Car Role"]/../following-sibling::div//span/input/..')
    USED_CAR_ROLE_VALUE = (By.XPATH, '(//label[text()="Used Car Role"]/../following-sibling::div//span)[2]')
    MANAGER_WITHOUT_PRICING_OPTION = (By.XPATH, '(//div[text()="Manager (without pricing)"])[2]')
    MANAGER_OPTION = (By.XPATH, '//div[text()="Manager"]')
    PRICER_REMOVED_ALERT = (By.XPATH, '//div[@class="ant-message-custom-content ant-message-info"]//span[2]')
    PRICER_REMOVED_ALERT_TEXT = '`Pricer` was removed from Merchandising roles'
    # Roles-Merchandising' sub-tab
    ROLES_MERCHANDISING_TAB = (By.XPATH, '//div[text()="Merchandising"]')
    MERCHANDISING_CHECKBOX_STATUS = (By.XPATH, '//input[@type="checkbox"]/..')
    USER_MERCHANDISING_ROLES_DEFAULTS = \
        ['Approver', 'Builder', 'Description Editor', 'Manager', 'Photographer', 'Pricer', 'Report Viewer', 'User']
    PRICER_CHECKBOX = (By.XPATH, '//span[text()="Pricer"]/preceding-sibling::span')
    MERCH_ROLES_SAVE_BTN = (By.XPATH, '//button[contains(@class, "ant-btn") and contains(.,"Save")]')

    @allure.step("Getting check-box names")
    def get_checkbox_name_merchandising(self, checkbox_status_locator: tuple, checkbox_num=1):
        """Get name of a check-box"""
        checkbox_name_path = f'({checkbox_status_locator[1]}/following-sibling::span)[{checkbox_num}]'
        name_locator = (By.XPATH, checkbox_name_path)
        return self.get_text(name_locator)

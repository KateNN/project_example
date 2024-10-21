from page_objects.DealerProfilePage import DealerProfilePage
from selenium.webdriver.common.by import By


class DealerProfileMaxSettingsPage(DealerProfilePage):
    # 'MAX Settings' / 'Ad Settings'
    AD_SETTINGS_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Ad Settings")]')
    TIER_0_INPUT = (By.XPATH, '//td[contains(., "Tier 0")]/following-sibling::td//input')
    TIER_1_INPUT = (By.XPATH, '//td[contains(., "Tier 1")]/following-sibling::td//input')
    TIER_2_INPUT = (By.XPATH, '//td[contains(., "Tier 2")]/following-sibling::td//input')
    TIER_3_INPUT = (By.XPATH, '//td[contains(., "Tier 3")]/following-sibling::td//input')
    TIER_DEFAULTS = ['4', '5', '0', '0']
    PREVIEW_TEXT_LENGTH = (
        By.XPATH, '//div[label[contains(., "How long is your listing site")]]/following-sibling::div//input')
    PREVIEW_TEXT_LENGTH_DEFAULT = '250'
    MORE_VERBOSE_DESCRIPTIONS_STATUS = (
        By.XPATH, '//div[label[contains(., "more verbose descriptions")]]/following-sibling::div//input/..')
    BREAK_UP_SYMBOL = (By.XPATH, '//div[label[contains(., "What Symbol")]]/following-sibling::div//input')
    BREAK_UP_SYMBOL_DEFAULT = '~'
    WHICH_BOOK_VALUE_SHOULD_BE_USED = \
        (By.XPATH, '(//div[label[contains(., "Which book value")]]/following-sibling::div//span)[2]')
    CALL_TO_ACTION_IN_PREVIEWS_STATUS = (
        By.XPATH, '//div[label[contains(., "show a call to action in previews?")]]/following-sibling::div//input/..')

    # 'MAX Settings' / 'Alerts'
    ALERTS_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Alerts")]')
    ALERTS_CHECKBOX_STATUS = (By.XPATH, '//td/label/span[contains (@class, "ant-checkbox")]')
    ALERTS_CHECKBOX_NAME = (By.XPATH, '//td[contains(., "At least")]')
    ALERTS_CHECKBOXES_DEFAULTED_ON = [3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 20]

    # 'MAX Settings' / 'Auto-Approve'
    AUTO_APPROVE_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Auto-Approve")]')
    AUTO_APPROVE_FIRST_NAME = (By.XPATH, '//div[label[contains(., "First Name")]]/following-sibling::div//input')
    AUTO_APPROVE_FIRST_NAME_DEFAULT = 'Help'
    AUTO_APPROVE_LAST_NAME = (By.XPATH, '//div[label[contains(., "Last Name")]]/following-sibling::div//input')
    AUTO_APPROVE_LAST_NAME_DEFAULT = 'Desk'
    AUTO_APPROVE_EMAIL = (By.XPATH, '//div[label[contains(., "Email")]]/following-sibling::div//input')
    AUTO_APPROVE_EMAIL_DEFAULT = 'maxautoapprove@gmail.com'
    AUTO_APPROVE_IS = (By.XPATH, '//div[label[contains(., "Auto-Approve is")]]/following-sibling::div//span[2]')
    AUTO_APPROVE_IS_DEFAULT = 'On (New & Used)'

    # 'MAX Settings' / 'Miscellaneous Settings'
    MISC_SETTINGS_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Miscellaneous")]')
    MISC_MAX_3_0_UPGRADE_STATUS = (By.XPATH, '//label/span[contains(., "Max 3.0")]//preceding-sibling::span')
    MISC_WEBLOADER_STATUS = (By.XPATH, '//label/span[contains(., "Webloader")]//preceding-sibling::span')
    MISC_BATCH_AUTOLOAD_STATUS = (By.XPATH, '//label/span[contains(., "Batch Autoload")]//preceding-sibling::span')
    MISC_DASHBOARD_STATUS = (By.XPATH, '//label/span[contains(., "  Dashboard")]//preceding-sibling::span')
    MISC_SHOW_ONLINE_CLASSIFIED_OVERVIEW_STATUS = (
        By.XPATH, '//label/span[contains(., "Online Classified Overview")]//preceding-sibling::span')
    MISC_SHOW_TIME_TO_MARKET_STATUS = (By.XPATH, '//label/span[contains(., "Time To Market")]//preceding-sibling::span')
    MISC_GROUP_LEVEL_DASHBOARD_STATUS = \
        (By.XPATH, '//label/span[contains(., "Group Level Dashboard")]//preceding-sibling::span')
    MISC_SEND_OPTIMAL_FORMAT_STATUS = \
        (By.XPATH, '//label/span[contains(., "Send Optimal Format")]//preceding-sibling::span')
    MISC_MOVE_VEHICLES_OFFLINE_STATUS = \
        (By.XPATH, '//label/span[contains(., "Move vehicles offline")]//preceding-sibling::span')
    MISC_SHOW_CTR_GRAPH_STATUS = \
        (By.XPATH, '//label/span[contains(., "Show CTR Graph")]//preceding-sibling::span')
    MISC_ENABLE_PHOTO_TRANSFERS_STATUS = \
        (By.XPATH, '//label/span[contains(., "Enable Photo Transfers")]//preceding-sibling::span')
    MISC_GID_PROVIDER_USED_INPUT = \
        (By.XPATH, '//div[text()="GID Provider:"]/following-sibling::div[contains(., "Used")]//span[2]')
    MISC_GID_PROVIDER_NEW_INPUT = \
        (By.XPATH, '//div[text()="GID Provider:"]/following-sibling::div[contains(., "New")]//span[2]')
    MISC_GID_PROVIDER_DEFAULT = 'Aultec'
    MISC_REPORT_DATA_SOURCE_USED_INPUT = \
        (By.XPATH, '//div[text()="Report Data Source:"]/following-sibling::div[contains(., "Used")]//span[2]')
    MISC_REPORT_DATA_SOURCE_NEW_INPUT = \
        (By.XPATH, '//div[text()="Report Data Source:"]/following-sibling::div[contains(., "New")]//span[2]')
    MISC_REPORT_DATA_SOURCE_DEFAULT = 'Aultec'

    # 'MAX Settings' / 'Setup Wizard'
    SETUP_WIZARD_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Setup Wizard")]')
    SETUP_WIZARD_MIN_MILEAGE_INPUT = \
        (By.XPATH, '//div[label[contains(., "the minimum mileage")]]/following-sibling::div//input')
    SETUP_WIZARD_MIN_MILEAGE_DEFAULT = '30000'
    SETUP_WIZARD_CHARACTERS_INPUT = \
        (By.XPATH, '//div[label[contains(., "How many characters")]]/following-sibling::div//input')
    SETUP_WIZARD_CHARACTERS_DEFAULT = '250'
    SETUP_WIZARD_LOW_PHOTO_THRESHOLD_INPUT = \
        (By.XPATH, '//div[label[contains(., "Low Photo Threshold")]]/following-sibling::div//input')
    SETUP_WIZARD_LOW_PHOTO_THRESHOLD_DEFAULT = '12'

    def get_checkbox_name_decoding(self, checkbox_status_locator: tuple, checkbox_num=1):
        """Works for 'Decoding' and 'Miscellaneous Settings' tab"""
        checkbox_name_path = f'({checkbox_status_locator[1]}/following-sibling::span)[{checkbox_num}]'
        name_locator = (By.XPATH, checkbox_name_path)
        return self.get_text(name_locator)

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

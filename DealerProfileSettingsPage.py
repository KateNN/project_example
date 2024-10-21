from page_objects.DealerProfilePage import DealerProfilePage
from selenium.webdriver.common.by import By
import allure
import re


class DealerProfileSettingsPage(DealerProfilePage):
    SETTINGS_TAB = (By.XPATH, '//div[text()="Settings"]')

    # 'Settings' / 'Upgrades'
    UPGRADES_SUB_TAB = (By.XPATH, '//div[contains(@class, "ant-tabs-tab-btn") and contains(., "Upgrades")]')
    ALL_UPGRADE_NAMES = (By.XPATH, '//table//td[1]')

    @allure.step("Getting all Upgrades names")
    def get_all_upgrades_names(self):
        all_upgrades_num = len(self.locate_all_elements(self.ALL_UPGRADE_NAMES))
        all_upgrades_names = []
        for i in range(1, all_upgrades_num + 1):
            path = f'(//table//td[1])[{i}]'
            upgrade_name_locator = (By.XPATH, path)
            upgrade_name = self.get_text(upgrade_name_locator)
            if '\n' in upgrade_name:
                delimiter = upgrade_name.find('\n')
                upgrade_name = upgrade_name[:delimiter:]
            all_upgrades_names.append(upgrade_name)
        return all_upgrades_names

    @allure.step("Getting key name for an Upgrade setting and locator for 'Active' button")
    def get_upgrade_key_name_and_locator(self, upgrade_name):
        upgrade_key_name = []
        for i in upgrade_name:
            if i.isalnum():
                upgrade_key_name.append(i.lower())
            elif i in [' ', '.', '-', '/']:
                upgrade_key_name.append('_')
            else:
                continue
        upgrade_key_name_joined = "".join(upgrade_key_name)
        upgrade_key_final = 'upgrades_' + re.sub('_+', '_', upgrade_key_name_joined)
        button_path = f'//table//td/h4[text()="{upgrade_name}"]/../following-sibling::td/button'
        button_locator = (By.XPATH, button_path)
        with allure.step(f"Returning key: '{upgrade_key_final}' and locator for 'Active' button: '{button_locator}'"):
            return upgrade_key_final, button_locator

from page_objects.DealerProfilePage import DealerProfilePage
from selenium.webdriver.common.by import By


class DealerProfilePricingPage(DealerProfilePage):
    PRICING_TAB = (By.XPATH, '//div[text()="Pricing"]')

    SYNDICATION_PRICE_SHOWROOM = (By.XPATH, '//div[text()="Syndication Price Showroom"]')
    SYND_PRICE_SHOWROOM_NEW_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price Showroom"]/../..//p)[1]')
    SYND_PRICE_SHOWROOM_NEW_VEHICLES_DEFAULT = 'Special Price'
    SYND_PRICE_SHOWROOM_USED_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price Showroom"]/../..//p)[2]')
    SYND_PRICE_SHOWROOM_USED_VEHICLES_DEFAULT = 'List Price'
    SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price Showroom"]/../..//p)[3]')
    SYND_PRICE_SHOWROOM_UNKNOWN_VEHICLES_DEFAULT = 'No pricing rules defined.'
    SYNDICATION_PRICE_1 = (By.XPATH, '//div[text()="Syndication Price 1"]')
    SYND_PRICE_1_NEW_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price 1"]/../..//p)[1]')
    SYND_PRICE_1_NEW_VEHICLES_DEFAULT = 'List Price'
    SYND_PRICE_1_USED_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price 1"]/../..//p)[2]')
    SYND_PRICE_1_USED_VEHICLES_DEFAULT = 'List Price'
    SYND_PRICE_1_UNKNOWN_VEHICLES = (By.XPATH, '(//div[text()="Syndication Price 1"]/../..//p)[3]')
    SYND_PRICE_1_UNKNOWN_VEHICLES_DEFAULT = 'No pricing rules defined.'
    WRITEBACK_PRICE = (By.XPATH, '//div[text()="Writeback Price"]')
    WRITEBACK_PRICE_NEW_VEHICLES = (By.XPATH, '(//div[text()="Writeback Price"]/../..//p)[1]')
    WRITEBACK_PRICE_NEW_VEHICLES_DEFAULT = 'Special Price'
    WRITEBACK_PRICE_USED_VEHICLES = (By.XPATH, '(//div[text()="Writeback Price"]/../..//p)[2]')
    WRITEBACK_PRICE_USED_VEHICLES_DEFAULT = 'List Price'
    WRITEBACK_PRICE_UNKNOWN_VEHICLES = (By.XPATH, '(//div[text()="Writeback Price"]/../..//p)[3]')
    WRITEBACK_PRICE_UNKNOWN_VEHICLES_DEFAULT = 'No pricing rules defined.'

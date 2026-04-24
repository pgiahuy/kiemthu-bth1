from selenium.webdriver.common.by import By

from eapp.test.pages.BasePage import BasePage


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5000/'
    SEARCH_INPUT = (By.CSS_SELECTOR,'#collapsibleNavbar > form > input')
    SEARCH_BUTTON = (By.CSS_SELECTOR,'#collapsibleNavbar > form > button')

    PROD_BTN_1 = (By.CSS_SELECTOR,'.container > div > div:nth-child(1) > div > div > button')
    PROD_BTN_2 = (By.CSS_SELECTOR,'.container > div > div:nth-child(2) > div > div > button')

    def open_page(self):
        self.open(self.URL)

    def search(self, kw):
        self.typing(*self.SEARCH_INPUT,kw)
        self.click(*self.SEARCH_BUTTON)

    def add_to_card(self):
        self.click(*self.PROD_BTN_1)
        self.click(*self.PROD_BTN_1)
        self.click(*self.PROD_BTN_2)
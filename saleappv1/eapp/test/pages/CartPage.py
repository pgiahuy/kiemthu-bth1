from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from eapp.test.pages.BasePage import BasePage


class CartPage(BasePage):
    URL = 'http://127.0.0.1:5000/cart'
    BTN_PAY = (By.CSS_SELECTOR,'.container > div.mt-1.mb-1 > button')

    def open_page(self):
        self.open(self.URL)

    def pay(self):
        self.click(*self.BTN_PAY)
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()
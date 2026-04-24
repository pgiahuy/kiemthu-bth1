from selenium.webdriver.common.by import By

from eapp.test.pages.BasePage import BasePage



class LoginPage(BasePage):
    URL = 'http://127.0.0.1:5000/login'
    USERNAME = (By.ID,'username')
    PASSWORD= (By.ID,'pwd')
    BTN= (By.CSS_SELECTOR,'.container > form  button')

    def open_page(self, url=URL):
        self.open(url)

    def login(self,username, pwd):
        self.typing(*self.USERNAME,username)
        self.typing(*self.PASSWORD,pwd)
        self.click(*self.BTN)
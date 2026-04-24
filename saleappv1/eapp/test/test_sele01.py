import time

from selenium.webdriver.common.by import By

from eapp.test.pages.CartPage import CartPage
from eapp.test.pages.LoginPage import LoginPage
from eapp.test.pages.HomePage import HomePage
from eapp.test.test_base import driver


def test_search_product(driver):
    # driver.get("http://127.0.0.1:5000/")
    kw = "iPhone"
    # search_box = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > form > input')
    # search_box.send_keys(kw)
    # btn = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > form > button').click()
    # time.sleep(2)
    # res = driver.find_elements(By.CSS_SELECTOR,'.container .card-title')
    # assert all(kw in r.text for r in res)

    home = HomePage(driver=driver)
    home.open_page()
    home.search(kw)

    time.sleep(1)

    res = driver.find_elements(By.CSS_SELECTOR, '.container .card-title')
    assert all(kw in r.text for r in res)

def test_add_to_cart(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_card()
    time.sleep(2)

    e = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > ul > li:nth-child(7) > a > span')
    assert int(e.text)== 3


def test_login(driver):
    login = LoginPage(driver=driver)
    login.open_page()
    login.login("admin","123456")
    time.sleep(1)
    assert driver.current_url == "http://127.0.0.1:5000/"
    e = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > ul > li:nth-child(5) > a')
    assert "admin" in e.text


def test_login_redirect(driver):
    login = LoginPage(driver=driver)
    login.open_page("http://127.0.0.1:5000/login?next=/cart")
    login.login("admin","123456")
    time.sleep(1)
    assert driver.current_url == "http://127.0.0.1:5000/cart"
    e = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > ul > li:nth-child(5) > a')
    assert "admin" in e.text

def test_pay_success(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_card()
    login=LoginPage(driver=driver)
    login.open_page("http://127.0.0.1:5000/login?next=/cart")
    login.login("admin", "123456")
    time.sleep(1)
    cart = CartPage(driver=driver)
    cart.open_page()
    cart.pay()
    e = driver.find_element(By.CSS_SELECTOR,'#collapsibleNavbar > ul > li:nth-child(7) > a > span')
    assert int(e.text)== 3

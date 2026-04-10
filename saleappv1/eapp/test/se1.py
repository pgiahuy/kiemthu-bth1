from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path="../../../.venv/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://vnexpress.net/")

articles = driver.find_elements(By.CSS_SELECTOR, '#automation_TV0 > article')

for a in articles :
    title = a.find_element(By.TAG_NAME,'h3')
    des = a.find_element(By.CLASS_NAME, 'description')
    img = a.find_element(By.CSS_SELECTOR, 'div > a > picture > img')

    print(title.text)
    print(des.text)
    print(img.get_attribute('src'))
    print("---------------")
    print("---------------")
driver.quit()
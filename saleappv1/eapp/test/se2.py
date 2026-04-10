from locust import exception
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path="../../../.venv/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://tiki.vn/dien-thoai-may-tinh-bang/c1789")
driver.execute_script("window.scrollTo(0,300)")
driver.implicitly_wait(3)

prods = driver.find_elements(By.CLASS_NAME, 'product-item')

data = []
for p in prods[:3]:
    title = p.find_element(By.CSS_SELECTOR, '.info h3').text
    link = p.get_attribute('href')
    data.append((title, link))


for title, link in data:
    driver.get(link)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    driver.implicitly_wait(3)
    print(title)
    print(link)
    while True:

        cmts = driver.find_elements(By.CLASS_NAME, 'review-comment')

        for cmt in cmts:
            des = cmt.find_element(By.CLASS_NAME, 'review-comment__content')
            print(des.text)


        next_btn = driver.find_element(By.CSS_SELECTOR, ".customer-reviews__pagination li:last-child a")

        if "disabled" in next_btn.get_attribute("class"):
            break

        next_btn.click()
        driver.implicitly_wait(3)


    print("---------------")

driver.quit()
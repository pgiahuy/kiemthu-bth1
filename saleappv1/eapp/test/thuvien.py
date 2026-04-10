import time

from locust import exception
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path="../../../.venv/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://thuvien.ou.edu.vn/")


searchBox = driver.find_element(By.ID, 'txtSearch')
searchBtn =  driver.find_element(By.CLASS_NAME, 'text-search')
kw= "Kiểm thử phần mềm"

searchBox.send_keys(kw)
driver.implicitly_wait(3)
searchBtn.click()
driver.implicitly_wait(3)

thumbs = driver.find_elements(By.CLASS_NAME,'thumb')
for c in thumbs:

    title = c.find_element(By.CSS_SELECTOR,'.text-thumb a')
    print(title.text)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
first = thumbs[0]
book = first.find_element(By.CSS_SELECTOR, ".img-thumb > a")


driver.execute_script("arguments[0].click();", book)
time.sleep(5)
table = driver.find_element(By.ID,'tblRecordDetails')
print(table)
rows = driver.find_elements(By.CSS_SELECTOR, "#tblRecordDetails tbody tr")
driver.save_screenshot("detail.png")
data = {}
print(rows)
for r in rows:
    cols = r.find_elements(By.TAG_NAME, "td")

    key = cols[0].text
    value = cols[1].text

    print(key, ":", value)

    data[key] = value


driver.quit()
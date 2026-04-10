from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="../../../.venv/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.xskthcm.com/")


tbl = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".table-bordered"))
)

rows = tbl.find_elements(By.CSS_SELECTOR, "tbody tr")

results = {}

for r in rows:
    cols = r.find_elements(By.TAG_NAME, "td")

    if len(cols) >= 2:
        giai = cols[0].get_attribute("innerText").strip()
        kq = cols[1].get_attribute("innerText").strip()
        results[giai] = kq

d = "6622"


for giai, kq in results.items():
    nums = [n.strip() for n in kq.split("-")]

    for n in nums:
        if d == n:
            print(f"TRÚNG {giai}")



driver.quit()
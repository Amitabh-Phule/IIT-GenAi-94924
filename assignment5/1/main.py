#1. Scrape Internship information and batches from Sunbeam website.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Run Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://sunbeaminfo.in/internship")
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

# Load dynamic content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
plus_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
)
plus_button.click()
table = driver.find_element(By.ID, "collapseSix")
tbody = table.find_element(By.TAG_NAME, "tbody")
rows = tbody.find_elements(By.TAG_NAME, "tr")
# Extract data
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) < 5:
        continue

    info = {
        "technology": cols[0].text,
        "aim": cols[1].text,
        "prerequisite": cols[2].text,
        "learning": cols[3].text,
        "location": cols[4].text
    }
    print(info)
driver.quit()

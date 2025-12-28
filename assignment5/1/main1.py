from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# start the selenium browser session
chrome_options = Options()
# chrome_options.add_argument("--headless=new")   
driver = webdriver.Chrome(options=chrome_options)

try:
   
    driver.get("https://sunbeaminfo.in/internship")
    print("Page Title:", driver.title)

    
    driver.implicitly_wait(5)

    # correct locator: use CSS selector for multiple classes
    table = driver.find_element(
        By.CSS_SELECTOR,
        "table.table.table-bordered.table-striped"
    )

    # get tbody and rows
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        
        if len(cols) < 7:
            continue

        info = {
            "sr": cols[0].text,
            "batch": cols[1].text,
            "batch duration": cols[2].text,
            "start date": cols[3].text,
            "end date": cols[4].text,
            "time": cols[5].text,
            "price": cols[6].text
        }

        
        print(info)
     

finally:
    driver.quit()
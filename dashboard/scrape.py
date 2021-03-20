from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

#This example requires Selenium WebDriver 3.13 or newer
# with webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT) as driver:
# with webdriver.Firefox() as driver:
# with webdriver.Chrome() as driver:
op = webdriver.ChromeOptions()
op.add_argument('headless')
with webdriver.Chrome(options=op) as driver:
    wait = WebDriverWait(driver, 10)
    driver.get('https://pfaf.org/user/Default.aspx')
    driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$txtSearch').send_keys('Radish' + Keys.RETURN)
    table = wait.until(presence_of_element_located((By.ID, 'ContentPlaceHolder1_gvresults')))
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        col = row.find_elements(By.TAG_NAME, 'td')
        for cell in col:
            print(cell.text, end=' ')
        print('')
    1/0
    print(first_result)
    print(first_result.get_attribute('innerHTML'))

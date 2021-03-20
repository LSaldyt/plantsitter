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
    driver.get('https://www.google.com/ncr')
    driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
    first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3>div")))
    print(first_result.get_attribute("textContent"))

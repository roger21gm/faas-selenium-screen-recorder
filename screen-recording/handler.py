from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    
    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    proxy = os.getenv('proxy', '')
    options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Chrome(chrome_options=options)
    
    driver.get(req)
    screenshot = driver.get_screenshot_as_base64()
    
    driver.close()
    driver.quit()

    return screenshot

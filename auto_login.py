# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005ACF645DEC18C31E9CB858B0F8CBAB9035B6107A1A3FF5C7C3B51B26A4EFDF02C6FCDA153FC8C6450C1757AE911F3633F63820B2DB58ABABA959BEBDA3395301998023732D91D1421EB3E8E48453E77267F18BB0170A4A7460AF7808ED2ABDBD07934C7E66F479C39D4B8C6D5A3E3FCF46814C16DFCEA6478A24D46375E891D9158036C8E5D5473069DAA7FF20ECB61376A24EFA6C143A9EF69CFAE6D8EE24A9A8D5DFC847E8B1D4861E0C457D8228E252DFD47FCE58DFE8319F690DAAEB15EFD906B81B22F7055D2EE6D807A5E8E5CA490610573721703235EF733A8C46DAC6A5BDB9758FB9BF7B08C81EF20C8C1BD85AE2830032DA86BBC31DE3FCD6655615E23209099AD710A700F7D0269EF41C0BC27AA371277E518584FC0D695141267C898FA3A2EF6F100C0247FB40FB595351F713F38F50304D252EFB969040D1298500D79E89B178D11FEDEFFBE61C343EC5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

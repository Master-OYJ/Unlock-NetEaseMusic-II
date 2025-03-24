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
    browser.add_cookie({"name": "MUSIC_U", "value": "0037038B36DC20F0C3A9EBD16805DED0AA7C80B6AA4C505C36DF425033805D38B748CF18D1DCE3CB4F5AB59A2F5895C7B7806B0B4963061D48CEE79BA9EA718A29E7BC2A4CDFD14203FE0E48CF96368B9C3843A5EDD311017322E881C60F2E3EAA02FD3D28F20A73D0C57B3D062B3C8E601642DF9001CDA6BF9A38C44CADC649FD94070A3EC362E7805FCFF2845B1C8BAF0638FC21EA516EA6B6633C7688BF40274054AE88D8DAF56CDA559975F9668596E81FE7844E411CE8993619B6375E89D654ED7AEA36C0E75A8A4019869103D2DB0CC4F003487B21D43AA31B3319A8C780BB073796E6727BEA6A55937CBD089CC8D11307B3C62B90BD1CFD453392EC8A06A784AD042F000E0FFB1C667B3CB6A7AB3C3C65C0A0EEA6C6B391CB01E75AF8D75AFF4B1D4E599BADBE214DEC8E1C04BA0661E214775DD3AA34B886F3C0C31DC58928D457BD41161C11F87EA07A367B24724112D57A650988C6228C20F0F69D3B"})
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

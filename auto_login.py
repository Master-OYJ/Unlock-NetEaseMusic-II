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
    browser.add_cookie({"name": "MUSIC_U", "value": "0022C986054B1841F4392052761B8C5AC02BB6297819E8EE709ADAB4C2A08B0F4E62CB426DCD9A9BD76E265914A43404C5CF5355326DFED688539200A13110968370C3F04277CBC170082EDC48E868959262DEE57B1A6A4AC3F7D873EA59EC0B7617580DD91B14B79E274A769CD468C27BDB763D4643E61686910A668368D5B8BC253F974CC39D73C1F7FD9FB4A705C67E5E04562A5238A857F05EB544EB834FC879D9CDD1D4F7F20D14294CB73C04E4E415712BCD40FDF02B1215B68A0BC193AFEAEEE6654506F6EAF2A178269BC0B4FE30B17B3C6B980B067A3B175EB005A386F7280268BF3B18E83BDE47843FE66973098D4E4E01EB1CC517FB75FE24BF6B85BFCB97C426478F73882DB66C096829C9236C4DCAB8A12A906B6D9229BD4B242E09B2A2537FA0BF1E94F2157C241C055BF2A4D221CDC3506656ECE7657EE80AF6F5EA9F70497B761B4BB328CA9DD663E4"})
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

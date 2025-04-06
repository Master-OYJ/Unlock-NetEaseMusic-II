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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BC120DF74E841B7221DE684E2B41C5E7CE2DD788B5BCC84D0998040B90B359D1E1248965D0FB69EB84ACAC95BE6F383A7DB26EFAA6054D117A4ABAD54295DB12BA371220AED84B1D162096F4E4EBA121A07EADC59879C6FFC680C3F7D9AFBB4DCB56285AD2F77FA27947AF0CA6360DC61B1C3614C5BF4DEB39959C2992317734083AE1950207F1F90F441BEE963E4A55ADE241578AFA7ED90CC671AFA9661502E59F322DF010A52F439281687CBF5B049E48FD63B8B3CDFBE922C831643FB6DA4A41FF84168E994CD64E06AECA3099E9015FCB21E1CE6A32E17B5A3990ADCF6B0E8EA3CF0D70C61B4B091D9C4D1AEA4152EEA184FA362D8B7FA07BC76AC0CED6199BD7501D56E64433520B7FB785284C169E97CB9C8BEF5C2214B30ED2EB393517C996A3CE4D5C2FF064ABC56B78B277C6374D3696DA414B3F4069B73DE0A53C52D25D8A5C3CD9B1CABCCAB1A5F4F3B848E9FAA1CA158E3D7F9C97C5B0F764FA"})
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

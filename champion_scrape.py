from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os

GOOGLE_CHROME_PATH = os.getenv('GOOGLE_CHROME_BIN')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = GOOGLE_CHROME_PATH


def get_runes_by_champion_name(champion_name):
    driver = webdriver.Chrome(
        options=options, executable_path=CHROMEDRIVER_PATH)
    url = f"https://u.gg/lol/champions/{champion_name}/build"
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "sp_message_iframe_403856")))
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    button.click()
    driver.switch_to.default_content()
    runes = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[2]/div[1]')
    runes.screenshot("test_screen.png")
    driver.quit()

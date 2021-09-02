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
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('window-size=1920x1080')
options.binary_location = GOOGLE_CHROME_PATH

def get_tierlist_by_role(role):
    tiercontainer_xpath = '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[5]/div'
    driver = webdriver.Chrome(
        options=options, executable_path=CHROMEDRIVER_PATH)

    setup_ugg_page(driver, role)

    tierlist = driver.find_element_by_xpath(
        tiercontainer_xpath)
    tierlist.screenshot("tierlist.png")
    driver.quit()

def get_url(role):
    if(role == "mid"):
        return f"https://u.gg/lol/mid-lane-tier-list"
    if(role == "top"):
        return f"https://u.gg/lol/top-lane-tier-list"
    if(role == "adc"):
        return f"https://u.gg/lol/adc-tier-list"
    if(role == "support"):
        return f"https://u.gg/lol/support-tier-list"
    if(role == "jungle"):
        return f"https://u.gg/lol/jungle-tier-list"


def setup_ugg_page(driver, role):
    driver.get(get_url(role))
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "sp_message_iframe_403856")))
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    button.click()
    driver.switch_to.default_content()
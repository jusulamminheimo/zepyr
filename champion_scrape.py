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


def get_url(is_aram, champion_name):
    if(is_aram):
        return f"https://u.gg/lol/champions/aram/{champion_name}-aram"
    else:
        return f"https://u.gg/lol/champions/{champion_name}/build"


def get_runes_by_champion_name(champion_name, is_aram):
    runes_container_xpath = '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[2]/div[1]'

    driver = webdriver.Chrome(
        options=options, executable_path=CHROMEDRIVER_PATH)

    driver.get(get_url(is_aram, champion_name))

    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "sp_message_iframe_403856")))
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    button.click()
    driver.switch_to.default_content()

    runes = driver.find_element_by_xpath(
        runes_container_xpath)
    runes.screenshot("runes.png")

    driver.quit()


def get_build_by_champion_name(champion_name, is_aram):
    if(is_aram):
        ability_container_xpath = '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[3]/div[1]'
        item_container_xpath = '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[6]'
    else:
        ability_container_xpath = '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[4]/div[1]'
        item_container_xpath = '//*[@id="content"]/div/div[1]/div/div/div[5]/div/div[7]'

    driver = webdriver.Chrome(
        options=options, executable_path=CHROMEDRIVER_PATH)
    driver.get(get_url(is_aram, champion_name))
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "sp_message_iframe_403856")))
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[2]/div[5]/button[2]')))
    button.click()
    driver.switch_to.default_content()

    abilities = driver.find_element_by_xpath(
        ability_container_xpath)
    abilities.screenshot("abilities.png")

    items = driver.find_element_by_xpath(
        item_container_xpath)
    items.screenshot("items.png")

    driver.quit()

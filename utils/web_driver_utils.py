from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def load_driver():
    options = Options()
    driver = webdriver.Chrome(service=Service("chromedriver"), options=options)
    return driver
def get_cookies(driver):
    return driver.get_cookies()

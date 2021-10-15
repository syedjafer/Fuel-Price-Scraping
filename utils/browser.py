from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constant import driver as con_driver


def create_browser_object():
        options = Options()
        # options.headless = True
        browser = webdriver.Chrome(con_driver.CHROMEDRIVER_LOC, chrome_options=options)
        return browser


def close_browser_object(browser):
        if browser:
                browser.close()

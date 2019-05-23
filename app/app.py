"""Capture Screenshots of Websites and Compare them with Highlighting."""
import os
import pathlib
import sys
from pathlib import Path
from time import gmtime, strftime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager


def setup_driver() -> webdriver.Firefox:
    """Create firefox driver for use."""
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(
        options=firefox_options, executable_path=GeckoDriverManager().install()
    )
    driver.maximize_window()
    return driver


def setup_screenshot_folder(url) -> None:
    """Create folder for screenshots to be saved in."""
    parsed_url = urlparse(url)
    save_directory = f"./screenshots/{parsed_url.netloc}"
    os.makedirs(save_directory, exist_ok=True)
    return save_directory, parsed_url


def retrieve_page(driver, url):
    """Have chrome driver retrieve and load webpage."""
    return driver.get(url)


def take_screenshot(driver, save_directory):
    """Take screenshot of loaded page in chrome driver."""
    now = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
    filename = f"{save_directory}/{now}.png"
    print(save_directory)
    print(now)
    print(filename)
    return driver.save_screenshot(filename)


def main(driver):
    """Run main program."""
    url = sys.argv[1]
    save_directory, parsed_url = setup_screenshot_folder(url)
    retrieve_page(driver, url)
    take_screenshot(driver, save_directory)


if __name__ == "__main__":
    try:
        driver = setup_driver()
        sys.exit(main(driver))
    except Exception as e:
        sys.exit(e)
    finally:
        driver.close()

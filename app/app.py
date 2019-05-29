"""Capture Screenshots of Websites and Compare them with Highlighting."""
import os
import pathlib
import sys
from io import BytesIO, StringIO
from pathlib import Path
from time import gmtime, strftime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from PIL import Image
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

    js = "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    scrollheight = driver.execute_script(js)
    print(f"scrollheight: {scrollheight}")

    slices = []
    offset = 0

    while offset < scrollheight:
        print(offset)

        driver.execute_script(f"window.scrollTo(0, {offset});")
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))

        offset += img.size[1]
        slices.append(img)
        driver.get_screenshot_as_file(f"{save_directory}/{now}_{offset}.png")
        print(scrollheight)

    screenshot = Image.new("RGB", (slices[0].size[0], scrollheight))
    offset = 0
    for img in slices:
        screenshot.paste(img, (0, offset))
        offset += img.size[1]

    screenshot.save(filename)


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

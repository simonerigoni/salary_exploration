"""Open web pages in Firefox, driven by Selenium."""

import time

from selenium import webdriver

from salary_exploration.config import SLEEP_TIME


def open_browser(url: str) -> webdriver.Firefox:
    """Open Firefox on url. The caller must quit the browser when done."""
    # Pause before every visit so we do not hammer the site.
    time.sleep(SLEEP_TIME)
    print(f"Connecting to {url}")
    browser = webdriver.Firefox()
    browser.get(url)
    return browser

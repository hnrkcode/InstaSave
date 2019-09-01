import os.path
import random
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from utils import settings


class WebDriver:
    """Responsible for starting and closing Selenium."""

    def __init__(self, useragent):
        """Initialize headless mode by default."""
        options = Options()
        options.add_argument("--headless")
        # Change settings in about:config.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", useragent)

        try:
            self.driver = webdriver.Firefox(
                profile,
                firefox_options=options,
                executable_path=settings.GECKODRIVER
            )
        except TypeError as e:
            sys.exit(e)
        except exceptions.WebDriverException as e:
            sys.exit(e)

    def open(self, url):
        """Open the url in the webdriver."""
        try:
            self.driver.get(url)
        except exceptions.WebDriverException as e:
            self.close(e)

    def close(self, msg=None):
        """Close the web driver."""
        self.driver.close()
        if msg:
            sys.exit(msg)


class URLScraper(WebDriver):
    """Collect urls to posts that should be downloaded."""

    def __init__(self, useragent):
        super().__init__(useragent)

    def _is_private(self, main):
        """Check if the account is private."""
        try:
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, 'html.parser')
            private = soup.find('h2').string
        except AttributeError:
            return main  # The account is public.
        else:
            self.close(private)

    def _user_exists(self):
        """Check if the user exists."""
        try:
            main = self._is_private(self.driver.find_element_by_class_name(settings.MAIN_CONTENT))
        except NoSuchElementException:
            main = self.driver.find_element_by_class_name(settings.NOT_AVAILABLE)
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, 'html.parser')
            message = soup.find('h2').string
            self.close(message)
        else:
            return main

    def get_urls(self, max=1):
        """Collects post urls."""

        main = self._user_exists()
        innerHTML = main.get_attribute("innerHTML")
        soup = BeautifulSoup(innerHTML, 'html.parser')
        posts = soup.find_all(class_=settings.POST)
        scroll_pos = 0
        urls = set()

        # Will only the latest post if not a higher number is specified.
        if max:
            total_posts = max
        # Will scrape every post url posted by the user.
        if not max:
            total_posts = int(soup.find_all(class_=settings.TOTAL_POSTS)[0].text)

        # Scroll down.
        while len(urls) < total_posts:
            # Limit the number of post urls to get to what 'total_posts' is.
            for post in posts[:total_posts]:
                url = "https://www.instagram.com" + post.parent['href']
                if len(urls) < total_posts:
                    urls.add(url)

            main = self.driver.find_element_by_class_name(settings.MAIN_CONTENT)
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, 'html.parser')
            posts = soup.find_all(class_=settings.POST)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            scroll_pos += 500
            print(f"Collecting urls: {len(urls)}/{total_posts}")

        return list(urls)

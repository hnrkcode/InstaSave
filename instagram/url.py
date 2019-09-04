import json
import os.path
import random
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from utils.settings import GECKODRIVER

MAIN_CONTENT = "SCxLW"
POST = "eLAPa"


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
                profile, firefox_options=options, executable_path=GECKODRIVER
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
        self.driver.quit()
        if msg:
            sys.exit(msg)


class URLScraper(WebDriver):
    """Collect urls to posts that should be downloaded."""

    def __init__(self, useragent):
        super().__init__(useragent)

    def scrape(self, max, hashtag):
        """Check page status before scraping urls."""
        # Hashtag or profle exists.
        if self._exists():
            # Hashtag or a public profile.
            if self._exists() and self._is_public(hashtag):
                return self._get_urls(max, hashtag)
            # Private profile.
            elif self._exists() and not self._is_public():
                print("Account is private.")
                return []
        # Hashtag or profile doesn't exists.
        print("Doesn't exists.")
        return []

    def _exists(self):
        """Test if profile or hashtag exists."""
        if "Page Not Found" in self.driver.title:
            return False
        return True

    def _is_public(self, hashtag):
        """Check if account is public."""
        # Make sure it's not a hashtag page before checking if account status.
        if not hashtag:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            script = soup.select("body > script:nth-child(6)")
            json_data = script[0].text[21:-1]
            data = json.loads(json_data)
            private = data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
                "is_private"
            ]
            if private:
                return False

        return True

    def _get_urls(self, max, hashtag):
        """Scrape a certain number of post urls from the page."""

        urls = set()
        scroll_pos = 0
        main = self.driver.find_element_by_class_name(MAIN_CONTENT)
        innerHTML = main.get_attribute("innerHTML")
        soup = BeautifulSoup(innerHTML, "html.parser")
        # Get all tags that contains post data.
        posts = soup.find_all(class_=POST)

        while len(urls) < max:
            for post in posts[:max]:
                # Link to the individual post.
                url = "https://www.instagram.com" + post.parent["href"]
                # Add it if maximum scraped posts isn't reached yet.
                if len(urls) < max:
                    urls.add(url)

            # Update HTML code.
            main = self.driver.find_element_by_class_name(MAIN_CONTENT)
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, "html.parser")
            posts = soup.find_all(class_=POST)
            # Scroll down to see more posts in the feed.
            self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            scroll_pos += 500
            print(f"Collecting urls: {len(urls)}/{max}")

        return list(urls)

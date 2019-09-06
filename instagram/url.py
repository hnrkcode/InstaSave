import json
import os.path
import random
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from utils.settings import GECKODRIVER

MAIN_CONTENT = "SCxLW"

POST = "eLAPa"


class WebDriver:
    """Responsible for starting and closing Selenium.

    Attributes:
        driver (obj): Selenium webdriver.
    """

    def __init__(self, useragent):
        """Initialize the webdriver.

        Set the webdriver to headless (i.e., hide browser GUI). Also modify the
        Firefox profile's preferences.

        Args:
            useragent (str): Overrides the default user agent.

        Raises:
            TypeError
            exceptions.WebDriverException

        """
        options = Options()
        options.headless = True
        # Change settings in about:config.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", useragent)

        try:
            self.driver = webdriver.Firefox(
                firefox_profile=profile, options=options, executable_path=GECKODRIVER
            )
        except (TypeError, exceptions.WebDriverException) as e:
            raise SystemExit(e)

    def open(self, url):
        """Start webdriver and visit url.

        Args:
            url (str): Page to visit.

        Raises:
            exceptions.WebDriverException: Shut down and print error message.

        """
        try:
            self.driver.get(url)
        except exceptions.WebDriverException as e:
            self.close(e)

    def close(self, msg=None):
        """Close webdriver."""
        self.driver.quit()
        if msg:
            raise SystemExit(msg)


class URLScraper(WebDriver):
    """Collect post urls to download.

    Inherit from WebDriver.

    Attributes:
        filelist (list): List with shortcodes that belongs to already
            downloaded posts.

    """

    def __init__(self, useragent, output):
        """Inherit from WebDriver and initialize list of downloaded posts.

        Args:
            useragent (str): Used for __init__ in WebDriver.
            output (str): Scan downloaded files and get their shortcodes.
        """
        super().__init__(useragent)
        self.filelist = [str(file)[-36:-25] for file in Path(output).rglob("*.*")]

    def scrape(self, limit, hashtag):
        """Scrape post urls if user or hashtag page exists.

        Args:
            limit (int): Stop scraping post urls when limit is reached.
            hashtag (bool): Tell if page belongs to hashtag or user.

        Returns:
            List with urls to posts that hasn't been downloaded yet. If the
            list is empty, the page is private or doesn't exist.

        """
        if self._exists():
            # Hashtag or a public profile.
            if self._exists() and self._is_public(hashtag):
                limit = self._check_limit(limit, hashtag)
                return self._get_urls(limit)
            # Private profile.
            elif self._exists() and not self._is_public():
                print("Account is private.")
                return []
        # Hashtag or profile doesn't exists.
        print("Doesn't exists.")
        return []

    def _exists(self):
        """Return true if user or hashtag exists."""
        if "Page Not Found" in self.driver.title:
            return False
        return True

    def _is_public(self, hashtag):
        """Return true if account is public."""
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

    def _check_limit(self, limit, hashtag):
        """Return limit that is less than or equal to existing posts."""
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        script = soup.select("body > script:nth-child(6)")
        json_data = script[0].text[21:-1]
        data = json.loads(json_data)

        if hashtag:
            total_posts = data["entry_data"]["TagPage"][0]["graphql"]["hashtag"][
                "edge_hashtag_to_media"
            ]["count"]
        else:
            total_posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"][
                "edge_owner_to_timeline_media"
            ]["count"]

        if limit > total_posts:
            return total_posts

        return limit

    def _get_urls(self, limit):
        """Return list with post urls to download files from."""
        urls = set()
        scroll_pos = 0
        main = self.driver.find_element_by_class_name(MAIN_CONTENT)
        innerHTML = main.get_attribute("innerHTML")
        soup = BeautifulSoup(innerHTML, "html.parser")
        posts = soup.find_all(class_=POST)

        # Run until the limit has been reached.
        while len(urls) < limit:
            # Go through all scraped post urls.
            for post in posts:
                path = post.parent["href"]
                url = "https://www.instagram.com" + path
                # Add url if limit hasn't yet been reachded and if the url
                # doesn't belong to a post that has been downloaded before.
                if len(urls) < limit and path[3:-1] not in self.filelist:
                    urls.add(url)

            # Get new urls as long as limit hasn't been reached.
            if len(urls) < limit:
                # Update HTML code.
                main = self.driver.find_element_by_class_name(MAIN_CONTENT)
                innerHTML = main.get_attribute("innerHTML")
                soup = BeautifulSoup(innerHTML, "html.parser")
                posts = soup.find_all(class_=POST)
                # Scroll down to see more posts in the feed.
                self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
                scroll_pos += 500

        return list(urls)

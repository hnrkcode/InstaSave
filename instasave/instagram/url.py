from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options

from instasave.utils import hook
from instasave.utils.jsonparser import parse_json
from instasave.utils.settings import GECKODRIVER

MAIN_CONTENT = "SCxLW"

POST = "eLAPa"

JSON_CSS_SELECTOR = "body > script:nth-child(6)"


class WebDriver:
    """Responsible for starting and closing Selenium."""

    def __init__(self, useragent):
        """Initialize headless webdriver with random user agent."""

        options = Options()
        # Hide the browser window.
        options.headless = True
        # Change settings in about:config.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", useragent)

        try:
            self.driver = webdriver.Firefox(
                firefox_profile=profile,
                options=options,
                executable_path=GECKODRIVER,
            )
        except (TypeError, exceptions.WebDriverException) as e:
            raise SystemExit(e)

    def open(self, url):
        """Start webdriver and visit url."""
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
        """Inherit from WebDriver and initialize list of downloaded posts."""

        super().__init__(useragent)
        # Scan downloaded files and get their shortcodes.
        self.filelist = [
            str(file)[-36:-25] for file in Path(output).rglob("*.*")
        ]

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
                limit = self._check_limit(limit)
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

    def _is_public(self, hashtag=False):
        """Return true if account is public."""

        if not hashtag:
            private = parse_json(
                self.driver.page_source, JSON_CSS_SELECTOR, hook.private_profile
            )
            if private:
                return False

        return True

    def _check_limit(self, limit):
        """Return limit that is less than or equal to existing posts."""

        try:
            total_posts = parse_json(
                self.driver.page_source, JSON_CSS_SELECTOR, hook.user_post_count
            )
        except KeyError:
            total_posts = parse_json(
                self.driver.page_source,
                JSON_CSS_SELECTOR,
                hook.hashtag_post_count,
            )

        if limit > total_posts:
            return total_posts

        return limit

    def _get_urls(self, limit):
        """Return list with post urls to download files from."""

        def update_post_list():
            """Update lookup list with post urls."""

            main = self.driver.find_element_by_class_name(MAIN_CONTENT)
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, "html.parser")

            return soup.find_all(class_=POST)

        urls = set()
        scroll_pos = 0
        posts = update_post_list()

        while True:
            # Go through all scraped post urls.
            for post in posts:
                # Stop when all wanted urls has been added to the list.
                if len(urls) == limit:
                    break

                shortcode = post.parent["href"][3:-1]

                # Add posts not previously downloaded.
                if shortcode not in self.filelist:
                    url = "https://www.instagram.com/p/" + shortcode
                    urls.add(url)

            # Get new urls as long as limit hasn't been reached.
            if len(urls) < limit:
                posts = update_post_list()
                # Scroll down to see more posts in the feed.
                self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
                scroll_pos += 500

                continue

            break

        return list(urls)

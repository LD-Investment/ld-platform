import logging

import pandas as pd
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

logger = logging.getLogger(__name__)

"""
Note that Custom Commands are only available in LOCAL environment.
See config/settings/local.py
"""


class Command(BaseCommand):
    help = "Command for scrapping web data using Selenium or Beautifulsoup"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Bypass input from command",
        )
        parser.add_argument(
            "--fear-greed",
            action="store_true",
            help="Run Dunamu Fear & Greed Index scrapper",
        )

    def handle(self, *args, **options):
        """Scrapper Command"""

        if options["fear_greed"]:
            self.scrap_dunamu_fear_greed_index()

        self.stdout.write(self.style.SUCCESS("Successfully scrapped data"))

    @staticmethod
    def _set_chrome_options() -> Options:
        """Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs: dict = {"profile.default_content_settings": {"images": 2}}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        return chrome_options

    def scrap_dunamu_fear_greed_index(self):
        """Scrap function for Dunamu Fear & Greed Index"""
        logger.info("Starting Dunamu Fear & Greed Index Scraper")
        driver = webdriver.Remote(
            command_executor="http://selenium-chrome:4444/wd/hub",
            options=self._set_chrome_options(),
        )
        driver.implicitly_wait(5)
        logger.info("Done. Now starting scrapping data")

        BASE_URL = "https://datavalue.dunamu.com/feargreedindex"

        driver.get(url=BASE_URL)

        last_page_xpath = (
            "/html/body/div[2]/div/div[1]/div/div/div[4]/div/div[3]/span/a[6]"
        )
        last_page_num = int(driver.find_element(By.XPATH, last_page_xpath).text)

        next_button_xpath = '//*[@id="table-series_next"]'

        result = pd.DataFrame()

        for _ in tqdm(range(1, last_page_num)):
            try:
                table_body_xpath = '//*[@id="table-series"]'
                table_body_element = driver.find_element(By.XPATH, table_body_xpath)
                table_body_html = table_body_element.get_attribute("outerHTML")
                pd_html = pd.read_html(table_body_html)[0]

                result = pd.concat([result, pd_html], ignore_index=True)
                driver.find_element(By.XPATH, next_button_xpath).click()

            except NoSuchElementException as e:
                logger.error(f"Web scraper encountered error: {e.msg}")

            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt. Exiting...")
                driver.quit()
                exit(1)

        logger.info("Saving result as csv file as 'fear_greed_index_result.csv'..")
        result.to_csv("fear_greed_index_result.csv")
        logger.info("Dunamu Fear & Greed Index scraper finished. Stopping..")
        driver.quit()

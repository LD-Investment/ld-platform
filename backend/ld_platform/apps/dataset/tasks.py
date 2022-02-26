import logging

import ccxt
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from ld_platform.apps.dataset.models import CoinnessNewsData, LongShortRatioData
from ld_platform.shared.choices import CryptoExchangeChoices

logger = logging.getLogger(__name__)


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


@shared_task(soft_time_limit=300)
def scrap_coinness_news():
    """Scraps Coinness News periodically

    E.g https://coinness.live/news/1002000
    에이프로빗 실시간 주요 암호화폐 시세            # title_selector
    14:002021년 7월 22일 목요일               # date_selector
    *BTC 37,731,000원 ▲4.60%               # content_selector
    *ETH 2,315,000원 ▲6.83%
    ...
    Bull 14 Bear 11                       # bull_bear_selector
    """

    logger.info("Starting Coinness Web Scraper")
    driver = webdriver.Remote(
        command_executor="http://selenium-chrome:4444/wd/hub",
        options=_set_chrome_options(),
    )
    driver.implicitly_wait(5)

    BASE_URL = "https://coinness.live/news"

    title_selector = "#root > div > div > main > div > div.sc-bBXrwG.gIQUtB > h3"
    content_selector = "#root > div > div > main > div > div.sc-bBXrwG.gIQUtB > div.sc-lmoMya.jQLGnc > span"
    # bull_bear_selector = "#root > div > div > main > div > div.sc-bBXrwG.gIQUtB >
    # div.sc-crrszt.fqZBup > div.left > div > button.bull.false"

    # Get the latest article number
    ARTICLE_NUM = 1011000
    qs = CoinnessNewsData.objects.all().order_by("-article_num")
    if qs.exists():
        ARTICLE_NUM = int(qs[0].article_num) + 1

    logger.info(f"The latest article number is: {ARTICLE_NUM}")

    MAX_RETRY = 5
    CUR_TRIAL = 0
    while CUR_TRIAL < MAX_RETRY:
        try:
            cur_url = f"{BASE_URL}/{ARTICLE_NUM}"
            driver.get(url=cur_url)
            logger.info(f"Successfully connected to `{cur_url}`")
            title = driver.find_element(By.CSS_SELECTOR, title_selector)
            content = driver.find_element(By.CSS_SELECTOR, content_selector)
            # bull_bear = driver.find_element(By.CSS_SELECTOR, bull_bear_selector)

            kwargs = {
                "article_num": ARTICLE_NUM,
                "title": title.text,
                "content": content.text,
                # "bull_bear": bull_bear.text,
            }

            logger.info(f"Data parsed from HTML: {kwargs}")
            CoinnessNewsData.objects.create(**kwargs)
            CUR_TRIAL = 0

        except NoSuchElementException as e:
            CUR_TRIAL += 1
            logger.error(f"Coinness web scraper encountered error: {e.msg}")
            logger.info(f"Current Trial: {CUR_TRIAL}")

        except SoftTimeLimitExceeded as e:
            logger.error(f"SoftTimeLimitExceeded in Celery task. {e}")
            driver.quit()
            exit(1)

        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt. Exiting...")
            driver.quit()
            exit(1)

        ARTICLE_NUM += 1

    logger.info("Coinness Web scraper finished. Stopping..")
    driver.quit()


@shared_task(soft_time_limit=60)
def scrap_long_short_ratio_data():
    logger.info("Starting Long/Short Ratio Scraper")
    # init CCXT
    binance = ccxt.binance({"option": {"defaultMarket": "futures"}})
    bybit = ccxt.bybit({"enableRateLimit": True})
    logger.info("Successfully initiated CCXT exchanges")

    # Get BINANCE L/S Ratio for each symbols
    logger.info("Now fetching L/S ratio data from Binacne")
    for symbol_choice in LongShortRatioData.BinanceSymbolChoices.choices:
        res = binance.fapiData_get_globallongshortaccountratio(
            {
                "symbol": symbol_choice[0],
                "period": "5m",
                "limit": 1,
            }
        )[0]
        cur_timestamp = int(res["timestamp"]) / 1000

        # check with the latest data
        qs = LongShortRatioData.objects.filter(
            exchange_name=CryptoExchangeChoices.BINANCE, symbol=symbol_choice[0]
        ).order_by("-timestamp")

        # skip if already created
        if qs.exists() and qs[0].timestamp == cur_timestamp:
            logger.info(
                f"Data already exists for exchange(={CryptoExchangeChoices.BINANCE}), "
                f"symbol(={symbol_choice[0]}), timestamp(={cur_timestamp})"
            )
            continue

        LongShortRatioData.objects.create(
            exchange_name=CryptoExchangeChoices.BINANCE,
            symbol=symbol_choice[0],
            long_ratio=float(res["longAccount"]),
            short_ratio=float(res["shortAccount"]),
            timestamp=cur_timestamp,
        )  # 10 digits
        logger.info(
            f"Saved new data for exchange(={CryptoExchangeChoices.BINANCE}), "
            f"symbol(={symbol_choice[0]}), timestamp(={cur_timestamp})"
        )

    # Get BYBIT L/S Ratio for each symbols
    logger.info("Now fetching L/S ratio data from Bybit")
    for (
        symbol_choice
    ) in (
        LongShortRatioData.BybitSymbolChoices.choices
    ):  # type: LongShortRatioData.BinanceSymbolChoices
        res = bybit.public_get_v2_public_account_ratio(
            {"symbol": symbol_choice[0], "period": "5min", "limit": 1}
        )["result"][0]
        cur_timestamp = int(res["timestamp"])

        # check with the latest data
        qs = LongShortRatioData.objects.filter(
            exchange_name=CryptoExchangeChoices.BYBIT, symbol=symbol_choice[0]
        ).order_by("-timestamp")

        # skip if already created
        if qs.exists() and qs[0].timestamp == cur_timestamp:
            logger.info(
                f"Data already exists for exchange(={CryptoExchangeChoices.BYBIT}), "
                f"symbol(={symbol_choice[0]}), timestamp(={cur_timestamp})"
            )
            continue

        LongShortRatioData.objects.create(
            exchange_name=CryptoExchangeChoices.BYBIT,
            symbol=symbol_choice[0],
            long_ratio=float(res["buy_ratio"]),
            short_ratio=float(res["sell_ratio"]),
            timestamp=cur_timestamp,
        )  # 10 digits

        logger.info(
            f"Saved new data for exchange(={CryptoExchangeChoices.BYBIT}), "
            f"symbol(={symbol_choice[0]}), timestamp(={cur_timestamp})"
        )

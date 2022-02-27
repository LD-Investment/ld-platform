import time

from selenium import webdriver
from tqdm import tqdm

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1280")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/78.0.3904.108 Safari/537.36"
)

driver = webdriver.Chrome("./chromedriver", options=options)

texts = []


def main(last_page: int):
    for i in range(1, last_page):
        print("collecting from page {}".format(i))
        url = "https://www.ddengle.com/index.php?mid=board_all&page=" + str(i)
        driver.get(url)

        elems = driver.find_elements_by_css_selector("a.hx.bubble.no_bubble")

        links = []
        for e in elems:
            links.append(e.get_attribute('href'))

        for link in tqdm(links, position=0, leave=True):
            driver.get(link)
            time.sleep(0.1)
            try:
                elem = driver.find_elements_by_xpath('//*[@id="zema9_body"]/article/div[1]')
                for e in elem:
                    texts.append(e.text)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    LAST_PAGE = 8567
    main(LAST_PAGE)

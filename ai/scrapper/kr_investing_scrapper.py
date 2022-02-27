import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_contents(num_id):
    url = "https://kr.investing.com/news/cryptocurrency-news/article-" + str(num_id)
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    news_req = requests.get(url, headers=headers)
    news_content = BeautifulSoup(news_req.content, "lxml")
    try:
        title = news_content.find("h1").text
    except Exception as e:
        print(e)
        title = None
    exclusions = ["다시 검색해주세요",
                  "코멘트를 추가합니다",
                  "의견을 통해 다른 사용자들과 교류하고, 관점을 공유하고, 저자와 서로 간에 의문점을 제시하시기를 바랍니다. 하지만, 저희 모두가 기대하고 소중히 여기는 높은 수준의 담화를 유지하기 위해, 다음과 같은 기준을 기억하시기 바랍니다:",
                  "스팸 또는 비방글은 사이트에서 삭제될 것이며 Investing.com의 결정에 따라 추후 댓글 등록이 금지될 것입니다.",
                  "%USER_NAME%(을)를 정말로 차단하시겠습니까?",
                  "그렇게 하면, 귀하와 %USER_NAME%(은)는 서로의 Investing.com 게시물을 볼 수 없습니다.",
                  "%USER_NAME%(은)는 차단 명단에 추가되었습니다.",
                  "방금 이 사람을 차단해제하였으므로 48시간 이후에 차단을 재개할 수 있습니다.",
                  "나는 이 의견이 다음과 같다고 생각합니다:",
                  "감사합니다!",
                  "중개인 찾기",
                  "토큰포스트에서 읽기"]

    arr = []
    for element in news_content.findAll():
        if (element.name == 'p') and (element.text not in exclusions):
            try:
                if 'textDiv' not in element.parent['class'] and len(element.text) > 5:
                    arr.append(element.text)
            except Exception as e:
                print(e)
    return title, ' '.join(arr)


def main(last_page: int):
    titles, contents = [], []
    for i in range(1, last_page):
        print("collecting from page {}...".format(i))
        url = "https://kr.investing.com/news/cryptocurrency-news/" + str(i)
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        main_news_req = requests.get(url, headers=headers)
        main_news_content = BeautifulSoup(main_news_req.content, "lxml")

        article_nums = set()

        try:
            for a in main_news_content.find_all("a", href=True):
                if "/news/cryptocurrency-news/article-" in a['href']:
                    num_list = re.findall(r'\d+', str(a['href']))
                    for x in num_list:
                        article_nums.add(int(x))
        except Exception as e:
            print(e)
            continue

        for num_id in tqdm(article_nums, position=0, leave=True):
            title, content = get_contents(num_id)
            titles.append(title)
            contents.append(content)

        if i % 500 == 0:
            print("Saving most recent checkpoint...")
            df = pd.DataFrame(list(zip(titles, contents)), columns=['Title', 'Content'])
            df.to_csv("crypto_news_investing_kr.csv", index=False)


if __name__ == '__main__':
    LAST_PAGE = 2970
    main(LAST_PAGE)

import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
from requests.adapters import HTTPAdapter, Retry

# from urllib3.util.retry import Retry

travelled_road = []
iteration_counter = 200


# headers = {"accept": "application/json, text/javascript, */*; q=0.01", "user-agent": "Mozilla/5.0 (Windows NT 10.0; "
#            "Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}


def make_fake_user_agent():
    real_headers = {"user-agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    real_not_mine_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                             'Connection': 'closed'}
    ua = UserAgent()
    headers = {"User-agent": str(ua.chrome)}
    # return headers
    return real_not_mine_headers


def scrapeWikiArticle(url, goal_url, counter):
    if url == goal_url:
        return travelled_road
    elif counter != 0:

        session = requests.Session()
        retry = Retry(connect=4, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            response = session.get(url, timeout=30, headers=make_fake_user_agent())
        except requests.exceptions.ConnectionError:
            print("---Connection refused---")

            response = None
            while response is None:
                try:
                    response = session.get(url, timeout=30, headers=make_fake_user_agent())
                    break
                except:
                    print('---Connection error occurred---')
                    sleep(random.uniform(1.5, 10.5))
                    continue

        counter -= 1
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find(id="firstHeading")
        try:
            print(title.text)
        except AttributeError:
            print(travelled_road[-1])

        allLinks = soup.find(id="bodyContent").find_all("a")
        random.shuffle(allLinks)
        linkToScrape = 0

        for link in allLinks:
            # We are only interested in other wiki articles
            if link['href'].find("/wiki/") == -1:
                continue

            # Use this link to scrape
            linkToScrape = link
            break

        full_link_name = "https://en.wikipedia.org" + linkToScrape['href']
        travelled_road.append(full_link_name)
        scrapeWikiArticle(full_link_name, goal_url, counter)

    else:
        return []


def wiki_racing_set(url_start, url_finish):
    start_and_finish = {url_start, url_finish}

    response = requests.get(url_start, headers=make_fake_user_agent())
    soup = BeautifulSoup(response.content, 'html.parser')
    first_title = soup.find(id="firstHeading").text

    response = requests.get(url_finish, headers=make_fake_user_agent())
    soup = BeautifulSoup(response.content, 'html.parser')
    second_title = soup.find(id="firstHeading").text

    print("----------Wiki racing started!-----------")
    print(f"---Link to start with -> {first_title}---")
    print(f"----Link to win race -> {second_title}---")
    print(f"--------------Let`s start!---------------")

    scrapeWikiArticle(url_start, url_finish, counter=200)


if __name__ == "__main__":
    wiki_racing_set("https://en.wikipedia.org/wiki/Web_scraping",
                    "https://en.wikipedia.org/wiki/CERN")

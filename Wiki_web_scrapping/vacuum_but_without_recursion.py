import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
from requests.adapters import HTTPAdapter, Retry


def wiki_racing_settings(url_start, url_finish):
    start_and_finish = {url_start, url_finish}

    response = requests.get(url_start, headers=make_fake_user_agent())
    soup = BeautifulSoup(response.content, 'html.parser')
    first_title = soup.find(id="firstHeading").text

    response = requests.get(url_finish, headers=make_fake_user_agent())
    soup = BeautifulSoup(response.content, 'html.parser')
    second_title = soup.find(id="firstHeading").text

    return {first_title: url_start, second_title: url_finish}


def make_fake_user_agent():
    real_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    real_not_mine_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                             'Connection': 'closed'}
    ua = UserAgent()
    fake_headers = {"User-agent": str(ua.chrome), 'Connection': 'closed'}
    return fake_headers


def scrapeWikiArticle(url: str, iteration_counter: int, goal_url: str,
                      dict_of_keys_and_links: dict, unwanted_titles: list, unwanted_urls: list):
    iteration_counter -= 1
    if url != goal_url:

        if iteration_counter != 0:

            session = requests.Session()
            retry = Retry(connect=4, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            response = None
            while response is None:
                try:
                    response = session.get(url, timeout=15, headers=make_fake_user_agent())

                except requests.exceptions.ConnectionError:
                    print("---Connection refused---")
                    try:
                        response = session.get(list(dict_of_keys_and_links.values())[-1], timeout=15,
                                               headers=make_fake_user_agent())
                    except:
                        response = session.get(random.choice(list(dict_of_keys_and_links.values())), timeout=15,
                                               headers=make_fake_user_agent())

            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find(id="firstHeading")
            try:
                url_title = title.text
                for title_we_dont_want in unwanted_titles:
                    if url_title.startswith(title_we_dont_want):
                        unwanted_urls.append(url)
                        scrapeWikiArticle(list(dict_of_keys_and_links.values())[-1], iteration_counter, goal_url,
                                          dict_of_keys_and_links, unwanted_titles, unwanted_urls)
                else:
                    if url_title not in dict_of_keys_and_links.keys():
                        dict_of_keys_and_links[url_title] = url
                        print(url_title)
            except AttributeError:
                scrapeWikiArticle(list(dict_of_keys_and_links.values())[-2], iteration_counter, goal_url,
                                  dict_of_keys_and_links, unwanted_titles, unwanted_urls)

            allLinks = soup.find(id="bodyContent").find_all("a")

            # random.shuffle(allLinks)
            linkToScrape = 0

            for link in allLinks:
                if link['href'] == goal_url:
                    scrapeWikiArticle(goal_url, iteration_counter, goal_url,
                                      dict_of_keys_and_links, unwanted_titles, unwanted_urls)

            for link in allLinks:
                # We are only interested in other wiki articles
                if link in unwanted_urls or link['href'] is None or link['href'].find("/wiki/") == -1:
                    continue

                # Use this link to scrape
                linkToScrape = link
                break

            full_link_name = "https://en.wikipedia.org" + linkToScrape['href']
            scrapeWikiArticle(full_link_name, iteration_counter, goal_url,
                              dict_of_keys_and_links, unwanted_titles, unwanted_urls)

        else:
            return []

    else:
        return list(dict_of_keys_and_links.values())


if __name__ == "__main__":
    ready_and_set = wiki_racing_settings("https://en.wikipedia.org/wiki/Web_scraping",
                                         "https://en.wikipedia.org/wiki/Data_scraping"
                                         )
    # "https://en.wikipedia.org/wiki/CERN"
    list_of_the_runners = list(ready_and_set.keys())
    print("Wiki racing started!")
    print("------------------------------------------------")
    print(f"Link to start with -> {list_of_the_runners[0]}")
    print("------------------------------------------------")
    print(f"Link to win race -> {list_of_the_runners[1]}")
    print("------------------------------------------------")
    print(f"Let`s start!")

    travelled_road = {}
    road_pits = ["Template:", "Wikipedia:", "Category:", "User:", "Help:", "File:", "Portal:", "Template talk:"]
    dont_want_to_travel_there = []

    go = scrapeWikiArticle(ready_and_set[list_of_the_runners[0]], 200, ready_and_set[list_of_the_runners[1]],
                           travelled_road, road_pits, dont_want_to_travel_there)

    print(go)

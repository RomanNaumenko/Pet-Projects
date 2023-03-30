# def scrapeWikiArticle(url, goal_url, counter):
#     if url == goal_url:
#         return travelled_road
#     elif counter != 0:
#
#         session = requests.Session()
#         retry = Retry(connect=4, backoff_factor=1)
#         adapter = HTTPAdapter(max_retries=retry)
#         session.mount('http://', adapter)
#         session.mount('https://', adapter)
#
#         try:
#             response = session.get(url, timeout=30, headers=make_fake_user_agent())
#         except requests.exceptions.ConnectionError:
#             print("---Connection refused---")
#
#             response = None
#             while response is None:
#                 try:
#                     response = session.get(url, timeout=30, headers=make_fake_user_agent())
#                     break
#                 except:
#                     print('---Connection error occurred---')
#                     sleep(random.uniform(1.5, 10.5))
#                     continue
#
#         counter -= 1
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         title = soup.find(id="firstHeading")
#         try:
#             print(title.text)
#         except AttributeError:
#             print(travelled_road[-1])
#
#         allLinks = soup.find(id="bodyContent").find_all("a")
#         random.shuffle(allLinks)
#         linkToScrape = 0
#
#         for link in allLinks:
#             # We are only interested in other wiki articles
#             if link['href'].find("/wiki/") == -1:
#                 continue
#
#             # Use this link to scrape
#             linkToScrape = link
#             break
#
#         full_link_name = "https://en.wikipedia.org" + linkToScrape['href']
#         travelled_road.append(full_link_name)
#         scrapeWikiArticle(full_link_name, goal_url, counter)
#
#     else:
#         return []


from typing import List
import time
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
from requests.adapters import HTTPAdapter, Retry

requests_per_minute = 100
links_per_page = 200


# travelled_road = []


class WikiRacer:
    counter = 200

    def _lap_racing(self, current_url, target_url, list_of_results):

        current_url_links = []

        session = requests.Session()
        retry = Retry(connect=100, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                   'Connection': 'close'}

        try:
            response = session.get(current_url, timeout=30, headers=headers)
        except requests.exceptions.ConnectionError:
            print("---Connection refused---")

            response = None
            while response is None:
                try:
                    response = session.get(current_url, timeout=30, headers=headers)
                    break
                except:
                    print('---Connection error occurred---')
                    sleep(random.uniform(1.5, 10.5))
                    continue

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find(id="firstHeading")
        try:
            print(title.text)
        except AttributeError:
            print(list_of_results[-1])

        allLinks = soup.find(id="bodyContent").find_all("a")
        for link in allLinks:

            if len(current_url_links) != links_per_page:
                full_link = "https://en.wikipedia.org" + link['href']

                if link['href'].find(f"/wiki/{target_url}"):
                    list_of_results.append(full_link)
                    break

                current_url_links.append(full_link)

            random_Link_choice = random.choice(current_url_links)
            list_of_results.append(random_Link_choice)

        return list_of_results

    def find_path(self, start: str, finish: str) -> List[str]:

        start = "https://uk.wikipedia.org/wiki/" + start
        finish = "https://uk.wikipedia.org/wiki/" + finish

        travelled_road = [start]

        while finish not in travelled_road:
            self._lap_racing(travelled_road[-1], finish, travelled_road)
            self.counter += 1
            if self.counter == 0:
                return []


if __name__ == "__main__":
    racer = WikiRacer()
    path = racer.find_path("https://uk.wikipedia.org/wiki/%D0%94%D1%80%D1%83%D0%B6%D0%B1%D0%B0",
                           "https://uk.wikipedia.org/wiki/%D0%A0%D0%B8%D0%BC")

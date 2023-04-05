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
# road_pits = ["Template:", "Wikipedia:", "Category:", "User:", "Help:", "File:", "Portal:", "Template talk:"]


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

        road_pits = ["Template:", "Wikipedia:", "Category:", "User:",
                     "Help:", "File:", "Portal:", "Template talk:",
                     "Категорія:", "Файл:", "Вікіпедія:", "Шаблон:",
                     "Категорії", "Довідка:", "Обговорення Вікіпедії:"]

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
        for pit in road_pits:
            if title.text.find(pit) != -1:
                list_of_results.pop()
                return list_of_results

        try:
            print(title.text)
            print(list_of_results[-1])
        except AttributeError:
            list_of_results.pop()
            return list_of_results
        """Todo: 
        1. Зробити перевірку на наявність road_pits.
        2. Зробити конкатенацію з 'link['href'].find("/wiki/") == -1' для правильної валідації посилання."""
        allLinks = soup.find(id="bodyContent").find_all("a")
        for link in allLinks:

            # if len(current_url_links) != links_per_page:
            try:
                if link['href'] is None or link['href'].find("/wiki/") == -1:
                    continue
            except KeyError:
                continue

            full_link = "https://uk.wikipedia.org" + link['href']
            """Here is mistake!
            Краще спробувати перевірити за тайтлом"""
            if full_link == target_url:
                list_of_results.append(full_link)
                break

            current_url_links.append(full_link)

        random_Link_choice = random.choice(current_url_links)
        list_of_results.append(random_Link_choice)
        return list_of_results

    def find_path(self, start: str, finish: str) -> List[str]:

        start_url = "https://uk.wikipedia.org/wiki/" + start
        finish_url = "https://uk.wikipedia.org/wiki/" + finish

        travelled_road = []
        travelled_road.append(start_url)

        while finish not in travelled_road:

            self._lap_racing(travelled_road[-1], finish_url, travelled_road)
            self.counter -= 1
            if self.counter == 0:
                return []


if __name__ == "__main__":
    racer = WikiRacer()
    path = racer.find_path("Якопо_Понтормо",
                           "Художник")

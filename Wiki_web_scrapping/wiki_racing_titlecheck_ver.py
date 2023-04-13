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


class WikiRacer:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                        'Connection': 'close'}
        self.road_pits = ["Template:", "Wikipedia:", "Category:", "User:",
                          "Help:", "File:", "Portal:", "Template talk:",
                          "Категорія:", "Файл:", "Вікіпедія:", "Шаблон:",
                          "Категорії", "Довідка:", "Обговорення Вікіпедії:"]

    def find_path(self, start: str, finish: str) -> List[str]:

        list_of_results = [start]
        list_of_temporary = []

        session = requests.Session()
        retry = Retry(connect=100, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        current_url = "https://uk.wikipedia.org/wiki/" + start
        # print(current_url)
        try:
            response = session.get(current_url, timeout=30, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print("---Connection refused---")
            response = None
            while response is None:
                response = session.get(current_url, timeout=30, headers=self.headers)
                break

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id="firstHeading")
        for unwanted_title in self.road_pits:
            if title.text.find(unwanted_title) != -1:
                print("Unwanted title! Let`s try another link.")
                return list_of_results

        all_links = soup.find_all('a')
        if len(list_of_temporary) != 200:
            for link in all_links:
                try:
                    link_title = link['title']
                    print(link_title)
                except KeyError:
                    continue
                if link_title == finish:
                    # full_link = "https://uk.wikipedia.org" + link['href']
                    list_of_results.append(link_title)
                    return list_of_results
                else:
                    list_of_temporary.append(link_title)
        else:
            random_link_choice = random.choice(list_of_temporary)
            list_of_results.append(random_link_choice)

        return list_of_results


if __name__ == "__main__":
    racer = WikiRacer()
    path = racer.find_path("Якопо_Понтормо",
                           "Художник")
    print(path)

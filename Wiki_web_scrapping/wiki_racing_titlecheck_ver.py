from typing import List
import time
# from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
from requests.adapters import HTTPAdapter, Retry

requests_per_minute = 100
links_per_page = 200


# road_pits = ("Template:", "Wikipedia:", "Category:", "User:",
#                           "Help:", "File:", "Portal:", "Template talk:",
#                           "Категорія:", "Файл:", "Вікіпедія:", "Шаблон:",
#                           "Категорії", "Довідка:", "Обговорення Вікіпедії:",
#                           "Редагувати розділ:")

class UnwantedTitleError(Exception):
    pass


class UnwantedLinkError(Exception):
    pass


class WikiRacer:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                        'Connection': 'close'}
        self.road_pits = (":", "Збільшити", "(ще не написана)", "Категорія:", "Файл:", "Вікіпедія:",
                          "Шаблон:", "Категорії", "Довідка:", "Обговорення Вікіпедії:",
                          "Редагувати розділ:", "Спеціальна:",  "en:", "Обговорення:")

    def find_path(self, start: str, finish: str, list_of_results: list) -> List[str]:

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
        print(f"Title: {title.text}")
        all_links = soup.find(id="bodyContent").find_all('a')

        for link in all_links:
            if len(list_of_temporary) <= 100:
                try:
                    link_title = link['title']
                    if link_title in list_of_temporary:
                        continue
                    for unwanted_title in self.road_pits:
                        if link_title.find(unwanted_title) != -1:
                            # print("Unwanted title! Let`s try another link.")
                            raise UnwantedTitleError
                    # print(link_title)
                    if link['href'].endswith('.png'):
                        raise UnwantedLinkError

                except (KeyError, UnwantedTitleError, UnwantedLinkError):
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
                print(list_of_results)
                break

        list_of_temporary.clear()
        return list_of_results

    def pathfinder(self, start: str, finish: str) -> List[str]:

        list_of_results = [start]
        counter = 200
        while finish not in list_of_results and counter != 0:
            result = self.find_path(list_of_results[-1], finish, list_of_results)
            list_of_results = result
            continue
        return list_of_results
    print("___________________")


if __name__ == "__main__":
    racer = WikiRacer()
    path = racer.pathfinder("Дружба",
                            "Рим")
    print(path)

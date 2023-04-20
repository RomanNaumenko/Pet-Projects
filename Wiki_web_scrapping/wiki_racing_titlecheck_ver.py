from typing import List
import time
# from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import pprint
from requests.adapters import HTTPAdapter, Retry
import psycopg2


class UnwantedTitleError(Exception):
    pass


class UnwantedLinkError(Exception):
    pass


class NonExistentLinkError(Exception):
    pass


class WikiRacer:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                        'Connection': 'close'}
        self.road_pits = (":", "Збільшити", "(ще не написана)", "Вікіпедія", "Категорія:", "Файл:",
                          "Вікіпедія:", "Шаблон:", "Категорії", "Довідка:", "Обговорення Вікіпедії:",
                          "Редагувати розділ:", "Спеціальна:", "en:", "Обговорення:",
                          "Перегляд цього шаблону")
        self.db_config = "host=localhost dbname=links_db user=postgres password=redeath25101993R"

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

                if link['href'] == f'https://uk.wikipedia.org/w/index.php?title={link_title}&action=edit':
                    raise NonExistentLinkError

            except (KeyError, UnwantedTitleError, UnwantedLinkError, NonExistentLinkError):
                continue

            if link_title == finish:
                # full_link = "https://uk.wikipedia.org" + link['href']
                list_of_results.append(link_title)
                return list_of_results
            else:
                list_of_temporary.append(link_title)
                continue
        try:
            list_of_temporary = list(set(list_of_temporary[0:200]))
            random_link_choice = random.choice(list_of_temporary)
            list_of_results.append(random_link_choice)
            # print(F"Urls: {list_of_results}")
            print(f"Urls in total: {len(list_of_results)}")
            print('\n')
            list_of_temporary.clear()
            return list_of_results

        except IndexError:
            list_of_results.pop()
            return list_of_results

    def url_storage_check(self, start: str, finish: str):
        with psycopg2.connect(self.db_config) as conn:
            with conn.cursor() as curs:
                curs.execute(f"SELECT path FROM paths "
                             f"WHERE start_point='{start}' AND finish_point='{finish}'")
                db_check = curs.fetchone()
                if db_check:
                    result = []
                    for every_sequence in db_check:
                        for every_elem in every_sequence:
                            result.append(every_elem)

                    return result

                """TODO: Make a check for a too long storage path sequence."""

    def url_storage_save(self, results: list):
        start = results[0]
        finish = results[-1]
        array = ["\"{every_elem}\"" for every_elem in results]
        with psycopg2.connect(self.db_config) as conn:
            with conn.cursor() as curs:
                curs.execute(f"INSERT INTO paths (start_point,finish_point,path) "
                             f"VALUES ('{start}', '{finish}', ARRAY[{array}])")

    def pathfinder(self, start: str, finish: str) -> List[str]:

        db_check = self.url_storage_check(start, finish)
        if db_check:
            return db_check

        list_of_results = [start]
        counter = 200
        while finish not in list_of_results:
            if counter == 0:
                break
            counter -= 1
            result = self.find_path(list_of_results[-1], finish, list_of_results)
            list_of_results = result

            continue
        # print(self.db_url_storage())
        if finish not in list_of_results:
            return []
        self.url_storage_save(list_of_results)
        return list_of_results

    print("___________________")


if __name__ == "__main__":
    racer = WikiRacer()
    # path = racer.pathfinder("Дружба",
    #                         "Рим")
    # path = racer.pathfinder("Мітохондріальна ДНК", "Вітамін K")
    path = racer.pathfinder('Мітохондріальна ДНК', 'Вітамін K')
    print(path)

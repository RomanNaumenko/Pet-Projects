from bs4 import BeautifulSoup
import requests
import lxml
import urllib.request, urllib.error, urllib.parse
import pprint
import random
import time

url = 'https://uk.wikipedia.org/wiki/%D0%94%D1%80%D1%83%D0%B6%D0%B1%D0%B0'
travelled_road = []
headers = {"accept": "application/json, text/javascript, */*; q=0.01", "user-agent": "Mozilla/5.0 (Windows NT 10.0; "
                                                                                     "Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}


def web_reader(path: str):
    with open(path, encoding="utf-8") as file:
        src = file.read()
        return src


def web_saviour(wiki_url: str):
    req = requests.get(wiki_url, headers=headers)
    src = req.text
    sliced_url = wiki_url.split('/')
    file_name = f"{sliced_url[3]}_{sliced_url[4]}"
    file_name_and_path = f"web_pages/{file_name}.html"
    with open(file_name_and_path, "w", encoding="utf-8") as file:
        file.write(src)

    return web_reader(file_name_and_path)


links_list = []


# soup = BeautifulSoup(web_saviour(url), 'lxml')
# wiki_title = soup.title.string
# travelled_road.append(wiki_title)


def scrape_wiki_article(url: str):

    response = requests.get(
        url=url,
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    print(title.text)
    links_list.append(title.text)

    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)
    linkToScrape = 0

    for link in allLinks:
        try:
        # We are only interested in other wiki articles
            if link['href'].find("/wiki/") == -1:
                continue
        except KeyError as error:
            print(error)
            continue

        # Use this link to scrape
        linkToScrape = link
        break

    scrape_wiki_article("https://en.wikipedia.org" + linkToScrape['href'])


scrape_wiki_article("https://uk.wikipedia.org/wiki/%D0%94%D1%80%D1%83%D0%B6%D0%B1%D0%B0")

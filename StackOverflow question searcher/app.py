import requests
from flask import Flask
import json

app = Flask(__name__)

response = requests.get("https://api.stackexchange.com/2.3/"
                        "questions?order=desc&sort=activity&site=stackoverflow")

for quests in response.json()['items']:
    if quests['answer_count'] == 0:
        print(f"{quests['title']}")
        print(f"{quests['link']}\n")
    else:
        print("-------SKIPPED-------")
    print()


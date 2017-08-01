import json
import telegram

with open("./server/secure_conf.json", "r") as conf_file:
     bot = telegram.Bot(token=json.load(conf_file)["token"])

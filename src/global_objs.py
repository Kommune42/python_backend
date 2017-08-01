import json
import telegram

with open("./conf/secure_conf.json", "r") as conf_file:
     bot = telegram.Bot(token=json.load(conf_file)["token"])

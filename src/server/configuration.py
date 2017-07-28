# -*- coding: utf-8 -*-
import telegram
import json

secure_conf = json.load(open("./secure_conf.conf"))
token = secure_conf["token"]
bot = telegram.Bot(token=token)

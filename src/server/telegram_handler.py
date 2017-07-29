# -*- coding: utf-8 -*-
import telegram
import json

with open("./secure_conf.json", "r") as conf_file:
     bot = telegram.Bot(token=json.load(conf_file)["token"])

updates_buffer = []
last_update_id = 0


def update_buffer():

    try:
        new_updates = bot.get_updates(offset=last_update_id + 1)
    except telegram.error.TimedOut:
        new_updates = []

    updates_buffer = updates_buffer + new_updates

    for update in new_updates:
        if update.update_id > last_update_id:
            last_update_id = update.update_id

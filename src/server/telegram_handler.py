# -*- coding: utf-8 -*-
import telegram
import json
from src.global_objs import bot
from src.server import buffer_management

import time

last_update_id = 0


def update_buffer():
    global last_update_id

    try:
        new_updates = bot.get_updates(offset=last_update_id + 1)
    except telegram.error.TimedOut:
        new_updates = []

    for update in new_updates:
        buffer_management.buffer_telegram_update(update)

    for update in new_updates:
        if update.update_id > last_update_id:
            last_update_id = update.update_id

def get_next_update(old_update_id):
    for update in []:
        if update.update_id > old_update_id:
            return update
    return None

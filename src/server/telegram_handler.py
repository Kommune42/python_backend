# -*- coding: utf-8 -*-
import telegram
import json
from src.global_objs import bot

updates_buffer = []
last_update_id = 0


def update_buffer():
    global last_update_id
    global updates_buffer

    try:
        new_updates = bot.get_updates()  # offset=last_update_id + 1)
    except telegram.error.TimedOut:
        new_updates = []

    updates_buffer = updates_buffer + new_updates

    for update in new_updates:
        if update.update_id > last_update_id:
            last_update_id = update.update_id


def get_next_update(old_update_id):
    for update in updates_buffer:
        if update.update_id > old_update_id:
            return update
    return None

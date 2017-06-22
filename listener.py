# -*- coding: utf-8 -*-
import os
from telegram.utils import webhookhandler
import queue
import config

update_queue = queue.Queue()

def init(bot):
    global server
    server = webhookhandler.WebhookServer(("saufbot.herokuapp.com", int(os.environ.get("PORT"))), webhookhandler.WebhookHandler, update_queue, config.token, bot)
    server.serve_forever()

def get_updates():
    updates = []
    while not update_queue.empty():
        updates.append(update_queue.get())
    return updates

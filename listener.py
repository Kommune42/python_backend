# -*- coding: utf-8 -*-
from telegram.utils import webhookhandler
import queue
import config

update_queue = queue.Queue()

def init(bot):
    global server
    server = webhookhandler.WebhookServer((config.webhook_address + config.token, 80), webhookhandler.WebhookHandler, update_queue, config.token, bot)
    server.serve_forever()

def get_updates():
    updates = []
    while not update_queue.empty():
        updates.append(update_queue.get())
    return updates

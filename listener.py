# -*- coding: utf-8 -*-
import telegram
import queue
import config

update_queue = queue.Queue()

def init(bot):
    global server
    server = telegram.utils.webhookhandler.WebhookServer((config.webhook_address, 80), telegram.utils.webhookhandler.WebhookHandler, update_queue, config.token, bot)
    server.serve_forever()

def get_updates():
    updates = []
    while not update_queue.empty():
        updates.append(update_queue.get())
    return updates

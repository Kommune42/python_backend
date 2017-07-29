# -*- coding: utf-8 -*-
import json
from communication import socket_handler
from . import telegram_handler

with open("./server_conf.json", "r") as conf_file:
    conf = json.load(conf_file)

connections_state = {}

def start():
    server = socket_handler.server(("", 4201), respond, "telegram_read")
    server.start()

def respond(msg, connection):
    if msg["action"] == "register_connection":
        handler_name = msg["data"]
        connections_state[connection] = {"last_update_id": 0}
        connection.send(socket_handler.message(action="ack"))
    if msg["action"] == "get_updates":
        if msg["data"].isdigit():
            pass
            #TODO What now?
        new_update = telegram_handler.get_new_updates(update_id=connections_state[connection]["last_update_id"])
        socket_handler.send_long(new_update.to_json(), connection)
        connections_state[connection]["last_update_id"] = new_update.id
        connection.send("ack")

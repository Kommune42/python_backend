# -*- coding: utf-8 -*-
import json
from communication import socket_handler
from . import telegram_handler

with open("./server/server_conf.json", "r") as conf_file:
    conf = json.load(conf_file)

connections_state = {}

def start():
    global server
    server = socket_handler.server(("", 4201), respond, "telegram_read")
    server.start()

def stop():
    server.stop()

def respond(msg, connection):
    if msg["action"] == "register_connection":
        handler_name = msg["data"]
        connections_state[connection] = {"last_update_id": 0}
        socket_handler.send_long(socket_handler.message(action="ack"), connection)
    if msg["action"] == "get_update":
        if msg["data"].isdigit():
            pass
            #TODO What now?
        new_update = telegram_handler.get_next_update(old_update_id=connections_state[connection]["last_update_id"])
        if new_update is not None:
            socket_handler.send_long(new_update.to_json(), connection)
            connections_state[connection]["last_update_id"] = new_update.id
            socket_handler.send_long(socket_handler.message(action="ack"), connection)
        else:
            socket_handler.send_long(socket_handler.message(action="ack"), connection)

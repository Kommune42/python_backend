# -*- coding: utf-8 -*-
import json
from lib.communication import socket_handler
import telegram_handler

with open("./conf/telegram_server/server_conf.json", "r") as conf_file:
    conf = json.load(conf_file)

connections_state = {}

def start():
    global server
    server = socket_handler.server(("", 4201), respond, "telegram_read")
    server.start()

def stop():
    server.stop()

def respond(msg, identifier):
    if msg["action"] == "register_connection":
        handler_name = msg["data"]
        connections_state[identifier] = {"last_update_id": 0}
        return socket_handler.message(action="ok")
    if msg["action"] == "get_update":
        if msg["data"].isdigit():
            pass
            #TODO What now?
        new_update = telegram_handler.get_next_update(old_update_id=connections_state[identifier]["last_update_id"])
        print "UPDATE: " + str(new_update)
        if new_update is not None:
            connections_state[identifier]["last_update_id"] = new_update.update_id
            return socket_handler.message(data=new_update.to_json())
        else:
            return socket_handler.message(data="{}")

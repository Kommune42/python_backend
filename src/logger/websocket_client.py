# -*- coding: utf-8 -*-
import telegram
from communication import socket_handler
import global_objs


client = socket_handler.client(name="logger")

def connect():
    client.connect_to(("localhost", 4201), module_name="telegram_read")
    client.request(socket_handler.message(action="register_connection"))

def get_update():
    returned_msg = client.request(socket_handler.message(action="get_update"))
    if returned_msg == {}:
        return "None"
    else:
        return telegram.Update.de_json(returned_msg["data"], global_objs.bot)  # FIXME Where does the bot come from?
    return "WHAT"

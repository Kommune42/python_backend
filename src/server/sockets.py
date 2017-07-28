import json
from communication import socket_handler


with open("./server_conf.json", "r") as conf_file:
    conf = json.load(conf_file)

def start():
    server = socket_handler.server(("", 4201), respond, "telegram_read")
    server.start()

def respond(data, conection):
    pass

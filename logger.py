# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import string
import json

import config
import helper
import busses


def log_message(msg):
    #log format: time type message

    time_str = str(time.time())
    line = time_str[:time_str.find(".")]
    line = line.rjust(10, str(" "))
    line += " "

    busses.status_bus["latest_messages"][msg.chat_id] = msg

    msg_type = helper.get_message_type(msg)
    if msg_type == "text" and msg.text.startswith("/"):
        msg_type = "command"

    appendix = "ERROR"
    if msg_type == "text":
        appendix = msg.text
    elif msg_type == "command":
        appendix = msg.text[1:]
    elif msg_type == "location":
        location_data = msg.location.to_dict()
        appendix = str(location_data["latitude"]) + "°, " + str(location_data["longitude"]) + "°"
    elif msg_type == "contact":
        appendix = str(msg.contact.user_id) + " " + msg.contact.first_name + " " + msg.contact.last_name
    elif msg_type == "new_user":
        appendix = str(msg.new_chat_member.id) + " " + str(msg.new_chat_member.first_name) + " " + str(msg.new_chat_member.last_name)
    elif msg_type in ["audio", "document", "game", "photo", "sticker", "video", "voice", "video_note", "unknown"]:
        appendix = ""

    msg_type = msg_type.rjust(10, str(" "))
    appendix = appendix.replace("\n", "\\n").rjust(40, str(" "))
    line += msg_type + " " + appendix + " "

    line += str(msg.chat_id) + "," + str(msg.message_id)
    line += "\n"

    with open(config.msg_log_file_path, "a") as log_file:
        log_file.write(line.encode("utf-8"))


def complete_log(update):
    with open(config.complete_log_file_path, "a") as log_file:
        data = update.to_dict()
        data.update({"time": time.time()})
        json_data = json.dumps(data)
        log_file.write(str(json_data).replace("\n", "\\n") + "\n".encode("utf-8"))

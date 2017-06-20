# -*- coding: utf-8 -*-
import telegram
import uuid
import config
import busses
import helper
from language import get_locale

def command_handler(msg):
    if len(msg.text) == 0:
        return
    command = msg.text.split()[0][1:]
    if len(command) + 2 < len(msg.text):
        args = msg.text[len(command) + 1:].split()
    else:
        args = []
    chat_type = msg.chat.type
    chat_id = msg.chat.id
    is_admin = msg.from_user.id in config.admin_ids

    if helper.is_conversation_status(None, msg):
        if command == get_locale("whereat"):
            msg.reply_text(get_locale("whereat_response"))
            helper.set_conversation_status(msg, "whereat")
        if command == get_locale("setat"):
            station = helper.correct_station_name(args[0])
            busses.status_bus["station"] = config.stations.index(station)
            msg.reply_text(get_locale("hereat") + station)

def text_handler(msg):
    chat_id = msg.chat.id
    text = msg.text
    if helper.is_conversation_status("whereat", msg):
        station = config.station_correcter.correct_word(text)
        if station in config.stations:
            msg.reply_text(get_locale("hereat") + station)
        else:
            msg.reply_text(get_locale("couldnotfindstation"))
        helper.set_conversation_status(msg, None)

def location_handler(msg):
    chat_id = msg.chat.id

    if helper.is_conversation_status("whereat", msg):
        station = helper.get_closest_station(msg.location.to_dict())
        msg.reply_text(get_locale("hereat") + station)
        helper.set_conversation_status(msg, None)

def inline_handler(inline):
    query = inline.query
    location = inline.location
    if len(query) == 0:
        return
    command = inline.query.split()[0]
    if len(command) + 1 < len(query):
        args = inline.query[len(command):].split()
    else:
        args = []
    if command == get_locale("setat"):
        if location is not None:
            station = helper.get_closest_station(location.to_dict())
        elif len(args) > 0:
            station = helper.correct_station_name(args[0])
        else:
            return

        inline.answer([telegram.InlineQueryResultArticle(id=uuid.uuid4(),
                                            title=station,
                                            input_message_content=telegram.InputTextMessageContent(
                                            "/" + get_locale("setat") + " " + station))])
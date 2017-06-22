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
    is_admin = True  # msg.from_user.id in config.admin_ids


    if helper.is_conversation_status(None, msg):

        if command == get_locale("setat") and is_admin:
            if len(args) == 0:
                msg.reply_text(get_locale("setat_response"))
                helper.set_conversation_status(msg, "setat")
            else:
                station = helper.correct_station_name(args[0])
                busses.status_bus["station"] = config.stations.index(station)
                msg.reply_text(get_locale("hereat") + station)

        if command == get_locale("whereat"):
            station = config.stations[busses.status_bus["station"]]
            msg.reply_text(get_locale("hereat") + station)

        if command == get_locale("cancel"):
            helper.set_conversation_status(msg, None)

        if command == get_locale("next") and is_admin:
            index = busses.status_bus["station"]
            index += 1
            index = index % len(config.stations)
            busses.status_bus["station"] = index
            msg.reply_text(get_locale("drivingto") + config.stations[index])

def text_handler(msg):
    chat_id = msg.chat.id
    text = msg.text

def location_handler(msg):
    chat_id = msg.chat.id

    if helper.is_conversation_status("setat", msg):
        station = helper.get_closest_station(msg.location.to_dict())
        busses.status_bus["station"] = config.stations.index(station)
        msg.reply_text(get_locale("hereat") + station)
        helper.set_conversation_status(msg, None)

def inline_handler(inline):
    query = inline.query
    location = inline.location
    is_admin =  True # inline.from_user.id in config.admin_ids

    if len(query) == 0:
        return
    command = inline.query.split()[0]

    if len(command) + 1 < len(query):
        args = inline.query[len(command):].split()
    else:
        args = []

    if command == get_locale("setat") and is_admin:
        if location is not None:
            station = helper.get_closest_station(location.to_dict())
        elif len(args) > 0:
            station = helper.correct_station_name(args[0])
        else:
            return
        query_result = telegram.InlineQueryResultArticle(id=uuid.uuid4(),
                                            title=station,
                                            input_message_content=telegram.InputTextMessageContent(
                                            "/" + get_locale("setat") + " " + station))
        inline.answer(results=[query_result], cache_time=0)

    if command == get_locale("whereat"):
        station = config.stations[busses.status_bus["station"]]
        query_result = telegram.InlineQueryResultArticle(id=uuid.uuid4(),
                                    title=station,
                                    input_message_content=telegram.InputTextMessageContent(
                                    get_locale("hereat") + station))
        inline.answer(results=[query_result], cache_time=0)

    if command == get_locale("next"):
        station = config.stations[busses.status_bus["station"] + 1]
        if is_admin:
            query_result = telegram.InlineQueryResultArticle(id=uuid.uuid4(),
                                                title=station,
                                                input_message_content=telegram.InputTextMessageContent(
                                                "/" + get_locale("next")))
        else:
            query_result = telegram.InlineQueryResultArticle(id=uuid.uuid4(),
                                        title=station,
                                        input_message_content=telegram.InputTextMessageContent(
                                        "/" + get_locale("whereat")))
        inline.answer(results=[query_result],cache_time=0)

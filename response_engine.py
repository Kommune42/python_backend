# -*- coding: utf-8 -*-
import telegram
import uuid
import config
import busses
import helper
import mangament_units
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
    location = msg.location
    is_admin = True  # msg.from_user.id in config.admin_ids


    if helper.is_conversation_status(None, msg):

        if command == get_locale("setat") and is_admin:

            possible_stations = []
            if location is not None:
                possible_stations.append(helper.get_closest_station(location.to_dict()))
            if len(args) > 0:
                possible_stations = possible_stations + helper.get_matches(args[0], 5 - len(possible_stations))
            if len(possible_stations) == 0:
                return

            reply_keyboard = []
            inline_button = telegram.inlinekeyboardbutton.InlineKeyboardButton

            for station in possible_stations:
                reply_keyboard.append([inline_button(station, callback_data="set_station_" + station)])

            reply_markup = telegram.inlinekeyboardmarkup.InlineKeyboardMarkup(reply_keyboard)
            msg.reply_text(get_locale("select"), reply_markup=reply_markup)

        if command == get_locale("setline"):
            if len(args) == 0:
                msg.reply_text(get_locale(config.line))
            elif is_admin:
                if args[0] in ["S41", "S42"]:
                    config.line = args[0]
                msg.reply_text(get_locale(config.line))

        if command == get_locale("whereat"):
            msg.reply_text(get_locale("hereat") + helper.get_current_station_name())

        if command == get_locale("cancel"):
            helper.set_conversation_status(msg, None)

        if command == get_locale("next") and is_admin:
            mangament_units.advance_station()
            msg.reply_text(get_locale("drivingto") + helper.get_current_station_name())

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

# def inline_handler(inline):
#     query = inline.query
#     location = inline.location
#     is_admin =  True # inline.from_user.id in config.admin_ids
#
#     if len(query) == 0:
#         return
#     command = inline.query.split()[0]
#
#     if len(command) + 1 < len(query):
#         args = inline.query[len(command):].split()
#     else:
#         args = []
#
#     def create_result_article(title, _input):
#         _id = uuid.uuid4()
#         input_message_content = telegram.InputTextMessageContent(_input)
#         return telegram.InlineQueryResultArticle(id=_id, title=station, input_message_content=input_message_content)
#
#
#     if command == get_locale("setat") and is_admin:
#         possible_stations = []
#         if location is not None:
#             possible_stations.append(helper.get_closest_station(location.to_dict()))
#         elif len(args) > 0:
#             possible_stations = possible_stations + helper.get_matches(args[0], 4)
#         else:
#             return
#
#         #Without arguments use location
#         if location is not None and len(args) == 0:
#             station = possible_stations[0]
#             result = create_result_article(station, get_locale("hereat") + station)
#         #Else use corrected args
#         elif len(args) > 0:
#             if location is None:
#                 station = possible_stations[0]
#                 result = create_result_article(station, get_locale("hereat") + station)
#             else:
#                 station = possible_stations[1]
#                 result = create_result_article(station, get_locale("hereat") + station)
#
#         inline.answer(results=[result], cache_time=0)
#
#     if command == get_locale("whereat"):
#         query_result = create_result_article(helper.get_current_station_name(),
#                                                 get_locale("hereat") + helper.get_current_station_name())
#         inline.answer(results=[query_result], cache_time=0)
#
#     if command == get_locale("next"):
#         station = config.stations[busses.status_bus["station"] + 1]
#         if is_admin:
#             query_result = create_result_article(station, get_locale("drivingto") + station)
#             mangament_units.advance_station()
#         else:
#             query_result = create_result_article(station, get_locale("noadmin"))
#         inline.answer(results=[query_result], cache_time=0)

def callback_handler(callback_query, bot):
    data = callback_query.data
    #TODO implement is_admin

    if data.startswith("set_station_"):
        arg = data.split("_")[-1]

        mangament_units.set_station(arg)

        callback_query.answer(get_locale("hereat") + arg)
        bot.send_message(chat_id=callback_query.message.chat.id, text=get_locale("hereat")+arg)

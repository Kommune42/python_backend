# -*- coding: utf-8 -*-
import telegram
import config
import helper
import listener
import busses
import response_engine

try:
    import heroku_satisfier
except ImportError:
    pass

saufi = telegram.Bot(token=config.token)

listener.update_queue(saufi)


for _ in range(500000):
    for update in busses.new_updates:
        #Some updates do not have a message
        if update.message is not None:
            msg = update.message
            msg_type = helper.get_message_type(msg)

            if not msg.chat.id in busses.conversation_bus:
                busses.conversation_bus[msg.chat.id] = {"state": None, "user": 0}

            if msg_type == "location":
                response_engine.location_handler(msg)

            if msg_type == "text":
                if msg.text[0] == "/":
                    response_engine.command_handler(msg)
                else:
                    response_engine.text_handler(msg)
        elif update.inline_query is not None:
            response_engine.inline_handler(update.inline_query)

        busses.handled_updates.append(update)

    listener.update_queue(saufi)

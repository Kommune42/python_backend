# -*- coding: utf-8 -*-
import telegram

import config
import helper
import listener
import busses
import response_engine
import logger

listener.update_queue(config.saufi)

try:
    while config.run:
        for update in busses.new_updates:
            logger.complete_log(update)
            #Some updates do not have a message
            if update.message is not None:
                msg = update.message
                msg_type = helper.get_message_type(msg)

                logger.log_message(msg)

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
                #TODO RE-IMPLEMENT INLINE BOT
                #response_engine.inline_handler(update.inline_query)
                pass
            elif update.callback_query is not None:
                try:
                    response_engine.callback_handler(update.callback_query, config.saufi)
                except telegram.error.BadRequest:
                    pass

            busses.handled_updates.append(update)

        listener.update_queue(config.saufi)
except KeyboardInterrupt:
    helper.shutdown()

# -*- coding: utf-8 -*-
import telegram
import config
import helper
import listener
import busses

saufi = telegram.Bot(token=config.token)

listener.update_queue(saufi)

print [helper.get_message_type(u.message) for u in busses.new_updates]
busses.handled_updates = busses.new_updates

listener.update_queue(saufi)

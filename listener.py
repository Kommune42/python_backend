# -*- coding: utf-8 -*-
import thread
import busses


def update_queue(bot):

    if len(busses.handled_updates) != 0:
        last_id = busses.handled_updates[-1].update_id
    else:
        last_id = -1

    busses.new_updates = busses.new_updates + bot.get_updates(offset=last_id + 1)

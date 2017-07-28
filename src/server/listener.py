# -*- coding: utf-8 -*-
import busses
import telegram


def update_queue(bot):

    #Determine last update id
    if len(busses.handled_updates) != 0:
        #use biggest id from handeled updates
        biggest_update_id = 0
        for update in busses.handled_updates:
            if biggest_update_id < update.update_id:
                last_id = update.update_id
                biggest_update_id = update.update_id
    else:
        last_id = -1

    #remove all already handeled updates
    for update in busses.new_updates:
        if update in busses.handled_updates:
            busses.new_updates.remove(update)

    try:
        busses.new_updates = busses.new_updates + bot.get_updates(offset=last_id + 1)
    except telegram.error.TimedOut:
        pass

    busses.handled_updates = []


def start(bus):
    return bus

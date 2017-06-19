# -*- coding: utf-8 -*-
import telegram
import config
import helper
import listener
import busses

saufi = telegram.Bot(token=config.token)

listener.update_queue(saufi)


for _ in range(50):
    for update in busses.new_updates:
        msg = update.message
        msg_type = helper.get_message_type(msg)

        if msg_type == "location":
            #biggest possible value
            smallest_distance = 259200
            for location in config.station_position.keys():
                distance = helper.get_distance(location, msg.location.to_dict())
                if smallest_distance > distance:
                    smallest_distance = distance
                    nearest_station = config.station_position[location]
            msg.reply_text(nearest_station)

        busses.handled_updates.append(update)

    listener.update_queue(saufi)

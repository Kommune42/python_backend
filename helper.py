# -*- coding: utf-8 -*-
import config
import busses

def get_message_type(msg):
    if msg.text is not None:
        return "text"
    elif msg.audio is not None:
        return "audio"
    elif msg.document is not None:
        return "document"
    elif msg.game is not None:
        return "game"
    elif msg.location is not None:
        return "location"
    elif msg.photo != []:
        return "photo"
    elif msg.sticker is not None:
        return "sticker"
    elif msg.video is not None:
        return "video"
    elif msg.voice is not None:
        return "voice"
    elif msg.video_note is not None:
        return "video_note"
    elif msg.contact is not None:
        return "contact"
    else:
        return "unknown"


def get_distance(coord_tuple, coord_dict):
    #Pythagoras
    return (coord_tuple[0] - coord_dict["latitude"]) ** 2 + (coord_tuple[1] - coord_dict["longitude"]) ** 2


def get_closest_station(location):
    smallest_distance = 259200
    for station_pos in config.station_position.keys():
        distance = get_distance(station_pos, location)
        if smallest_distance > distance:
            smallest_distance = distance
            nearest_station = config.station_position[station_pos]
    return nearest_station

def correct_station_name(attempt):
    return None  # FIXME

def get_conversation_status(msg):
    return busses.conversation_bus[msg.chat.id]["state"]

def is_conversation_status(state, msg):
    #Check if users conversation status has given state
    return (msg.from_user.id == busses.conversation_bus[msg.chat.id]["user"]
            and busses.conversation_bus[msg.chat.id]["state"] == state)

def set_conversation_status(msg, state):
    busses.conversation_bus[msg.chat.id]["user"] = msg.from_user.id
    busses.conversation_bus[msg.chat.id]["state"] = state

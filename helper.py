# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pendulum
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


def edits1(word):
    letters    =  "/abcdefghijklmnoprstuwzßöü"
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def amount_common_char(str1, str2):
    str1 = set(str1)
    str2 = set(str2)
    return len(str1.intersection(str2))

def clostest_levenshtein_station(test_str):
    #19 is highest possible value
    smallest_distance = 20
    result = config.stations[0]
    for station in config.stations:
        #ä never appears anywhere else
        padded_station = station.ljust(20, u"ä")
        distance = 20 - amount_common_char(padded_station.lower(), test_str.lower())
        if distance < smallest_distance:
            smallest_distance = distance
            result = station
    return result


def get_matches(attempt, amount_results=1):
    closest_match = None

    matches = []
    #test beginnings
    for station in config.stations:
            if station.lower().find(attempt.lower()) >= 0:
                matches.append(station)
    if len(matches) == 1:
        closest_match = matches[0]
        if amount_results == 1:
            return closest_match

    results = {station: [0, 0] for station in config.stations}
    for edit1 in edits1(attempt):
        station = clostest_levenshtein_station(edit1)
        results[station][0] += 1

    #get top [amount_results] from results
    sorted_stations_by_likelyness = sorted(results, key=results.__getitem__, reverse=True)
    return [sorted_stations_by_likelyness[index] for index in range(amount_results)
                if index < len(sorted_stations_by_likelyness)]

def get_conversation_status(msg):
    return busses.conversation_bus[msg.chat.id]["state"]

def is_conversation_status(state, msg):
    #Check if users conversation status has given state
    if busses.conversation_bus[msg.chat.id]["state"] is None:
        return state is None
    else:
        return (msg.from_user.id == busses.conversation_bus[msg.chat.id]["user"]
                and busses.conversation_bus[msg.chat.id]["state"] == state)

def set_conversation_status(msg, state):
    busses.conversation_bus[msg.chat.id]["user"] = msg.from_user.id
    busses.conversation_bus[msg.chat.id]["state"] = state

def get_current_station_name():
    return config.stations[busses.status_bus["station"]]

def shutdown():
    data = {}
    data["station"] = busses.status_bus["station"]
    data["line"] = busses.status_bus["line"]
    data["admin_ids"] = config.admin_ids
    data["language"] = config.lang
    data["set_at_time"] = busses.status_bus["set_at_time"]
    data["arrive_time"] = busses.status_bus["arrive_time"]
    with open("./conf.conf", "w") as dynamic_conf_file:
        json.dump(data, dynamic_conf_file)
    config.run = False


def time_diff_for_humans(time_diff):
    return pendulum.now().add(seconds=time_diff).diff_for_humans(locale=config.lang)

def get_time_since_epoch(timelike):
    try:
        seconds_since_epoch = pendulum.parse(timelike).diff(pendulum.now().EPOCH).in_seconds()
        return seconds_since_epoch
    except pendulum.parsing.exceptions.ParserError:
        return None

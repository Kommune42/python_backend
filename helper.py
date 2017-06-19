# -*- coding: utf-8 -*-
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

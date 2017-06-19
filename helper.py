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
    elif msg.photo is not None:
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
    elif msg.location is not None:
        return "location"
    else:
        return "unknown"

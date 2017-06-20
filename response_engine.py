import config
import busses
import helper
from language import get_locale

def command_handler(msg):
    command = msg.text[1:]
    chat_type = msg.chat.type
    chat_id = msg.chat.id
    is_admin = msg.from_user.id in config.admin_ids

    if helper.is_conversation_status(None, msg):
        if command == get_locale("whereat"):
            msg.reply_text(get_locale("whereat_response"))
            helper.set_conversation_status(msg, "whereat")

def text_handler(msg):
    chat_id = msg.chat.id
    text = msg.text
    if helper.is_conversation_status("whereat", msg):
        station = config.station_correcter.correct_word(text)
        if station in config.stations:
            msg.reply_text(get_locale("hereat") + station)
        else:
            msg.reply_text(get_locale("couldnotfindstation"))
        helper.set_conversation_status(msg, None)

def location_handler(msg):
    chat_id = msg.chat.id

    if helper.is_conversation_status("whereat", msg):
        station = helper.get_closest_station(msg.location.to_dict())
        msg.reply_text(get_locale("hereat") + station)
        helper.set_conversation_status(msg, None)

def inline_handler(inline):
    query = inline.query
    location = inline.location.to_dict()
    command = inline.query.split()[0]
    args = inline.query[len(command):].split()
    if command == get_locale("setat"):
        if location is not None:
            station = helper.get_closest_station(location)
        else:
            station = helper.correct_station_name(args[0])

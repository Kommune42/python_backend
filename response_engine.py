import config
import language
import busses
import helper

def command_handler(msg):
    command = msg.text[1:]
    chat_type = msg.chat.type
    chat_id = msg.chat.id
    is_admin = msg.from_user.id in config.admin_ids

    if helper.get_conversation_status(msg) == None:
        if command == language.conf[config.lang]["whereat"]:
            msg.reply_text(language.conf[config.lang]["whereat_response"])
            helper.set_conversation_status(msg, "whereat")

def text_handler(msg):
    chat_id = msg.chat.id
    if helper.get_conversation_status(msg) == "whereat":
        helper.set_conversation_status(msg, None)

def location_handler(msg):
    chat_id = msg.chat.id

    if helper.get_conversation_status(msg) == "whereat":
        station = helper.get_closest_station(msg.location.to_dict())
        msg.reply_text(language.conf[config.lang]["hereat"] + station)
        helper.set_conversation_status(msg, None)

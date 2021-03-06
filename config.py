# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
import telegram
import busses

#fetch token
secure_conf = json.load(open("./secure_conf.conf"))
token = secure_conf["token"]

saufi = telegram.Bot(token=token)

#running state
run = True

msg_log_file_path = "./msg_log.txt"
complete_log_file_path = "./log.log"

#load config and state
with open("./state.json", "r") as internal_state_file:
    busses.status_bus.update(json.load(internal_state_file))

with open("./conf.conf", "r") as dynamic_conf_file:
    dynamic_conf = json.load(dynamic_conf_file)

admin_ids = dynamic_conf["admin_ids"]
lang = dynamic_conf["language"]
busses.status_bus["line"] = dynamic_conf["line"]
busses.status_bus["station"] = dynamic_conf["station"]
busses.status_bus["set_at_time"] = dynamic_conf["set_at_time"]
busses.status_bus["arrive_delay"] = dynamic_conf["arrive_delay"]
busses.status_bus["latest_messages"] = {chat_id: telegram.Message.de_json(json.loads(dynamic_conf["latest_messages"][chat_id]), saufi) for chat_id in dynamic_conf["latest_messages"]}

#manually changeable Constants
station_position = {
    (52.548611, 13.389444): "Gesundbrunnen",
    (52.549444, 13.413889): "Schönhauser Allee",
    (52.543889, 13.426111): "Prenzlauer Allee",
    (52.539722, 13.439444): "Greifswalder Straße",
    (52.529444, 13.454444): "Landsberger Allee",
    (52.523889, 13.464444): "Storkower Straße",
    (52.514167, 13.474722): "Frankfurter Allee",
    (52.503056, 13.468889): "Ostkreuz",
    (52.4938  , 13.4615  ): "Treptower Park",
    (52.4729  , 13.4554  ): "Sonnenallee",
    (52.469167, 13.441667): "Neukölln",
    (52.467661, 13.431488): "Hermannstraße",
#   (,): "Tempelhofer Feld",
    (52.470756, 13.38535 ): "Tempelhof",
    (52.475556, 13.364444): "Südkreuz",
    (52.479   , 13.352   ): "Schöneberg",
    (52.478611, 13.343889): "Insbrucker Platz",
    (52.4775  , 13.328611): "Bundesplatz",
    (52.480278, 13.3125  ): "Heidelberger Platz",
    (52.488611, 13.300278): "Hohenzollerndamm",
    (52.496111, 13.290556): "Halensee",
    (52.501   , 13.284   ): "Westkreuz",
    (52.507778, 13.283611): "Messe Nord/ICC",
    (52.518056, 13.284444): "Westend",
    (52.530434, 13.299795): "Jungfernheide",
    (52.534444, 13.329444): "Beusselstraße",
    (52.536   , 13.344   ): "Westhafen",
    (52.543348, 13.368296): "Wedding",
}

stations = [
    "Gesundbrunnen",
    "Schönhauser Allee",
    "Prenzlauer Allee",
    "Greifswalder Straße",
    "Landsberger Allee",
    "Storkower Straße",
    "Frankfurter Allee",
    "Ostkreuz",
    "Treptower Park",
    "Sonnenallee",
    "Neukölln",
    "Hermannstraße",
#    "Tempelhofer Feld",
    "Tempelhof",
    "Südkreuz",
    "Schöneberg",
    "Insbrucker Platz",
    "Bundesplatz",
    "Heidelberger Platz",
    "Hohenzollerndamm",
    "Halensee",
    "Westkreuz",
    "Messe Nord/ICC",
    "Westend",
    "Jungfernheide",
    "Beusselstraße",
    "Westhafen",
    "Wedding"
]

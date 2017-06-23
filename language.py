# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import config

conf = {
    "de": {
        "whereat": "wo",
        "setat_response": "Sag mir wo du bist",
        "hereat": "Da Crew is hier: ",
        "couldnotfindstation": "Hab nich verstanden welche Station",
        "setat": "wirhier",
        "cancel": "abbrechen",
        "next": "nächste",
        "drivingto": "Auf auf. Nächste Station: ",
        "noadmin": "Ich bin dumm, weil ich kein Admin bin"
    },
    "en": {
        "whereat": "whereat",
        "setat_response": "Where you at?",
        "hereat": "Da Crew is here: ",
        "couldnotfindstation": "COULD YOU SPEAK UP A BIT? I DIDNT GET THAT",
        "setat": "setat",
        "cancel": "cancel",
        "next": "next",
        "drivingto": "All onboard. Next station is: ",
        "noadmin": "I am dumb because I am no admin"
    }
}

def get_locale(key):
    return conf[config.lang][key]

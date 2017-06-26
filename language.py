# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import config

conf = {
    "de": {
        "whereat": "wo",
        "setat_response": "Sag mir wo du bist",
        "hereatnow": "Da Crew ist hier: ",
        "hereatfut": "Treffen bei: ",
        "hereatago": "Da Crew war hier: ",
        "couldnotfindstation": "Hab nich verstanden welche Station",
        "setat": "wirhier",
        "cancel": "abbrechen",
        "next": "nächste",
        "drivingto": "Auf auf. Nächste Station: ",
        "noadmin": "Ich bin dumm, weil ich kein Admin bin",
        "select": "Such dir was aus",
        "uselocation": "GPS benutzen",
        "setline": "linie",
        "S41": "Im Uhrzeigersinn (S41)",
        "S42": "Gegen den Uhrzeigersinn (S42)",
        "shutdown": "bye"
    },
    "en": {
        "whereat": "whereat",
        "setat_response": "Where you at?",
        "hereatnow": "Da Crew is here: ",
        "hereatfut": "Meeting at: ",
        "hereatago": "Da Crew was here: ",
        "couldnotfindstation": "COULD YOU SPEAK UP A BIT? I DIDNT GET THAT",
        "setat": "setat",
        "cancel": "cancel",
        "next": "next",
        "drivingto": "All onboard. Next station is: ",
        "noadmin": "I am dumb because I am no admin",
        "select": "Thy might now choose thire destination",
        "uselocation": "Use GPS",
        "setline": "line",
        "S41": "clockwise (S41)",
        "S42": "counterclockwise (S42)",
        "shutdown": "shutdown"
    }
}

def get_locale(key):
    return conf[config.lang][key]

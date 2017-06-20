import config

conf = {
    "de": {
        "whereat": "standort",
        "whereat_response": "Bitte antworte mit Position oder Stationennamen",
        "hereat": "Da Crew is hier: ",
        "couldnotfindstation": "Hab nich verstanden welche Station",
        "setat": "standort"
    },
    "en": {
        "whereat": "whereat",
        "whereat_response": "Send your location or a station name",
        "hereat": "Da Crew is here: ",
        "couldnotfindstation": "COULD YOU SPEAK UP A BIT? I DIDNT GET THAT",
        "setat": "setat"
    }
}

def get_locale(key):
    return conf[config.lang][key]

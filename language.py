import config

conf = {
    "de": {
        "whereat": "wo",
        "setat_response": "Sag mir wo du bist",
        "hereat": "Da Crew is hier: ",
        "couldnotfindstation": "Hab nich verstanden welche Station",
        "setat": "sindhier",
        "cancel": "abbrechen",
        "next": "nächste"
    },
    "en": {
        "whereat": "whereat",
        "setat_response": "Where you at?",
        "hereat": "Da Crew is here: ",
        "couldnotfindstation": "COULD YOU SPEAK UP A BIT? I DIDNT GET THAT",
        "setat": "setat",
        "cancel": "cancel",
        "next": "next"
    }
}

def get_locale(key):
    return conf[config.lang][key]

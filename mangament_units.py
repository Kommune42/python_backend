# -*- coding: utf-8 -*-
import config
import busses


def advance_station():
    index = busses.status_bus["station"]
    index += 1
    index = index % len(config.stations)
    busses.status_bus["station"] = index
    

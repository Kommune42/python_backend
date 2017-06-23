# -*- coding: utf-8 -*-
import config
import busses


def advance_station():
    index = busses.status_bus["station"]
    if busses.status_bus["line"] == "S41":
        index += 1
    if busses.status_bus["line"] == "S42":
        index -= 1
    index = index % len(config.stations)
    busses.status_bus["station"] = index

def set_station(station_name):
    busses.status_bus["station"] = config.stations.index(station_name)

# -*- coding: utf-8 -*-
import socket
import threading
import json
import re

with open("./global_conf.json", "r") as global_conf_file:
    global_conf = json.load(global_conf_file)

with open("./communication/conf.json", "r") as conf_file:
    local_conf = json.load(conf_file)

max_size_websocket = global_conf["max_size_websocket"]
termination_symbol = local_conf["termination_symbol"]

class server(object):

    def __init__(self, dest, responding_function, name="NONE", max_connections=20):
        self.s = socket.socket()
        self.s.bind(dest)
        self.s.listen(max_connections)

        self.responding_function = responding_function

        self.name = name

        self.threads_run = {"ack_con": True, "read": True}
        self.connections_active = {}

        self.connections = []
        self.lookup_table = {}

    def accept_connections(self):
        while self.threads_run["ack_con"]:
            connection, addr = self.s.accept()
            send_long(message(data=self.name, action="ack"), connection)
            msg = recv_long(connection)
            if msg["action"] == "ack":
                #TODO: What to do with name?
                connection_name = msg["data"]
                self.connections.append(connection)
                self.lookup_table[connection] = addr
                self.connections_active[connection] = False
                send_long(message(action="ready"), connection)
                print "Connected to " + connection_name
            elif msg["data"] != "nack":
                send_long(message(data=self.name, action="close"), connection)
                connection.close()
                print "Tried to initiate Connection with wrong initialization: " + msg["action"]

    def close_connection(self, connection):
        self.lookup_table.pop(connection)
        self.connections.remove(connection)
        self.connections_active.pop(connection)
        send_long(message(action="close"), connection)
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()

    def read_connections(self):
        while self.threads_run["read"]:
            for connection in self.connections:
                if not self.connections_active[connection]:
                    self.connections_active[connection] = True
                    msg = recv_long(connection)
                    self.responding_function(msg, connection)
                    if msg["action"] == "close":
                        print "closing connection"
                        self.threads_run["read"] = False
                        self.threads_run["ack_con"] = False
                        self.close_connection(connection)
                    self.connections_active[connection] = False

    def start(self):
        ack_con = threading.Thread(target=self.accept_connections, name="ack_con")
        read = threading.Thread(target=self.read_connections, name="read")
        ack_con.start()
        read.start()

    def stop(self):
        for connection in self.connections:
            send_long(message(action="close"), connection)
            connection.close()


class client(object):

    def __init__(self, name="NONE"):
        self.s = socket.socket()

        self.name = name

        self.threads_run = {}

    def connect_to(self, dest, module_name="NONE"):
        self.s.connect(dest)
        ack_msg = recv_long(self.s)
        if ack_msg["action"] == "ack" and ack_msg["data"] == module_name:
            send_long(message(action="ack", data=self.name), self.s)
            print "Connection Established"
        else:
            send_long(message(action="nack"), self.s)
            print "Connection terminated: Nack"
            self.s.close() #FIXME sort out protocol
        recv_long(self.s) # Wait for server to be ready

    def request(self, msg):
        send_long(msg, self.s)
        send_long(message(action="ack"), self.s)
        return recv_long(self.s)

    def close(self):
        send_long(message(action="close"), self.s)
        self.s.close()


def recv_long(connection):
    print "STARTED RECIVING"
    finished = False
    data = ""
    regex_pattern = "0*\\" + termination_symbol + "$"
    while not finished:
        print "NOT FINISHED"
        data = data + connection.recv(max_size_websocket)
        print "GOT RAW DATA: " + data
        if re.search(regex_pattern, data) is not None:
            data = re.sub(regex_pattern, "", data)
            finished = True

    print "FINISHED RECIEVING: " + data
    return json.loads(data)

def send_long(msg, connection):
    print "SEND: " + msg
    data = json.loads(msg)
    assert "action" in data.keys()
    assert "error" in data.keys()
    assert "data" in data.keys()

    # sends the message base 64 encoded to limit the possible characters
    # followed by the termination_symbol wich is no symbol of the base 64
    print "RAW DATA SENT: " + msg
    length = connection.send(msg)
    overhang = length % max_size_websocket
    print "BYTE LENGHT: " + str(length)
    print "BYTE OVERHANG: " + str(overhang)
    print "AMOUNT OF ZEROS: " + str(max_size_websocket - overhang - 1)
    if overhang != 0:
        connection.send(("0" * (max_size_websocket - overhang - 1)) + termination_symbol)
    print "FINISHED SENDING"

def message(data="", action="", error=""):
    return json.dumps({"data": data, "action": action, "error": error})

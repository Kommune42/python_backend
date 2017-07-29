import socket
import threading
import json
import os


with open("./global_conf.json", "r") as global_conf_file:
    global_conf = json.load(global_conf_file)

max_size_websocket = global_conf["max_size_websocket"]

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
            connection.send(self.name)
            data = connection.recv(max_size_websocket)
            msg = json.loads(data)
            if msg["action"] == "ack":
                #TODO: What to do with name?
                connection_name = msg["data"]
                connection.send(message(data=self.name, action="ack"))
                self.connections.append(connection)
                self.lookup_table[connection] = addr
                self.connections_active[connection] = False
                print "Connected to " + connection_name
            else:
                connection.send(message(data=self.name, action="nack"))
                print "Tried to initiate Connection with wrong initialization: " + str(addr)

    def close_connection(self, connection):
        self.lookup_table.pop(connection)
        self.connections.pop(connection)
        self.connections_active.pop(connection)
        connection.send(message(action="close"))
        connection.shutdown()
        connection.close()

    def read_connections(self):
        while self.threads_run["read"]:
            for connection in self.connections:
                if not self.connections_active[connection]:
                    self.connections_active[connection] = True
                    data = connection.recv(max_size_websocket)
                    msg = json.loads(data)
                    self.responding_function(msg, connection)
                    if msg["action"] == "close":
                        print "closing connection"
                        self.threads_run["read"] = False
                        self.threads_run["ack_con"] = False
                        #self.close_connection(connection)
                    else:
                        self.connections_active[connection] = False

    def start(self):
        ack_con = threading.Thread(target=self.accept_connections, name="ack_con")
        read = threading.Thread(target=self.read_connections, name="read")
        ack_con.start()
        read.start()


def send_long(msg, connection):
    #~Three bytes per char should be enough
    max_string_length = max_size_websocket / 3
    #Split msg into max_string_length sized blocks
    msg_blocks = [msg[i:max_string_length+i] for i in range(0, len(msg), max_string_length)]
    for block in msg_blocks:
        connection.send(block)

def message(data="", action="", error=""):
    return json.dumps({"data": data, "action": action, "error": error})

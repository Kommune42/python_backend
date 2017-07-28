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
            self.connections.append(connection)
            self.lookup_table[connection] = addr
            self.connections_active[connection] = False
            connection.send(self.name)
            data = connection.recv(max_size_websocket)
            msg = json.loads(data)
            print msg
            print msg["action"] == "ack"
            if msg["action"] == "ack":
                connection_name = msg["data"]
                print "Connected to " + connection_name
            else:
                #TODO Delete records of connection
                print "Tried to initiate Connection with wrong initialization: " + str(addr)
            #TODO: What to do with name?

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


def message(data="", action="", error=""):
    return json.dumps({"data": data, "action": action, "error": error})

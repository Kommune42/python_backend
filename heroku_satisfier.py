import socket
import os

_ = socket.socket()
try:
    _.bind(("saufbot.herokuapp.com", int(os.environ.get("PORT"))))
except:
    print "WHY?"

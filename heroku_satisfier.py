import socket
import os

_ = socket.socket()
try:
    _.bind(("0.0.0.0", int(os.environ.get("PORT"))))
    _.listen(1)
except:
    print "WHY?"
print "BOUND"

from . import telegram_handler
from . import socket_interface


telegram_handler.update_buffer()
socket_interface.start()

def start():
    run = True
    while run:
        try:
            telegram_handler.update_buffer()
        except KeyboardInterrupt:
            socket_interface.stop()
            run = False

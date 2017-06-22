import os
import telegram

token = os.environ.get("TOKEN")

botti = telegram.Bot(token=token)

while True:
	print botti.get_updates()

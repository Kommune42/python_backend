# -*- coding: utf-8 -*-
global handled_updates
global new_updates
global conversation_bus
global status_bus

handled_updates = []
new_updates = []
conversation_bus = {}  # chat_id: state
status_bus = {"station": 0, "line": "S42", "arrive_delay": 0, "set_at_time": 0, "latest_messages":{}}

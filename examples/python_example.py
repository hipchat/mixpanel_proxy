#!/usr/bin/python

import json
import socket

MIXPANEL_TOKEN = 'abc123'

data = {
    'event': 'test',
    'properties': {
        'distinct_id': 123456,
        'token': MIXPANEL_TOKEN,
    }}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8067))
sock.send("%s\r\n" % json.dumps(data))
sock.close()
print "Sent: %r" % data


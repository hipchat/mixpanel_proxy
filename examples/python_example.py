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
message = "%s\r\n" % json.dumps(data)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, ("127.0.0.1", 8067))

print "Sent: %r" % data

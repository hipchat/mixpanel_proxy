require 'rubygems'
require 'json'
require 'socket'

MIXPANEL_TOKEN = 'abc123'

data = {
  "event" => "test",
  "properties" => {
    "distinct_id" => 123456,
    "token" => MIXPANEL_TOKEN
  }
}

sock = UDPSocket.new
sock.send(JSON.generate(data)+"\r\n", 0, 'localhost', 8067)

puts "Sent: " + JSON.generate(data)

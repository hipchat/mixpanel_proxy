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

sock = TCPSocket.open('localhost', 8067)
sock.puts(JSON.generate(data)+"\r\n")
sock.close()

puts "Sent: " + JSON.generate(data)

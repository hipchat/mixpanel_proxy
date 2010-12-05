<?php

define('MIXPANEL_TOKEN', 'abc123');

$data = array(
  'event' => 'test',
  'properties' => array(
    'distinct_id' => 123456,
    'token' => MIXPANEL_TOKEN
  )
);

$sock = fsockopen("localhost", 8067, $errno, $errstr, 5);
if (!$sock) {
  echo "Error connecting: $errno - $errstr";
  exit;
}

fwrite($sock, json_encode($data)."\r\n");
fclose($sock);
echo "sent: ".json_encode($data);


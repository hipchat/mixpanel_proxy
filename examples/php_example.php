<?php

define('MIXPANEL_TOKEN', 'abc123');

$data = array(
  'event' => 'test',
  'properties' => array(
    'distinct_id' => 123456,
    'token' => MIXPANEL_TOKEN
  )
);

$sock = fsockopen("udp://127.0.0.1", 8067, $errno, $errstr);
fwrite($sock, json_encode($data));
fclose($sock);
echo "sent: ".json_encode($data);

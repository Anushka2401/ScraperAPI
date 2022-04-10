<?php
$items = 'iphones';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,"http://127.0.0.1:5000/".$items);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);


$server_output = curl_exec($ch);

curl_close($ch);
echo $server_output;

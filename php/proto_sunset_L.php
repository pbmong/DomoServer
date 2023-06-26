<?php
$cmd = "python /var/www/html/Domo/backend/mqtt_sunset_send_to_topic.py ".$_GET['TOPIC']." 1";
echo $cmd.": ";
$output = shell_exec($cmd);
echo $output;

$url = "http://192.168.1.187/Domo/";

header('Location: '.$url);  
?>
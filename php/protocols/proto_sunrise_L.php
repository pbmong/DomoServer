<?php
$cmd = "python /var/www/html/Domo/backend/protocol_mqtt_sunrise_send_to_topic.py ".$_GET['TOPIC']." 1";
/*example: "python /var/www/html/Domo/backend/protocol_mqtt_sunrise_send_to_topic.py home/bedroom/L 1"*/

echo $cmd.": ";
$output = shell_exec($cmd);
echo $output;

$url = "http://192.168.1.187/Domo/";

header('Location: '.$url);  
?>

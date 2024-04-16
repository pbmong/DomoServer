<?php
$servername = "localhost";
$username = "pi";
$password = "raspberry";
$database = "DomoServer";

echo "GET / ". $_GET['TOPIC'] . " : " . $_GET['VALUE'] . "<br>";

$cmd = "python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py '". $_GET['TOPIC'] ."' ".$_GET['VALUE'];
/*example: python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py home/bedroom/L ON*/

echo $cmd.": ";
$output = shell_exec($cmd);
echo $output;

$url = "http://192.168.1.187/Domo/";

header('Location: '.$url);  
?>

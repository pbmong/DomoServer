<?php
$cmd = "mosquitto_pub -h localhost -t ".$_GET['TOPIC']." -m REQ";
echo $cmd.": ";
$output = shell_exec($cmd);
echo $output;

$url = "http://192.168.1.187/Domo/";

header('Location: '.$url);  
?>
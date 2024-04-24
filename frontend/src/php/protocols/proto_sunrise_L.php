<?php
$servername = getenv("DB_HOSTNAME")?:"mysql";
$username = getenv("DB_USER")?:"root";
$password = getenv("DB_PASSWORD")?:"root";
$database = getenv("DB_NAME")?:"DomoServer";
$external_ip = getenv("EXTERNAL_IP")?:"localhost";
$external_port = getenv("EXTERNAL_PORT")?:"80";
$pma_port = getenv("PMA_PORT")?:"8081";
$api_port = getenv("API_BACKEND_PORT")?:"8000";

echo "GET / ". $_GET['TOPIC'];


// API call
$response = file_get_contents('http://'. $external_ip .':'. $api_port .'/protocol_sunrise?topic='. $_GET['TOPIC'] .'&value='. $_GET['VALUE']);

echo "Response: ".$response;

$url = "http://".$external_ip;

//header('Location: '.$url);  
?>

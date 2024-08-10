<?php
$servername = getenv("DB_HOSTNAME")?:"mysql";
$username = getenv("DB_USER")?:"root";
$password = getenv("DB_PASSWORD")?:"root";
$database = getenv("DB_NAME")?:"DomoServer";
$external_ip = getenv("EXTERNAL_IP")?:"localhost";
$external_port = getenv("EXTERNAL_PORT")?:"80";
$pma_port = getenv("PMA_PORT")?:"8081";
$api_port = getenv("API_BACKEND_PORT")?:"8000";

// API call
$execute = 'http://'. $external_ip .':'. $api_port .'/delete_cleaning_register?register_id='. $_GET['ID'];
$response = file_get_contents($execute);

echo "Response: ".$response;

// Redirect to UI
$url = "http://".$external_ip."/cleaning_register_UI.php?";

header('Location: '.$url);  
?>
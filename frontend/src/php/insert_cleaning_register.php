<?php
$servername = getenv("DB_HOSTNAME")?:"mysql";
$username = getenv("DB_USER")?:"root";
$password = getenv("DB_PASSWORD")?:"root";
$database = getenv("DB_NAME")?:"DomoServer";
$external_ip = getenv("EXTERNAL_IP")?:"localhost";
$external_port = getenv("EXTERNAL_PORT")?:"80";
$pma_port = getenv("PMA_PORT")?:"8081";
$api_port = getenv("API_BACKEND_PORT")?:"8000";


// Validate Datetime
$datetime = $_GET['DATETIME'];

$datetime_valid = true;

if (strlen($datetime) != 19){
	$datetime_valid = false;
}
elseif ($datetime[4] != '-' || $datetime[7] != '-' || $datetime[10] != '_' || $datetime[13] != ':' || $datetime[16] != ':'){
	$datetime_valid = false;
}

if ($datetime_valid){
	// API parameters
	$room = $_GET['ROOM'];
	$level = $_GET['LEVEL'];

	echo $room;
	echo $level;

	$execute = 'http://'. $external_ip .':'. $api_port .'/insert_cleaning_register?room='. $room .'&datetime='. $_GET['DATETIME'] .'&level='. $level;
	echo $execute;

	// API call
	$response = file_get_contents($execute);

	echo "Response: ".$response;
}

// Redirect to UI
$url = "http://".$external_ip."/cleaning_register_UI.php?";

header('Location: '.$url);  
?>
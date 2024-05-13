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

// Process weekday
$weekday = 0;
if ($_GET['M']){
	$weekday += 1;
    }
if ($_GET['T']){
	$weekday += 2;
    }

if ($_GET['W']){
	$weekday += 4;
    }

if ($_GET['X']){
	$weekday += 8;
    }

if ($_GET['F']){
	$weekday += 16;
    }

if ($_GET['S']){
	$weekday += 32;
    }

if ($_GET['N']){
	$weekday += 64;
    }

if ($datetime_valid){
	// API parameters
	$command = "python mqtt_send_to_topic_and_ddbb.py ".$_GET['TOPIC']." ". $_GET['VALUE'];
	$encoded_command = urlencode($command);
	$execute = 'http://'. $external_ip .':'. $api_port .'/insert_command?command='. $encoded_command .'&datetime='. $_GET['DATETIME'] .'&weekday='. $weekday;

	// API call
	$response = file_get_contents($execute);

	echo "Response: ".$response;
}

// Redirect to UI
$url = "http://".$external_ip."/programed_commands_UI.php?";

header('Location: '.$url);  
?>
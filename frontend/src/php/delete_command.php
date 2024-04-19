<?php
$servername = getenv("DB_HOSTNAME")?:"mysql";
$username = getenv("DB_USER")?:"root";
$password = getenv("DB_PASSWORD")?:"root";
$database = getenv("DB_NAME")?:"DomoServer";
$external_ip = getenv("EXTERNAL_IP")?:"localhost";
$external_port = getenv("EXTERNAL_PORT")?:"80";
$pma_port = getenv("PMA_PORT")?:"8081";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "DELETE FROM `programed_commands` WHERE ID = ".$_GET["ID"];
echo $sql;

if ($conn->query($sql) === TRUE) {
  echo "record deleted successfully";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$url = "http://".$external_ip."/programed_commands_UI.php?";

header('Location: '.$url);  
?>
<?php
$servername = "localhost";
$username = "pi";
$password = "raspberry";
$database = "DomoServer";

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

$url = "http://192.168.1.187/Domo/frontend/programed_commands_UI.php?";

header('Location: '.$url);  
?>
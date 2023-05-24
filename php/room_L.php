<?php
$servername = "localhost";
$username = "pi";
$password = "raspberry";
$database = "DomoServer";

echo "GET: " . $_GET['MEANING'] . " - " . $_GET['VALUE'] . "<br>";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    echo("Connection failed: " . $conn->connect_error . "<br>");
}else{
    echo "Connected successfully <br>";    
}

/*$sql = "UPDATE home_room SET VALUE='" . $_GET['VALUE'] . "' WHERE MEANING='L'";

if ($conn->query($sql) === TRUE) {
  echo "Record updated successfully<br>";
} else {
  echo "Error updating record: " . $conn->error . "<br>";
}*/

mysqli_close($conn);

$cmd = "python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py home/room/L ".$_GET['VALUE'];
echo $cmd.": ";
$output = shell_exec($cmd);
echo $output;

$url = "http://192.168.1.187/Domo/";

header('Location: '.$url);  
?>
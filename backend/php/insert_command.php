<?php
$servername = "localhost";
$username = "pi";
$password = "raspberry";
$database = "DomoServer";

$idmin = 0;
$idmax = 100;
if ($_GET['TOPIC'] == "home/bedroom/R" && $_GET['VALUE'] == "OFF"){
	$idmin = 0;
	$idmax = 9;
    }
if ($_GET['TOPIC'] == "home/bedroom/R" && $_GET['VALUE'] == "ON"){
	$idmin = 10;
	$idmax = 19;
    }
if ($_GET['TOPIC'] == "home/bedroom/L" && $_GET['VALUE'] == "OFF"){
	$idmin = 20;
	$idmax = 29;
    }
if ($_GET['TOPIC'] == "home/bedroom/L" && $_GET['VALUE'] == "ON"){
	$idmin = 30;
	$idmax = 39;
    }
if ($_GET['TOPIC'] == "home/bedroom/C" && $_GET['VALUE'] == "OFF"){
	$idmin = 40;
	$idmax = 49;
    }
if ($_GET['TOPIC'] == "home/bedroom/C" && $_GET['VALUE'] == "ON"){
	$idmin = 50;
	$idmax = 59;
    }

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

echo $_GET['TOPIC'] . " " . $_GET['VALUE'] ." (". $idmin. "-" . $idmax .")". " | " . $_GET['DATETIME'] . " | " . $_GET['M'] . $_GET['L'] . $_GET['W'] . $_GET['X'] . $_GET['F'] . $_GET['S'] . $_GET['N'] ." (". $weekday.") <br>";
 
// Create connection
$conn = new mysqli($servername, $username, $password, $database);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
 
$sql = "SELECT * FROM `programed_commands` where ID >= ".$idmin." and ID <= ".$idmax." ORDER BY `ID` DESC";
//echo $sql ."<br>";

$result = $conn->query($sql);
if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
	$id = $row[ID] + 1;
	//if($id > $idmax)
		//manage id error
    } else {
        $id = $idmin;
    }
if ($conn->query($sql) === TRUE) {
  echo "New record created successfully";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$sql = "INSERT INTO `programed_commands` (`ID`, `COMMAND`, `DATETIME`, `WEEKDAY`) 
	VALUES ('".$id."', 'python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py ".$_GET['TOPIC']." ". $_GET['VALUE'].
	"', '".$_GET['DATETIME']."', '".$weekday."');";

if ($conn->query($sql) === TRUE) {
  echo "New record created successfully";
} else {
  echo "Error: " . $sql . "<br>" . $conn->error;
}

$url = "http://192.168.1.187/Domo/frontend/programed_commands_UI.php?";

header('Location: '.$url);  
?>
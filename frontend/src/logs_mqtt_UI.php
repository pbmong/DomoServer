<head>
<link rel="stylesheet" href="css/UI_styles_1.css">
</head>
<body>
    <?php
        $external_ip = getenv("EXTERNAL_IP")?:"localhost";
        $external_port = getenv("EXTERNAL_PORT")?:"80";
        $pma_port = getenv("PMA_PORT")?:"8081";

        echo '<form action="http://'.$external_ip;
        echo ":".$external_port;
    ?>/index.php" method="get">
    <button class='tittle_button' type="submit">MAIN MENU</button>
    </form>
    <div><div class='section'>MQTT LOGS</div>
    <?php
    echo "<form class='filter' action='http://".$external_ip."/logs_mqtt_UI.php' method='get'>"
    ?><select class='filter' name='filter'>
    
    <?php
    $servername = getenv("DB_HOSTNAME")?:"mysql";
    $username = getenv("DB_USER")?:"root";
    $password = getenv("DB_PASSWORD")?:"root";
    $database = getenv("DB_NAME")?:"DomoServer";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $database);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT DISTINCT TOPIC FROM mqtt_historic";
    
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		echo "<option class='filter' value='".$row["TOPIC"]."'>".$row["TOPIC"]."</option>";
            }
    } else {
        echo "0 results";
    }

    $max_logs = 20;
    if ($_GET['max_logs']){
	$max_logs = $_GET['max_logs'];
    }
    echo "</select><input class='filter' type='text' name='max_logs' maxlength='3' size='1' value='". $max_logs ."'>";

    $conn->close();
    ?>
    <button class='filter' type="submit">Apply</button></form><br>
    <?php
    $servername = getenv("DB_HOSTNAME")?:"mysql";
    $username = getenv("DB_USER")?:"root";
    $password = getenv("DB_PASSWORD")?:"root";
    $database = getenv("DB_NAME")?:"DomoServer";
    
    // Create connection
    $conn = new mysqli($servername, $username, $password, $database);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $topic_filter = $_GET['filter']??"home/bedroom/T";
    echo "<div class='sub_section'>Log: ". $topic_filter."</div><br><table>";
    
    $max_logs =  $_GET['max_logs']?? 20;
    $sql = "SELECT * FROM mqtt_historic WHERE TOPIC = '$topic_filter' ORDER BY DATETIME DESC LIMIT $max_logs ";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		echo "<tr><td class='logs'>".$row["DATETIME"].": ".$row["VALUE"]."</td></tr>";
            }
    } else {
        echo "0 results";
    }

    $conn->close();
    ?>
    </table></div>
</body>
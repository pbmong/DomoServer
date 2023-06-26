<head>
<link rel="stylesheet" href="frontend/UI_styles.css">
</head>
<body>
    <br><div><div class='section'> EXTERNAL<label></div>
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

    $sql = "SELECT * FROM home_external";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		if($row["MEANING"] == "Temperature")
            	echo "<div class='data'> Temp: ".$row["VALUE"]." ".$row["UNIT"]."</div>";
            }
    } else {
        echo "0 results";
    }

    $conn->close();
    ?>
    <div><div class='section'>AREAS<label></div>
<!----   ROOM      -->
    <form action="http://192.168.1.187/Domo/frontend/room_UI.php" method="get">
    <button class='tittle' type="submit">ROOM</button>
    </form>
    <br>
<!----   LIVING ROOM      -->
    <form action="http://192.168.1.187/Domo/frontend/living_room_UI.php" method="get">
    <button class='tittle' type="submit">LIVING ROOM</button>
    </form>
    <br>
<!----   LOGS     -->
    <form action="http://192.168.1.187/Domo/frontend/logs_mqtt_UI.php" method="get">
    <button class='tittle' type="submit">MQTT LOGS</button>
    </form>
    <br>
<!----   DDBB     -->
    <form action="http://192.168.1.187/phpmyadmin/sql.php?server=1&db=DomoServer&table=home_external&pos=0" method="get">
    <button class='tittle' type="submit">DDBB</button>
    </form>
    <br>
</body>

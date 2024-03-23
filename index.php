<head>
<link rel="stylesheet" href="frontend/UI_styles_1.css">
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
    <div><div class='section'>AREAS<label></div><br>
<!----   BEDROOM      -->
    <form action="http://192.168.1.187/Domo/frontend/bedroom_UI.php" method="get">
    <button class='tittle_button' type="submit">BEDROOM</button>
    </form>
    <br>
<!----   LIVING ROOM      -->
    <form action="http://192.168.1.187/Domo/frontend/living_room_UI.php" method="get">
    <button class='tittle_button' type="submit">LIVING ROOM</button>
    </form>
    <br>
    <div><div class='section'>INFO<label></div><br>
<!----   LOGS     -->
    <form action="http://192.168.1.187/Domo/frontend/logs_mqtt_UI.php" method="get">
    <button class='tittle_button' type="submit">MQTT LOGS</button>
    </form>
    <br>
<!----   COMMANDS     -->
    <form action="http://192.168.1.187/Domo/frontend/programed_commands_UI.php" method="get">
    <button class='tittle_button' type="submit">COMMANDS</button>
    </form>
    <br>
<!----   DDBB     -->
    <form action="http://192.168.1.187/phpmyadmin/sql.php?server=1&db=DomoServer&table=home_external&pos=0" method="get">
    <button class='tittle_button' type="submit">DDBB</button>
    </form>
    <br>
</body>

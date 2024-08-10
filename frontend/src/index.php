<head>
<link rel="stylesheet" href="css/UI_styles_1.css">
</head>
<body>
    <br><div><div class='section'> EXTERNAL<label></div>
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
    <div><div class='section'>ROOMS<label></div><br>
<!----   BEDROOM      -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$external_port;
    ?>/bedroom_UI.php' method='get'><button class='tittle_button' type="submit">BEDROOM</button>
    </form>
    <br>
<!----   LIVING ROOM      -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$external_port;
    ?>/living_room_UI.php' method="get"><button class='tittle_button' type="submit">LIVING ROOM</button>
    </form>
    <br>
<!----   CLEANING REGISTER      -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$external_port;
    ?>/cleaning_register_UI.php' method="get"><button class='tittle_button' type="submit">CLEANING<br />REGISTER</button>
    </form>
    <br>

    <div><div class='section'>INFO<label></div><br>
<!----   LOGS     -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$external_port;
    ?>/logs_mqtt_UI.php' method="get"><button class='tittle_button' type="submit">MQTT LOGS</button>
    </form>
    <br>
<!----   COMMANDS     -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$external_port;
    ?>/programed_commands_UI.php' method="get"><button class='tittle_button' type="submit">COMMANDS</button>
    </form>
    <br>
<!----   DDBB     -->
    <?php
        echo "<form action='http://".$external_ip;
        echo ":".$pma_port;
    ?>/index.php?route=/sql&pos=0&db=DomoServer' method="get"><button class='tittle_button' type="submit">DDBB</button>
    </form>
    <br>
</body>

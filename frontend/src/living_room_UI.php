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
    <!----   LIVING ROOM      -->
    <br><div><div class='section'>LIVING ROOM</div><br>
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

    $sql = "SELECT * FROM home_living_room";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		if($row["MEANING"] == "T" | $row["MEANING"] == "H")
                    echo "<div class='data'>".$row["MEANING"].": ".$row["VALUE"]." ".$row["UNIT"]."</div>";
            }
    } else {
        echo "0 results";
    }

    $conn->close();
    ?> 
    </div>
</body>
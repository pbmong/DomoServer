<head>
    <style>
	.tittle{
            font-size: 120px
        }
	.data{
	    font-size: 100px
	}
        form{
            font-size: 100px;
	    margin: 0px
        }
        button{
            font-size: 100px
        }
    </style>
</head>
<body>
    <br><div class='tittle'> -- EXTERNAL --</div><br>
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
            	echo "<div class='data'>".$row["MEANING"].": ".$row["VALUE"]." ".$row["UNIT"]."</div>";
            }
    } else {
        echo "0 results";
    }

    $conn->close();
    ?>
<!----   ROOM      -->
    <br><div class='tittle'> -- ROOM --</div><br>
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

    $sql = "SELECT * FROM home_room";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) 
            if($row["MEANING"] == 'R'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/php/room_R.php" method="get">
                        <label name="MEANING" for="MEANING" value="R"> RELE:</label>
                        <button name="VALUE" type="submit" for="VALUE" value="OFF">ON</button>
                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/php/room_R.php" method="get">
                        <label name="MEANING" for="MEANING" value="R"> RELE:</label>
                        <button name="VALUE" type="submit" for="VALUE" value="ON">OFF</button>
                    </form>';;
                }
            }
    } else {
        echo "0 results";
    }

    $sql = "SELECT * FROM home_room";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) 
            if($row["MEANING"] == 'L'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/php/room_L.php" method="get">
                        <label name="MEANING" for="MEANING" value="L"> LIGHT:</label>
                        <button name="VALUE" type="submit" for="VALUE" value="OFF">ON</button>
                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/php/room_L.php" method="get">
                        <label name="MEANING" for="MEANING" value="L"> LIGHT:</label>
                        <button name="VALUE" type="submit" for="VALUE" value="ON">OFF</button>
                    </form>';;
                }
            }
    } else {
        echo "0 results";
    }

    $sql = "SELECT * FROM home_room";
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
<!----   LIVING ROOM      -->
    <br><div class='tittle'> -- LIVING ROOM --</div><br>
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
    <br>
<!----   LOGS     -->
    <form action="http://192.168.1.187/Domo/php/logs_mqtt_UI.php" method="get">
    -- <button class='tittle' type="submit">MQTT LOGS</button> --
    </form>
    
</body>

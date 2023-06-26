<head>
<link rel="stylesheet" href="UI_styles.css">
</head>
<body>
   <div><form action="http://192.168.1.187/Domo/index.php" method="get">
    <button class='tittle' type="submit">MAIN MENU</button>
    </form></div>
    <br><div><div class='section'> ROOM </div><br>
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
        {
	    if($row["MEANING"] == 'R'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/php/room_R.php" method="get">
                        <label name="MEANING" class="data" for="MEANING" value="R"> RELE:</label>
                        <button name="VALUE" class="atc_button" type="submit" for="VALUE" value="OFF">ON</button>
                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/php/room_R.php" method="get">
                        <label name="MEANING" class="data" for="MEANING" value="R"> RELE:</label>
                        <button name="VALUE" class="atc_button" type="submit" for="VALUE" value="ON">OFF</button>
                    </form>';;
                }
            }
	    if($row["MEANING"] == 'L'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/php/room_L.php" method="get">
                        <label name="MEANING" class="data" for="MEANING" value="L"> LIGHT:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="OFF">ON</button>
                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/php/room_L.php" method="get">
                        <label name="MEANING" class="data" for="MEANING" value="L"> LIGHT:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="ON">OFF</button>
                    </form>';;
                }
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
    ?></div><br>

<!-- PROTOCOLS -->
    <br><div><div class='section'>PROTOCOLS</div><br>
    <form action="http://192.168.1.187/Domo/php/proto_sunset_L.php" method="get">
    <button name="TOPIC" class='atc_button' type="submit" value="home/room/L" style="margin: 10px 10px 10px 60px;">Sunset</button>
    </form>
    <form action="http://192.168.1.187/Domo/php/proto_sunrise_L.php" method="get">
    <button name="TOPIC" class='atc_button' type="submit" value="home/room/L" style="margin: 10px 10px 10px 60px;">Sunrise</button>
    </form></div>
</body>
<head>
<link rel="stylesheet" href="css/UI_styles_1.css">
</head>
<body>
   <div><form action="http://192.168.1.187/Domo/index.php" method="get">
    <button class='tittle_button' type="submit">MAIN MENU</button>
    </form></div>
    <br><div><div class='section'> BEDROOM </div><br>
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

    $sql = "SELECT * FROM home_bedroom";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) 
        {
	    if($row["MEANING"] == 'R'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label class="data"> RELE:</label>
                        <button name="VALUE" class="atc_button" type="submit" for="VALUE" value="OFF">ON</button>
			<input name="TOPIC" value="home/bedroom/R" style="display:none"></input>
                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label class="data"> RELE:</label>
                        <button name="VALUE" class="atc_button" type="submit" for="VALUE" value="ON">OFF</button>
			<input name="TOPIC" value="home/bedroom/R" style="display:none"></input>
                    </form>';;
                }
            }
	    if($row["MEANING"] == 'L'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label class="data"> LIGHT:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="OFF">ON</button>
			<input name="TOPIC" for="TOPIC" value="home/bedroom/L" style="display:none"></input>

                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label name="MEANING" class="data"> LIGHT:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="ON">OFF</button>
			<input name="TOPIC" for="TOPIC" value="home/bedroom/L" style="display:none"></input>
                    </form>';;
                }
            }
	    if($row["MEANING"] == 'C'){
                if($row["VALUE"] == 'ON'){
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label class="data"> CAMERA:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="OFF">ON</button>
			<input name="TOPIC" for="TOPIC" value="home/bedroom/C" style="display:none"></input>

                    </form>';
                }else{
                    echo '<form action="http://192.168.1.187/Domo/frontend/php/update_parameter.php" method="get">
                        <label name="MEANING" class="data"> CAMERA:</label>
                        <button class="atc_button" name="VALUE" type="submit" for="VALUE" value="ON">OFF</button>
			<input name="TOPIC" for="TOPIC" value="home/bedroom/C" style="display:none"></input>
                    </form>';;
                }
            }
	}
    } else {
        echo "0 results";
    }

    $sql = "SELECT * FROM home_bedroom";
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
    <!--
    <form action="http://192.168.1.187/Domo/frontend/php/protocols/proto_photo_C.php" method="get">
    <button name="TOPIC" class='atc_button' type="submit" value="home/bedroom/C" style="margin: 10px 10px 10px 60px;">Camera</button>
    </form>
    -->
    <form action="http://192.168.1.187/Domo/frontend/php/protocols/proto_sunset_L.php" method="get">
    <button name="TOPIC" class='atc_button' type="submit" value="home/bedroom/L" style="margin: 10px 10px 10px 60px;">Sunset</button>
    </form>

    <form action="http://192.168.1.187/Domo/frontend/php/protocols/proto_sunrise_L.php" method="get">
    <button name="TOPIC" class='atc_button' type="submit" value="home/bedroom/L" style="margin: 10px 10px 10px 60px;">Sunrise</button>
    </form></div>
</body>
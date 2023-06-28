<head>
<link rel="stylesheet" href="UI_styles_1.css">
</head>
<body>
    <form action="http://192.168.1.187/Domo/index.php" method="get">
    <button class='tittle_button' type="submit">MAIN MENU</button>
    </form>
    <!----   LIVING ROOM      -->
    <br><div><div class='section'>LIVING ROOM</div><br>
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
    </div>
</body>
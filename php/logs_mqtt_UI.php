<head>
    <style>
	.tittle{
            font-size: 120px
        }
	.data{
	    font-size: 100px
	}
        .filter{
	    font-size: 75px
	}
	.logs{
	    font-size: 75px
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
    <br><div class='tittle'> -- MQTT LOGS --</div><br>
    <form action="http://192.168.1.187/Domo/php/logs_mqtt_UI.php" method="get"><select class='filter' name='filter'>
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
    $sql = "SELECT DISTINCT TOPIC FROM mqtt_historic";
    
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		echo "<option class='filter' value='".$row["TOPIC"]."'>".$row["TOPIC"]."</div>";
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

    $topic_filter = "home/room/T";
    if ($_GET['filter']){
	$topic_filter = $_GET['filter'];
    }
    echo "<div class='data'>Log: ". $topic_filter."</div><br><table>";
    
    $max_logs = 20;
    if ($_GET['max_logs']){
	$max_logs = $_GET['max_logs'];
    }

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
    </table>
</body>
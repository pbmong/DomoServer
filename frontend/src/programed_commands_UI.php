<head>
<link rel="stylesheet" href="css/UI_styles_1.css">
<style>
    table, th, td {
    	border: 3px solid; 
    	border-color: var(--base);
    }
    .datetime_filter{
	font-size: 80px;
	color: var(--text);
    }
</style>
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
    <div><div class='section'>INSERT CMD</div>
    <?php
    echo "<form class='filter' action='http://".$external_ip;
    echo ":".$external_port."/php/insert_command.php' method='get'>";
    ?>
    <select class='filter' name='TOPIC'>
    	<option class='filter' value='home/bedroom/R'>home/bedroom/R</option>
    	<option class='filter' value='home/bedroom/L'>home/bedroom/L</option>
    	<option class='filter' value='home/bedroom/C'>home/bedroom/C</option>
    </select>
    <select class='filter' name='VALUE'>
    	<option class='filter' value='ON'>ON</option>
    	<option class='filter' value='OFF'>OFF</option>
    </select>
    <input class='datetime_filter' type="text" name="DATETIME" value="YYYY-MM-DD_hh:mm:ss" maxlength="19" size="18"> 
    <DIV>	
	    M <input class='filter' type="checkbox" name="M" value="M" style="width:60px;height:60px;">
	    T <input class='filter' type="checkbox" name="T" value="T" style="width:60px;height:60px;">
	    W <input class='filter' type="checkbox" name="W" value="W" style="width:60px;height:60px;">
	    X <input class='filter' type="checkbox" name="X" value="X" style="width:60px;height:60px;">
	    F <input class='filter' type="checkbox" name="F" value="F" style="width:60px;height:60px;">
	    S <input class='filter' type="checkbox" name="S" value="S" style="width:60px;height:60px;">
	    N <input class='filter' type="checkbox" name="N" value="N" style="width:60px;height:60px;">
    </div>
    <button class='filter' type="submit">Apply</button></form><br>
    <div class='section'>COMMAND LIST</div><br><table>
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
 
    $sql = "SELECT * FROM `programed_commands` where ID < 100 ORDER BY `ID` ASC";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		$offset = strlen("python mqtt_send_to_topic_and_ddbb.py");
		$command = substr($row["COMMAND"], $offset);
		echo "<tr><td class='logs'> " . $row["ID"] ." |" . $command
			." | ".$row["DATETIME"]." | ". decbin($row["WEEKDAY"]) ."</td></tr>";
            }
    }

    $conn->close();
    ?>

    </table></div><br>

    <div><div class='section'>DELETE CMD</div>
    <?php
    echo "<form class='filter' action='http://".$external_ip;
    echo ":".$external_port."/php/delete_command.php' method='get'>";
    ?>
    <input class='filter' type="text" name="ID" value="0" maxlength="3" size="1"> 
    <button class='filter' type="submit">Apply</button></form><br>
</body>
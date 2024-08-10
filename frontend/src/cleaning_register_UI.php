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
    <div><div class='section'>INSERT REGISTER</div>
    <?php
    echo "<form class='filter' action='http://".$external_ip;
    echo ":".$external_port."/php/insert_cleaning_register.php' method='get'>";
    ?>
    <select class='filter' name='ROOM'>
    	<option class='filter' value='bedroom'>Bedroom   </option>
    	<option class='filter' value='livingroom'>Livingroom</option>
    	<option class='filter' value='kitchen'>Kitcken   </option>
    	<option class='filter' value='bathroom'>Bathroom  </option>
    </select>
    <select class='filter' name='LEVEL'>
    	<option class='filter' value='1'>Basic</option>
    	<option class='filter' value='2'>Intense</option>
    	<option class='filter' value='3'>Absolute</option>
    </select>
    <?php
    $datetime = date("Y-m-d_H:i:s");
    echo "<input class='datetime_filter' type='text' name='DATETIME' value='". $datetime ."' maxlength='19' size='18'>";
    ?>
    <button class='filter' type="submit">Apply</button></form><br>
    <div class='section'>REGISTER LIST</div><br><table>
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
 
    $sql = "SELECT * FROM `cleaning_register` where ID < 100 ORDER BY `ID` ASC";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc())
	    {
		    echo "<tr><td class='logs'> " . $row["ID"] ." | ". $row["DATETIME"] ." | ".$row["ROOM"] ." | ".$row["LEVEL"] . "</td></tr>";
        }
    }

    $conn->close();
    ?>

    </table></div><br>

    <div><div class='section'>DELETE REGISTER</div>
    <?php
    echo "<form class='filter' action='http://".$external_ip;
    echo ":".$external_port."/php/delete_cleaning_register.php' method='get'>";
    ?>
    <input class='filter' type="text" name="ID" value="0" maxlength="3" size="1"> 
    <button class='filter' type="submit">Apply</button></form><br>
</body>
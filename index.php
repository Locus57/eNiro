<html>
<head>
<title>Status e-Niro</title>
<style>
#Cellules {
border-collapse: collapse;
width; 100%;
}
#Cellules tr:nth-child(even){background-color: #f2f2f2;}
#Cellules tr:nth-child(odd){background-color: #e0e0e0;}

#Cellules td:hover {background-color: #0ddd0d;}

#Cellules td {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  color: black;
}

#progress {
  background: #333;
  border-radius: 13px;
  height: 18px;
  width: 180px;
  padding: 3px;
}

#progress:after {
  display: block;
  background: orange;
  width: 50%;
  height: 100%;
  border-radius: 9px;
}
div#colonne1 {
	float: left;
	width: 240px;
}
div#colonne2 {
	float: left;
	width: 200px;
}
div#colone3 {
	float: left;
	width: 70px;
}
</style>
</head>
<body>
<h1>e-Niro</h1>
<?php
// Connexion et sélection de la base
// CREATE TABLE IF NOT EXISTS AUX_BATTERY (`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,Valeur float, PRIMARY KEY (`date`));
 $link = mysqli_connect('localhost', 'eniro', 'eniro','eniro')
     or die('Impossible de se connecter : ' . mysql_error());
//StateOfCharge StateOfChargeDisplays
 $query = 'SELECT * FROM StateOfCharge order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $StateOfCharge=$line['Valeur'];
 $query = 'SELECT * FROM StateOfChargeDisplay order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $StateOfChargeDisplay=$line['Valeur'];
 $query = 'SELECT * FROM BatteryCurrent order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $BatteryCurrent=$line['Valeur'];
 $query = 'SELECT * FROM BatteryDCVoltage order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $BatteryDCVoltage=$line['Valeur'];
 $query = 'SELECT * FROM InletMaxTempBattery order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $InletMaxTempBattery=$line['Valeur'];
 $query = 'SELECT * FROM InletMinTempBattery order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $InletMinTempBattery=$line['Valeur'];
 $query = 'SELECT * FROM TempModuleBat1 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $TempModuleBat1=$line['Valeur'];
 $query = 'SELECT * FROM TempModuleBat2 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $TempModuleBat2=$line['Valeur'];
 $query = 'SELECT * FROM TempModuleBat3 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $TempModuleBat3=$line['Valeur'];
 $query = 'SELECT * FROM TempModuleBat4 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $TempModuleBat4=$line['Valeur'];
 $query = 'SELECT * FROM InletTempBattery order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $InletTempBattery=$line['Valeur'];
 $query = 'SELECT * FROM MaximumCellVoltage order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MaximumCellVoltage=$line['Valeur'];
 $query = 'SELECT * FROM MinimumCellVoltage order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MinimumCellVoltage=$line['Valeur'];
 $query = 'SELECT * FROM MaximumCellVoltageNo order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MaximumCellVoltageNo=$line['Valeur'];
 $query = 'SELECT * FROM MinimumCellVoltageNo order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MinimumCellVoltageNo=$line['Valeur'];

 $query = 'SELECT * FROM BatteryFanStatus order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $BatteryFanStatus=$line['Valeur'];
 $query = 'SELECT * FROM BatteryFanFeedback order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $BatteryFanFeedback=$line['Valeur'];
 $query = 'SELECT * FROM AuxillaryBatteryVoltage order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $AuxillaryBatteryVoltage=$line['Valeur'];
 $query = 'SELECT * FROM Gps';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $longitude=$line['longitude'];
 $lattitude=$line['lattitude'];
 $query = 'SELECT * FROM CumulativeChargeCurrent order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $CumulativeChargeCurrent=$line['Valeur'];
 $query = 'SELECT * FROM CumulativeDischargeCurrent order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $CumulativeDischargeCurrent=$line['Valeur'];
 $query = 'SELECT * FROM CumulativeEnergyCharged order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $CumulativeEnergyCharged=$line['Valeur'];
 $query = 'SELECT * FROM CumulativeEnergyDischarged order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $CumulativeEnergyDischarged=$line['Valeur'];
 $query = 'SELECT * FROM OperatingTime order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $OperatingTime=$line['Valeur'];
 $query = 'SELECT * FROM InverterCapacitorVoltage order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $InverterCapacitorVoltage=$line['Valeur'];
 $query = 'SELECT * FROM MotorSpeed1 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MotorSpeed1=$line['Valeur'];
 $query = 'SELECT * FROM MotorSpeed2 order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MotorSpeed2=$line['Valeur'];
 $query = 'SELECT * FROM HVCharging order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $HVCharging=$line['Valeur'];
 $query = 'SELECT * FROM StateOfHealth order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $StateOfHealth=$line['Valeur'];
 $query = 'SELECT * FROM MaximumDeteriorationCellNo order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MaximumDeteriorationCellNo=$line['Valeur'];
 $query = 'SELECT * FROM MinimumDeteriorationCellNo order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $MinimumDeteriorationCellNo=$line['Valeur'];
 $query = 'SELECT * FROM BatteryCellVoltageDeviation order by date desc limit 1';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
 $line=mysqli_fetch_array($result, MYSQLI_ASSOC);
 $BatteryCellVoltageDeviation=$line['Valeur'];

  echo "<div>La dernière position connue de la voiture <a href=http://www.openstreetmap.org/?mlat=".$lattitude."&mlon=".$longitude."&zoom=12>Longitude=".$longitude." et lattitude=".$lattitude."</a></div>";
 echo "<div id=colonne1>Etat de Charge</div><div id=colonne2><progress id=progress max=100 value=".$StateOfCharge." ></progress></div><div id=colonne3>".$StateOfCharge." %</div><br><br>";
 echo "<div id=colonne1>Etat de Charge visualisé</div><div id=colonne2><progress id=progress max=100 value=".$StateOfChargeDisplay." ></progress></div><div id=colonne3>".$StateOfChargeDisplay." %</div><br><br>";
 echo "<div id=colonne1>Etat de sante batterie</div><div id=colonne2><progress id=progress max=100 value=".$StateOfHealth." ></progress></div><div id=colonne3>".$StateOfHealth." %</div><br><br>";
 echo "<div id=colonne1>Charge haute tension</div><div id=colonne2>".$HVCharging."</div><br><br>";
 echo "<div id=colonne1>Conso batterie actuelle</div><div id=colonne2>".$BatteryCurrent." A</div><br><br>";
 echo "<div id=colonne1>Batterie DC</div><div id=colonne2>".$BatteryDCVoltage." Volts</div><br><br>";
 echo "<div id=colonne1>Temp max entree batterie</div><div id=colonne2>".$InletMaxTempBattery." °C</div><br><br>";
 echo "<div id=colonne1>Temp min entree batterie</div><div id=colonne2>".$InletMinTempBattery." °C</div><br><br>";
 echo "<div id=colonne1>Temp entree batterie</div><div id=colonne2>".$InletTempBattery." °C</div><br><br>";
 echo "<div id=colonne1>Temp dans batterie</div><div id=colonne2>".$TempModuleBat1." °C, ".$TempModuleBat2." °C, ".$TempModuleBat3." °C, ".$TempModuleBat4." °C</div><br><br>";
 echo "<div id=colonne1>Cellule Max et Volts</div><div id=colonne2>".$MaximumCellVoltageNo." avec ".$MaximumCellVoltage." V</div><br><br>";
 echo "<div id=colonne1>Cellule Min et Volts</div><div id=colonne2>".$MinimumCellVoltageNo." avec ".$MinimumCellVoltage." V</div><br><br>";
 echo "<div id=colonne1>Etat Ventil batterie</div><div id=colonne2><progress id=progress max=9 value=".$BatteryFanStatus." ></progress></div><div id=colonne3>".$BatteryFanStatus." (0-9)</div><br><br>";
 echo "<div id=colonne1>Retour Ventil batterie</div><div id=colonne2><progress id=progress max=120 value=".$BatteryFanFeedback." ></progress></div><div id=colonne3>".$BatteryFanFeedback." Hz</div><br><br>";
 echo "<div id=colonne1>Batterie auxilliaire</div><div id=colonne2>".$AuxillaryBatteryVoltage." Volts</div><br><br>";
 echo "<div id=colonne1>Cumul de courant chargé</div><div id=colonne2>".$CumulativeChargeCurrent." AH</div><br><br>";
 echo "<div id=colonne1>Cumul de courant dechargé</div><div id=colonne2>".$CumulativeDischargeCurrent." AH</div><br><br>";
 echo "<div id=colonne1>Cumul d'energie chargé</div><div id=colonne2>".$CumulativeEnergyCharged." kwh</div><br><br>";
 echo "<div id=colonne1>Cumul d'energie dechargé</div><div id=colonne2>".$CumulativeEnergyDischarged." kwh</div><br><br>";
 echo "<div id=colonne1>Temps d'utilisation</div><div id=colonne2>".$OperatingTime." heures</div><br><br>";
 echo "<div id=colonne1>Tension du condensateur de l'onduleur</div><div id=colonne2>".$InverterCapacitorVoltage." Volts</div><br><br>";
 echo "<div id=colonne1>Vitesse moteur</div><div id=colonne2>".$MotorSpeed1." et ".$MotorSpeed2."</div><br><br>";
 echo "<div id=colonne1>Cellule deteriorée max</div><div id=colonne2>".$MaximumDeteriorationCellNo."</div><br><br>";
 echo "<div id=colonne1>Cellule deteriorée min</div><div id=colonne2>".$MinimumDeteriorationCellNo."</div><br><br>";
 echo "<div id=colonne1>Deviation des cellules</div><div id=colonne2>".$BatteryCellVoltageDeviation."</div><br><br>";
 
 // Exécution des requêtes SQL
 $query = 'SELECT * FROM Cellules order by id';
 $result = mysqli_query($link,$query) or die('Échec de la requête : ' . mysqli_error());
// Affichage des résultats en HTML
 echo "<center><p>Etat des Cellules</p>";
 echo "<table id=\"Cellules\">\n";
 $i=0;
 while ($line = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
     if ($i==0) echo "\t<tr>\n";
     echo "\t\t<td width=40>".($line['Valeur'])."</td>\n";
     $i++;
     if ($i==16) {
	     echo "\t</tr>\n";
	     $i=0;
     }
 }
 echo "</table></center>\n";
 mysqli_free_result($result);
 // Fermeture de la connexion
 mysqli_close($link);
?>
</html>
</body>

#!/bin/bash
#A executer 1 fois pour la creation des fichiers rrd 
mkdir /home/pi/rrd
rrdtool create /home/pi/rrd/StateOfCharge.rrd -s 600 DS:Valeur:GAUGE:600:0:120  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/StateOfChargeDisplay.rrd -s 600 DS:Valeur:GAUGE:600:0:120  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/StateOfHealth.rrd -s 600 DS:Valeur:GAUGE:600:0:120  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/BatteryCurrent.rrd -s 600 DS:Valeur:GAUGE:600:0:120  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/BatteryDCVoltage.rrd -s 600 DS:Valeur:GAUGE:600:0:520  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/InletTempBattery.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/InletMaxTempBattery.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/InletMinTempBattery.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/TempModuleBat1.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/TempModuleBat2.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/TempModuleBat3.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/TempModuleBat4.rrd -s 600 DS:Valeur:GAUGE:600:-50:100  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/BatteryFanStatus.rrd -s 600 DS:Valeur:GAUGE:600:0:10  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/BatteryFanFeedback.rrd -s 600 DS:Valeur:GAUGE:600:0:150  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/AuxillaryBatteryVoltage.rrd -s 600 DS:Valeur:GAUGE:600:0:20  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460
rrdtool create /home/pi/rrd/InverterCapacitorVoltage.rrd -s 600 DS:Valeur:GAUGE:600:0:20  RRA:AVERAGE:0.5:1:288 RRA:AVERAGE:0.5:3:672 RRA:AVERAGE:0.5:12:744 RRA:AVERAGE:0.5:72:1460

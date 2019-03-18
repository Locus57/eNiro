#!/bin/bash
mkdir /var/www/html/stats
#
# Generation des graphiques Volts
# A lancer toutes les 5 minutes via Crontab
#
for i in AuxillaryBatteryVoltage InverterCapacitorVoltage BatteryCurrent BatteryDCVoltage
do
echo $i
rrdtool graph /var/www/html/stats/$i.jour.png -a PNG --start -86400 --end now --title="$i" --vertical-label "Volts" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"Volts"' 
rrdtool graph /var/www/html/stats/$i.semaine.png -a PNG --start -604800 --end now --title="$i" --vertical-label "Volts" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"Volts"' 
rrdtool graph /var/www/html/stats/$i.mois.png -a PNG --start -18144000 --end now --title="$i" --vertical-label "Volts" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"Volts"' 
rrdtool graph /var/www/html/stats/$i.annee.png -a PNG --start -31536000 --end now --title="$i" --vertical-label "Volts" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"Volts"' 
done

#
# Generation des graphiques Temperature
#
for i in TempModuleBat1 TempModuleBat2 TempModuleBat3 TempModuleBat4 InletMaxTempBattery InletMinTempBattery InletTempBattery
do
echo $i
rrdtool graph /var/www/html/stats/$i.jour.png -a PNG --start -86400 --end now --title="$i" --vertical-label "°C" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"°C"' 
rrdtool graph /var/www/html/stats/$i.semaine.png -a PNG --start -604800 --end now --title="$i" --vertical-label "°C" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"°C"' 
rrdtool graph /var/www/html/stats/$i.mois.png -a PNG --start -18144000 --end now --title="$i" --vertical-label "°C" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"°C"' 
rrdtool graph /var/www/html/stats/$i.annee.png -a PNG --start -31536000 --end now --title="$i" --vertical-label "°C" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"°C"' 
done

#
# Generation des graphiques Pourcents
#
for i in StateOfChargeDisplay StateOfCharge StateOfHealth
do
echo $i
rrdtool graph /var/www/html/stats/$i.jour.png -a PNG --start -86400 --end now --title="$i" --vertical-label "%" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"%"' 
rrdtool graph /var/www/html/stats/$i.semaine.png -a PNG --start -604800 --end now --title="$i" --vertical-label "%" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"%"' 
rrdtool graph /var/www/html/stats/$i.mois.png -a PNG --start -18144000 --end now --title="$i" --vertical-label "%" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"%"' 
rrdtool graph /var/www/html/stats/$i.annee.png -a PNG --start -31536000 --end now --title="$i" --vertical-label "%" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:"%"' 
done

#
# Generation des graphiques autres
#
for i in BatteryFanStatus BatteryFanFeedback
do
echo $i
rrdtool graph /var/www/html/stats/$i.jour.png -a PNG --start -86400 --end now --title="$i" --vertical-label "" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:""' 
rrdtool graph /var/www/html/stats/$i.semaine.png -a PNG --start -604800 --end now --title="$i" --vertical-label "" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:""' 
rrdtool graph /var/www/html/stats/$i.mois.png -a PNG --start -18144000 --end now --title="$i" --vertical-label "" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:""' 
rrdtool graph /var/www/html/stats/$i.annee.png -a PNG --start -31536000 --end now --title="$i" --vertical-label "" DEF:Valeur=/home/pi/rrd/$i.rrd:Valeur:AVERAGE 'LINE1:Valeur#ff0000:""' 
done


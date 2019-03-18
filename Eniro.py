#!/usr/bin/python3

#
# eNiroObd2
# Ce script se connecte (via bluetooth ou série) à une connexion Obd2 de eNiro
# pour extraire divers données et les stocker dans une base de données MySql locale
# Prévoir la création d'une base Mysql nommée eniro avec les comptes eniro, mot de passe eniro
# Pour plus de securité, vous pouvez changer ces éléments
# L'accès se fait via le /dev/rfcomm0 qui est rattaché au boitier Elm327
# v0.5 17/03/2019: Version initiale pour validation technique de la chaine 
#
import serial
import time
import mysql.connector
import gpsd
import os

now = time.strftime('%Y-%m-%d %H-%M-%S')
jour = time.strftime('%Y-%m-%d 00-00-00')

#
# Connexion au service Gpsd
#
gpsd.connect()

#Effectue un test pour voir si le Gps est fixé
os.system('gpspipe -l -o /tmp/gpspipe.txt -p -w -n 10')
GpsOk=0
with open('/tmp/gpspipe.txt') as openfileobject:
    for line in openfileobject:
        if (line.find('"mode":3')>0):
            GpsOk=1

if (GpsOk>0):
    gps=gpsd.get_current()
#
#Connexion a la base de donnees
#
# Base Mysql locale avec:
# Nombase: eniro
# util: eniro
# pass: eniro
#
connexionBD = mysql.connector.connect(
        host = 'localhost',
        user = 'eniro',
        password = 'eniro',
        database = 'eniro'
        )

#
# Création des tables si elles n'existent pas dans la base de données
# Rien de compliqué ni optimisé, une table par élément recupéré sauf pour le voltage des cellules et la table Gps
# Chaque table donc à la structure suivante:
# date   ==> "Date du jour" ou "date du jour+heure"
# Valeur ==> float qui contient la valeur reprise au moment du script
#
# Pour la table Cellules, elle contient:
# id     ==> 0 à 95 
# Valeur ==> Voltage de la cellule
# 
cursor=connexionBD.cursor()
cursor.execute("DROP TABLE IF EXISTS Cellules")
cursor.execute("DROP TABLE IF EXISTS Gps")
connexionBD.commit();
cursor.execute("CREATE TABLE IF NOT EXISTS Cellules (id integer,Valeur float)")
cursor.execute("CREATE TABLE IF NOT EXISTS Gps (longitude float, lattitude float)")

#
# Création des autres tables
#
ListeDesTables= ['StateOfCharge','BatteryCurrent','BatteryDCVoltage','InletMaxTempBattery',
        'InletMinTempBattery','TempModuleBat1','TempModuleBat2','TempModuleBat3','TempModuleBat4',
        'InletTempBattery','MaximumCellVoltage','MaximumCellVoltageNo','MinimumCellVoltage',
        'MinimumCellVoltageNo','BatteryFanStatus','BatteryFanFeedback','AuxillaryBatteryVoltage',
        'CumulativeChargeCurrent','CumulativeDischargeCurrent','CumulativeEnergyCharged',
        'CumulativeEnergyDischarged','OperatingTime','InverterCapacitorVoltage','MotorSpeed1',
        'MotorSpeed2','HVCharging','StateOfChargeDisplay','StateOfHealth','MaximumDeteriorationCellNo',
        'MinimumDeteriorationCellNo','BatteryCellVoltageDeviation']

for elm in ListeDesTables:
    print("CREATE TABLE IF NOT EXISTS "+elm+" (`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,Valeur float, PRIMARY KEY (`date`))")
    cursor.execute("CREATE TABLE IF NOT EXISTS "+elm+" (`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,Valeur float, PRIMARY KEY (`date`))")

#
# Mise à jour position Gps
#
if (GpsOk>0):
    cursor.execute("INSERT INTO Gps Values ('"+str(gps.lon)+"','"+str(gps.lat)+"')")
#
# Connexion à l'Elm327 via Bluetooth via le pseudo dev '/dev/rfcomm0' en vitesse 9600bauds
#
ser=serial.Serial('/dev/rfcomm0', 9600, dsrdtr=0)
try:
    ser.in_waiting
except serial.serialutil.SerialException:
    print("Connexion impossible avec Elm327")

Reponse=[]
VoltageCellule=[]
NoCellule=0
#
# Exemple de trames reçues 0x220101
# a été utilisé pour le dev sans avoir la voiture
#
ReponseATraiter1=b'SEARCHING...\r7EC 10 3E 62 01 01 FF F7 E7 \r7EC 21 FF B9 1B A0 46 50 03 \r7EC 22 00 04 0F B7 0B 0A 09 \r7EC 23 09 0A 09 00 00 08 CD \r7EC 24 0A CD 32 00 00 92 00 \r7EC 25 00 3C 34 00 00 38 55 \r7EC 26 00 00 16 BD 00 00 14 \r7EC 27 91 00 0A 29 92 0D 01 \r7EC 28 92 00 00 00 00 03 E8 \r\r>'
ReponseATraiter2=b'7EC 10 27 62 01 02 FF FF FF \r7EC 21 FF CD CD CD CD CD CD \r7EC 22 CD CD CD CD CD CD CD \r7EC 23 CD CD CD CD CD CD CD \r7EC 24 CD CD CD CD CD CD CD \r7EC 25 CD CD CD CD CD AA AA \r\r>'
ReponseATraiter3=b'7EC 10 27 62 01 03 FF FF FF \r7EC 21 FF CD CD CD CD CD CD \r7EC 22 CD CD CD CD CD CD CD \r7EC 23 CD CD CD CD CD CD CD \r7EC 24 CD CD CD CD CD CD CD \r7EC 25 CD CD CD CD CD AA AA \r\r>'
ReponseATraiter4=b'7EC 10 27 62 01 04 FF FF FF \r7EC 21 FF CD CD CD CD CD CD \r7EC 22 CD CD CD CD CD CD CD \r7EC 23 CD CD CD CD CD CD CD \r7EC 24 CD CD CD CD CD CD CD \r7EC 25 CD CD CD CD CD AA AA \r\r>'
ReponseATraiter5=b'7EC 10 2E 62 01 05 00 3F FF \r7EC 21 90 00 00 00 00 00 00 \r7EC 22 00 00 00 00 00 00 1B \r7EC 23 A0 46 50 00 01 50 D0 \r7EC 24 00 03 E8 00 00 00 00 \r7EC 25 C2 00 00 CD CD 00 00 \r7EC 26 0A 00 00 00 00 AA AA \r\r>'

#
# Fonction d'init du module Elm327, perso c'est un Elm327 Ebay en v1.5
# ATZ  =Reset du module
# ATE0 =Enlever l'echo local
# ATH1 =Activer des header sur chaque ligne (ECU qui répond)
# ATL0 =Retrait du linefeed (fin de ligne)
# ATSP0=Gestion des espaces dans la réponse du Mcu
#
def InitObd():
    AppelOBD('ATZ',1)
    AppelOBD('ATE0',0.5)
    AppelOBD('ATH1',0.5)
    AppelOBD('ATL0',0.5)
    AppelOBD('ATSP0',2)

#
# Fonction d'envoi d'une demande à l'Obd2, stocké dans le tuple "Reponse"
# Parametre s=Ordre à envoyer à l'Obd2
# 	    t=Temps d'attente avant réponse
#
def AppelOBD(s,t):
    print(s)
    ser.flushInput();
    ser.write(bytes(s + '\r\n', encoding = 'utf-8'))
    ser.flush();
    ser.timeout = 1
    time.sleep(t)
    while ser.in_waiting:
        Reponse.append(ser.readline())

# 
# Fonction de filtre binaire d'un octet pour les traiter les 96 Cellules de la batterie
#
def RecupBinaire(Rep,Chaine,decalage):
    LChaine=len(Chaine)+decalage
    Pos=Rep.find(Chaine)
#    print(Rep[Pos+LChaine:Pos+LChaine+2])
    return Rep[Pos+LChaine:Pos+LChaine+2]

#
# Fonction de recup d'un octet dans une chaine
#
def Recup1(Rep,Chaine,decalage):
    LChaine=len(Chaine)+decalage
    Pos=Rep.find(Chaine)
#    print (Rep[Pos+LChaine:Pos+LChaine+2])
    return int(Rep[Pos+LChaine:Pos+LChaine+2],16)

#
# Fonction de recup de 2 octets dans une chaine
#
def Recup2(Rep,Chaine,decalage):
    LChaine=len(Chaine)+decalage
    Pos=Rep.find(Chaine)
#    print(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5])
    return int(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5],16)

#
# Fonction de recup de 3 octets dans une chaine
#
def Recup3(Rep,Chaine,decalage):
    LChaine=len(Chaine)+decalage
    Pos=Rep.find(Chaine)
#    print(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5]+Rep[Pos+LChaine+6:Pos+LChaine+8])
    return int(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5]+Rep[Pos+LChaine+6:Pos+LChaine+8],16)

#
# Fonction de recup de 4 octets dans une chaine
#
def Recup4(Rep,Chaine,decalage):
    LChaine=len(Chaine)+decalage
    Pos=Rep.find(Chaine)
#    print(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5]+Rep[Pos+LChaine+6:Pos+LChaine+8]+Rep[Pos+LChaine+9:Pos+LChaine+11])
    return int(Rep[Pos+LChaine:Pos+LChaine+2]+Rep[Pos+LChaine+3:Pos+LChaine+5]+Rep[Pos+LChaine+6:Pos+LChaine+8]+Rep[Pos+LChaine+9:Pos+LChaine+11],16)

#
# Fonction de Maj d'une table avec la valeur et la date+heure actuelle
# Table =Nom de la table
# Valeur=Valeur à inserer dans la table
#
def MajBase(Table,Valeur):
    print("INSERT INTO "+str(Table)+" Values ('"+str(now)+"','"+str(Valeur)+"') ON DUPLICATE KEY UPDATE Valeur='"+str(Valeur)+"'")
    cursor.execute("INSERT INTO "+str(Table)+" Values ('"+str(now)+"','"+str(Valeur)+"') ON DUPLICATE KEY UPDATE Valeur='"+str(Valeur)+"'")

#
# Fonction de Maj d'une table avec la valeur et la date actuelle
# Table =Nom de la table
# Valeur=Valeur à inserer dans la table
#
def MajBaseJour(Table,Valeur):
    print("INSERT INTO "+str(Table)+" Values ('"+str(jour)+"','"+str(Valeur)+"') ON DUPLICATE KEY UPDATE Valeur='"+str(Valeur)+"'")
    cursor.execute("INSERT INTO "+str(Table)+" Values ('"+str(jour)+"','"+str(Valeur)+"') ON DUPLICATE KEY UPDATE Valeur='"+str(Valeur)+"'")

#
# Fonction qui va traiter le retour de l'ordre 0x220101
# Ce script va parser la chaine, se placer sur les octets, extraire
# les valeurs (1, 2, 3 ou 4 octets) et les stocker dans les tables qui vont bien
#
def ATraiterBloc1(Rep):
    StateOfCharge=Recup1(Rep,b'7EC 21 FF ',0)/2
    print("StateOfCharge:" + str(StateOfCharge)+" %")
    MajBase("StateOfCharge",StateOfCharge)
    BatteryCurrent=Recup2(Rep,b'7EC 22 ',0)/10
    print("Battery Current:" + str(BatteryCurrent)+" A")
    MajBase("BatteryCurrent",BatteryCurrent)
    BatteryDCVoltage=Recup2(Rep,b'7EC 22 ',6)/10
    print("Battery DC Voltage:" + str(BatteryDCVoltage)+" V")
    MajBase("BatteryDCVoltage",BatteryDCVoltage)
    InletMaxTempBattery=Recup1(Rep,b'7EC 22 ',12)
    print("InletMaxTempBattery:"+ str(InletMaxTempBattery)+" °C")
    MajBase("InletMaxTempBattery",InletMaxTempBattery)
    InletMinTempBattery=Recup1(Rep,b'7EC 22 ',15)
    print("InletMinTempBattery:"+ str(InletMinTempBattery)+" °C")
    MajBase("InletMinTempBattery",InletMinTempBattery)
    TempModuleBat1=Recup1(Rep,b'7EC 22 ',18)
    print("TempModuleBat1:"+ str(TempModuleBat1)+" °C")
    MajBase("TempModuleBat1",TempModuleBat1)
    TempModuleBat2=Recup1(Rep,b'7EC 23 ',0)
    print("TempModuleBat2:"+ str(TempModuleBat2)+" °C")
    MajBase("TempModuleBat2",TempModuleBat2)
    TempModuleBat3=Recup1(Rep,b'7EC 23 ',3)
    print("TempModuleBat3:"+ str(TempModuleBat3)+" °C")
    MajBase("TempModuleBat3",TempModuleBat3)
    TempModuleBat4=Recup1(Rep,b'7EC 23 ',6)
    print("TempModuleBat4:"+ str(TempModuleBat4)+" °C")
    MajBase("TempModuleBat4",TempModuleBat4)
    InletTempBattery=Recup1(Rep,b'7EC 23 ',15)
    print("InletTempBattery:"+ str(InletTempBattery)+" °C")
    MajBase("InletTempBattery",InletTempBattery)
    Maximum_Cell_Voltage=Recup1(Rep,b'7EC 23 ',18)/50
    print("Maximum Cell Voltage:"+ str(Maximum_Cell_Voltage))
    MajBase("MaximumCellVoltage",Maximum_Cell_Voltage)
    Maximum_Cell_Voltage_No=Recup1(Rep,b'7EC 24 ',0)
    print("Maximum Cell Voltage No:"+ str(Maximum_Cell_Voltage_No))
    MajBase("MaximumCellVoltageNo",Maximum_Cell_Voltage_No)
    Minimum_Cell_Voltage=Recup1(Rep,b'7EC 24 ',3)/50
    print("Minium Cell Voltage:"+ str(Minimum_Cell_Voltage))
    MajBase("MinimumCellVoltage",Minimum_Cell_Voltage)
    Minimum_Cell_Voltage_No=Recup1(Rep,b'7EC 24 ',6)
    print("Minium Cell Voltage No:"+ str(Minimum_Cell_Voltage_No))
    MajBase("MinimumCellVoltageNo",Minimum_Cell_Voltage_No)
    Battery_Fan_Status=Recup1(Rep,b'7EC 24 ',9)
    print("Battery_Fan_Status:"+ str(Battery_Fan_Status))
    MajBase("BatteryFanStatus",Battery_Fan_Status)
    Battery_Fan_Feedback=Recup1(Rep,b'7EC 24 ',12)
    print("Battery_Fan_Feedback:"+ str(Battery_Fan_Feedback)+" Hz")
    MajBase("BatteryFanFeedback",Battery_Fan_Feedback)
    Auxillary_Battery_Voltage=Recup1(Rep,b'7EC 24 ',15)/10
    print("Auxillary_Battery_Voltage:"+ str(Auxillary_Battery_Voltage)+" V")
    MajBase("AuxillaryBatteryVoltage",Auxillary_Battery_Voltage)
    CumulativeChargeCurrent=Recup1(Rep,b'7EC 24 ',18)*16777216+Recup3(Rep,b'7EC 25 ',0)/10
    print("CumulativeChargeCurrent:"+ str(CumulativeChargeCurrent)+" AH")
    MajBase("CumulativeChargeCurrent",CumulativeChargeCurrent)
    CumulativeDischargeCurrent=Recup4(Rep,b'7EC 25 ',9)/10
    print("CumulativeDischargeCurrent:"+ str(CumulativeDischargeCurrent)+" AH")
    MajBase("CumulativeDischargeCurrent",CumulativeDischargeCurrent)
    CumulativeEnergyCharged=Recup4(Rep,b'7EC 26 ',0)/10
    print("CumulativeEnergyCharged:"+ str(CumulativeEnergyCharged)+" kwh")
    MajBase("CumulativeEnergyCharged",CumulativeEnergyCharged)
    CumulativeEnergyDischarged=(Recup1(Rep,b'7EC 27 ',0)+Recup3(Rep,b'7EC 26 ',12)*256)/10
    print("CumulativeEnergyDischarged:"+ str(CumulativeEnergyDischarged)+" kwh")
    MajBase("CumulativeEnergyDischarged",CumulativeEnergyDischarged)
    OperatingTime=round(Recup4(Rep,b'7EC 27 ',3)/3600)
    print("OperatingTime:"+ str(OperatingTime)+" heures")
    MajBase("OperatingTime",OperatingTime)
    InverterCapacitorVoltage=(Recup1(Rep,b'7EC 27 ',18)*256+Recup1(Rep,b'7EC 28 ',0))
    print("Inverter Capacitor Voltage:" +str(InverterCapacitorVoltage)+" V")
    MajBase("InverterCapacitorVoltage",InverterCapacitorVoltage)
    MotorSpeed1=Recup2(Rep,b'7EC 28 ',3)
    print("MotorSpeed1:"+str(MotorSpeed1))
    MajBase("MotorSpeed1",MotorSpeed1)
    MotorSpeed2=Recup2(Rep,b'7EC 28 ',9)
    print("MotorSpeed2:"+str(MotorSpeed2))
    MajBase("MotorSpeed2",MotorSpeed2)
    HV_Charging=(Recup1(Rep,b'7EC 21 ',18)&128)/128
    print("HV_Charging:"+str(HV_Charging))
    MajBase("HVCharging",HV_Charging)
    connexionBD.commit()

#
# Fonction qui va traiter le retour de l'ordre 0x220102 à 0x220104
# Utilisée pour la reprise des valeurs des 96 cellules
# Stocke la valeur dans la table Cellules
#
def ATraiterBloc2(Rep):
    global NoCellule
    for i in range(0,18,3):
        VoltageCellule.append(RecupBinaire(Rep,b'7EC 21 FF ',i))
        cursor.execute("insert into Cellules values ("+str(NoCellule)+","+str(int(RecupBinaire(Rep,b'7EC 21 FF ',i),16)/50)+");")
        NoCellule=NoCellule+1
    for i in range(0,19,3):
        VoltageCellule.append(RecupBinaire(Rep,b'7EC 22 ',i))
        cursor.execute("insert into Cellules values ("+str(NoCellule)+","+str(int(RecupBinaire(Rep,b'7EC 22 ',i),16)/50)+");")
        NoCellule=NoCellule+1
    for i in range(0,19,3):
        VoltageCellule.append(RecupBinaire(Rep,b'7EC 23 ',i))
        cursor.execute("insert into Cellules values ("+str(NoCellule)+","+str(int(RecupBinaire(Rep,b'7EC 23 ',i),16)/50)+");")
        NoCellule=NoCellule+1
    for i in range(0,19,3):
        VoltageCellule.append(RecupBinaire(Rep,b'7EC 24 ',i))
        cursor.execute("insert into Cellules values ("+str(NoCellule)+","+str(int(RecupBinaire(Rep,b'7EC 24 ',i),16)/50)+");")
        NoCellule=NoCellule+1
    for i in range(0,14,3):
        VoltageCellule.append(RecupBinaire(Rep,b'7EC 25 ',i))
        cursor.execute("insert into Cellules values ("+str(NoCellule)+","+str(int(RecupBinaire(Rep,b'7EC 25 ',i),16)/50)+");")
        NoCellule=NoCellule+1
    connexionBD.commit()

#
# Fonction qui va traiter le retour de l'ordre 0x220105
# Ce script va parser la chaine, se placer sur les octets, extraire
# les valeurs (1, 2, 3 ou 4 octets) et les stocker dans les tables qui vont bien
# 
def ATraiterBloc3(Rep):
    StateOfChargeDisplay=Recup1(Rep,b'7EC 25 ',0)/2
    print("StateOfChargeDisplay:" + str(StateOfChargeDisplay)+" %")
    MajBase("StateOfChargeDisplay",StateOfChargeDisplay)
    StateOfHealth=Recup2(Rep,b'7EC 24 ',3)/10
    print("StateOfHealth:" + str(StateOfHealth)+" %")
    MajBase("StateOfHealth",StateOfHealth)
    Maximum_Deterioration_Cell_No=Recup1(Rep,b'7EC 24 ',9)
    print("Maximum_Deterioration_Cell_No:"+ str(Maximum_Deterioration_Cell_No))
    MajBase("MaximumDeteriorationCellNo",Maximum_Deterioration_Cell_No)
    Minimum_Deterioration_Cell_No=Recup1(Rep,b'7EC 24 ',18)
    print("Minimum_Deterioration_Cell_No:"+ str(Minimum_Deterioration_Cell_No))
    MajBase("MinimumDeteriorationCellNo",Minimum_Deterioration_Cell_No)
    Battery_Cell_Voltage_Deviation=Recup1(Rep,b'7EC 23 ',12)/50
    print("Battery cell Voltage Deviation:"+str(Battery_Cell_Voltage_Deviation))
    MajBase("BatteryCellVoltageDeviation",Battery_Cell_Voltage_Deviation)
    connexionBD.commit()

#
# Début du script 
#
print("e-Niro")

InitObd()
Reponse.clear()


#
# Ajout des filtres/masques sur le bus CAN pour limiter les resultats à recevoir du module Obd2
# 0x7EC contient les réponses attendus pour toutes les commandes
#
AppelOBD('ATCM FFF',1.0)
AppelOBD('ATCF 7EC',1.0)

# Appel 0x220101, traitement des valeurs retournées
Reponse.clear()
AppelOBD('220101',2)
ATraiterBloc1(Reponse[0])

# Appel 0x220102 à 0x220104, traitement des valeurs retournées
NoCellule=0
Reponse.clear()
AppelOBD('220102',2)
ATraiterBloc2(Reponse[0])
Reponse.clear()
AppelOBD('220103',2)
ATraiterBloc2(Reponse[0])
Reponse.clear()
AppelOBD('220104',2)
ATraiterBloc2(Reponse[0])

# Appel 0x220105, traitement des valeurs retournées
Reponse.clear()
AppelOBD('220105',2)
ATraiterBloc3(Reponse[0])

ser.close()


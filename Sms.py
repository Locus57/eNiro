#!/usr/bin/python3
#
# Ce script va vérifier toutes les 30 secondes s'il n'a pas reçu de Sms, s'il en reçoit 1 d'un No de telephone précis,
# Il renverra un Sms avec la date et la charge actulle du véhicule.
# C'est modulable avec d'autres choses, comme l'état de charge, etc...
# Il travaille sur le port /dev/ttyUSB0 qui est rattaché à une carte Sim800L et un abonnement Gsm de base (Style Free à 2euros)
# Pas d'abonnement Data, que du Sms dans notre cas
# 
import serial
import time, sys
import datetime
import mysql.connector

#
# Fonction principal et unique fonction
#
def setup():
    #Le pseudo dev sur lequel est rattaché le Sim800l 
    SERIAL_PORT = "/dev/ttyUSB0"  
    ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
    #Init du modem
    ser.write(b"ATZ\r") # Reset du module Sim800
    time.sleep(3)
    #Saisie du code PIN de la carte SIM, attention à bien rentrer le bon code
    #Au bout de 3 erreurs, il faudra replacer la carte Sim dans un telephone et revalider avec
    #le code Puke fourni avec la Sim 
    ser.write(b"AT+CPIN=1234\r") # Envoi code pin
    time.sleep(3)
    ser.write(b"AT+CMGF=1\r") # Passage en mode texte
    time.sleep(3)
    ser.write(b'AT+CMGDA="DEL ALL"\r') # Purge des Sms qui sont dans la Sim
    time.sleep(3)
    reply = ser.read(ser.inWaiting()) # Vidage du buffer du port série
    print("Boucle infini qui test l'arrivée de SMS...")
    while True:
        reply = ser.read(ser.inWaiting())
        print(reply)
        if reply != b"":
	    #Verif si un Sms est dans la Sim
            ser.write(b"AT+CMGR=1\r") 
            time.sleep(3)
            reply = ser.read(ser.inWaiting())
            print("Voici le SMS:")
            print(reply)
	    #Pour eviter de répondre ç d'autres SMS, on vérifie que le telephone qui a fait la demande est le bon
	    #En vérifiant son No
            if b"33601020304" in reply:
		#Connexion à la Base de données Mysql
                connexionBD = mysql.connector.connect(
                    host = 'localhost',
                    user = 'eniro',
                    password = 'eniro',
                    database = 'eniro'
                )
                cursor=connexionBD.cursor()
		#On recupère la valeur à renvoyer
                cursor.execute("SELECT * FROM StateOfChargeDisplay order by date desc limit 1")
                Jour,StateOfChargeDisplay = cursor.fetchone()
                print("Etat de charge:")
                print(StateOfChargeDisplay)
                print(Jour)
                cursor.execute("SELECT * FROM HVCharging order by date desc limit 1")
                Jour,HVChargine = cursor.fetchone()
                if HVCharging == b"0":
                   HVC="En charge"
                else:
                   HVC="Pas en charge"
                connexionBD.close()
		#On prépare le message qui sera envoyé
		#Laisser le \x1a, c'est le code de fin de Sms qui va indiquer au Sim800L d'envoyer le Sms
                ChaineAEnvoyer=str("e-Niro:")+str(Jour)+str(" ")+HVC+" avec "+str(StateOfChargeDisplay)+str(" %\x1a\r")
                print(ChaineAEnvoyer)
		#On indique le telephone de destination du Sms
                ser.write(b'AT+CMGS="+33601020304"\r')
                time.sleep(3)
                ser.write(ChaineAEnvoyer.encode('ascii')) # encodage en Ascii de notre message à envoyer
                time.sleep(3)
                ser.write(b'AT+CMGDA="DEL ALL"\r') # On vide tous les sms dans la Sim
                time.sleep(3)
                ser.read(ser.inWaiting()) # On vide le Buffer du port série
                time.sleep(3)
        else:
            print("Aucun sms en attente")
        time.sleep(30)
#
# Appel de la boucle principale
#
setup()

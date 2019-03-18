# eNiro
Remote access to eNiro, like UVO Connect

Kia does not provide remote access (via UVO Connect) in Europ for eNiro EV.
I like Nissan Connect to see Ev charging status, Gps position.
With this project, I want to remotly access eNiro Chargins status through Wifi or Gsm.

What you need:
1. RaspberryPI2 or 3
2. Usb-Bluetooth module
3. Elm327 Obd2 - Bluetooth module
4. Gps - Usb module (Optionnal)
5. Gsm - Usb module (Optionnal) like Sim800L

A python script will interrogate the car via the Obd2 socket and parse the answers in a Mysql database about the state of the batteries.

A web page in php / mysql will display the contents of the database.

A last script waits for an SMS and returns to the sender an answer with the state of charge and its percentage.

It is a Proof of Concept, need some optimizations.


# thesis-project
# RPI-1

Below is the guide to setup the code and run it.

Steps 

1. Clone the GitHub repository RPI-1
2. Install the Arduino software on RPI.
3. Setup the ESP board and install the MQTT PubSubClient library by Nick O’Leary on Arduino IDE.
4. Connect a ESP8266 board to RPI, select the respective port on Arduino IDE.
5. Make necessary changes to the receiver code, such as wifi network, ip address, etc., and upload the receiver code to the ESP8266 board.
6. Change the MAC address in senders and upload the code to the boards.
7. Install MQTT via terminal.
8. Install the necessary libraries for the individual folders - deployment-server, drive-upload and mobile net, using respective requirements.txt files, with python.
9. Connect the camera to the RPI pins.
10. Connect servo motor to the RPI using this : https://www.youtube.com/watch?v=xHDT4CwjUQE
11. Connect GPS to the RPI and configure the settings by following this : https://www.hackster.io/bhushanmapari/interfacing-u-blox-neo-6m-gps-module-with-raspberry-pi-3d15a5
12. Paste the .service files in /etc/systemd/system/ and enable and start the services

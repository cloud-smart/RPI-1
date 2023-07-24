/* Including the libraries */
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

/*
/*
//#ifndef APSSID
#define APSSID "ESP_Wifi_01"
#define APPSK "123456"
//#endif

/* Setting the Credentials 
const char *ssid = APSSID;
const char *password = APPSK;


ESP8266WebServer server(80);

/* Go to http://198.168.4.1 
void handleRoot(){
  server.send(200, "text/html", "<h1>Hi! You're Connected.</h1>");
}

/* Run Once 
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point...");

  //We can remove the password parameter if we want the AP to be open
  //boolean result = WiFi.softAP(ssid, password);
  boolean result = WiFi.softAP("ESP_Wifi_01", "pass");  
  if(result == true){
    Serial.println("Ready");
  }else{
    Serial.println("Failed");
  }

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP Address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP Server Started");
  
}

/* Runs in a Loop 
void loop() {
  Serial.printf("Stations Connected = %d\n", WiFi.softAPgetStationNum());
  server.handleClient();
  delay(3000);

}
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef APSSID
#define APSSID "MySoftAP"
/*#define APPSK "thereisnospoon"*/
#endif

/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = "mysoftap";
/*const char *password = APPSK;*/

ESP8266WebServer server(80);

/* Just a little test message.  Go to http://192.168.4.1 in a web browser
   connected to this access point to see it.
*/
void handleRoot() {
  server.send(200, "text/html", "<h1>You are connected</h1>");
}

void setup() {
  delay(1000);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password, 1);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

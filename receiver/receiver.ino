#include <ESP8266WiFi.h>
#include <espnow.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
  char msg[32];
  int val;
} struct_message;

// Create a struct_message called myData
struct_message myData;

int prev_time = 0;
int DELAY = 25000;
int curr_time;

#ifndef APSSID
#define APSSID "MySoftAP"
#endif
#ifndef APPWD
#define APPWD "mysoftap"
#endif


//WiFi credentials
//const char* ssid = "n.o.y.b";
//const char* wifi_password = "applesamsung123";
//const char* ssid = "snsriramaLab";
//const char* wifi_password = "Cloud&Smart";
const char* ssid = "JioFi4_0E75A8";
const char* wifi_password = "jio12345";

// MQTT parameters
//const char* mqtt_server = "192.168.0.103";
//const char* mqtt_server = "192.168.0.132";
const char* mqtt_server = "192.168.225.25";
const char* mqtt_topic = "motion_detection";
const char* mqtt_username = "user";
const char* mqtt_password = "pwd";
const char* clientID = "ESPClient";

// Initializes the wifiClient and the PubSubClient
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient);


// Callback function that will be executed when data is received
void OnDataRecv(uint8_t * mac, uint8_t *incomingData, uint8_t len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.println("ESP_NOW msg rcvd");
  Serial.println(myData.val);
  Serial.println(myData.msg);
  if (client.publish(mqtt_topic, myData.msg)) {
    Serial.println("Message sent via MQTT!");
  }
  Serial.println("");
}

void wifi_connect() {
  
  //Connect to wifi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  
  client.setServer(mqtt_server, 1883);

  // Connect to MQTT Broker
  if (client.connect( clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Connecting to WiFi for MQTT
  wifi_connect();

  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // register for recv CB to get recv packer info
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);

}

void loop() {
  curr_time = millis();

  if ((curr_time - prev_time) > DELAY) {
    ESP.restart();
    prev_time = curr_time;
  }
}

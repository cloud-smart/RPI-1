#include <ESP8266WiFi.h>
#include <espnow.h>

// REPLACE WITH RECEIVER MAC Address
uint8_t broadcastAddress[] = {0xE8, 0xDB, 0x84, 0xE0, 0x46, 0x35};

// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
  char msg[32];
  int val;
} struct_message;

struct_message myData;

//Declare variables
int prev_time = 0;
int curr_time;
const int DELAY = 3000;
const int THRESHOLD = 900;

// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  if (sendStatus == 0){
    Serial.println("Delivery success");
  }
  else {
    Serial.println("Delivery fail");
  }
}
 
void setup() {
  Serial.begin(115200);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  Serial.println(WiFi.macAddress());
  
  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, 
  //we will register for Send CB to get the status of Trasnmitted packet
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

  pinMode(D0, OUTPUT);
}
 
void loop() {  
  
  curr_time = millis();

  if ((curr_time - prev_time) > DELAY) {
    if(analogRead(A0) >= THRESHOLD) {
      
      strcpy(myData.msg, "Sender 1");
      myData.val = analogRead(A0);
      
      Serial.println(myData.val);

      digitalWrite(D0, HIGH); 
      
      esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
    }
    else {
      digitalWrite(D0, LOW);
    }
    prev_time = millis();
  }
}

/*
  vgc: WaterStation
*/

#include <WiFi.h>
#include <PubSubClient.h>

#define PUMP_PIN 18
#define DEVICE_TOPIC "canteiroA/WaterStation"

const char* ssid = "<WifiName>";
const char* password = "<WifiPwd>";
const char* mqtt_server = "<BrokerIpAddress>";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

boolean pump_on = false;



void setup() {
  Serial.begin(115200);
  Serial.println("starting device...");
  delay(500);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN,HIGH);
  
  Serial.println("Finished setup");
  delay(1000);
}

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
  if(String(topic) == DEVICE_TOPIC){
    Serial.println("Work Work");
    if(messageTemp == "pump/on"){
      pump_on = true;
      digitalWrite(PUMP_PIN,LOW);
      client.publish("canteiroA/WaterStation/pump", "ON");
    }else if(messageTemp == "pump/off"){
      pump_on = false;
      digitalWrite(PUMP_PIN,HIGH);
      client.publish("canteiroA/WaterStation/pump", "OFF");
    }else if(messageTemp == "pump/status"){
      char pump_status[8];
      dtostrf(pump_on, 1, 2, pump_status);
      client.publish("canteiroA/WaterStation/pump", pump_status);
    }
    

  }
}

void reconnect(){
  while(!client.connected()){
    Serial.print("Attempting MQTT connection...");
    if(client.connect("WaterStation")) {
      Serial.println("connected");
      client.subscribe(DEVICE_TOPIC);
    }else{
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if(!client.connected()){
    reconnect();
  }
  client.loop();
  
  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    //client.publish("canteiroA/EnvTracker/Soilhum", humString);
  }
}

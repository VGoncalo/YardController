/*
  vgc: EnvTrackerBotV2
  This device gathers sensor readings and sends msm to mqtt broker
    [ToDo]: get battery lvl and notify rpi on threshold
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DFROBOT_PWD 23
#define SOILHUM_PIN 32
#define DHT_PIN 4
#define LUMENS_PIN 34
#define DHTTYPE DHT11
#define DEVICE_TOPIC "canteiroA/EnvTracker"

#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP_DAY  1800 
#define TIME_TO_SLEEP_NIGHT  3600
RTC_DATA_ATTR int bootCount = 0;

const char* ssid = "<WifiName>";
const char* password = "<WifiPwd>";
const char* mqtt_server = "<BrokerIpAddress>";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

int soil_hum = 0;
int lumens = 0;
float dht_humidity = 0.00;
float dht_temperature = 0.00;
boolean isNight = false;

DHT dht(DHT_PIN, DHTTYPE);


void getSensorReadings(){
  digitalWrite(DFROBOT_PWD,HIGH);
  delay(500);

  // Capacitor SoilHumidity Sensor
  soil_hum = analogRead(SOILHUM_PIN);
  char humString[8];
  dtostrf(soil_hum, 1, 2, humString);
  client.publish("canteiroA/EnvTracker/soilhum", humString);
  delay(250);

  // DHT11 Sensor
  float dht_humidity = dht.readHumidity();
  char dhthumString[8];
  dtostrf(dht_humidity, 1, 2, dhthumString);
  client.publish("canteiroA/EnvTracker/airhum", dhthumString);
  float dht_temperature = dht.readTemperature();
  char dhttempString[8];
  dtostrf(dht_temperature, 1, 2, dhttempString);
  client.publish("canteiroA/EnvTracker/airtemp", dhttempString);
  delay(250);

  // Lumens Sensor
  lumens = analogRead(LUMENS_PIN);
  char lumsString[8];
  dtostrf(lumens, 1, 2, lumsString);
  client.publish("canteiroA/EnvTracker/lums", humString);
  if(lumens < 250){
    isNight = true;
  }else{
    isNight = false;
  }
  delay(250);
  
  digitalWrite(DFROBOT_PWD,LOW);
}

void setup() {
  ++bootCount;
  
  pinMode(DFROBOT_PWD,OUTPUT);
  pinMode(SOILHUM_PIN,INPUT);
  pinMode(DHT_PIN,INPUT);
  pinMode(LUMENS_PIN,INPUT);
  delay(500);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  
  if(isNight){
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP_NIGHT * uS_TO_S_FACTOR);
  }else{
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP_DAY * uS_TO_S_FACTOR);  
  }
  
  dht.begin();
  
  delay(500);
}

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("EnvTracker")) {
      client.subscribe(DEVICE_TOPIC);
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if(!client.connected()){
    reconnect();
  }
  client.loop();

  getSensorReadings();

  Serial.flush();
  esp_deep_sleep_start();
}

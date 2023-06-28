#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define TEMPERATURE_PUBLISHING_PERIOD 60 //seconds
#define HUMIDITY_PUBLISHING_PERIOD 60 //seconds
#define MIDDLE_DELAY 30 //seconds
#define DHTPIN 2     // Digital pin connected to the DHT sensor 

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
//#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)

// WiFi
const char *ssid = "MIWIFI_sCXc"; // Enter your WiFi name
const char *password = "dteQNyhF";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.1.108"; // Enter your WiFi or Ethernet IP
const int mqtt_port = 1883;
const char *tem_topic = "home/room/T";
const char *hum_topic = "home/room/H";
const char *tem_err_topic = "home/room/T/error";
const char *hum_err_topic = "home/room/H/error";

WiFiClient espClient;
PubSubClient client(espClient);

DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

int timer = 0;
void callback(char *topic, byte *payload, unsigned int length) {
 Serial.print("Message arrived in topic: ");
 Serial.println(topic);
 Serial.print("Message:");
 
 for (int i = 0; i < length; i++) {
  Serial.print((char) payload[i]);
 }
 
 Serial.println();
 Serial.println(" - - - - - - - - - - - -");
}

void setup() {
  // DHT setup
  sensor_t sensor;
  dht.begin();
  delayMS = sensor.min_delay / 1000;
  
 // Set software serial baud to 115200;
 Serial.begin(115200);
 
 // connecting to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.println("Connecting to WiFi..");
 }
 
 Serial.println("Connected to the WiFi network");
 
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 
 while (!client.connected()) {
 String client_id = "esp8266-client-";
 client_id += String(WiFi.macAddress());
 
 Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
 if (client.connect(client_id.c_str())) {
  Serial.println("Public emqx mqtt broker connected");
 } else {
  Serial.print("failed with state ");
  Serial.print(client.state());
  delay(2000);
 }
}
 
 // publish and subscribe
 //client.publish(topic, "Hello From ESP8266!\n");
}

void loop() {
 char *message_pub = "";
 // Get temperature event and print its value.
 sensors_event_t event;
 
 if((timer % (TEMPERATURE_PUBLISHING_PERIOD)) == 0){
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
    client.publish(tem_err_topic, "Error reading temperature!");
  }
  else 
  {
   //float T = 25 + random(-5,5);
   float T = -1;
   bool check = true;
   while(check){
    T = event.temperature;
    if (T >= 0 && T <= 60 )
    check = false;
   }
   
   String message = String(T);
   message.toCharArray(message_pub, message.length());
   client.publish(tem_topic, message_pub);
   Serial.print(tem_topic);
   Serial.print(": ");
   Serial.println(T);
  
   message_pub = "\0";
  }
 }
 if(((timer - MIDDLE_DELAY) % HUMIDITY_PUBLISHING_PERIOD) == 0){
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
    client.publish(hum_err_topic, "Error reading humidity!");
  }
  else {
   float H = -1;
   bool check = true;
   while(check){
    H = event.temperature;
    if (H >= 0 && H <= 100 )
    check = false;
   }
  
   String message = String(H);
   message.toCharArray(message_pub, message.length());
   client.publish(hum_topic, message_pub);
   Serial.print(hum_topic);
   Serial.print(": ");
   Serial.println(H);
  
   message_pub = "\0";
  }
 }
 timer += 5;
 delay(5000);
 client.loop();
}

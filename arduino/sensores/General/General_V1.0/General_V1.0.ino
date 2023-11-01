#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define TEMPERATURE_PUBLISHING_PERIOD 30 //seconds
#define HUMIDITY_PUBLISHING_PERIOD 30 //seconds

// WiFi
const char *ssid = "MIWIFI_sCXc_rt"; // Enter your WiFi name
const char *password = "dteQNyhF";  // Enter WiFi password
// MQTT Broker
const char *mqtt_broker = "192.168.1.108"; // Enter your WiFi or Ethernet IP
const int mqtt_port = 1883;
const char *tem_topic = "home/kitchen/T";
const char *hum_topic = "home/kitchen/H";

WiFiClient espClient;
PubSubClient client(espClient);

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
 
 if((timer % (TEMPERATURE_PUBLISHING_PERIOD)) == 0){
  float T = 25 + random(-5,5);
  
  String message = String(T);
  message.toCharArray(message_pub, message.length());
  client.publish(tem_topic, message_pub);
  Serial.print(tem_topic);
  Serial.print(": ");
  Serial.println(T);
  
  message_pub = "\0";
 }

 if(((timer - 10) % HUMIDITY_PUBLISHING_PERIOD) == 0){
  float H = 50 + random(-10,10);
  
  String message = String(H);
  message.toCharArray(message_pub, message.length());
  client.publish(hum_topic, message_pub);
  Serial.print(hum_topic);
  Serial.print(": ");
  Serial.println(H);
  
  message_pub = "\0";
 }

 timer += 5;
 delay(5000);
 client.loop();
}

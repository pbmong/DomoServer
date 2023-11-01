#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define RELE_PIN    0
#define SUB_REFRESH 2*60*1000 //ms

// WiFi
const char *ssid = "MIWIFI_sCXc_rt"; // Enter your WiFi name
const char *password = "dteQNyhF";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.1.187"; // Enter your WiFi or Ethernet IP
const char *topic = "home/bedroom/R";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long initMillis = millis();

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");

  String message;
  
  for (int i = 0; i < length; i++) {
    message.concat(((char) payload[i]));
  }
 
 Serial.println(message);
 Serial.println(" - - - - - - - - - - - -");

 if(message == "OFF"){
   Serial.println("Rele turned on");
   digitalWrite(RELE_PIN, HIGH);
 }
 else if(message == "ON"){
   Serial.println("Rele turned off");
   digitalWrite(RELE_PIN, LOW);
 }
}


void setup() {
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, LOW);
  
  // Set software serial baud to 115200;
  Serial.begin(115200);
 
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
  send_subscription(topic);
}


void loop() {
 
 client.loop();
 if(!client.connected()){
   send_subscription(topic);
 }
 delay(1000);
}

void send_subscription(const char *topic){
  
  if(WiFi.status() != WL_CONNECTED){
    //WiFi.close();
  
    // connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
    }
  
    Serial.println("Connected to the WiFi network");
  }
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  
  client.subscribe(topic);
 
  return;
}

void send_publish(const char *topic, char *message_pub){
  
  if(WiFi.status() != WL_CONNECTED){
    //WiFi.close();
  
    // connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
    }
  
    Serial.println("Connected to the WiFi network");
  }
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  
  client.publish(topic, message_pub);
  client.disconnect();
  
  return;
}

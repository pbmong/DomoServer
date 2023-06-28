#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <DHT.h>

#define TEMPERATURE_PUBLISHING_PERIOD 60 //seconds
#define HUMIDITY_PUBLISHING_PERIOD 60 //seconds
#define MIDDLE_DELAY 30 //seconds
#define MAX_RETRIES 5 // maximum number of retries
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
const char *err_topic = "home/room/T/error";

WiFiClient espClient;
PubSubClient client(espClient);

DHT dht(DHTPIN, DHTTYPE);

String message = "\0";
int timer = 0;
float T, prev_T = -1;

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
  dht.begin();
  
  // Set software serial baud to 115200;
  Serial.begin(115200);
 
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
 
}

void loop() {
  char *message_pub = "";
  
  if((timer % (TEMPERATURE_PUBLISHING_PERIOD)) == 0){

    bool check = true;
    T = dht.readTemperature();

    if (prev_T == -1)
      prev_T = T;
    if (!isnan(T)){
      send_publish(err_topic, "T has nan value");
    }else if (())
    else if ((!isnan(T)) &&(T >= 0) && (T <= 60) && (abs(T - prev_T) < 5))
      check = false;

    message = String(T);
    if(check){
      message.toCharArray(message_pub, message.length());
      Serial.println(message);
      send_publish(err_topic, message_pub);
    }else{
      message.toCharArray(message_pub, message.length());
      send_publish(tem_topic, message_pub);
      Serial.print(tem_topic);
      Serial.print(": ");
      Serial.println(T);
      
      prev_T = T;
    }

    message_pub = "\0";
    message = "\0";
  }
 
  timer += 5;
  delay(5000);
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

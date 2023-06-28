#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "DHTesp.h"

#define PUBLISHING_PERIOD 600 //seconds
#define DHTPIN 2     // Digital pin connected to the DHT sensor 

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
//#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)

// WiFi
const char *ssid = "MIWIFI_sCXc"; // Enter your WiFi name
const char *password = "dteQNyhF";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.1.187"; // Enter your WiFi or Ethernet IP
const int mqtt_port = 1883;
const char *tem_topic = "home/bedroom/T";
const char *hum_topic = "home/bedroom/H";
const char *tem_err_topic = "home/bedroom/T/error";
const char *hum_err_topic = "home/bedroom/H/error";

WiFiClient espClient;
PubSubClient client(espClient);

//DHT dht(DHTPIN, DHTTYPE);
DHTesp dht;

String message = "\0";
int timer = 0;
float T, H, prev_H = -1, prev_T = -1;

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
  pinMode(DHTPIN, INPUT);
  dht.setup(DHTPIN, DHTesp::DHT11); //Connect DHT11 sensor to GPIO 2
  delay(100);

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
  char *message_pub_T = "";
  bool check = true;

  T = dht.getTemperature();

  if (prev_T == -1)
    prev_T = T;
  if (isnan(T)) {
    send_publish(tem_err_topic, "T has nan value");
  }
  if ((!isnan(T)) && (T >= 0) && (T <= 60) && (abs(T - prev_T) < 5)) {
    message = String(T);
    message.toCharArray(message_pub_T, message.length());
    send_publish(tem_topic, message_pub_T);
    Serial.print(tem_topic);
    Serial.print(": ");
    Serial.println(T);

    prev_T = T;
  }
  else {
    message = String(T);
    message.toCharArray(message_pub_T, message.length());
    Serial.println(message);
    send_publish(tem_err_topic, message_pub_T);
  }

  message = "\0";

  char *message_pub_H = "";
  H = dht.getHumidity();

  if (prev_H == -1)
    prev_H = H;
  if (isnan(H)) {
    send_publish(hum_err_topic, "H has nan value");
  }
  if ((!isnan(H)) && (H >= 0) && (H <= 100) && (abs(H - prev_H) < 20)) {
    message = String(H);
    message.toCharArray(message_pub_H, message.length());
    send_publish(hum_topic, message_pub_H);
    Serial.print(hum_topic);
    Serial.print(": ");
    Serial.println(H);

    prev_H = H;
  }
  else {
    message = String(H);
    message.toCharArray(message_pub_H, message.length());
    Serial.println(message);
    send_publish(hum_err_topic, message_pub_H);
  }

  message = "\0";

  delay(PUBLISHING_PERIOD * 1000);
}

void send_publish(const char *topic, char *message_pub) {

  if (WiFi.status() != WL_CONNECTED) {
    //WiFi.close();

    // connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
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
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }

  client.publish(topic, message_pub);
  client.disconnect();

  return;
}

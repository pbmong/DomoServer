/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-cam-post-image-photo-server/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <Arduino.h>
#include <WiFi.h>  
#include <NTPClient.h> //For request date and time
#include <WiFiUdp.h>
#include <PubSubClient.h>

#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_camera.h"

#include "FS.h"                // SD Card ESP32
#include "SD_MMC.h"            // SD Card ESP32
#include <EEPROM.h>            // read and write from flash memory

// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define FLASH_GPIO_NUM    4
// Photos configuration
#define PHOTOS_NUM        5
#define PHOTOS_DELAY      5000  //miliseconds

// Wifi
#define TCP_TIMEOUT       20000  //miliseconds

//SD
#define EEPROM_SIZE 1

//Wifi
const char* ssid = "MIWIFI_sCXc_rt";
const char* password = "dteQNyhF";

//MQTT
char* mqtt_server = "192.168.1.187";
const int mqtt_port = 1883;
const char *cam_topic = "home/bedroom/C";
const char *pir_topic = "home/bedroom/P";
WiFiClient espClient;
PubSubClient mqtt_client(espClient);

//HTTP post
const String serverName = "192.168.1.187";   // REPLACE WITH YOUR Raspberry Pi IP ADDRESS
const int serverPort = 80;
const String serverPath = "/Domo/php/upload_photo.php";     // The default serverPath should be upload.php
const String file_name = "bedroom_C_";
WiFiClient client;

//UTC Time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", (3600*2), 60000);

//Camera config
camera_config_t config;

const int timerInterval = 30000;    // time between each HTTP POST image
unsigned long previousMillis = 0;   // last time image was sent
bool camera_flag = false;
int pictureNumber = 0;

void callback(char *topic, byte *payload, unsigned int length) {
 Serial.print("Message arrived in topic: ");
 Serial.println(topic);
 Serial.print("Message:");

 for (int i = 0; i < length; i++) {
  Serial.print((char) payload[i]);
 }
 
 String message;
  
 for (int i = 0; i < length; i++) {
   message.concat(((char) payload[i]));
 }
 Serial.println();
 Serial.println(" - - - - - - - - - - - -");
 if(message == "REQ")
    camera_flag = true;
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("ESP32-CAM IP Address: ");
  Serial.println(WiFi.localIP());

  initMemoryCard();
  initCamera();
  timeClient.begin();
  timeClient.update();
    
  takePhoto("test_file_"); 
  send_publish(cam_topic, "ACK");
  send_subscription(cam_topic);
}

void loop() {
  if (camera_flag) {
    camera_flag = false;
    for(int i = 0; i < PHOTOS_NUM; i++){
      unsigned long initMillis = millis();
      sendPhoto(file_name);
      while (millis() - initMillis < PHOTOS_DELAY) {
        //mqtt_client.loop();
      }
  }
    send_publish(cam_topic, "ACK");
    send_subscription(cam_topic);
  }

  mqtt_client.loop();
}

void takePhoto(String file_name){
  camera_fb_t * fb = NULL;
  
  // Take Picture with Camera
  fb = esp_camera_fb_get();  
  if(!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  // initialize EEPROM with predefined size
  EEPROM.begin(EEPROM_SIZE);
  pictureNumber = EEPROM.read(0) + 1;
  
  // Path where new picture will be saved in SD Card
  String path = "/picture" + String(pictureNumber) +".jpg";

  fs::FS &fs = SD_MMC; 
  Serial.printf("Picture file name: %s\n", path.c_str());
  
  File file = fs.open(path.c_str(), FILE_WRITE);
  if(!file){
    Serial.println("Failed to open file in writing mode");
  } 
  else {
    file.write(fb->buf, fb->len); // payload (image), payload length
    Serial.printf("Saved file to path: %s\n", path.c_str());
    EEPROM.write(0, pictureNumber);
    EEPROM.commit();
  }
  file.close();
  esp_camera_fb_return(fb); 
  return;
}

String sendPhoto(String file) {
  mqtt_client.disconnect();
  camera_fb_t * fb = NULL;
  // Take Picture with Camera
  fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("FB Camera capture failed");
    delay(1000);
    ESP.restart();
  }
  
  unsigned long initMillis = millis();
  while (millis() - initMillis < 200) {
    //mqtt_client.loop();
  }
  
  String getAll;
  String getBody;
  
  Serial.println("Connecting to server: " + serverName);
  client.setTimeout(TCP_TIMEOUT);
  if (client.connect(serverName.c_str(), serverPort)) {
    
    Serial.println("Connection successful!");    
    String head = "--RandomNerdTutorials\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"" + file + timeClient.getFormattedTime()+".jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
    String tail = "\r\n--RandomNerdTutorials--\r\n";

    uint32_t imageLen = fb->len;
    uint32_t extraLen = head.length() + tail.length();
    uint32_t totalLen = imageLen + extraLen;
  
    client.println("POST " + serverPath + " HTTP/1.1");
    client.println("Host: " + serverName);
    client.println("Content-Length: " + String(totalLen));
    client.println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
    client.println();
    client.print(head);
  
    uint8_t *fbBuf = fb->buf;
    size_t fbLen = fb->len;
    for (size_t n=0; n<fbLen; n=n+1024) {
      if (n+1024 < fbLen) {
        client.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen%1024>0) {
        size_t remainder = fbLen%1024;
        client.write(fbBuf, remainder);
      }
    }   
    client.print(tail);
    
    int timoutTimer = 10000;
    long startTimer = millis();
    boolean state = false;

    Serial.println("Listening response...");
    while ((startTimer + timoutTimer) > millis()) {
      Serial.print(".");
      delay(100);      
      while (client.available()) {
        char c = client.read();
        if (c == '\n') {
          if (getAll.length()==0) { state=true; }
          getAll = "";
        } 
        else if (c != '\r') { getAll += String(c); }
        if (state==true) { getBody += String(c); }
        startTimer = millis();
      }
      if (getBody.length()>0) { break; }
    }
    Serial.println();
    client.stop();
    Serial.println(getBody);
  }
  else {
    getBody = "Connection to " + serverName +  " failed.";
    Serial.println(getBody);
  }
  
  esp_camera_fb_return(fb);
  return getBody;
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
  mqtt_client.setServer(mqtt_server, mqtt_port);
  mqtt_client.setCallback(callback);
  
  while (!mqtt_client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (mqtt_client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.println(mqtt_client.state());
      delay(2000);
    }
  }
  
  mqtt_client.subscribe(topic);
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
  mqtt_client.setServer(mqtt_server, mqtt_port);
  mqtt_client.setCallback(callback);
  
  while (!mqtt_client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (mqtt_client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.println(mqtt_client.state());
      delay(2000);
    }
  }
  
  mqtt_client.publish(topic, message_pub);
  mqtt_client.disconnect();
  
  return;
}
  

void initCamera() {
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  
  config.pixel_format = PIXFORMAT_JPEG; 
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  
  config.frame_size = FRAMESIZE_UXGA;
  config.jpeg_quality = 64;
  config.fb_count = 2;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    delay(1000);
    ESP.restart();
  } 
}

void initMemoryCard(){
  //Serial.println("Starting SD Card");
  if(!SD_MMC.begin()){
    Serial.println("SD Card Mount Failed");
    return;
  }
  
  uint8_t cardType = SD_MMC.cardType();
  if(cardType == CARD_NONE){
    Serial.println("No SD Card attached");
    return;
  }
    
  return;
}

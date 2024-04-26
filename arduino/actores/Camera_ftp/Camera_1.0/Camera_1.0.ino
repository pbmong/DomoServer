#include "esp_camera.h"
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"
#include "time.h"

#include <WiFi.h>
#include <WiFiClient.h>   
#include <NTPClient.h> //For request date and time
#include <WiFiUdp.h>
#include <PubSubClient.h>
#include "ESP32_FTPClient.h"

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
#define PHOTOS_NUM        1
#define PHOTOS_DELAY      5000 //miliseconds
#define ALARM_DELAY       30000 //milisends

//Wifi
const char* ssid = "MIWIFI_sCXc_rt";
const char* password = "dteQNyhF";
const char* server = "192.168.1.187";

//HTTP post
const String serverName = "192.168.1.187";
const int serverPort = 80;
const String serverPath = "/Domo/php/upload_photo.php";

//FTP
char* ftp_user = "pi";
char* ftp_pass = "raspberry";
char* ftp_path = "/Downloads";
String file_name = "bedroom_C_";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", (3600*2), 60000);
//ESP32_FTPClient ftp (server,ftp_user,ftp_pass, 5000, 2);

//MQTT
const int mqtt_port = 1883;
const char *cam_topic = "home/bedroom/C";
const char *pir_topic = "home/bedroom/P";
WiFiClient espClient;
PubSubClient client(espClient);

camera_config_t config;
bool camera_flag = false;

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
 if(message == "ON")
    camera_flag = true;
 if(message == "OFF")
    camera_flag = false;
}

void setup() {
  //PIR setup
  pinMode(GPIO_NUM_13, INPUT);
  
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
  Serial.begin(115200);

  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
  
  //INIT FLASH PIN
  pinMode(FLASH_GPIO_NUM, OUTPUT);
  digitalWrite(FLASH_GPIO_NUM, LOW);
  initCamera();
  timeClient.begin();
  timeClient.update();
  
  //ftp.OpenConnection();
  
  //takePhoto("test_file_");
  
  send_publish(cam_topic, "ACK");
  
  send_subscription(cam_topic);
}

void loop() {
  bool pir = digitalRead(GPIO_NUM_13);
  Serial.println(pir);
  
  if (camera_flag && pir) {
    send_publish(cam_topic, "DET");
    
    unsigned long alarm_initMillis = millis();
    for(int i = 0; i < PHOTOS_NUM; i++){
      unsigned long photo_initMillis = millis();
      takePhoto(file_name);
      while (millis() - photo_initMillis < PHOTOS_DELAY) {
        client.loop();
      }
  }
    send_publish(cam_topic, "ACK");
  
    while (millis() - alarm_initMillis < ALARM_DELAY) {
        client.loop();
      }
    send_subscription(cam_topic);
  }

  client.loop();
}

void takePhoto(String file) {
  camera_fb_t * fb = NULL;
  // Take Picture with Camera
  fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("FB Camera capture failed");
    delay(1000);
    ESP.restart();
  }
  camera_fb_t * fb1 = NULL;
  // Take Picture with Camera
  fb1 = esp_camera_fb_get();
  if(!fb1) {
    Serial.println("FB aux Camera capture failed");
    delay(1000);
    ESP.restart();
  }
  
  unsigned long initMillis = millis();
  while (millis() - initMillis < 200) {
    client.loop();
  }
  /*
   * Upload to http post server
   */
  String getAll;
  String getBody;

  Serial.println("Connecting to server: " + serverName);
  String head = "--RandomNerdTutorials\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"" + file+timeClient.getFormattedTime()+".jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
  String tail = "\r\n--RandomNerdTutorials--\r\n";

  uint32_t imageLen = fb->len;
  uint32_t extraLen = head.length() + tail.length();
  uint32_t totalLen = imageLen + extraLen;
  
  Serial.println("POST " + serverPath + " HTTP/1.1");
  Serial.println("Host: " + serverName);
  Serial.println("Content-Length: " + String(totalLen));
  Serial.println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
  Serial.println();
  Serial.print(head);
    
  if (espClient.connect(serverName.c_str(), serverPort)) {
    Serial.println("Connection successful!");    
    
    espClient.println("POST " + serverPath + " HTTP/1.1");
    espClient.println("Host: " + serverName);
    espClient.println("Content-Length: " + String(totalLen));
    espClient.println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
    espClient.println();
    espClient.print(head);
  
    uint8_t *fbBuf = fb->buf;
    size_t fbLen = fb->len;
    for (size_t n=0; n<fbLen; n=n+1024) {
      if (n+1024 < fbLen) {
        espClient.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen%1024>0) {
        size_t remainder = fbLen%1024;
        espClient.write(fbBuf, remainder);
      }
    }   
    espClient.print(tail);
    
    int timoutTimer = 10000;
    long startTimer = millis();
    boolean state = false;
    
    while ((startTimer + timoutTimer) > millis()) {
      Serial.print(".");
      delay(100);      
      while (espClient.available()) {
        char c = espClient.read();
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
    espClient.stop();
    Serial.println(getBody);
  }
  else {
    getBody = "Connection to " + serverName +  " failed.";
    Serial.println(getBody);
  }
    
    /*
     * Free buffer
     */
    esp_camera_fb_return(fb); 
    esp_camera_fb_return(fb1); 

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
  client.setServer(server, mqtt_port);
  client.setCallback(callback);
  
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.println(client.state());
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
  client.setServer(server, mqtt_port);
  client.setCallback(callback);
  
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
 
    Serial.printf("The client %s connects to mosquitto mqtt broker\n", client_id.c_str());
 
    if (client.connect(client_id.c_str())) {
      Serial.println("Public emqx mqtt broker connected");
    }else {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  
  client.publish(topic, message_pub);
  //client.disconnect();
  
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

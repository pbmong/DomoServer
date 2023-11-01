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

#include "FS.h"                // SD Card ESP32
#include "SD_MMC.h"            // SD Card ESP32
//#include <EEPROM.h>            // read and write from flash memory

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
//SD
#define EEPROM_SIZE 1
// Photos configuration
#define PHOTOS_NUM        10
#define PHOTOS_DELAY      2*1000//miliseconds

//Wifi
const char* ssid = "MIWIFI_sCXc_rt";
const char* password = "dteQNyhF";
char* server = "192.168.1.187";

//FTP
char* ftp_user = "pi";
char* ftp_pass = "raspberry";
char* ftp_path = "/Downloads";
char* file_name = "/bedroom_C_";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", (3600*2), 60000);
ESP32_FTPClient ftp (server,ftp_user,ftp_pass, 5000, 2);

//MQTT
const int mqtt_port = 1883;
const char *cam_topic = "home/bedroom/C";
const char *pir_topic = "home/bedroom/P";
WiFiClient espClient;
PubSubClient client(espClient);

camera_config_t config;
String  SD_files[PHOTOS_NUM];
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
  //digitalWrite(GPIO_NUM_13, LOW);
  
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
  
  initMemoryCard();
  
  String file_path = takePhoto(SD_MMC,"/test_file_");
  sendPhoto(SD_MMC, file_path);
  send_publish(cam_topic, "ACK");
  
  send_subscription(cam_topic);
}

void loop() {
  bool pir = digitalRead(GPIO_NUM_13);
  //Serial.println(pir);
  
  if (camera_flag && pir == false){
    send_publish(cam_topic, "DET");

    //Take photos
    for(int i = 0; i < PHOTOS_NUM; i++){
      unsigned long initMillis = millis();
      SD_files[i] = takePhoto(SD_MMC, file_name);
      while (millis() - initMillis < PHOTOS_DELAY) {
         client.loop();
      }
    }

    //Send photos
    for(int i = 0; i < PHOTOS_NUM; i++){
      sendPhoto(SD_MMC, SD_files[i]);
      client.loop();
    }
    
    send_publish(cam_topic, "ACK");
    send_subscription(cam_topic);
  }

  client.loop();
}

String takePhoto(fs::FS& fs, String file_name){
  camera_fb_t * fb = NULL;
  
  // Take Picture with Camera
  fb = esp_camera_fb_get();  
  if(!fb) {
    Serial.println("Camera capture failed");
    return "Camera error";
  }
  // initialize EEPROM with predefined size
  //EEPROM.begin(EEPROM_SIZE);
  
  // Path where new picture will be saved in SD Card
  String date = timeClient.getFormattedTime();
  date.replace(":","-");
  String path = file_name + date + ".jpg";

  Serial.printf("Picture file name: %s\n", path.c_str());
  
  File file = fs.open(path.c_str(), FILE_WRITE);
  if(!file){
    Serial.println("Failed to open file in writing mode");
  } 
  else {
    file.write(fb->buf, fb->len); // payload (image), payload length
    Serial.printf("Saved file to path: %s\n", path.c_str());
    //EEPROM.write(0, pictureNumber);
    //EEPROM.commit();
  }
  file.close();
  esp_camera_fb_return(fb); 
  return path;
}

void sendPhoto(fs::FS& fs, String file) {
  String file_sd_path = file;
  file.replace("/","");
  unsigned long initMillis = millis();
  
  /*
   * Upload to ftp server
   */
  ftp.OpenConnection();
  ftp.ChangeWorkDir(ftp_path);
  ftp.InitFile("Type I");
  
  Serial.println("Subiendo "+file);
  int str_len = file.length() + 1; 
  char char_array[str_len];
  file.toCharArray(char_array, str_len);
  ftp.NewFile(char_array);
  
  //ftp.WriteData( fb->buf, fb->len );
  File photo = fs.open(file_sd_path);
  if (!photo) {
      Serial.println("Failed to open file for reading");
      return;
  }
  while (photo.available()) {
      // Create and fill a buffer
      unsigned char buf[1024];
      int readVal = photo.read(buf, sizeof(buf));
      ftp.WriteData(buf,sizeof(buf));
  }
  photo.close();
  
  ftp.CloseFile();
  ftp.CloseConnection();

  return;
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
  config.jpeg_quality = 32;
  config.fb_count = 2;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    delay(1000);
    ESP.restart();
  } 
}

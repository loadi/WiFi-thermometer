#include <ESP8266WiFi.h>
#include "DHT.h"
#include <ESP8266HTTPClient.h>
#define DHTTYPE DHT11

const char* ssid = "MyWiFi";            // SSID
const char* password = "password";     // password
const int sleep = 300;                // timeout 
uint8_t DHTPin = D5;                 // DHT pin
const char* HOST = "domain.ru";     // hostname

DHT dht(DHTPin, DHTTYPE);                
float temperature;
float humidity;

void setup(){
  pinMode(DHTPin, INPUT);
  dht.begin();
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
  }
}

void loop(){
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  sendData(temperature, humidity);
  delay(sleep * 1000);
}

void sendData(float t, float h){  
  WiFiClient client;
  if (!client.connect(HOST, 80)){
    return;
  }
  
  String data = "temp=" + String(t) + "&hum=" + String(h);
  client.println("POST /addData HTTP/1.1");
  client.println("Host: " + String(HOST));
  client.println("Accept: */*");
  client.println("Connection: close");
  client.println("Content-Type: application/x-www-form-urlencoded");
  client.print("Content-Length: ");
  client.println(data.length());
  client.println();
  client.print(data);
  delay(500);
  if (client.connected()){ 
    client.stop();
  }
}

 

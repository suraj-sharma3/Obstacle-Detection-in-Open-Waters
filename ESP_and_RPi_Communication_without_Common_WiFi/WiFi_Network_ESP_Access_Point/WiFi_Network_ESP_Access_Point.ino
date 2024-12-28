#include <WiFi.h>

// Define the WiFi network name (SSID) and password
const char* ssid = "ESP32_Swimmer_Network";  // Replace with your desired network name
const char* password = "12345678";           // Replace with your desired password

void setup() {
  // Start Serial Monitor
  Serial.begin(115200);

  // Start the ESP32 in Access Point mode
  WiFi.softAP(ssid, password);

  // Get the ESP32's IP address
  IPAddress IP = WiFi.softAPIP();
  Serial.println("WiFi Access Point Started");
  Serial.print("SSID: ");
  Serial.println(ssid);
  Serial.print("Password: ");
  Serial.println(password);
  Serial.print("Access Point IP Address: ");
  Serial.println(IP);
}

void loop() {
  // Keep the program running
}

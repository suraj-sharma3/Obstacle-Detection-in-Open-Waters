#include <WiFi.h>

// Define the SSID and Password for the Access Point
const char* ssid = "ESP32_Access_Point";  // Customize your SSID
const char* password = "12345678";        // Minimum 8 characters

void setup() {
  // Start Serial Monitor
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("Initializing Access Point...");
  
  // Start the Access Point
  if (WiFi.softAP(ssid, password)) {
    Serial.println("Access Point started successfully.");
  } else {
    Serial.println("Failed to start Access Point.");
    return;  // Stop here if the AP setup failed
  }

  // Wait a moment for the AP to initialize
  delay(2000);

  // Print the IP address of the Access Point
  IPAddress IP = WiFi.softAPIP();
  Serial.print("Access Point IP Address: ");
  Serial.println(IP);
}

void loop() {
  // Nothing is needed in the loop for this example
}

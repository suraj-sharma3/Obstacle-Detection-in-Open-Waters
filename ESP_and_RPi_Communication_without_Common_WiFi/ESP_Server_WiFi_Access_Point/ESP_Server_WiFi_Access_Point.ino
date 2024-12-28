#include <WiFi.h>

// WiFi network credentials
const char* ssid = "ESP32_Swimmer_Network";
const char* password = "12345678";

WiFiServer server(80); // Create a server on port 80 (HTTP)

void setup() {
  Serial.begin(115200);

  // Start the Access Point
  WiFi.softAP(ssid, password);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");

  // Print Access Point details
  Serial.print("Access Point IP Address: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client Connected");
    String request = client.readStringUntil('\r'); // Read the client's request
    Serial.println(request);
    client.flush();

    // Respond to the client
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<h1>ESP32 Access Point</h1>");
    client.println("<p>Your message was received!</p>");
    delay(10);

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected");
  }
}

#include <WiFi.h>

// WiFi network credentials
const char* ssid = "ESP32_Swimmer_Network";
const char* password = "12345678";

WiFiServer server(80); // Create a server on port 80 (HTTP)

// Define the pin for the haptic motor
const int motorPin = 5; // Change this pin as per your ESP32 wiring

void setup() {
  Serial.begin(115200);

  // Configure the motor pin as output
  pinMode(motorPin, OUTPUT);
  digitalWrite(motorPin, LOW); // Ensure the motor is off at the start

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

    // Read the client's request
    String request = client.readStringUntil('\r');
    Serial.println("Received Request: " + request);
    client.flush();

    // Check if the received string is "vibrate"
    if (request.indexOf("vibrate") >= 0) {
      Serial.println("Command: Vibrate");
      vibrateMotor();
    } else {
      Serial.println("Command: No action");
    }

    // Respond to the client
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<h1>ESP32 Access Point</h1>");
    client.println("<p>Your command was received!</p>");
    delay(10);

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected");
  }
}

// Function to vibrate the motor twice
void vibrateMotor() {
  for (int i = 0; i < 2; i++) {
    digitalWrite(motorPin, HIGH); // Turn the motor on
    delay(500);                   // Vibrate for 500 ms
    digitalWrite(motorPin, LOW);  // Turn the motor off
    delay(500);                   // Pause for 500 ms
  }
}

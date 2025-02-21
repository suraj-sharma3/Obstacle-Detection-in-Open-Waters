#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "LAPTOP-2FKFHUU1 2914";
const char* password = "09U37x=2";
const char* mqtt_server = "test.mosquitto.org";

const int vibrationMotorPin = 5;  // GPIO pin for the motor

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Received message on topic '");
  Serial.print(topic);
  Serial.print("': ");
  Serial.println(message);  // Print received message

  if (message == "right") {
    Serial.println("Vibrating Right Wristband!");  // Print Vibrate action
    digitalWrite(vibrationMotorPin, HIGH);
    delay(500);  // Vibrate for 500ms
    digitalWrite(vibrationMotorPin, LOW);
  }
}

void setup() {
  Serial.begin(115200);  // Initialize Serial Monitor
  pinMode(vibrationMotorPin, OUTPUT);
  digitalWrite(vibrationMotorPin, LOW);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(1000);
  }
  Serial.println("Connected to WiFi!");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32_Right")) {
      Serial.println("Connected to MQTT!");
      client.subscribe("swim/movement");  // Subscribe to topic
      Serial.println("Subscribed to swim/movement");
    } else {
      Serial.println("Failed to connect. Retrying...");
      delay(5000);
    }
  }
}

void loop() {
  client.loop();  // Keep checking for messages
}

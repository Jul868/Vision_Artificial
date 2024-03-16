#include <WiFi.h>
#include <ESP32Servo.h>
const char* ssid = "Motorola";  // Reemplaza esto por tu SSID
const char* password = "Qwe12345";  // Reemplaza esto por tu contraseña de WiFi

WiFiServer server(502);  // Crea un servidor que escuche en el puerto 502

Servo myservo;

void setup() {
  myservo.attach(5);  // El pin al que está conectado el servo
  Serial.begin(115200);

  // Conectar a la red WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado");
  Serial.print("Direccion IP: ");
  Serial.println(WiFi.localIP());

  // Inicia el servidor
  server.begin();
}

void loop() {
  WiFiClient client = server.available();  // Escucha a los clientes entrantes

  if (client) {
    Serial.println("Cliente conectado");
    while (client.connected()) {
      if (client.available() > 0) {
        int degrees = client.parseInt();  // Lee el grado enviado desde Python
        Serial.print("Grados recibidos: ");
        Serial.println(degrees);
        if (degrees >= 0 && degrees <= 180) {  // Verifica que esté en el rango permitido
          myservo.write(degrees);  // Mueve el servo a la posición indicada
          // Enviar confirmación al cliente
          client.println("Movimiento del servo completado");
          Serial.println("Movimiento del servo realizado");
        }
        myservo.write(0);
      }
    }
    // Cierra la conexión fuera del bucle while(client.connected())
    Serial.println("Cliente desconectado");
    myservo.write(0);
    client.stop();
  }
}

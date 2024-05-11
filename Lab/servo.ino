#include <WiFi.h>
#include <ESP32Servo.h>

// Datos de conexión WiFi
const char* ssid = "Motorola";  // Reemplaza esto por tu SSID de red
const char* password = "Qwe12345";  // Reemplaza esto por tu contraseña de WiFi

// Configuración del servidor WiFi en el puerto 502
WiFiServer server(502);

// Creación del objeto servo
Servo myservo;

void setup() {
  // Configura el pin del servo
  myservo.attach(33);

  // Inicialización del puerto serie para depuración
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
  // Escucha conexiones entrantes
  WiFiClient client = server.available();

  // Inicializa el servo a la posición cero
  myservo.write(0);

  if (client) {  // Si hay un cliente conectado
    Serial.println("Cliente conectado");
    while (client.connected()) {
      if (client.available() > 0) {
        int degrees = client.parseInt();  // Lee el grado enviado desde Python
        Serial.print("Grados recibidos: ");
        Serial.println(degrees);

        // Verifica que el grado esté en el rango permitido
        if (degrees >= 0 && degrees <= 180) {
          myservo.write(degrees);  // Mueve el servo a la posición indicada
          client.println("Movimiento del servo completado");  // Enviar confirmación al cliente
          Serial.println("Movimiento del servo realizado");
          delay(1000);
        }

        // Retorna el servo a la posición inicial (opcional)
        myservo.write(0);
      }
    }
    // Desconexión del cliente
    Serial.println("Cliente desconectado");
    client.stop();
  }
}

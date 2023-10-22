import http.server
import socketserver
import requests
import json

API_KEY = "4e02f39241345f4554632c35141a9e85"
port = 9089

# Función para obtener datos meteorológicos
def obtener_datos_metereologicos(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            condiciones_climaticas = {"ciudad": data["name"], "clima": data["weather"][0]["description"], "temperatura": data["main"]["temp"] - 273.15}
            return condiciones_climaticas
        else:
            return "No disponible"
    except Exception as e:
        return f"Error: {str(e)}"

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/weather/'):
            ciudad = self.path[9:]
            resultado = obtener_datos_metereologicos(ciudad)
            if resultado == "No disponible":
                self.send_response(404)
                self.end_headers() 
            else:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resultado).encode())  
        else:
            super().do_GET()


# Configuración del servidor
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Servidor web en el puerto {port} para OpenWeather")
    httpd.serve_forever()
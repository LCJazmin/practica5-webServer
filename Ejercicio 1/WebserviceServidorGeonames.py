import http.server
import socketserver
import requests
import json

USERNAME = "lcjazmin_"
port = 9089

def obtener_informacion_ubicacion(lugar):
    url = f"http://api.geonames.org/searchJSON?name={lugar}&maxRows=1&username={USERNAME}"
    try:
        response = requests.get(url)
        data = response.json()
        if "geonames" in data and data["totalResultsCount"] > 0:
            ubicacion = {"name": data["geonames"][0]["name"], "pais": data["geonames"][0]["countryName"], "code": data["geonames"][0]["countryCode"], 'poblacion': data["geonames"][0]["population"]} 
            return ubicacion
        else:           
            return "No disponible"
    except Exception as e:
        print(f"Error: {str(e)}")

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/geonames/'):
            lugar = self.path[9:]
            resultado = obtener_informacion_ubicacion(lugar)
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
    print(f"Servidor web en el puerto {port} para Geonames")
    httpd.serve_forever()
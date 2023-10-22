import http.server
import socketserver
import requests
import json

port = 8888

def obtener_informacion_geografica(lugar):
    USERNAME = "lcjazmin_"
    url = f"http://api.geonames.org/searchJSON?name={lugar}&maxRows=1&username={USERNAME}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["totalResultsCount"] > 0:
            if "geonames" in data:
                #return f"<br>Nombre: {data['name']}<br>País: {data['countryName']} [{data['countryCode']}]<br>"
                return {"name": data["geonames"][0]["name"], "pais": data["geonames"][0]["countryName"], "codPais": data["geonames"][0]["countryCode"]}
        else:           
            return "No disponible"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "No disponible"
    
def obtener_datos_metereologicos(ciudad):
    API_KEY = "4e02f39241345f4554632c35141a9e85"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            #return f"Clima: {data['weather'][0]['description']}<br>Temperatura: {(data['main']['temp'] - 273.15):.2f}"
            return {"ciudad": data["name"], "clima": data["weather"][0]["description"], "temperatura": data["main"]["temp"] - 273.15}
        else:
            return "No disponible"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "No disponible"
            
def get_token():
    client_id = '19806827be2e4bddacf5097324edd3b8'; # Your client id
    client_secret = '908323da77d54008b9697d7bc7193c61'; # Your secret
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token

def obtener_listas_reproduccion(codPais):
    access_token = get_token()
    url = f"https://api.spotify.com/v1/browse/featured-playlists?country={codPais}"
    try:
        response = requests.get(url, headers = {'Authorization': 'Bearer {token}'.format(token = access_token)})
        data = response.json()
        total = data['playlists']['limit']
        if total > 0:
            listas = []
            for i in range(0,total):
                listas.append({'nombre': data['playlists']['items'][i]['name'],
                               'URL': data['playlists']['items'][i]['external_urls']['spotify'],
                               'canciones': data['playlists']['items'][i]['tracks']['total']})
            return {"total": total, "listas": listas}
        else:           
            return "No disponible"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "No disponible"

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location','/APIWebIntegrado.html')
            self.end_headers()
        elif self.path.startswith('/integrado/'):
            lugar = self.path[11:]
            info_lugar = obtener_informacion_geografica(lugar)
            if info_lugar == "No disponible":
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(info_lugar).encode())
            else:
                info_clima = obtener_datos_metereologicos(info_lugar["name"])
                info_listas = obtener_listas_reproduccion(info_lugar["codPais"])
                resultado = {"lugar": info_lugar, "clima": info_clima, "listas_reproduccion": info_listas}
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(resultado).encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Servidor web en el puerto {port} para Geonames-Weather-Spotify")
    httpd.serve_forever()
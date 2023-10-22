import http.server
import socketserver
import requests
import json

port = 9090

def get_token():
    client_id = '19806827be2e4bddacf5097324edd3b8'; # Your client id
    client_secret = '908323da77d54008b9697d7bc7193c61'; # Your secret
    redirect_uri = f"http://localhost:{port}/"
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token

def obtener_listas(codPais):
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
            return {'total': total, 'listas': listas}
        else:           
            return "No disponible"
    except Exception as e:
        print(f"Error: {str(e)}")

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/spotify/'):
            codPais = self.path[9:]
            resultado = obtener_listas(codPais)
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
    print(f"Servidor web en el puerto {port} para Spotify")
    httpd.serve_forever()
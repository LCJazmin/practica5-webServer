import requests

# URL del servidor web (asegúrate de que la dirección y el puerto coincidan)
url_base = 'http://localhost:9089'

def obtener_informacion(lugar):
    url = f'{url_base}/geonames/{lugar}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f'\nLugar: {data["name"]}\nPaís: {data["pais"]} [{ data["code"]}]\nPoblación: {data["poblacion"]}\n'
    elif response.status_code == 404:
        return f'\nUbicacón no encontrada'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

# Ejemplos de uso
lugar = input("Lugar: ")
resultado = obtener_informacion(lugar)
print(resultado)
    

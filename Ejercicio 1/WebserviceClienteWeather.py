import requests

# URL del servidor web (asegúrate de que la dirección y el puerto coincidan)
url_base = 'http://localhost:9089'

def obtener_clima(ciudad):
    url = f'{url_base}/weather/{ciudad}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f'Clima: {data["clima"]}\nTemperatura: {data["temperatura"]:.2f} °C\n'
    elif response.status_code == 404:
        return f'Ubicacón no encontrada'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

# Ejemplos de uso
ciudad = input("Ciudad: ")
resultado = obtener_clima(ciudad)
print(resultado)
    

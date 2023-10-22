import requests

# URL del servidor web (asegúrate de que la dirección y el puerto coincidan)
url_base = 'http://localhost:9090'
    
def obtener_listas(codPais):
    url = f'{url_base}/spotify/{codPais}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data #f'Nombre: {data["nombre"]}\n: {data["canciones"]}\nURL: {data["URL"]}\n'
    elif response.status_code == 404:
        return f'Ubicacón no encontrada'
    else:
        return f'Error en la solicitud: Código {response.status_code}'

# Ejemplos de uso
codPais = input("Código de País: ")
resultado = obtener_listas(codPais)
total = resultado["total"]
for i in range(0, total):
    print(f"Lista {i+1} - {resultado['listas'][i]['nombre']} - {resultado['listas'][i]['canciones']} canciones - URL: {resultado['listas'][i]['URL']}")

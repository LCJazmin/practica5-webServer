import requests

# URL del servidor web (asegúrate de que la dirección y el puerto coincidan)
url_base = 'http://localhost:9090'

def obtener_informacion(lugar):  
    url = f'{url_base}/integrado/{lugar}'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return 1
    else:
        return f'Error en la solicitud: Código {response.status_code}'

# Ejemplos de uso
lugar = input("Lugar: ")
info = obtener_informacion(lugar)
if info != 1:
    print(f'\nLugar: {info["lugar"]["name"]}\nPaís: {info["lugar"]["pais"]} [{info["lugar"]["codPais"]}]')
    if info["clima"] == "No disponible":
        print("No se obtuvieron datos metereológicos.")
    else:
        print(f'Clima: {info["clima"]["clima"]}\nTemperatura: {info["clima"]["temperatura"]:.2f} °C\n')
    if info["listas_reproduccion"] == "No disponible":
            print("No se obtuvieron listas de reproducción.")
    else:
        print(f'Listas de reproducción populares del país: {info["listas_reproduccion"]["total"]}')
        for i in range(0,info["listas_reproduccion"]["total"]):
            print(f'{i+1}) {info["listas_reproduccion"]["listas"][i]["nombre"]} - {info["listas_reproduccion"]["listas"][i]["canciones"]} canciones - URL: {info["listas_reproduccion"]["listas"][i]["URL"]}')

else:
    print(f"\nNo se obtuvieron datos para {lugar}.")
from flask import Flask, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# --- Configuración de la App Flask y API ---
app = Flask(__name__)
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATIONSTACK_BASE_URL = "http://api.aviationstack.com/v1/flights"
CHECKWX_API_KEY = os.getenv("CHECKWX_API_KEY")
CHECKWX_BASE_URL = "https://api.checkwx.com/metar"

def obtener_datos_vuelo_api(numero_vuelo):
    """
    Función que se conecta a AviationStack. Es la misma lógica de buscar_vuelo.py,
    pero preparada para ser usada por el servidor web.
    """
    if not AVIATIONSTACK_API_KEY:
        return {"error": "Clave de API de AviationStack no encontrada."}

    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'flight_iata': numero_vuelo,
        'limit': 1
    }

    try:
        response = requests.get(AVIATIONSTACK_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and data["data"]:
            return data["data"][0]
        else:
            return {"error": f"No se encontraron datos para el vuelo {numero_vuelo}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error al conectar con la API externa: {e}"}

def obtener_metar_api(icao_code):
    """
    Obtiene el reporte METAR para un código de aeropuerto ICAO dado.
    """
    if not CHECKWX_API_KEY:
        return {"error": "Clave de API de CheckWX no encontrada."}
    
    headers = {'X-API-Key': CHECKWX_API_KEY}
    url = f"{CHECKWX_BASE_URL}/{icao_code}/decoded"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("data") and data["data"]:
            return data["data"][0]
        else:
            return {"error": f"No se encontraron datos METAR para {icao_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al conectar con la API de CheckWX: {e}"}

# --- Ruta para servir la página principal ---
@app.route('/')
def index():
    """
    Esta ruta sirve el archivo index.html que se encuentra en la carpeta 'templates'.
    """
    return render_template('index.html')


# --- Definición de la Ruta de la API ---
@app.route('/api/flight/<string:flight_number>', methods=['GET'])
def get_flight_data(flight_number):
    """
    Este es el endpoint de nuestra API. Cuando se llama a una URL como
    http://127.0.0.1:5000/api/flight/IBE6848, esta función se ejecuta.
    """
    print(f"Recibida petición para el vuelo: {flight_number}")
    datos_vuelo = obtener_datos_vuelo_api(flight_number)
    
    if "error" in datos_vuelo:
        return jsonify(datos_vuelo), 500

    # Obtener datos METAR
    departure_icao = datos_vuelo.get('departure', {}).get('icao')
    arrival_icao = datos_vuelo.get('arrival', {}).get('icao')

    metar_data = {}
    if departure_icao:
        metar_data['departure'] = obtener_metar_api(departure_icao)
    if arrival_icao:
        metar_data['arrival'] = obtener_metar_api(arrival_icao)

    # Combinar todos los datos
    response_data = {
        'flight': datos_vuelo,
        'metar': metar_data
    }

    return jsonify(response_data)

# --- Punto de Entrada para Ejecutar el Servidor ---
if __name__ == '__main__':
    # app.run() inicia el servidor. 
    # debug=True hace que el servidor se reinicie automáticamente cuando cambiamos el código.
    app.run(debug=True)
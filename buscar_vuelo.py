import os
import requests
import json
import argparse
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# --- Configuración de APIs ---
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATIONSTACK_BASE_URL = "http://api.aviationstack.com/v1/flights"
OPENSKY_BASE_URL = "https://opensky-network.org/api/states/all"

def obtener_datos_vuelo_aviationstack(flight_iata=None, dep_iata=None, arr_iata=None, flight_date=None):
    """
    Consulta la API de AviationStack para obtener los datos generales de un vuelo.
    """
    print("--- Buscando datos generales en AviationStack... ---")
    if not AVIATIONSTACK_API_KEY:
        print("Error: Clave de API de AviationStack no encontrada.")
        return None

    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'limit': 1
    }

    if flight_iata: 
        params['flight_iata'] = flight_iata
    if dep_iata:
        params['dep_iata'] = dep_iata
    if arr_iata:
        params['arr_iata'] = arr_iata
    if flight_date:
        params['flight_date'] = flight_date

    if not (flight_iata or dep_iata or arr_iata or flight_date):
        print("Error: Debes proporcionar al menos un parámetro de búsqueda (ej. --flight, --departure, --arrival, --date).")
        return None

    try:
        response = requests.get(AVIATIONSTACK_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and data["data"]:
            print("¡Datos generales encontrados en AviationStack!")
            return data["data"][0]
        else:
            print(f"\nError: No se encontraron datos generales para la búsqueda realizada en AviationStack.\nRespuesta de la API: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con AviationStack: {e}")
        return None

def obtener_telemetria_opensky(icao24):
    """
    Obtiene la telemetría en vivo de OpenSky Network para un ICAO24 específico.
    """
    print(f"\n--- Buscando telemetría en vivo para ICAO24 {icao24} en OpenSky Network... ---")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(OPENSKY_BASE_URL, headers=headers)
        # OpenSky devuelve 200 incluso si no hay datos, pero puede dar 403 si bloquea la IP/User-Agent
        response.raise_for_status() 
        data = response.json()

        if data.get("states"):
            for state in data["states"]:
                if state[0] == icao24: # state[0] es el icao24 en la respuesta de OpenSky
                    print("¡Telemetría en vivo encontrada en OpenSky!")
                    return {
                        "latitude": state[6],
                        "longitude": state[5],
                        "baro_altitude_meters": state[7],
                        "velocity_mps": state[9],
                        "true_track_degrees": state[10],
                        "vertical_rate_mps": state[11],
                        "on_ground": state[8],
                    }
            print(f"No se encontró telemetría en vivo para ICAO24 {icao24} en la lista actual de OpenSky.")
            return None
        else:
            print("No se recibieron estados de aviones de OpenSky Network.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con OpenSky Network: {e}")
        return None

def mostrar_info_vuelo(datos):
    """
    Procesa y muestra la información del vuelo de forma clara en la terminal.
    """
    if not datos:
        return

    # Función auxiliar para mostrar datos o "No disponible"
    def get(data, key, default="No disponible"):
        return data.get(key) if data and data.get(key) else default

    # --- Información General ---
    flight = get(datos, 'flight')
    airline = get(datos, 'airline')
    status = get(datos, 'flight_status', 'Desconocido').capitalize()
    print(f"\n✈️  Resumen del Vuelo {get(flight, 'iata')} - {get(airline, 'name')} | Estado: {status}")
    print("----------------------------------------------------------")

    # --- Salida ---
    departure = get(datos, 'departure')
    print(f"🛫 Salida:")
    print(f"    Aeropuerto: {get(departure, 'airport')}")
    print(f"    Terminal: {get(departure, 'terminal')} | Puerta: {get(departure, 'gate')}")
    print(f"    Hora Programada: {get(departure, 'scheduled').replace('T', ' ').replace('+00:00', ' UTC')}")
    print(f"    Hora Estimada:   {get(departure, 'estimated').replace('T', ' ').replace('+00:00', ' UTC')}")

    # --- Llegada ---
    arrival = get(datos, 'arrival')
    print(f"\n🛬 Llegada:")
    print(f"    Aeropuerto: {get(arrival, 'airport')}")
    print(f"    Terminal: {get(arrival, 'terminal')} | Puerta: {get(arrival, 'gate')}")
    print(f"    Recogida Equipaje: {get(arrival, 'baggage')}")
    print(f"    Hora Programada: {get(arrival, 'scheduled').replace('T', ' ').replace('+00:00', ' UTC')}")
    print(f"    Hora Estimada:   {get(arrival, 'estimated').replace('T', ' ').replace('+00:00', ' UTC')}")

    # --- Posicionamiento en Vivo (OpenSky) ---
    live_telemetry = get(datos, 'live_telemetry_opensky')
    if live_telemetry != "No disponible":
        print(f"\n🛰️  Datos de Posicionamiento en Vivo (OpenSky):")
        print(f"    Latitud: {get(live_telemetry, 'latitude')} | Longitud: {get(live_telemetry, 'longitude')}")
        print(f"    Altitud: {get(live_telemetry, 'baro_altitude_meters')} metros")
        print(f"    Velocidad: {round(get(live_telemetry, 'velocity_mps', 0) * 3.6, 2)} km/h") # Convertir m/s a km/h
    else:
        print("\n🛰️  Datos de Posicionamiento en Vivo (OpenSky): No disponibles (el vuelo puede no estar en el aire o no tener datos en vivo en OpenSky)")
    
    print("----------------------------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rastreador de vuelos Aeris.')
    parser.add_argument('--flight', type=str, help='Número de vuelo (ej. AA1)')
    parser.add_argument('--departure', type=str, help='Código IATA del aeropuerto de salida (ej. JFK)')
    parser.add_argument('--arrival', type=str, help='Código IATA del aeropuerto de llegada (ej. LAX)')
    parser.add_argument('--date', type=str, help='Fecha del vuelo en formato YYYY-MM-DD (ej. 2025-07-11)')

    args = parser.parse_args()

    # Obtener datos generales de AviationStack
    datos_generales = obtener_datos_vuelo_aviationstack(
        flight_iata=args.flight,
        dep_iata=args.departure,
        arr_iata=args.arrival,
        flight_date=args.date
    )

    datos_completos = datos_generales # Inicializamos con los datos generales

    if datos_generales and datos_generales.get('aircraft') and datos_generales['aircraft'].get('icao24'):
        icao24 = datos_generales['aircraft']['icao24']
        telemetria_opensky = obtener_telemetria_opensky(icao24)
        if telemetria_opensky:
            datos_completos["live_telemetry_opensky"] = telemetria_opensky
    
    mostrar_info_vuelo(datos_completos)
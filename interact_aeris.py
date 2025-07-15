import subprocess
import os
from datetime import datetime

def run_search(flight=None, departure=None, arrival=None, date=None):
    """
    Ejecuta buscar_vuelo.py con los argumentos proporcionados y captura su salida.
    """
    command = ["python", "buscar_vuelo.py"]
    if flight: 
        command.extend(["--flight", flight])
    if departure: 
        command.extend(["--departure", departure])
    if arrival: 
        command.extend(["--arrival", arrival])
    if date: 
        command.extend(["--date", date])

    # Configurar la codificación para la salida de la consola en Windows
    # Esto es crucial para que subprocess.run decodifique correctamente la salida
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'

    try:
        # Ejecutar el comando y capturar la salida, forzando la codificación UTF-8
        result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', env=env)
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "Error: Asegúrate de que Python está en tu PATH y buscar_vuelo.py existe.", ""
    except Exception as e:
        return f"Error inesperado al ejecutar el script: {e}", ""

def get_flight_date():
    """
    Permite al usuario seleccionar la fecha del vuelo, usar la fecha de hoy, o no especificarla.
    Devuelve la fecha en formato YYYY-MM-DD o None si no se especifica.
    """
    while True:
        print("\n--- Seleccionar Fecha ---")
        print("1. Fecha de hoy")
        print("2. Introducir fecha manualmente (DD-MM-AAAA)")
        print("3. No especificar fecha (solo para vuelos activos)")
        choice = input("Elige una opción (1-3): ").strip()

        if choice == '1':
            return datetime.now().strftime("%Y-%m-%d")
        elif choice == '2':
            while True:
                date_str = input("Introduce la fecha (DD-MM-AAAA): ").strip()
                try:
                    # Convertir de DD-MM-AAAA a YYYY-MM-DD
                    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
                except ValueError:
                    print("Formato de fecha incorrecto. Usa DD-MM-AAAA.")
        elif choice == '3':
            return None
        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")

def main():
    print("\n--- Rastreador de Vuelos Aeris ---")
    
    while True:
        flight_date = get_flight_date()
        if flight_date:
            print(f"Fecha seleccionada: {flight_date}")
        else:
            print("No se especificará la fecha de búsqueda.")

        print("\n--- Tipo de Búsqueda ---")
        print("1. Buscar por número de vuelo")
        print("2. Buscar por aeropuertos de salida y llegada")
        search_type = input("Elige una opción (1-2): ").strip()

        args = {}
        if flight_date: # Solo añadir la fecha si se ha especificado
            args['date'] = flight_date

        valid_input = False

        if search_type == '1':
            flight_num = input("Número de vuelo (ej. AA1): ").strip()
            if flight_num:
                args['flight'] = flight_num
                valid_input = True
            else:
                print("El número de vuelo no puede estar vacío.")
        elif search_type == '2':
            dep_airport = input("Código IATA aeropuerto de salida (ej. JFK): ").strip()
            arr_airport = input("Código IATA aeropuerto de llegada (ej. LAX): ").strip()
            if dep_airport and arr_airport:
                args['departure'] = dep_airport
                args['arrival'] = arr_airport
                valid_input = True
            else:
                print("Debes introducir ambos códigos IATA de aeropuerto.")
        else:
            print("Opción no válida. Por favor, elige 1 o 2.")
        
        if not valid_input:
            continue # Volver al inicio del bucle para elegir tipo de búsqueda

        stdout, stderr = run_search(**args)

        print("\n--- Resultado de la Búsqueda ---")
        # Asegurarse de que stdout no es None antes de imprimir o buscar en él
        if stdout:
            print(stdout)
        else:
            print("No se recibió ninguna salida del script de búsqueda.")

        if stderr:
            print("--- Errores (stderr) ---")
            print(stderr)

        # Comprobar si se encontraron datos (buscando una cadena específica en la salida)
        # Asegurarse de que stdout no es None antes de buscar en él
        if stdout and "¡Datos generales encontrados en AviationStack!" in stdout and "Error: No se encontraron datos" not in stdout:
            print("\nBúsqueda completada con éxito.")
            break # Salir del bucle si se encontraron datos
        else:
            retry = input("No se encontraron datos o hubo un error. ¿Quieres intentarlo de nuevo? (s/n): ").lower()
            if retry != 's':
                break

if __name__ == "__main__":
    # Configurar la página de códigos para la consola en Windows
    os.system("chcp 65001")
    main()
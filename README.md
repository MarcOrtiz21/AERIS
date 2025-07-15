# Aeris Flight Tracker

**Aeris** is a simple yet powerful flight tracking application. It provides real-time flight status, departure and arrival information, and live telemetry data. The project consists of a command-line interface (CLI) to fetch and display flight data, and a web interface to visualize it.

## Features

- **Flight Search:** Look up flights using flight number, departure airport, or arrival airport.
- **Real-Time Status:** Get up-to-date information on flight status (e.g., scheduled, en-route, landed).
- **Detailed Information:** Access details such as departure/arrival times, terminals, gates, and baggage claim information.
- **Live Telemetry:** For flights that are currently in the air, Aeris can provide live telemetry data including:
    - Latitude and Longitude
    - Altitude
    - Speed
    - True Track
    - Vertical Rate
- **METAR Weather Reports:** Get weather reports for both departure and arrival airports.
- **Web Interface:** A simple and clean web interface to easily search for and visualize flight data.

## How It Works

Aeris integrates with multiple APIs to gather comprehensive flight information:

- **AviationStack:** Used to get general flight data, including schedules, airport information, and flight status.
- **OpenSky Network:** Provides live telemetry data for airborne flights.
- **CheckWX:** Used to fetch METAR (Meteorological Aerodrome Report) weather data for airports.

## Project Structure

```
/
├── .env                # Environment variables (API keys)
├── .gitignore          # Git ignore file
├── app.py              # Flask web server
├── buscar_vuelo.py     # Command-line flight search tool
├── interact_aeris.py   # Interactive CLI script
├── Procfile            # For deployment (e.g., Heroku)
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── run_aeris.bat       # Batch script to run the application
├── static/
│   ├── script.js       # JavaScript for the web interface
│   └── style.css       # CSS for the web interface
└── templates/
    └── index.html      # HTML for the web interface
```

## Getting Started

### Prerequisites

- Python 3.x
- An internet connection

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/aeris.git
   cd aeris
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API keys:**
   - Create a `.env` file in the root of the project.
   - Add your API keys to the `.env` file:
     ```
     AVIATIONSTACK_API_KEY="your_aviationstack_api_key"
     CHECKWX_API_KEY="your_checkwx_api_key"
     ```
   - You can get your API keys from:
     - [AviationStack](https://aviationstack.com/)
     - [CheckWX](https://www.checkwx.com/api)

### Usage

#### Command-Line Interface (CLI)

You can use `buscar_vuelo.py` to search for flights directly from your terminal.

**Examples:**

- **Search by flight number:**
  ```bash
  python buscar_vuelo.py --flight IBE6848
  ```

- **Search by departure and arrival airports:**
  ```bash
  python buscar_vuelo.py --departure MAD --arrival JFK
  ```

- **Search by flight number and date:**
  ```bash
  python buscar_vuelo.py --flight UAL901 --date 2025-07-15
  ```

#### Web Interface

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and go to:**
   ```
   http://127.0.0.1:5000
   ```

3. **Enter a flight number in the search box and click "Search".**

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.


# Aeris Flight Tracker

**Aeris** es una aplicación de seguimiento de vuelos simple pero potente. Proporciona estado de vuelos en tiempo real, información de salidas y llegadas, y datos de telemetría en vivo. El proyecto consta de una interfaz de línea de comandos (CLI) para obtener y mostrar datos de vuelos, y una interfaz web para visualizarlos.

## Características

- **Búsqueda de Vuelos:** Busca vuelos por número de vuelo, aeropuerto de salida o aeropuerto de llegada.
- **Estado en Tiempo Real:** Obtén información actualizada sobre el estado de los vuelos (p. ej., programado, en ruta, aterrizado).
- **Información Detallada:** Accede a detalles como horarios de salida/llegada, terminales, puertas de embarque e información de recogida de equipaje.
- **Telemetría en Vivo:** Para vuelos que están actualmente en el aire, Aeris puede proporcionar datos de telemetría en vivo, incluyendo:
    - Latitud y Longitud
    - Altitud
    - Velocidad
    - Rumbo Verdadero
    - Tasa de Ascenso/Descenso
- **Informes Meteorológicos METAR:** Obtén informes meteorológicos para los aeropuertos de salida y llegada.
- **Interfaz Web:** Una interfaz web simple y limpia para buscar y visualizar fácilmente los datos de los vuelos.

## Cómo Funciona

Aeris se integra con múltiples APIs para recopilar información completa sobre los vuelos:

- **AviationStack:** Se utiliza para obtener datos generales de los vuelos, incluyendo horarios, información de aeropuertos y estado de los vuelos.
- **OpenSky Network:** Proporciona datos de telemetría en vivo para vuelos en el aire.
- **CheckWX:** Se utiliza para obtener datos meteorológicos METAR (Meteorological Aerodrome Report) para los aeropuertos.

## Estructura del Proyecto

```
/
├── .env                # Variables de entorno (claves de API)
├── .gitignore          # Archivo .gitignore
├── app.py              # Servidor web Flask
├── buscar_vuelo.py     # Herramienta de búsqueda de vuelos por línea de comandos
├── interact_aeris.py   # Script interactivo de la CLI
├── Procfile            # Para despliegue (p. ej., Heroku)
├── README.md           # Este archivo
├── requirements.txt    # Dependencias de Python
├── run_aeris.bat       # Script para ejecutar la aplicación
├── static/
│   ├── script.js       # JavaScript para la interfaz web
│   └── style.css       # CSS para la interfaz web
└── templates/
    └── index.html      # HTML para la interfaz web
```

## Cómo Empezar

### Prerrequisitos

- Python 3.x
- Una conexión a internet

### Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/aeris.git
   cd aeris
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura tus claves de API:**
   - Crea un archivo `.env` en la raíz del proyecto.
   - Añade tus claves de API al archivo `.env`:
     ```
     AVIATIONSTACK_API_KEY="tu_clave_de_api_de_aviationstack"
     CHECKWX_API_KEY="tu_clave_de_api_de_checkwx"
     ```
   - Puedes obtener tus claves de API en:
     - [AviationStack](https://aviationstack.com/)
     - [CheckWX](https://www.checkwx.com/api)

### Uso

#### Interfaz de Línea de Comandos (CLI)

Puedes usar `buscar_vuelo.py` para buscar vuelos directamente desde tu terminal.

**Ejemplos:**

- **Buscar por número de vuelo:**
  ```bash
  python buscar_vuelo.py --flight IBE6848
  ```

- **Buscar por aeropuertos de salida y llegada:**
  ```bash
  python buscar_vuelo.py --departure MAD --arrival JFK
  ```

- **Buscar por número de vuelo y fecha:**
  ```bash
  python buscar_vuelo.py --flight UAL901 --date 2025-07-15
  ```

#### Interfaz Web

1. **Inicia el servidor Flask:**
   ```bash
   python app.py
   ```

2. **Abre tu navegador web y ve a:**
   ```
   http://127.0.0.1:5000
   ```

3. **Introduce un número de vuelo en el cuadro de búsqueda y haz clic en "Buscar".**

## Contribuir

¡Las contribuciones son bienvenidas! Si tienes alguna idea, sugerencia o informe de error, por favor abre un "issue" o envía un "pull request".

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

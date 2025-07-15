document.addEventListener('DOMContentLoaded', () => {
    // Elementos de la UI
    const searchButton = document.getElementById('search-button');
    const flightInput = document.getElementById('flight-input');
    const flightInfoContainer = document.getElementById('flight-info');
    const metarInfoContainer = document.getElementById('metar-info');
    const mapContainer = document.getElementById('map');
    const recentSearchesContainer = document.getElementById('recent-searches-container');

    // Estado de la aplicación
    let map = null;
    let marker = null;
    let routeLine = null;
    let recentSearches = [];

    const showLoader = () => {
        flightInfoContainer.innerHTML = '<div class="loader"></div>';
        metarInfoContainer.style.display = 'none';
        mapContainer.style.display = 'none';
    };

    const fetchFlightData = async (flightNumberFromClick) => {
        const flightNumber = flightNumberFromClick || flightInput.value.trim().toUpperCase();
        if (!flightNumber) {
            flightInfoContainer.innerHTML = '<p style="color: red;">Por favor, introduce un número de vuelo.</p>';
            return;
        }

        showLoader();

        try {
            const response = await fetch(`/api/flight/${flightNumber}`);
            const data = await response.json();

            if (response.ok && data.flight && !data.flight.error) {
                saveRecentSearch(flightNumber);
                displayFlightInfo(data.flight);
                displayMetarInfo(data.metar);
                updateMap(data.flight);
            } else {
                flightInfoContainer.innerHTML = `<p style="color: red;">Error: ${data.flight.error || 'No se encontraron datos.'}</p>`;
            }
        } catch (error) {
            flightInfoContainer.innerHTML = `<p style="color: red;">Error de conexión. Inténtalo de nuevo más tarde.</p>`;
            console.error("Error en la petición fetch:", error);
        }
    };

    const displayFlightInfo = (data) => {
        const { departure, arrival, airline, flight, flight_status } = data;
        const infoHtml = `
            <h3>Vuelo: ${airline.name} (${flight.iata})</h3>
            <p><strong>Estado:</strong> ${flight_status}</p><hr>
            <h4>Salida</h4>
            <p><strong>Aeropuerto:</strong> ${departure.airport} (${departure.iata})</p>
            <p><strong>Hora Programada:</strong> ${new Date(departure.scheduled).toLocaleString()}</p>
            <hr><h4>Llegada</h4>
            <p><strong>Aeropuerto:</strong> ${arrival.airport} (${arrival.iata})</p>
            <p><strong>Hora Programada:</strong> ${new Date(arrival.scheduled).toLocaleString()}</p>
        `;
        flightInfoContainer.innerHTML = infoHtml;
    };

    const displayMetarInfo = (metarData) => {
        if (!metarData || (!metarData.departure && !metarData.arrival)) {
            metarInfoContainer.style.display = 'none';
            return;
        }
        metarInfoContainer.style.display = 'block';
        let metarHtml = '<h3>Información Meteorológica (METAR)</h3>';
        const formatMetar = (metar, type) => {
            if (!metar || metar.error) return `<p>No hay datos METAR para el aeropuerto de ${type}.</p>`;
            return `<h4>Aeropuerto de ${type} (${metar.icao})</h4>
                    <p><strong>Viento:</strong> ${metar.wind.degrees}° a ${metar.wind.speed_kts} nudos</p>
                    <p><strong>Visibilidad:</strong> ${metar.visibility.meters} m</p>
                    <p><strong>Temperatura:</strong> ${metar.temperature.celsius}°C</p>`;
        };
        metarHtml += formatMetar(metarData.departure, 'Salida');
        metarHtml += '<hr>';
        metarHtml += formatMetar(metarData.arrival, 'Llegada');
        metarInfoContainer.innerHTML = metarHtml;
    };

    const updateMap = (flightData) => {
        const { live, departure, arrival } = flightData;
        if (live && typeof live.latitude !== 'undefined') {
            mapContainer.style.display = 'block';
            const lat = live.latitude;
            const lon = live.longitude;
            const bounds = [[lat, lon]];

            if (!map) {
                map = L.map('map').setView([lat, lon], 8);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
                marker = L.marker([lat, lon]).addTo(map);
            } else {
                map.setView([lat, lon]);
                marker.setLatLng([lat, lon]);
            }
            marker.bindPopup(`<b>Vuelo: ${flightData.flight.iata}</b>`).openPopup();

            // Dibujar ruta (si tenemos coordenadas de aeropuertos)
            // NOTA: AviationStack no provee lat/lon de aeropuertos en el endpoint de vuelos.
            // Esta funcionalidad requeriría una llamada extra o una fuente de datos diferente.
            // Por ahora, solo se muestra el avión.

            map.fitBounds(bounds);

        } else {
            mapContainer.style.display = 'none';
        }
    };

    const saveRecentSearch = (flightNumber) => {
        if (!recentSearches.includes(flightNumber)) {
            recentSearches.unshift(flightNumber);
            recentSearches = recentSearches.slice(0, 5); // Guardar solo los 5 más recientes
            localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
            displayRecentSearches();
        }
    };

    const loadRecentSearches = () => {
        const storedSearches = localStorage.getItem('recentSearches');
        if (storedSearches) {
            recentSearches = JSON.parse(storedSearches);
            displayRecentSearches();
        }
    };

    const displayRecentSearches = () => {
        if (recentSearches.length === 0) {
            recentSearchesContainer.style.display = 'none';
            return;
        }
        recentSearchesContainer.style.display = 'block';
        let listHtml = '<h4>Búsquedas Recientes:</h4><ul class="recent-searches-list">';
        recentSearches.forEach(flight => {
            listHtml += `<li class="recent-search-item" data-flight="${flight}">${flight}</li>`;
        });
        listHtml += '</ul>';
        recentSearchesContainer.innerHTML = listHtml;
    };

    const init = () => {
        loadRecentSearches();
        searchButton.addEventListener('click', () => fetchFlightData());
        flightInput.addEventListener('keyup', (e) => e.key === 'Enter' && fetchFlightData());
        recentSearchesContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('recent-search-item')) {
                const flightNumber = e.target.dataset.flight;
                flightInput.value = flightNumber;
                fetchFlightData(flightNumber);
            }
        });
    };

    init();
});

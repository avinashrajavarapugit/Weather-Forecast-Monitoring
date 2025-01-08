document.getElementById('monitor-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const cities = document.getElementById('cities').value.split(',').map(city => city.trim());
    const interval = parseInt(document.getElementById('interval').value);
    const duration = parseInt(document.getElementById('duration').value);

    const response = await fetch(`/start-monitoring`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cities, interval, duration })
    });

    if (response.ok) {
        alert('Monitoring started successfully!');
        fetchWeatherData();
    } else {
        alert('Failed to start monitoring. Please try again.');
    }
});

async function fetchWeatherData(city = '') {
    const response = await fetch(`/weather-data?city=${city}`);
    if (response.ok) {
        const data = await response.json();
        renderCharts(data.data);
    } else {
        console.error('Failed to fetch weather data');
    }
}

function renderCharts(data) {
    const ctxTemp = document.getElementById('temp-chart').getContext('2d');
    const ctxFeelsLike = document.getElementById('feels-like-chart').getContext('2d');
    const ctxWeatherCondition = document.getElementById('weather-condition-chart').getContext('2d');

    const labels = data.map(item => item.date);
    const temps = data.map(item => item.temp);
    const feelsLike = data.map(item => item.feels_like);
    const weatherConditions = data.map(item => item.weather_condition);

    new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperature (°C)',
                data: temps,
                borderColor: 'blue',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Temperature (°C)' } }
            }
        }
    });

    new Chart(ctxFeelsLike, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Feels Like Temperature (°C)',
                data: feelsLike,
                borderColor: 'green',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Temperature (°C)' } }
            }
        }
    });

    new Chart(ctxWeatherCondition, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Weather Condition',
                data: weatherConditions,
                backgroundColor: 'orange',
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Frequency' } }
            }
        }
    });
}

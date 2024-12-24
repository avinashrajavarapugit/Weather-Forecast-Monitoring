import React, { useEffect, useState } from 'react';

const WeatherDashboard = () => {
  const [weatherData, setWeatherData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/weather')
      .then(response => response.json())
      .then(data => setWeatherData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>Weather Data</h1>
      <table>
        <thead>
          <tr>
            <th>City</th>
            <th>Date</th>
            <th>Temperature (°C)</th>
            <th>Condition</th>
            <th>Feels Like (°C)</th>
          </tr>
        </thead>
        <tbody>
          {weatherData.map((row, index) => (
            <tr key={index}>
              <td>{row[1]}</td>
              <td>{row[2]}</td>
              <td>{row[3]}</td>
              <td>{row[4]}</td>
              <td>{row[5]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default WeatherDashboard;



# Weather Monitoring System

# site Link: https://weatherforecastmonitoring.onrender.com/

## Overview

This project monitors and stores weather data for various cities using data from the OpenWeatherMap API. The backend is built with **Python** and **Flask**, while weather data is stored in an **SQLite** database. The project provides an API for retrieving weather data and includes a front-end built using **React** to display the data in a dashboard.

## Features

- **Real-time Weather Data**: Fetches and stores current weather data for multiple cities.
- **API Endpoints**: 
  - `/weather`: Fetches all weather data stored in the database.
  - `/weather/<city>`: Fetches weather data for a specific city.
- **Weather Alerts**: Sends email alerts if the temperature exceeds a threshold for two consecutive intervals.
- **Data Visualization**: Displays temperature trends and weather summaries over time.
- **React Dashboard**: Interactive web dashboard to view weather data.

## Technologies Used

- **Python**: Flask for the backend API.
- **SQLite**: To store weather data.
- **OpenWeatherMap API**: For fetching weather data.
- **React**: For the front-end dashboard.
- **Matplotlib**: For visualizing temperature trends.
- **SMTP (Gmail)**: For sending email alerts.

## Setup Instructions

### 1. Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/weather-monitoring.git
   cd weather-monitoring
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the SQLite database**:
   The database and tables are automatically created when the app runs. No additional setup is needed for the database.

4. **Run the Flask server**:
   ```bash
   python app.py
   ```

   The backend server will be available at `http://localhost:5000`.

### 2. Frontend Setup

1. **Install React dependencies**:
   Navigate to the `frontend` directory and install the necessary dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the React app**:
   ```bash
   npm start
   ```

   The front-end dashboard will be available at `http://localhost:3000`.

### 3. Environment Configuration

- **OpenWeatherMap API Key**: Make sure to replace `API_KEY` in the Python code with your own OpenWeatherMap API key.

- **Email Configuration**: Update the email credentials in the Python code for sending alerts.

## API Endpoints

- **GET `/weather`**: Fetch all weather data.
- **GET `/weather/<city>`**: Fetch weather data for a specific city.

Example response:
```json
[
  {
    "id": 1,
    "city": "Delhi",
    "date": "2024-12-24",
    "temp": 28.5,
    "weather_condition": "Clear",
    "feels_like": 30.0
  }
]
```

## Data Visualization

The backend calculates daily weather summaries (average, max, min temperatures) and visualizes temperature trends using Matplotlib. The React front-end displays the fetched weather data in a table format.

## Email Alerts

Email alerts are sent if the temperature exceeds 35°C for two consecutive updates. This is configured in the `send_email_alert` function.

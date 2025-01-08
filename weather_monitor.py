import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt
from statistics import mean
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Weather (
    id INTEGER PRIMARY KEY,
    city TEXT,
    date TEXT,
    temp REAL,
    weather_condition TEXT,
    feels_like REAL
)
''')

# Save weather data to database
def save_to_db(city, date, temp, weather_condition, feels_like):
    cursor.execute('''
    INSERT INTO Weather (city, date, temp, weather_condition, feels_like)
    VALUES (?, ?, ?, ?, ?)
    ''', (city, date, temp, weather_condition, feels_like))
    conn.commit()

# OpenWeatherMap API key
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# List of cities

# Function to convert Kelvin to Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Function to retrieve weather data from OpenWeatherMap API
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to send alert via email
def send_email_alert(subject, body):
    sender_email = os.getenv('SMTP_EMAIL')
    receiver_email = os.getenv('ALERT_RECEIVER_EMAIL')
    password = os.getenv('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")

# Function to process and store daily weather summary
def process_weather_data(city, data_store, alerts, data):
    alert_threshold = 35
    temp = kelvin_to_celsius(data['main']['temp'])
    weather_condition = data['weather'][0]['main']
    feels_like = kelvin_to_celsius(data['main']['feels_like'])
    timestamp = data['dt']
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

    # Save data to SQLite
    save_to_db(city, date, temp, weather_condition, feels_like)
    
    
    if date not in data_store:
        data_store[date] = {'temps': [], 'weather_conditions': []}
    
    # Append temperature and weather condition to the day's list
    data_store[date]['temps'].append(temp)
    data_store[date]['weather_conditions'].append(weather_condition)
    
    # Check for alert conditions (if temp > 35 for two consecutive intervals)
    if len(alerts[city]) > 0 and temp > alert_threshold and alerts[city][-1]['temp'] > alert_threshold:
        send_email_alert(
            f"Temperature Alert for {city}",
            f"The temperature in {city} exceeded {alert_threshold}°C for two consecutive updates!"
        )
    
    # Store latest weather info for alert tracking
    alerts[city].append({'temp': temp, 'weather_condition': weather_condition})

# Function to calculate daily aggregates (average, max, min temp, dominant weather condition)
def calculate_daily_summary(data_store):
    for date, data in data_store.items():
        avg_temp = mean(data['temps'])
        max_temp = max(data['temps'])
        min_temp = min(data['temps'])
        dominant_weather = max(set(data['weather_conditions']), key=data['weather_conditions'].count)
        
        print(f"Weather Summary for {date}:")
        print(f"Average Temp: {avg_temp:.2f}°C")
        print(f"Max Temp: {max_temp:.2f}°C")
        print(f"Min Temp: {min_temp:.2f}°C")
        print(f"Dominant Weather Condition: {dominant_weather}\n")

# Function to visualize daily temperature trends
def visualize_data(data_store):
    dates = list(data_store.keys())
    avg_temps = [mean(data['temps']) for data in data_store.values()]
    max_temps = [max(data['temps']) for data in data_store.values()]
    min_temps = [min(data['temps']) for data in data_store.values()]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label="Average Temp", marker='o')
    plt.plot(dates, max_temps, label="Max Temp", marker='o')
    plt.plot(dates, min_temps, label="Min Temp", marker='o')
    
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Daily Temperature Trends")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main function to run the system
def run_weather_monitor(interval, duration, CITIES):
    data_store = {}
    alerts = {city: [] for city in CITIES}
    
    start_time = time.time()
    while time.time() - start_time < duration:
        for city in CITIES:
            data = get_weather_data(city)
            if data:
                process_weather_data(city, data_store, alerts, data)
        time.sleep(interval)
    
    calculate_daily_summary(data_store)
    visualize_data(data_store)

# Run the system (interval of 5 minutes, for 24 hours)

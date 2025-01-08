from flask import Flask, request, jsonify, render_template
import threading
import sqlite3
import os
import webbrowser
from weather_monitor import run_weather_monitor, send_email_alert

app = Flask(__name__, static_folder='static', template_folder='templates')

# Path to the SQLite database
DB_PATH = 'weather_data.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    cities = data.get('cities', [])
    interval = data.get('interval', 300)
    duration = data.get('duration', 3600)

    if not cities:
        return jsonify({'error': 'Cities list is required'}), 400

    thread = threading.Thread(target=run_weather_monitor, args=(interval, duration, cities))
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Monitoring started successfully!'})

@app.route('/weather-data', methods=['GET'])
def get_weather_data():
    city_filter = request.args.get('city', '')
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        if city_filter:
            cursor.execute("""
                SELECT city, date, temp, weather_condition, feels_like
                FROM weather
                WHERE city LIKE ?
                ORDER BY date DESC
                LIMIT 100
            """, (f"%{city_filter}%",))
        else:
            cursor.execute("""
                SELECT city, date, temp, weather_condition, feels_like
                FROM weather
                ORDER BY date DESC
                LIMIT 100
            """)

        rows = cursor.fetchall()

        weather_data = {
            'data': [
                {
                    'city': row[0],
                    'date': row[1],
                    'temp': row[2],
                    'weather_condition': row[3],
                    'feels_like': row[4]
                }
                for row in rows
            ]
        }
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({'error': f"Failed to fetch weather data: {str(e)}"}), 500
    finally:
        connection.close()

@app.route('/send-alert', methods=['POST'])
def send_alert():
    data = request.json
    city = data.get('city', 'Unknown City')
    temp = data.get('temp', 'N/A')
    threshold = data.get('threshold', 20)

    if temp != 'N/A' and temp > threshold:
        subject = f"Temperature Alert for {city}"
        body = f"The temperature in {city} has exceeded {threshold}°C. Current temperature: {temp}°C."
        try:
            send_email_alert(subject, body)
            return jsonify({'message': 'Alert sent successfully!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'No alert sent as temperature is within safe range.'}), 200

if __name__ == '__main__':
    threading.Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)

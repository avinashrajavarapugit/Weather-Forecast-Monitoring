from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

# Database connection function
def connect_db():
    conn = sqlite3.connect('weather_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint to fetch all weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Weather")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    weather_data = [dict(row) for row in rows]
    return jsonify(weather_data)

# Endpoint to filter weather data by city
@app.route('/weather/<city>', methods=['GET'])
def get_weather_by_city(city):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Weather WHERE city = ?", (city,))
    rows = cursor.fetchall()
    conn.close()

    weather_data = [dict(row) for row in rows]
    return jsonify(weather_data)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Render the HTML file

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('locations.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  lat REAL, lon REAL, address TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

@app.route('/')
def index():
    return open('static/index.html').read()

@app.route('/api/locations', methods=['GET'])
def get_locations():
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT lat, lon, address FROM locations ORDER BY timestamp DESC LIMIT 100')

    data = [
        {
            'lat': row[0],
            'lon': row[1],
            'address': row[2]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(data)

@app.route('/api/track', methods=['POST'])
def track_location():
    data = request.json

    lat = data.get('lat')
    lon = data.get('lon')
    address = data.get('address')

    conn = sqlite3.connect('locations.db')

    conn.execute(
        "INSERT INTO locations (lat, lon, address) VALUES (?, ?, ?)",
        (lat, lon, address)
    )

    conn.commit()
    conn.close()

    return {"status": "success"}, 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

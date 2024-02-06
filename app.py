from flask import Flask
import sqlite3
import math

app = Flask(__name__)


def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 3959  # Radius of Earth in miles
    return c * r


def find_nearby_sites(user_lat, user_lon):
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()

    # Bounding box query (example: +/- 5 degrees)
    lat_range = (user_lat - 5, user_lat + 5)
    lon_range = (user_lon - 5, user_lon + 5)

    cursor.execute("SELECT * FROM dive_sites WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?",
                   (*lat_range, *lon_range))
    nearby_sites = []

    for site in cursor.fetchall():
        site_lat, site_lon = site['latitude'], site['longitude']
        distance = haversine(user_lat, user_lon, site_lat, site_lon)
        if distance <= 345.85:
            nearby_sites.append(site)

    connection.close()
    return nearby_sites


@app.route('/find_nearby_sites/<float:user_lat>/<float:user_lon>')
def get_nearby_sites(user_lat, user_lon):
    nearby_sites = find_nearby_sites(user_lat, user_lon)
    return {'nearby_sites': nearby_sites}


if __name__ == '__main__':
    app.run()

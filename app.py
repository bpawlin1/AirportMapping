from flask import Flask, jsonify, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from geoalchemy2 import Geometry
import scrape_weather
from models import db, Airport
import csv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://brian:Bandit2015@localhost:5432/airports'  # Replace with your PostgreSQL connection details

db.init_app(app)
with app.app_context():
        db.create_all()

def activate_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scrape_weather.scrape_metar_data, trigger="interval", min=1)
    scheduler.start()

def insert_airports_from_csv(csv_file):
    with app.app_context():
        with open(csv_file, 'r') as file:  # Specify the correct encoding here
            csv_reader = csv.DictReader(file)

            print(csv_reader.fieldnames)

            for row in csv_reader:
                airport = Airport(
                    country_code=row['country_code'],
                    region_name=row['region_name'],
                    iata=row['iata'],
                    icao=row['icao'],
                    airport=row['airport'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude'])
                )
                db.session.add(airport)
            db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

# Flask route to retrieve airport data as GeoJSON
@app.route('/airports/geojson', methods=['GET'])
def airports_geojson():
    airports = Airport.query.all()

    features = []
    for airport in airports:
        feature = {
            'type': 'Feature',
            'properties': {
                'country_code': airport.country_code,
                'region_name': airport.region_name,
                'iata': airport.iata,
                'icao': airport.icao,
                'airport': airport.airport
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [airport.longitude, airport.latitude]
            }
        }
        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return jsonify(geojson)

if __name__ == '__main__':
    



    insert_airports_from_csv('airport.csv')
    print('data loaded')
    app.run(debug=True)
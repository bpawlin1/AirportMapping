from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airport(db.Model):
    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2))
    region_name = db.Column(db.String(255))
    iata = db.Column(db.String(3))
    icao = db.Column(db.String(4))
    airport = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, country_code, region_name, iata, icao, airport, latitude, longitude):
        self.country_code = country_code
        self.region_name = region_name
        self.iata = iata
        self.icao = icao
        self.airport = airport
        self.latitude = latitude
        self.longitude = longitude
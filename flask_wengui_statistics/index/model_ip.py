"""Database models."""

from datetime import datetime
from .. import db


class IP(db.Model):
    """IP model."""

    __tablename__ = "ip_record"
    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.String(15), index=True, nullable=True, unique=False)

    page = db.Column(db.String(25), index=False, nullable=True, unique=False)

    city = db.Column(db.String(25), index=False, nullable=True, unique=False)

    region = db.Column(db.String(25), index=False, nullable=True, unique=False)

    country_name = db.Column(db.String(25), index=False,
                             nullable=True, unique=False)

    country_capital = db.Column(db.String(25), index=False,
                                nullable=True, unique=False)

    timezone = db.Column(db.String(25), index=False,
                         nullable=True, unique=False)

    latitude = db.Column(db.Float, nullable=True, unique=False)

    longitude = db.Column(db.Float, nullable=True, unique=False)

    org = db.Column(db.String(35), nullable=True, unique=False)

    browser = db.Column(db.String(100), nullable=True, unique=False)

    time = db.Column(db.DateTime, unique=False, default=datetime.now)

    def google_map(self):
        return 'https://www.google.com/maps/search/?api=1&query='+str(self.lanti)+','+str(self.longti)

    def access_from(self):
        return self.Montreal + '/' + self.region + '/' + self.country_name

    def datetime_serialize(self,value):
        # """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        # return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
        return value.strftime("%Y-%m-%d,")+value.strftime("%H:%M:%S")

    @property
    def serialize(self):
        # Return object data in easily serializable format
        return {'id': self.id,
                'ip': self.ip,
                'page': self.page,
                'city': self.city,
                'region': self.region,
                'country_name': self.country_name,
                'country_capital': self.country_capital,
                'timezone': self.timezone,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'org': self.org,
                'browser': self.browser,
                'time': self.datetime_serialize(self.time)}

    def __repr__(self):
        return "<IP: {}>".format(self.ip)

    def __init__(self, page, ip, city, region, country_name, country_capital, timezone, latitude, longitude, org, browser):
        self.page = page
        self.ip = ip
        self.city = city
        self.region = region
        self.country_name = country_name
        self.country_capital = country_capital
        self.timezone = timezone
        self.latitude = latitude
        self.longitude = longitude
        self.org = org
        self.browser = browser

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including date and precipitation"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations names"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs in the last year for station USC00519281"""
    # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').filter(Measurement.date <='2017-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of temperature observations
    year_tobs = []
    for result in results:
        row = {}

        row["date"] = result[0]
        row["tobs"] = int(result[1])
        year_tobs.append(row)

    return jsonify(year_tobs)


@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)
    
    # Query using functions for min, avg and max for dates given
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= f'{start}').all()
    
    session.close()

    # Create a dictionary from the query data and append to a list for results
    start_date_values = []
    for min,avg,max in results:
        start_dict = {}
        start_dict["Min Temp"] = min
        start_dict["Avg Temp"] = avg
        start_dict["Max Temp"] = max
        start_date_values.append(start_dict)

    return jsonify(start_date_values)


@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    session = Session(engine)
    
    # Query using functions for min, avg and max for dates given 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= f'{start}').filter(Measurement.date <= f'{end}').all()
    
    session.close()

    # Create a dictionary from the query data and append to a list for results
    start_end_date_values = []
    for min,avg,max in results:
        start_end_dict = {}
        start_end_dict["Min Temp"] = min
        start_end_dict["Avg Temp"] = avg
        start_end_dict["Max Temp"] = max
        start_end_date_values.append(start_end_dict)

    return jsonify(start_end_date_values)


if __name__ == '__main__':
    app.run(debug=True)
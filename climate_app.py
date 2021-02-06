from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)




@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/&lt;start> <br/>"
        f"/api/v1.0/&lt;start>/&lt;end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precipitation_dictionary = {}
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    for row in precipitation_scores:
        precipitation_dictionary[row[0]] = row[1]
    return jsonify(precipitation_dictionary)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    clean_data = [row[0] for row in stations]
    return jsonify(clean_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    response = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-22').all()
    session.close()
    clean_data = [row[0] for row in response]
    return jsonify(clean_data)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    response = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
         filter(Measurement.date >= start).\
         group_by(Measurement.date).all()
    
    session.close()

    start_data = list(np.ravel(response))

    return jsonify(start_data)




@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    response = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    

    session.close()

    start_end_data = list(np.ravel(response))


    return jsonify(start_end_data)














if __name__ == "__main__":
    app.run(debug=True)


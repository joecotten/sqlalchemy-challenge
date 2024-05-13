# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


Base=automap_base()

Base.prepare(autoload_with=engine)

Measurement=Base.classes.measurement

Station=Base.classes.station

session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """App Routes"""
    return (
        f"HomePage: '/'"
        f"Preciptation Analysis '/api/v1.0/precipitation'"
        f"Station List '/api/v1.0/stations"
        f"Temp And Date observations of most-active station '/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).\
                filter(Measurement.date >= dt.date(2016,8,23)).all()
    session.close()
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)
    print(precip_list)
    return jsonify(precip_list)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()
    session.close()

  
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).\
        filter(Measurement.date >= dt.date(2016,8,23)).all()               
    session.close()

    tobs = list(np.ravel(results))
  
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")

def start(start):


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
                            func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
                            func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()


    session.close()
 
    return jsonify(results)

if __name__ == '__main__':
    app.run()
    
session.close()
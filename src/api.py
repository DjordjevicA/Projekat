import database
import models

"""Functions handling API endpoints."""



def getMeasurements(variable=None):
    measurements = models.Measurement.query
    if variable is not None:
        measurements = measurements.filter_by(variable=variable)
    measurements = measurements.all()
    measurements = map(lambda m: m.to_dict(), measurements)
    return list(measurements)


def createMeasurement(body):
    source = models.Source.query.filter_by(id=body["source_id"]).first()
    if source is None:
        return ("Source not found.", 404)
    variable = models.Variable.query.filter_by(name=body["variable"]).first()
    if variable is None:
        return ("Variable not found.", 404)
    station = models.Station.query.filter_by(id=body["station_id"]).first()
    if station is None:
        return ("Station not found.", 404)
    measurement = models.Measurement(time=body["time"], value=body["value"], source=source, variable=variable, station=station)
    database.db.session.add(measurement)
    database.db.session.commit()
    return measurement.to_dict()


def getMeasurementById(id):
    measurement = models.Measurement.query.filter_by(id=id).first()
    if measurement is None:
        return ("Measurement not found.", 404)
    return measurement.to_dict()


def updateMeasurementById(body, id):
    measurement = models.Measurement.query.filter_by(id=id).first()
    if measurement is None:
        return ("Measurement not found.", 404)
    for field, value in body.items():
        if hasattr(measurement, field):
            setattr(measurement, field, value)
    database.db.session.commit()
    return 200


def deleteMeasurementById(id):
    measurement = models.Measurement.query.filter_by(id=id).delete()
    if not measurement:
        return ("Measurement not found.", 404)
    database.db.session.commit()
    return 200 


def getLocations(country=None):
    locations = models.Location.query
    if country is not None:
        locations = locations.filter_by(country=country)
    locations = locations.all()
    locations = map(lambda l: l.to_dict(), locations)
    return list(locations)


def createLocation(body):
    location = models.Location(name=body["name"], country=body["country"], lat=body["lat"], long=body["long"], altitude=body["altitude"], type=body["type"])
    database.db.session.add(location)
    database.db.session.commit()
    return location.to_dict()


def getLocationById(id):
    location = models.Location.query.filter_by(id=id).first()
    if location is None:
        return ("Location not found.", 404)
    return location.to_dict()


def updateLocationById(body, id):
    location = models.Location.query.filter_by(id=id).first()
    if location is None:
        return ("Location not found.", 404)
    location.name = body["name"]
    location.lat = body["lat"]
    location.long = body["long"]
    location.country = body["country"]
    location.altitude = body["altitude"]
    location.type = body["type"]
    database.db.session.commit()
    return 200


def deleteLocationById(id):
    location = models.Location.query.filter_by(id=id).delete()
    if not location:
        return ("Location not found.", 404)
    database.db.session.commit()
    return 200


def getSources(location=None):
    sources = models.Source.query
    if location is not None:
        sources = sources.filter(models.Source.location.has(models.Location.name.ilike('%{}%'.format(location))))
    sources = sources.all()
    sources = map(lambda s: s.to_dict(), sources)
    return list(sources)


def createSource(body):
    if "location_id" not in body:
        return ("Location ID not provided.", 400)
    location_id = body["location_id"]
    location = models.Location.query.get(location_id)
    if location is None:
        return (f"Location with ID {location_id} not found.", 404)
    source = models.Source(
        code=body["code"],
        name=body["name"],
        type=body["type"],
        location=location  
    )
    database.db.session.add(source)
    database.db.session.commit()
    return source.to_dict()


def getSourceById(id):
    source = models.Source.query.filter_by(id=id).first()
    if source is None:
        return ("Source not found.", 404)
    return source.to_dict()


def updateSourceById(body, id):
    source = models.Source.query.filter_by(id=id).first()
    if source is None:
        return ("Source not found.", 404)
    source.name = body["name"]
    source.type = body["type"]
    database.db.session.commit()
    return 200


def deleteSourceById(id):
    source = models.Source.query.filter_by(id=id).delete()
    if not source:
        return ("Source not found.", 404)
    database.db.session.commit()
    return 200


def getVariables(name=None):
    variables = models.Variable.query
    if name is not None:
        variables = variables.filter_by(name=name)
    variables = variables.all()
    variables = map(lambda v: v.to_dict(), variables)
    return list(variables)


def createVariable(body):
    variable = models.Variable(name=body["name"], unit=body["unit"])
    database.db.session.add(variable)
    database.db.session.commit()
    return variable.to_dict()


def getVariableById(id):
    variable = models.Variable.query.filter_by(id=id).first()
    if variable is None:
        return ("Variable not found.", 404)
    return variable.to_dict()


def updateVariableById(body, id):
    variable = models.Variable.query.filter_by(id=id).first()
    if variable is None:
        return ("Variable not found.", 404)
    variable.name = body["name"]
    variable.unit = body["unit"]
    database.db.session.commit()
    return 200


def deleteVariableById(id):
    variable = models.Variable.query.filter_by(id=id).delete()
    if not variable:
        return ("Variable not found.", 404)
    database.db.session.commit()
    return 200


def getStations(location=None):
    stations = models.Station.query
    if location is not None:
        stations = stations.filter(models.Station.location.has(models.Location.name.ilike('%{}%'.format(location))))
    stations = stations.all()
    stations = map(lambda s: s.to_dict(), stations)
    return list(stations)


def createStation(body):
    if "location_id" not in body:
        return ("Location ID not provided.", 400)
    location_id = body["location_id"]
    location = models.Location.query.get(location_id)
    if location is None:
        return (f"Location with ID {location_id} not found.", 404)
    station = models.Station(
        name=body["name"],
        type=body["type"],
        capacity=body["capacity"],
        location=location  
    )
    database.db.session.add(station)
    database.db.session.commit()
    return station.to_dict()


def getStationById(id):
    station = models.Station.query.filter_by(id=id).first()
    if station is None:
        return ("Station not found.", 404)
    return station.to_dict()


def updateStationById(body, id):
    station = models.Station.query.filter_by(id=id).first()
    if station is None:
        return ("Station not found.", 404)
    station.name = body["name"]
    station.type = body["type"]
    station.capacity = body["capacity"]
    database.db.session.commit()
    return 200


def deleteStationById(id):
    station = models.Station.query.filter_by(id=id).delete()
    if not station:
        return ("Station not found.", 404)
    database.db.session.commit()
    return 200

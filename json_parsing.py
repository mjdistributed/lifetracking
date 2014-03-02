import colander

class Placemark(colander.MappingSchema):
	thoroughfare = colander.SchemaNode(colander.String())
	postalCode = colander.SchemaNode(colander.String())
	subAdministrativeArea = colander.SchemaNode(colander.String())
	subLocality = colander.SchemaNode(colander.String())
	subThoroughfare = colander.SchemaNode(colander.String())
	locality = colander.SchemaNode(colander.String())
	name = colander.SchemaNode(colander.String())
	country = colander.SchemaNode(colander.String())
	administrativeArea = colander.SchemaNode(colander.String())

class Location(colander.MappingSchema):
	verticalAccuracy = colander.SchemaNode(colander.Int())
	# timestamp
	longitude = colander.SchemaNode(colander.Float())
	latitude = colander.SchemaNode(colander.Float())
	course = colander.SchemaNode(colander.Int())
	placemark = Placemark()
	horizontalAccuracy = colander.SchemaNode(colander.Int())
	speed = colander.SchemaNode(colander.Int())

class Audio(colander.MappingSchema):
	avg = colander.SchemaNode(colander.Float(), validator = colander.Range(-100, 100))
	peak = colander.SchemaNode(colander.Float(), validator = colander.Range(-100, 100))

class Weather(colander.MappingSchema):
	windMPH = colander.SchemaNode(colander.Int())
	windDirection = colander.SchemaNode(colander.String())
	tempF = colander.SchemaNode(colander.Int())
	precipTodayIn = colander.SchemaNode(colander.Int())
	windGustKPH = colander.SchemaNode(colander.Decimal())
	pressureIn = colander.SchemaNode(colander.Decimal())
	pressureMb = colander.SchemaNode(colander.Decimal())
	relativeHumidity = colander.SchemaNode(colander.String())
	longitude = colander.SchemaNode(colander.Decimal())
	precipTodayMetric = colander.SchemaNode(colander.Int())
	windKPH = colander.SchemaNode(colander.Decimal())
	windDegrees =colander.SchemaNode(colander.Int())
	tempC = colander.SchemaNode(colander.Decimal())
	weather = colander.SchemaNode(colander.String())
	uv = colander.SchemaNode(colander.Int())
	dewpointC = colander.SchemaNode(colander.Int())
	visibilityKM = colander.SchemaNode(colander.Decimal())

class Snapshot(colander.MappingSchema):
	battery = colander.SchemaNode(colander.Float(), validator = colander.Range(0,1))
	location = Location()
	steps = colander.SchemaNode(colander.Int(), validator = colander.Range(0,9999))
	day = colander.SchemaNode(colander.Int(), validator = colander.Range(0, 599999999))
	audio = Audio()
	sync = colander.SchemaNode(colander.Int(), validator = colander.Range(0 ,1))
	connection = colander.SchemaNode(colander.Int(), validator = colander.Range(0, 1))
	background = colander.SchemaNode(colander.Int(), validator = colander.Range(0, 1))
	dwellStatus = colander.SchemaNode(colander.Int(), validator = colander.Range(0, 1))
	draft = colander.SchemaNode(colander.Int(), validator = colander.Range(0, 1))
	weather = Weather()
	# date = colander.SchemaNode(colander.DateTime())



class Data(colander.SequenceSchema):
	snapshot = Snapshot()

cstruct = {
      "battery" : 0.9,
      "location" : {
        "verticalAccuracy" : 10,
        "longitude" : -95.40391789528709,
        "latitude" : 29.72951176488592,
        "course" : 0,
        "placemark" : {
          "thoroughfare" : "Banks St",
          "postalCode" : "77098",
          "subAdministrativeArea" : "Harris",
          "subLocality" : "Boulevard Oaks",
          "subThoroughfare" : "1745",
          "locality" : "Houston",
          "name" : "1745 Banks St",
          "country" : "United States",
          "administrativeArea" : "TX"
        },
        "horizontalAccuracy" : 65,
        "speed" : -1
      },
      "steps" : 0,
      "day" : 413532000,
      "audio" : {
        "avg" : -58.64249,
        "peak" : -49.91104
      },
      "sync" : 0,
      "connection" : 1,
      "background" : 0,
      "dwellStatus" : 0,
      "draft" : 0,
      "weather" : {
        "windMPH" : 6,
        "windDirection" : "SW",
        "tempF" : 40,
        "precipTodayIn" : 0,
        "windGustKPH" : 11.3,
        "feelslikeC" : 2,
        "visibilityMi" : 10,
        "feelslikeF" : 36,
        "stationID" : "KTXHOUST256",
        "latitude" : 29.730955,
        "windGustMPH" : 7,
        "pressureIn" : 30.2,
        "pressureMb" : 1023,
        "relativeHumidity" : "90%",
        "longitude" : -95.43055,
        "precipTodayMetric" : 0,
        "windKPH" : 9.699999999999999,
        "windDegrees" : 225,
        "tempC" : 4.4,
        "weather" : "Overcast",
        "uv" : 0,
        "dewpointC" : 3,
        "visibilityKM" : 16.1
      }
     }

schema = Snapshot()
deserialized = schema.deserialize(cstruct)

print(deserialized)
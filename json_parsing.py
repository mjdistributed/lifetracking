import colander
import limone

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

class Response(colander.MappingSchema):
  questionPrompt = colander.SchemaNode(colander.String())
  numericResponse = colander.SchemaNode(colander.Int(), missing = colander.drop)
  textResponse = colander.SchemaNode(colander.String(), missing = colander.drop)
  answeredOptions = colander.SchemaNode(colander.List(), missing = colander.drop)

class Responses(colander.SequenceSchema):
  response = Response()
  


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
  responses = Responses(missing=colander.drop)
  #date = colander.SchemaNode(colander.DateTime())

class Snapshots(colander.SequenceSchema):
  snapshot = Snapshot()

@limone.content_schema
class Data(colander.MappingSchema):
  snapshots = Snapshots()

cstruct = {
  "snapshots" : [
    {
      "battery" : 0.9,
      "location" : {
        "verticalAccuracy" : 10,
        "timestamp" : 413536108.072888,
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
      },
      "date" : 413536104.402608,
      "responses" : [
        {
          "numericResponse" : "2",
          "questionPrompt" : "How many coffees did you have today?"
        },
        {
          "questionPrompt" : "What did you learn today?",
          "textResponse" : "Plan ahead well. Guiding others is rewarding. "
        }
      ]
    },
    {
      "battery" : 0.9,
      "location" : {
        "verticalAccuracy" : 10,
        "timestamp" : 413536222.497276,
        "longitude" : -95.40407273043402,
        "latitude" : 29.7294426879126,
        "course" : 0,
        "placemark" : {
          "thoroughfare" : "Banks St",
          "postalCode" : "77098",
          "subAdministrativeArea" : "Harris",
          "subLocality" : "Boulevard Oaks",
          "subThoroughfare" : "1749",
          "locality" : "Houston",
          "name" : "1749 Banks St",
          "country" : "United States",
          "administrativeArea" : "TX"
        },
        "horizontalAccuracy" : 65,
        "speed" : -1
      },
      "steps" : 0,
      "day" : 413532000,
      "audio" : {
        "avg" : -53.87271,
        "peak" : -36.89292
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
      },
      "date" : 413536221.651338,
      "responses" : [
        {
          "questionPrompt" : "Are you working?",
          "answeredOptions" : [
            "Yes"
          ]
        },
        {
          "questionPrompt" : "What are you doing?",
          "tokens" : [
            "Thermo problem set"
          ]
        },
        {
          "questionPrompt" : "Where are you?",
          "locationResponse" : {
            "text" : "Home",
            "location" : {
              "verticalAccuracy" : 3,
              "timestamp" : 413536249.598942,
              "longitude" : -95.40422318512145,
              "latitude" : 29.72944823096481,
              "course" : 0,
              "horizontalAccuracy" : 5,
              "speed" : 0
            }
          }
        }
      ]
    },
    {
      "battery" : 0.8,
      "location" : {
        "verticalAccuracy" : 10,
        "timestamp" : 413543626.49033,
        "longitude" : -95.40395343743923,
        "latitude" : 29.72955756391125,
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
        "horizontalAccuracy" : 74.88592302612217,
        "speed" : -1
      },
      "steps" : 0,
      "day" : 413532000,
      "audio" : {
        "avg" : -47.39773,
        "peak" : -40.90244
      },
      "sync" : 0,
      "connection" : 1,
      "background" : 0,
      "dwellStatus" : 0,
      "draft" : 0,
      "weather" : {
        "windMPH" : 0,
        "windDirection" : "SSW",
        "tempF" : 40,
        "precipTodayIn" : 0,
        "windGustKPH" : 0,
        "feelslikeC" : 4,
        "visibilityMi" : 10,
        "feelslikeF" : 40,
        "stationID" : "KTXHOUST256",
        "latitude" : 29.730955,
        "windGustMPH" : 0,
        "pressureIn" : 30.18,
        "pressureMb" : 1022,
        "relativeHumidity" : "88%",
        "longitude" : -95.43055,
        "precipTodayMetric" : 0,
        "windKPH" : 0,
        "windDegrees" : 202,
        "tempC" : 4.4,
        "weather" : "Overcast",
        "uv" : 0,
        "dewpointC" : 3,
        "visibilityKM" : 16.1
      },
      "date" : 413543624.614822,
      "responses" : [
        {
          "questionPrompt" : "Are you working?",
          "answeredOptions" : [
            "Yes"
          ]
        },
        {
          "questionPrompt" : "What are you doing?",
          "tokens" : [
            "Thermo problem set"
          ]
        },
        {
          "questionPrompt" : "Where are you?",
          "locationResponse" : {
            "text" : "Home",
            "location" : {
              "verticalAccuracy" : 3,
              "timestamp" : 413536249.598942,
              "longitude" : -95.40422318512145,
              "latitude" : 29.72944823096481,
              "course" : 0,
              "horizontalAccuracy" : 5,
              "speed" : 0
            }
          }
        }
      ]
    },
    {
      "battery" : 0.7,
      "location" : {
        "verticalAccuracy" : 10,
        "timestamp" : 413547055.335176,
        "longitude" : -95.40421608711512,
        "latitude" : 29.72952076578435,
        "course" : 0,
        "placemark" : {
          "thoroughfare" : "Banks St",
          "postalCode" : "77098",
          "subAdministrativeArea" : "Harris",
          "subLocality" : "Boulevard Oaks",
          "subThoroughfare" : "1755",
          "locality" : "Houston",
          "name" : "1755 Banks St",
          "country" : "United States",
          "administrativeArea" : "TX"
        },
        "horizontalAccuracy" : 65,
        "speed" : -1
      },
      "steps" : 15,
      "day" : 413532000,
      "audio" : {
        "avg" : -62.2,
        "peak" : -55.40989
      },
      "sync" : 0,
      "connection" : 1,
      "background" : 0,
      "dwellStatus" : 0,
      "draft" : 0,
      "weather" : {
        "windMPH" : 0,
        "windDirection" : "SSW",
        "tempF" : 40,
        "precipTodayIn" : 0,
        "windGustKPH" : 0,
        "feelslikeC" : 4,
        "visibilityMi" : 10,
        "feelslikeF" : 40,
        "stationID" : "KTXHOUST256",
        "latitude" : 29.730955,
        "windGustMPH" : 0,
        "pressureIn" : 30.18,
        "pressureMb" : 1022,
        "relativeHumidity" : "88%",
        "longitude" : -95.43055,
        "precipTodayMetric" : 0,
        "windKPH" : 0,
        "windDegrees" : 202,
        "tempC" : 4.4,
        "weather" : "Overcast",
        "uv" : 0,
        "dewpointC" : 3,
        "visibilityKM" : 16.1
      },
      "date" : 413547054.645001
    },
    {
      "battery" : 0.95,
      "location" : {
        "verticalAccuracy" : 10,
        "timestamp" : 413573243.22673,
        "longitude" : -95.40405756154604,
        "latitude" : 29.72945778439238,
        "course" : 0,
        "placemark" : {
          "thoroughfare" : "Banks St",
          "postalCode" : "77098",
          "subAdministrativeArea" : "Harris",
          "subLocality" : "Boulevard Oaks",
          "subThoroughfare" : "1749",
          "locality" : "Houston",
          "name" : "1749 Banks St",
          "country" : "United States",
          "administrativeArea" : "TX"
        },
        "horizontalAccuracy" : 65,
        "speed" : -1
      },
      "steps" : 58,
      "day" : 413532000,
      "audio" : {
        "avg" : -53.30972,
        "peak" : -38.45331
      },
      "sync" : 0,
      "connection" : 1,
      "background" : 0,
      "dwellStatus" : 0,
      "draft" : 0,
      "weather" : {
        "windMPH" : 0,
        "windDirection" : "South",
        "tempF" : 52,
        "precipTodayIn" : 0,
        "windGustKPH" : 0,
        "feelslikeC" : 11.1,
        "visibilityMi" : 5,
        "feelslikeF" : 52,
        "stationID" : "KTXHOUST256",
        "latitude" : 29.730955,
        "windGustMPH" : 0,
        "pressureIn" : 30.2,
        "pressureMb" : 1023,
        "relativeHumidity" : "70%",
        "longitude" : -95.43055,
        "precipTodayMetric" : 0,
        "windKPH" : 0,
        "windDegrees" : 180,
        "tempC" : 11.1,
        "weather" : "Overcast",
        "uv" : 2,
        "dewpointC" : 6,
        "visibilityKM" : 8
      },
      "date" : 413573242.322871,
      "responses" : [
        {
          "questionPrompt" : "How did you sleep?",
          "answeredOptions" : [
            "Poorly"
          ]
        }
      ]
    }
  ]
}

tst = Data.deserialize(cstruct)
print(tst.snapshots[0].battery)

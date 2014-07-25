import json

class Payload(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)

cstruct = """
{
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
      }
    }
   ]
}
"""

test = """
	{
		"action": "print", 
		"method": "onData", 
		"data": "Madan Mohan"
	}
"""

p = Payload(cstruct)
print(p)
print(p.snapshots)
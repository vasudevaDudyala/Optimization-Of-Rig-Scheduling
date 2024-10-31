
class Well(object):
    def __init__(self,id,name,wellParams):
        self.id = id
        self.name = name
        self.startTime = wellParams["startTime"]
        self.endTime = wellParams["endTime"]
        self.productionRate = int(input("enter well {} production volume/production rate :".format(self.id)))
        self.workoverTime = wellParams["workoverTime"]
        self.priority = wellParams["priority"]
        self.lossFactor=wellParams['lossFactor']
        self.well_location=wellParams['well_location']
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "productionRate": self.productionRate,
            "workoverTime": self.workoverTime,
            "priority": self.priority,
            "well_location":self.well_location,
            "lossFactor":self.lossFactor,
        }

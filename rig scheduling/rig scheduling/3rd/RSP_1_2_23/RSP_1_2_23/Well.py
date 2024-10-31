
class Well(object):
    def __init__(self,id,name,wellParams):
        self.id = id
        self.name = name
        self.startTime = wellParams["startTime"]
        self.endTime = wellParams["endTime"]
        self.productionRate = wellParams["productionRate"]
        self.workoverTime = wellParams["workoverTime"]
        self.priority = wellParams["priority"]
        self.lossFactor=wellParams['lossFactor']
        self.location=wellParams['location']
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "productionRate": self.productionRate,
            "workoverTime": self.workoverTime,
            "priority": self.priority,
            "location":self.location,
            "lossFactor":self.lossFactor,
        }

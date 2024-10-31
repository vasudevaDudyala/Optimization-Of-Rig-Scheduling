
class Well(object):
    def __init__(self,id,name,wellParams):
        self.id = id
        self.name = name
        self.startTime = wellParams["startTime"]
        self.endTime = wellParams["endTime"]
        self.productionRate = wellParams["productionRate"]
        self.processingTime = wellParams["processingTime"]
        self.priority = wellParams["priority"]

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "productionRate": self.productionRate,
            "processingTime": self.processingTime,
            "priority": self.priority
        }
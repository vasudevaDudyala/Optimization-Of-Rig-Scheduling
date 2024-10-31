
class Well(object):
    def __init__(self,id,name,well_type,depth_capacity,wellParams):
        self.id = id
        self.name = name
        self.well_type=well_type
        self.depth_capacity=depth_capacity
        self.startTime = wellParams["startTime"]
        self.endTime = wellParams["endTime"]
        self.productionRate =25 #int(input("enter well {} production volume/production rate :".format(self.id)))
        self.workoverTime = wellParams["workoverTime"]
        self.priority = wellParams["priority"]
        self.lossFactor=wellParams['lossFactor']
        self.well_location=wellParams['well_location']
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "well_type":self.well_type,
            "depth_capacity":self.depth_capacity,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "productionRate": self.productionRate,
            "workoverTime": self.workoverTime,
            "priority": self.priority,
            "well_location":self.well_location,
            "lossFactor":self.lossFactor,
        }

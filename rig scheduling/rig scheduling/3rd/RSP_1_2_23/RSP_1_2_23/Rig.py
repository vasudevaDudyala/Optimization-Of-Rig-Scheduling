class Rig(object):

    def __init__(self,id,name,rigParams):
        self.id = id
        self.name = name
        self.speed = rigParams['speed']
        self.assignedWells = []
        self.workoverTime = 0
        self.startTime=[]
        self.endTime=[]
        self.startTime = rigParams['startTime']
        self.endTime = rigParams['endTime']
        self.travelTime=[]
        self.location=rigParams['location']

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "assignedWells" : self.assignedWells,
            'workoverTime' : self.workoverTime,
            "startTime": self.startTime,
            "endTime":self.endTime,
            "location":self.location,
            "travelTime":self.travelTime,
            "startTime":self.startTime,
            "endTime" : self.endTime
        }

class Rig(object):

    def __init__(self,id,name,rigParams):
        self.id = id
        self.name = name
        self.speed = rigParams['speed']
        self.assignedWells = []
        self.processingTime = 0

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "assignedWells" : self.assignedWells,
            'processingTime' : self.processingTime
        }

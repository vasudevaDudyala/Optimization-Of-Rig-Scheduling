class Rig(object):

    def __init__(self, id, name, rigParams):
        self.id = id
        self.name = name
        self.speed = int(input("enter rig {} average speed  :".format(self.id)))
        self.assigned_wells = []
        self.workoverTime = 0
        self.interventionStartTime = []
        self.interventionEndTime = []
        self.mastupStatus = input("enter rig status(mastup or mastdown)  :".format(self.id))
        self.mastupStartTime = []
        self.mastupEndTime = []
        self.mastdownStartTime = []
        self.mastdownEndTime = []
        self.arrivalTime = []
        self.rig_location=rigParams['rig_location']
        self.mastupTime = int(input("enter rig {} mast uptime  :".format(self.id)))
        self.mastdownTime = int(input("enter rig {} mast downtime  :".format(self.id)))
        self.returnTime=[]
        self.distances=[]
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "assigned_wells" : self.assigned_wells,
            'workoverTime' : self.workoverTime,
            "interventionStartTime": self.interventionStartTime,
            "interventionEndTime": self.interventionEndTime,
            "mastupStatus": self.mastupStatus,
            "mastupStartTime":self.mastupStartTime,
            "mastupEndTime":self.mastupEndTime,
            "mastdownStartTime":self.mastdownStartTime,
            "mastdownEndTime":self.mastdownEndTime,
            "rig_location":self.rig_location,
            "arrivalTime":self.arrivalTime,
            "mastupTime": self.mastupTime,
            "mastdownTime": self.mastdownTime,
            "returnTime" : self.returnTime,
            "distances":self.distances
            }

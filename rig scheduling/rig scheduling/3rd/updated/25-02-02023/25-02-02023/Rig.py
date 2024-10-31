class Rig(object):

    def __init__(self,id,name,rig_type,depth_capacity,horsepower,crew_size,rate_per_day,rigParams):
        self.id = id
        self.name = name
        self.rig_type=rig_type
        self.depth_capacity=depth_capacity
        self.horsepower=horsepower
        self.crew_size=crew_size
        self.rate_per_day=rate_per_day
        #self.speed = int(input("enter rig {} average speed  :".format(self.id)))
        self.speed = 20
        self.assigned_wells = []
        self.workoverTime = 0
        self.interventionStartTime=[]
        self.interventionEndTime=[]
        self.mastupStartTime=[]
        self.mastupEndTime=[]
        self.mastdownStartTime=[]
        self.mastdownEndTime=[]
        self.arrivalTime=[]
        self.rig_location=rigParams['rig_location']
        self.rig_init_status=rigParams['rig_init_status']
        self.maintanceStartTime=[]
        self.maintanceEndTime=[]
        self.rig_maintance = rigParams['rig_maintance']
        self.mastupTime = 8 #int(input("enter rig {} mast uptime  :".format(self.id)))
        self.mastdownTime = 16 # int(input("enter rig {} mast downtime  :".format(self.id)))
        self.returnTime=[]
        self.distances=[]
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rig_type":self.rig_type,
            "depth_capacity":self.depth_capacity,
            "horsepower":self.horsepower,
            "crew_size":self.crew_size,
            "rate_per_day":self.rate_per_day,
            "speed": self.speed,
            "rig_maintance":self.rig_maintance,
            "assigned_wells" : self.assigned_wells,
            'workoverTime' : self.workoverTime,
            "rig_init_status":self.rig_init_status,
            "interventionStartTime": self.interventionStartTime,
            "interventionEndTime": self.interventionEndTime,
            "maintanceStartTime":self.maintanceStartTime,
            "maintanceEndTime":self.maintanceEndTime,
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

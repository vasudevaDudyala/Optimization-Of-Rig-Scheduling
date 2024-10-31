class Rig:
    def _init_(self, name, rig_type, depth_capacity, horsepower):
        self.name = name
        self.rig_type = rig_type
        self.depth_capacity = depth_capacity
        self.horsepower = horsepower

# Define a list of rigs
rigs = [
    Rig("Rig A", "Drilling", 1000, 1000),
    Rig("Rig B", "Drilling", 2000, 1500),
    Rig("Rig C", "Workover", 500, 750),
    Rig("Rig D", "Workover", 1000, 1000),
    Rig("Rig E", "Workover", 1500, 1200)
]

# Classify the rigs based on their parameters
drilling_rigs = [rig for rig in rigs if rig.rig_type == "Drilling" and rig.depth_capacity >= 1500 and rig.horsepower >= 1200]
workover_rigs = [rig for rig in rigs if rig.rig_type == "Workover" and rig.depth_capacity >= 1000 and rig.horsepower >= 750]

# Print the classified rigs
print("Drilling Rigs:")
for rig in drilling_rigs:
    print("- {} (depth capacity: {}, horsepower: {})".format(rig.name, rig.depth_capacity, rig.horsepower))
print("")

print("Workover Rigs:")
for rig in workover_rigs:
    print("- {} (depth capacity: {}, horsepower: {})".format(rig.name, rig.depth_capacity, rig.horsepower))
print("")
import math

cluster_well_locations = [[(310, 330), (310, 340), (310, 335), (315, 330)], [(100, 110), (110, 105), (110, 115)]]
low_drilling_rigs = [{'id': '6', 'name': 'Rig6', 'rig_type': 'Drilling', 'depth_capacity': 5200, 'horsepower': 1400, 'crew_size': 6, 'rate_per_day': 9000, 'speed': 20, 'rig_maintance': 4, 'assigned_wells': [], 'workoverTime': 0, 'rig_init_status': 'mastDown', 'interventionStartTime': [], 'interventionEndTime': [], 'maintanceStartTime': [], 'maintanceEndTime': [], 'mastupStartTime': [], 'mastupEndTime': [], 'mastdownStartTime': [], 'mastdownEndTime': [], 'rig_location': '(470 , 490)', 'arrivalTime': [], 'mastupTime': 8, 'mastdownTime': 16, 'returnTime': [], 'distances': []},
                     {'id': '7', 'name': 'Rig7', 'rig_type': 'Drilling', 'depth_capacity': 5200, 'horsepower': 1400, 'crew_size': 6, 'rate_per_day': 9000, 'speed': 20, 'rig_maintance': 4, 'assigned_wells': [], 'workoverTime': 0, 'rig_init_status': 'mastDown', 'interventionStartTime': [], 'interventionEndTime': [], 'maintanceStartTime': [], 'maintanceEndTime': [], 'mastupStartTime': [], 'mastupEndTime': [], 'mastdownStartTime': [], 'mastdownEndTime': [], 'rig_location': '(300 , 310)', 'arrivalTime': [], 'mastupTime': 8, 'mastdownTime': 16, 'returnTime': [], 'distances': []}]

for cluster in cluster_well_locations:
    min_distance = math.inf
    min_distance_rig = None
    for rig in low_drilling_rigs:
        rig_location = eval(rig['rig_location'])
        distance = min([math.sqrt((x - rig_location[0])**2 + (y - rig_location[1])**2) for x, y in cluster])
        if distance < min_distance:
            min_distance = distance
            min_distance_rig = rig
    min_distance_rig['assigned_wells'].append(cluster)
    min_distance_rig['distances'].append(min_distance)
print(min_distance_rig)


import math


def assign_rigs(clusters, rigs, wells_dictionary):
    drilling_rig_assignments = {}
    for cluster in clusters:
        # cluster_wells = cluster.wells
        # get the well ids for the wells in the cluster
        cluster_well_ids = [well['id'] for well in low_drilling_wells if well['name'] in clusters]


        # get the depth capacity of the cluster wells
        cluster_depth_capacity = max(
            [well['depth_capacity'] for well in low_drilling_wells if well['name'] in clusters])

        # loop through the rigs and assign them to the cluster if they have sufficient depth capacity
        for rig in low_drilling_rigs:
            if rig['depth_capacity'] >= cluster_depth_capacity:
                for well in cluster_well_ids:
                    drilling_rig_assignments[well] = rig['name']
                low_drilling_rigs.remove(rig)
                break

    return drilling_rig_assignments

def distance_between_wells(well1, well2):
    x1, y1 = eval(well1['well_location'])
    x2, y2 = eval(well2['well_location'])
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def distance_between_all_wells(low_drilling_wells):
    distances = []

    for i, well1 in enumerate(low_drilling_wells):
        cluster = []
        for j, well2 in enumerate(low_drilling_wells):
            if i != j:
                distance = distance_between_wells(well1, well2)
                print(distance)
                if distance <= 30:
                    cluster.append(well2['name'])

        distances.append(cluster)

    flat_list = list(set([item for sublist in distances for item in sublist]))
    # print(flat_list)
    return flat_list

low_drilling_wells =[{'id': '0', 'name': 'well1', 'well_type': 'Drilling', 'depth_capacity': 3000, 'startTime': '22-02-2023', 'endTime': '6-03-2023', 'productionRate': 25, 'workoverTime': 2, 'priority': 4, 'well_location': '(100,220)', 'lossFactor': 0.26}, {'id': '2', 'name': 'well3', 'well_type': 'Drilling', 'depth_capacity': 5000, 'startTime': '27-02-2023', 'endTime': '21-03-2023', 'productionRate': 25, 'workoverTime': 2, 'priority': 5, 'well_location': '(193,110)', 'lossFactor': 0.38},
                     {'id': '3', 'name': 'well4', 'well_type': 'Drilling', 'depth_capacity': 3000, 'startTime': '22-02-2023', 'endTime': '6-03-2023', 'productionRate': 25, 'workoverTime': 2, 'priority': 4, 'well_location': '(120,156)', 'lossFactor': 0.26}, {'id': '5', 'name': 'well6', 'well_type': 'Drilling', 'depth_capacity': 5000, 'startTime': '27-02-2023', 'endTime': '21-03-2023', 'productionRate': 25, 'workoverTime': 2, 'priority': 5, 'well_location': '(210,175)', 'lossFactor': 0.38}]

low_drilling_rigs = [{'id': '6', 'name': 'Rig6', 'rig_type': 'Drilling', 'depth_capacity': 5200, 'horsepower': 1400, 'crew_size': 6, 'rate_per_day': 9000, 'speed': 20, 'rig_maintance': 4, 'assigned_wells': [], 'workoverTime': 0, 'rig_init_status': 'mastDown', 'interventionStartTime': [], 'interventionEndTime': [], 'maintanceStartTime': [], 'maintanceEndTime': [], 'mastupStartTime': [], 'mastupEndTime': [], 'mastdownStartTime': [], 'mastdownEndTime': [], 'rig_location': '(100 , 100)', 'arrivalTime': [], 'mastupTime': 8, 'mastdownTime': 16, 'returnTime': [], 'distances': []}]


flat_list = distance_between_all_wells(low_drilling_wells)
drilling_rig_assignment = assign_rigs(flat_list, low_drilling_rigs, low_drilling_wells)
print("flat_list",flat_list)
print(drilling_rig_assignment)
print('test', low_drilling_rigs)



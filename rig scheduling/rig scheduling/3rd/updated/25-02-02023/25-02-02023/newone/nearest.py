from scipy.spatial.distance import cdist
from numpy import array, ravel
from datetime import datetime, timedelta
import re

from datetime import datetime, timedelta

def distance_mat(rigs, wells):
    distance_matrix = cdist(rigs, wells, 'euclidean')
    return distance_matrix

def end_to_start_distance(rigs_dictionary, rigs):
    for i in range(len(rigs_dictionary)):
        distance_matrix = distance_mat([rigs_dictionary[i]['rigs_locations']], [rigs[i]])
        distance = ravel(distance_matrix).tolist()
        rigs_dictionary[i]['distances'].append(distance[0])
    return rigs_dictionary



def early_completed(rigs_dictionary, well_dict, nearest):
    print('  rigs_dict',rigs_dictionary,well_dict,nearest)
    for i in range(len(well_dict)):
        if well_dict[i]['well_location'] == nearest:
            print('msg')
            startTime_str = rigs_dictionary[0]['startTime'].strftime("%d-%m-%Y %H:%M:%S.%f")
            startTimeObj = datetime.strptime(startTime_str, '%d-%m-%Y %H:%M:%S.%f')
            newTimeObj = startTimeObj + timedelta(days=well_dict[i]['processing_time'])
            newTime = newTimeObj.strftime('%d-%m-%Y %H:%M:%S.%f')
            print(rigs_dictionary[0]['startTime'], well_dict[i]['processing_time'])
            well_dict_str = rigs_dictionary[0]['startTime'].strftime("%d-%m-%Y %H:%M:%S.%f")
            well_dict[i]['startTime'] = well_dict_str
            rigs_dictionary[0]['startTime'] = newTime
            print('sd', rigs_dictionary)
            print(well_dict[i]['processing_time'])
            well_dict[i]['endTime'] = newTime
            rigs_dictionary[0]['processing_time'] += well_dict[i]['processing_time']
    rigs_dictionary = sorted(rigs_dictionary, key=lambda x: (x['processing_time']))
    print('sodfljsd',rigs_dictionary)
    return rigs_dictionary,well_dict


def allocate_wells_to_rigs(rigs, wells, rigs_dictionary, wells_dictionary):
    wells_dict1 = []
    for dict in wells_dictionary:
        wells_dict1.append(dict)
    print(rigs)
    print(wells)
    print(rigs_dictionary)
    print(wells_dictionary)
    # assigned_wells = []
    # assigned_rigs = []
    while len(wells) > 0:
        for i in range(len(rigs)):

            print('remaining wells = ', wells)
            print('performing rig', rigs_dictionary[0]['rigs_locations'])
            distance_matrix = cdist(array([rigs_dictionary[0]['rigs_locations']]), wells, 'euclidean')
            print(distance_matrix)
            # to find minimum distance well for the rig
            sorted_distance_matrix = sorted(distance_matrix[0])
            print('sorted_distance_matrix = ', sorted_distance_matrix)

            rig_start_time = datetime.strptime(rigs_dictionary[0]['startTime'], '%d-%m-%Y %H:%M:%S.%f')
            print(rig_start_time, type(rig_start_time))
            # to check the rig_start_date and well_release_date also to find minimum distance well
            # rig_startTime is less than well end time
            for date in range(len(sorted_distance_matrix)):
                for distance in range(len(distance_matrix[0])):
                    if sorted_distance_matrix[date] == distance_matrix[0][distance]:
                        travelling_time = distance_matrix[0][distance]/18       #18km/hour
                        travelling_time = timedelta(hours = travelling_time)
                        print('travelling_time = ', travelling_time)
                        rig_start_time = rig_start_time + travelling_time
                        print('rig_start_time', rig_start_time)
                        well_start_time = datetime.strptime(wells_dict1[distance]['startTime'], '%d-%m-%Y')
                        well_end_time = datetime.strptime(wells_dict1[distance]['endTime'], '%d-%m-%Y')
                        print('seq', well_start_time, well_end_time)
                        if well_end_time >= rig_start_time >= well_start_time :
                            nearest_well = distance
                            min_distance = distance_matrix[0][distance]
                            print('nearest_well', nearest_well)
                            break
                else:
                    continue
                break
            print(well_start_time)
            # well_start_time = datetime.strptime(wells_dictionary[nearest_well]['startTime'], '%d-%m-%Y')
            print('hh', rig_start_time,well_start_time,well_end_time)
            # if rig_start_time >= well_start_time:

            print('kk', nearest_well,min_distance)
            # for assigned wells
            for k in range(len(wells_dictionary)):
                print('inner')
                print(wells)
                print(wells[nearest_well], wells_dictionary[k]['well_location'])
                if wells[nearest_well] == wells_dictionary[k]['well_location']:
                    rigs_dictionary[0]['assigned_wells'].append(wells_dictionary[k]['name'])
            print('minimum_distance, nearest well = ', min_distance, nearest_well)
            rigs_dictionary[0]['distances'].append(min_distance)
            # update rig location with corresponding minimum well location
            rigs_dictionary[0]['rigs_locations'] = wells[nearest_well]
            rigs_dictionary[0]['startTime'] = rig_start_time

            print('          ',rig_start_time)
            # rigs_dictionary[0]['startTime'] = wells_dictionary[nearest_well]['endTime']
            print('after assign rig',rigs_dictionary)
            # distance from final rig location to original location
            rigs_dictionary, wells_dictionary = early_completed(rigs_dictionary, wells_dictionary, wells[nearest_well])
            wells.pop(nearest_well)
            wells_dict1.pop(nearest_well)
            print('after delete well then rigs_dictionary',rigs_dictionary)
            # print('\n')
            if len(wells) == 0:
                break
    rigs_dictionary = sorted(rigs_dictionary, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
    rigs_dictionary = end_to_start_distance(rigs_dictionary, rigs)

    return rigs_dictionary, wells_dictionary


# # Example usage
rigs_locations = [(15.460098, 78.464362)]
wells_locations = [(15.480501, 78.484286), (15.479581, 78.481497), (15.479643, 78.486754), (15.478175, 78.491174), (15.476655, 78.487988), (15.473015, 78.481282),
                   (15.47164, 78.483385)]
# , (353, 276), (318, 854), (939, 529)
wells_dict = [{'name': 'well 1', 'processing_time': 2, 'well_location': (15.480501, 78.484286),
               'startTime':'05-04-2023','endTime':'14-04-2023'},
              {'name': 'well 2','processing_time': 2, 'well_location':  (15.479581, 78.481497),'startTime':'04-04-2023','endTime':'14-04-2023'},
         {'name': 'well 3', 'processing_time': 5, 'well_location': (15.479643, 78.486754),'startTime':'04-04-2023','endTime':'14-04-2023'},
        {'name': 'well 4', 'processing_time': 2, 'well_location': (15.478175, 78.491174),'startTime':'04-04-2023','endTime':'24-04-2023'},
         {'name': 'well 5', 'processing_time': 3, 'well_location': (15.476655, 78.487988),'startTime':'06-04-2023','endTime':'16-04-2023'},
        {'name': 'well 6', 'processing_time': 3, 'well_location': (15.473015, 78.481282),'startTime':'05-04-2023','endTime':'12-04-2023'},
         {'name': 'well 7', 'processing_time': 4, 'well_location': (15.47164, 78.483385),'startTime':'07-04-2023','endTime':'15-04-2023'}]
#, {'name': 'well 8', 'processing_time': 4, 'well_location': (353, 276)},
         #{'name': 'well 9', 'processing_time': 1, 'well_location': (318, 854)}, {'name': 'well 10', 'processing_time': 5, 'well_location': (939, 529)}]
rigs_dict = [{'name': 'Rig 1', 'processing_time': 0, 'rigs_locations': (15.460098, 78.464362), 'assigned_wells': [],
              'distances': [], 'mast_up': 2, 'startTime':'04-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'}

             ]

rigs_dict, wells_dict = allocate_wells_to_rigs(rigs_locations, wells_locations,rigs_dict,wells_dict)
print(rigs_dict)
print(wells_dict)

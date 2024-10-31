from scipy.spatial.distance import cdist
from numpy import array, ravel
import re
# r = [[0, 5], [1, 6], [2, 7], [3, 8], [4, 9]]
# for i in range(len(r)):
#     print(r[i][-1])

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

    for i in range(len(well_dict)):
        if well_dict[i]['well_location'] == nearest:
            rigs_dictionary[0]['processing_time'] += well_dict[i]['processing_time']
    rigs_dictionary = sorted(rigs_dictionary, key=lambda x: (x['processing_time']))
    print('sodfljsd',rigs_dictionary)
    return rigs_dictionary


def allocate_wells_to_rigs(rigs, wells, rigs_dictionary, wells_dictionary):
    print(rigs)
    print(wells)
    print(rigs_dictionary)
    print(wells_dictionary)
    # assigned_wells = []
    # assigned_rigs = []
    while len(wells) > 0:
        for i in range(len(rigs)-1):
            print(i)
            print('remaining wells = ', wells)
            print('performing rig', rigs_dictionary[0]['rigs_locations'])
            distance_matrix = cdist(array([rigs_dictionary[0]['rigs_locations']]), wells, 'euclidean')
            print(distance_matrix)
            # to find minimum distance well for the rig
            min_distance = float("inf")
            nearest_well = None
            for j in range(len(wells)):
                if distance_matrix[0][j] < min_distance:
                    min_distance = distance_matrix[0][j]
                    nearest_well = j
            # for assigned wells
            for k in range(len(wells_dictionary)):
                print('inner')
                print(wells[nearest_well], wells_dictionary[k]['well_location'])
                if wells[nearest_well] == wells_dictionary[k]['well_location']:
                    rigs_dictionary[0]['assigned_wells'].append(wells_dictionary[k]['name'])
            print('minimum_distance, nearest well = ', min_distance, nearest_well)
            rigs_dictionary[0]['distances'].append(min_distance)
            # update rig location with corresponding minimum well location
            rigs_dictionary[0]['rigs_locations'] = wells[nearest_well]
            print('after assign rig',rigs_dictionary)
            # distance from final rig location to original location
            rigs_dictionary = early_completed(rigs_dictionary, wells_dictionary, wells[nearest_well])
            wells.pop(nearest_well)
            print('after delete well then rigs_dictionary',rigs_dictionary)
            # print('\n')
            if len(wells) == 0:
                break
    rigs_dictionary = sorted(rigs_dictionary, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
    rigs_dictionary = end_to_start_distance(rigs_dictionary, rigs)

    return rigs_dictionary


# # Example usage
# rigs_locations = [(15.460098, 78.464362), (15.479684,78.477977), (15.485858, 78.485273)]
# wells_locations = [(15.480501, 78.484286), (15.479581, 78.481497), (15.479643, 78.486754), (15.478175, 78.491174), (15.476655, 78.487988), (15.473015, 78.481282),
#                    (15.47164, 78.483385)]
# # , (353, 276), (318, 854), (939, 529)
# wells_dict = [{'name': 'well 1', 'processing_time': 2, 'well_location': (15.480501, 78.484286),
#                'startTime':'04-04-2023','endTime':'14-04-2023'},
#               {'name': 'well 2','processing_time': 2.5, 'well_location':  (15.479581, 78.481497),'startTime':'04-04-2023','endTime':'14-04-2023'},
#          {'name': 'well 3', 'processing_time': 5, 'well_location': (15.479643, 78.486754),'startTime':'04-04-2023','endTime':'14-04-2023'},
#         {'name': 'well 4', 'processing_time': 2, 'well_location': (15.478175, 78.491174),'startTime':'04-04-2023','endTime':'14-04-2023'},
#          {'name': 'well 5', 'processing_time': 3, 'well_location': (15.476655, 78.487988),'startTime':'06-04-2023','endTime':'16-04-2023'},
#         {'name': 'well 6', 'processing_time': 3, 'well_location': (15.473015, 78.481282),'startTime':'04-04-2023','endTime':'14-04-2023'},
#          {'name': 'well 7', 'processing_time': 4, 'well_location': (15.47164, 78.483385),'startTime':'07-04-2023','endTime':'15-04-2023'}]
# #, {'name': 'well 8', 'processing_time': 4, 'well_location': (353, 276)},
#          #{'name': 'well 9', 'processing_time': 1, 'well_location': (318, 854)}, {'name': 'well 10', 'processing_time': 5, 'well_location': (939, 529)}]
# rigs_dict = [{'name': 'Rig 1', 'processing_time': 0, 'rigs_locations': (15.460098, 78.464362), 'assigned_wells': [],
#               'distances': [], 'mast_up': 2, 'startTime':'04-04-2023', 'endTime':'30-04-2023'},
#              {'name': 'Rig 2', 'processing_time': 0, 'rigs_locations': (15.460098, 78.464362), 'assigned_wells': [],
#               'distances': [], 'mast_up': 2, 'startTime':'04-04-2023', 'endTime':'02-05-2023'}]

rigs_locations = [(15.460098, 78.464362), (15.479684,78.477977), (15.485858, 78.485273)]
wells_locations = [(15.480501, 78.484286), (15.479581, 78.481497), (15.479643, 78.486754), (15.478175, 78.491174), (15.476655, 78.487988), (15.473015, 78.481282),
                   (15.47164, 78.483385)]
# , (353, 276), (318, 854), (939, 529)
wells_dict = [{'name': 'well 1', 'processing_time': 2, 'well_location': (15.480501, 78.484286),
               'startTime':'04-04-2023','endTime':'14-04-2023'},
              {'name': 'well 2','processing_time': 2, 'well_location':  (15.479581, 78.481497),'startTime':'04-04-2023','endTime':'14-04-2023'},
         {'name': 'well 3', 'processing_time': 5, 'well_location': (15.479643, 78.486754),'startTime':'04-04-2023','endTime':'14-04-2023'},
        {'name': 'well 4', 'processing_time': 2, 'well_location': (15.478175, 78.491174),'startTime':'04-04-2023','endTime':'14-04-2023'},
         {'name': 'well 5', 'processing_time': 3, 'well_location': (15.476655, 78.487988),'startTime':'06-04-2023','endTime':'16-04-2023'},
        {'name': 'well 6', 'processing_time': 3, 'well_location': (15.473015, 78.481282),'startTime':'04-04-2023','endTime':'14-04-2023'},
         {'name': 'well 7', 'processing_time': 4, 'well_location': (15.47164, 78.483385),'startTime':'07-04-2023','endTime':'15-04-2023'}]
#, {'name': 'well 8', 'processing_time': 4, 'well_location': (353, 276)},
         #{'name': 'well 9', 'processing_time': 1, 'well_location': (318, 854)}, {'name': 'well 10', 'processing_time': 5, 'well_location': (939, 529)}]
rigs_dict = [{'name': 'Rig 1', 'processing_time': 0, 'rigs_locations': (15.460098, 78.464362), 'assigned_wells': [],
              'distances': [], 'mast_up': 2, 'startTime':'04-04-2023', 'endTime':'30-04-2023'},
             {'name': 'Rig 2', 'processing_time': 0, 'rigs_locations': (15.460242, 78.464462), 'assigned_wells': [],
              'distances': [], 'mast_up': 2, 'startTime':'04-04-2023', 'endTime':'02-05-2023'}]

rigs_dict = allocate_wells_to_rigs(rigs_locations, wells_locations,rigs_dict,wells_dict)
print(rigs_dict)


import numpy as np
from datetime import datetime, timedelta
from Rig import Rig
from Well import Well
from scipy.spatial.distance import cdist
from numpy import array,ravel
import re
import math
from functools import reduce


class classify(object):

    def __init__(self,wells,rigs,rigname,algorithm_type):

        self.wells=wells
        self.rigs=rigs
        self.rigname=rigname
        self.algorithm_type = algorithm_type
    # assign low_drilling_wells to low_drilling_rigs based on depth capacity and distance between well and rig
    
    
    # assign wells to rigs based on distance between well and rig, well start time and end time

    def distance_mat(self,rigs, wells):
        #print(rigs,wells)
        rigs_list=[]
        for elem in rigs:
            #nums = elem.strip('()').split(',')
            #nums = [float(num) for num in nums]
            rigs_list.append(tuple(elem))
        wells_list=[]
        for elem in rigs:
            #nums = elem.strip('()').split(',')
            #nums = [float(num) for num in nums]
            wells_list.append(tuple(elem))      
        distance_matrix = cdist(rigs_list, wells_list, 'euclidean')
        return distance_matrix

    def end_to_start_distance(self,rigs_dictionary, rigs):
        for i in range(len(rigs_dictionary)):
            distance_matrix = self.distance_mat([rigs_dictionary[i]['rig_location']], [rigs[i]])
            distance = ravel(distance_matrix).tolist()
            rigs_dictionary[i]['distances'].append(distance[0])
        return rigs_dictionary

    def early_completed(self,rigs_dictionary, well_dict,nearest):

        # print('  rigs_dict', rigs_dictionary, well_dict, nearest)
        for i in range(len(well_dict)):
            # if well_dict[i]['well_location'] == list(nearest):
                print('msg')
                startTime_str = rigs_dictionary[0]['startTime'].strftime("%d-%m-%Y %H:%M:%S.%f")
                startTimeObj = datetime.strptime(startTime_str, '%d-%m-%Y %H:%M:%S.%f')
                newTimeObj = startTimeObj + timedelta(days=well_dict[i]['workoverTime'])
                newTime = newTimeObj.strftime('%d-%m-%Y %H:%M:%S.%f')
                # print(rigs_dictionary[0]['startTime'], well_dict[i]['workoverTime'])
                well_dict_str = rigs_dictionary[0]['startTime'].strftime("%d-%m-%Y %H:%M:%S.%f")
                well_dict[i]['startTime'] = well_dict_str
                rigs_dictionary[0]['startTime'] = newTime
                # print('sd', rigs_dictionary)
                # print(well_dict[i]['workoverTime'])
                well_dict[i]['endTime'] = newTime
                rigs_dictionary[0]['workoverTime'] += well_dict[i]['workoverTime']
        rigs_dictionary = sorted(rigs_dictionary, key=lambda x: (x['workoverTime']))
        # print('sodfljsd', rigs_dictionary)
        return rigs_dictionary, well_dict
    
    def allocate_wells_to_rigs(self,rigs, wells, rigs_dictionary, wells_dictionary):
        # print('welcome to allocate_wells_to_rigs')
        # print(rigs)
        # print(wells)
        # print(rigs_dictionary)
        # print(wells_dictionary)
        wells_dict1 = []
        for dict in wells_dictionary:
            wells_dict1.append(dict)
        # print(rigs)
        # print(wells)
        # print(rigs_dictionary)
        # print(wells_dictionary)
        # assigned_wells = []
        # assigned_rigs = []
        while len(wells) > 0:
            for i in range(len(rigs)):

                # print('remaining wells = ', wells)
                # print('performing rig', rigs_dictionary[0]['rig_location'])
                distance_matrix = cdist(array([rigs_dictionary[0]['rig_location']]), wells, 'euclidean')
                # print(distance_matrix)
                # to find minimum distance well for the rig
                sorted_distance_matrix = sorted(distance_matrix[0])
                # print('sorted_distance_matrix = ', sorted_distance_matrix)
                # print(rigs_dictionary[0]['startTime'])
                rig_start_time = datetime.strptime(rigs_dictionary[0]['startTime'], '%d-%m-%Y %H:%M:%S.%f')
                # to check the rig_start_date and well_release_date also to find minimum distance well
                # rig_startTime is less than well end time
                for date in range(len(sorted_distance_matrix)):
                    for distance in range(len(distance_matrix[0])):
                        if sorted_distance_matrix[date] == distance_matrix[0][distance]:
                            travelling_time = distance_matrix[0][distance] / 18  # 18km/hour
                            travelling_time = timedelta(hours=travelling_time)
                            # print('travelling_time = ', travelling_time)
                            rig_start_time = rig_start_time + travelling_time
                            # print('rig_start_time', rig_start_time)
                            well_start_time = datetime.strptime(wells_dict1[distance]['startTime'], '%d-%m-%Y')
                            well_end_time = datetime.strptime(wells_dict1[distance]['endTime'], '%d-%m-%Y')
                            # print('seq', well_start_time, well_end_time)
                            if well_end_time >= rig_start_time >= well_start_time:
                                nearest_well = distance
                                min_distance = distance_matrix[0][distance]
                                # print('nearest_well', nearest_well)
                                break
                    else:
                        continue
                    break
                # print(well_start_time)
                # well_start_time = datetime.strptime(wells_dictionary[nearest_well]['startTime'], '%d-%m-%Y')
                # print('hh', rig_start_time, well_start_time, well_end_time)
                # if rig_start_time >= well_start_time:

                # print('kk', nearest_well, min_distance)
                # for assigned wells
                for k in range(len(wells_dictionary)):
                    # print('inner')
                    # print(wells)
                    # print(wells[nearest_well], wells_dictionary[k]['well_location'])
                    if list(wells[nearest_well]) == wells_dictionary[k]['well_location']:
                        rigs_dictionary[0]['assigned_wells'].append(wells_dictionary[k]['name'])
                # print('minimum_distance, nearest well = ', min_distance, nearest_well)
                rigs_dictionary[0]['distances'].append(min_distance)
                # update rig location with corresponding minimum well location
                rigs_dictionary[0]['rigs_locations'] = wells[nearest_well]
                rigs_dictionary[0]['startTime'] = rig_start_time

                # print('          ', rig_start_time)
                # rigs_dictionary[0]['startTime'] = wells_dictionary[nearest_well]['endTime']
                # print('after assign rig', rigs_dictionary)
                # distance from final rig location to original location
                rigs_dictionary, wells_dictionary = self.early_completed(rigs_dictionary, wells_dictionary,
                                                                    wells[nearest_well])
                wells.pop(nearest_well)
                wells_dict1.pop(nearest_well)
                # print('after delete well then rigs_dictionary', rigs_dictionary)
                # print('\n')
                if len(wells) == 0:
                    break
        rigs_dictionary = sorted(rigs_dictionary, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
        rigs_dictionary = self.end_to_start_distance(rigs_dictionary, rigs)

        return rigs_dictionary, wells_dictionary

    
        
    def convert_string_to_tuple(self, locations):
        
        # new_loc = [[int(num) for num in s.strip('()').split(',')] for s in loc]
        #print('locations',locations)
        loc=[(float(coord[0]), float(coord[1])) for coord in locations]
        return loc
    # assign low_drilling_wells to low_drilling_rigs based on depth capacity and distance between well and rig
        
    # assign wells to rigs based on distance between well and rig
    def assign_wells_to_rigs(self, well_ids, rig_ids, distance_matrix):
        # create a dictionary with key as rig_id and value as list of well_ids
        rig_assignments = {}
        for rig_id in rig_ids:
            rig_assignments[rig_id] = []
        # assign wells to rigs based on distance
        for well_id in well_ids:
            # get the index of the well in the well_ids list
            well_index = well_ids.index(well_id)
            # get the distance of the well from each rig
            well_distances = distance_matrix[well_index]
            # get the index of the rig with the minimum distance
            rig_index = np.argmin(well_distances)
            # get the rig_id of the rig with the minimum distance
            rig_id = rig_ids[rig_index]
            # add the well_id to the list of well_ids assigned to the rig
            rig_assignments[rig_id].append(well_id)
        return rig_assignments
    def assign_low_drilling_wells(self, low_drilling_wells, low_drilling_rigs):
        low_drilling_rig_assignments = {}
        low_drilling_well_ids = [well['id'] for well in low_drilling_wells]
        low_drilling_rig_ids = [rig['name'] for rig in low_drilling_rigs]
        low_drilling_well_locations = [well['well_location'] for well in low_drilling_wells]
        low_drilling_rig_locations = [rig['rig_location'] for rig in low_drilling_rigs]
        low_drilling_rig_locations = self.convert_string_to_tuple(low_drilling_rig_locations)
        low_drilling_well_locations = self.convert_string_to_tuple(low_drilling_well_locations)
        first = np.array(low_drilling_well_locations)
        second = np.array(low_drilling_rig_locations)
##        print('first',first)
##        print('second',second)
        # print(first,second)
        low_drilling_distance_matrix = cdist(first, second, 'euclidean')
        #print(low_drilling_distance_matrix)
        low_drilling_rig_assignments = {}
       
        if self.algorithm_type==1:
            
            low_drilling_rig_assignments = self.assign_wells_to_rigs(low_drilling_well_ids, low_drilling_rig_ids,low_drilling_distance_matrix)
        elif self.algorithm_type==2:
           
            low_drilling_rig_assignments, low_drilling_wells = self.allocate_wells_to_rigs(low_drilling_rig_locations,low_drilling_well_locations,low_drilling_rigs,low_drilling_wells)
            #print('low.....................................',low_drilling_rig_assignments)
        return low_drilling_rig_assignments,low_drilling_wells
        
    def assign_mid_drilling_wells(self, mid_drilling_wells, mid_drilling_rigs):
        mid_drilling_rig_assignments = {}
        mid_drilling_well_ids = [well['id'] for well in mid_drilling_wells]
        mid_drilling_rig_ids = [rig['name'] for rig in mid_drilling_rigs]
        mid_drilling_well_locations = [well['well_location'] for well in mid_drilling_wells]
        mid_drilling_rig_locations = [rig['rig_location'] for rig in mid_drilling_rigs]
        # mid_drilling_distance_matrix = cdist(mid_drilling_well_locations, mid_drilling_rig_locations, 'euclidean')
        mid_drilling_rig_locations = self.convert_string_to_tuple(mid_drilling_rig_locations)
        mid_drilling_well_locations = self.convert_string_to_tuple(mid_drilling_well_locations)
        first = np.array(mid_drilling_well_locations)
        second = np.array(mid_drilling_rig_locations)
        #print(mid_drilling_rig_locations)
        #print(mid_drilling_well_locations)
        mid_drilling_distance_matrix = cdist(first, second, 'euclidean')
        #print(mid_drilling_distance_matrix)
        mid_drilling_rig_assignments = {}
        if self.algorithm_type==1:
            
            mid_drilling_rig_assignments = self.assign_wells_to_rigs(mid_drilling_well_ids, mid_drilling_rig_ids,mid_drilling_distance_matrix)
        elif self.algorithm_type==2:
           
            mid_drilling_rig_assignments, mid_drilling_wells = self.allocate_wells_to_rigs(mid_drilling_rig_locations,mid_drilling_well_locations,mid_drilling_rigs,mid_drilling_wells)
        return mid_drilling_rig_assignments,mid_drilling_wells

    def assign_high_drilling_wells(self, high_drilling_wells, high_drilling_rigs):
        high_drilling_rig_assignments = {}
        high_drilling_well_ids = [well['id'] for well in high_drilling_wells]
        high_drilling_rig_ids = [rig['name'] for rig in high_drilling_rigs]
        high_drilling_well_locations = [well['well_location'] for well in high_drilling_wells]
        high_drilling_rig_locations = [rig['rig_location'] for rig in high_drilling_rigs]
        # high_drilling_distance_matrix = cdist(high_drilling_well_locations, high_drilling_rig_locations, 'euclidean')
        high_drilling_rig_locations = self.convert_string_to_tuple(high_drilling_rig_locations)
        high_drilling_well_locations = self.convert_string_to_tuple(high_drilling_well_locations)
        first = np.array(high_drilling_well_locations)
        second = np.array(high_drilling_rig_locations)
        #print(high_drilling_rig_locations)
        #print(high_drilling_well_locations)
        high_drilling_distance_matrix = cdist(first, second, 'euclidean')
        #print(high_drilling_distance_matrix)
        high_drilling_rig_assignments = {}
        if self.algorithm_type==1:
            
            high_drilling_rig_assignments = self.assign_wells_to_rigs(high_drilling_well_ids, high_drilling_rig_ids,high_drilling_distance_matrix)
        elif self.algorithm_type==2:
            
            high_drilling_rig_assignments, high_drilling_wells = self.allocate_wells_to_rigs(high_drilling_rig_locations,high_drilling_well_locations,high_drilling_rigs,high_drilling_wells)
    
        return high_drilling_rig_assignments,high_drilling_wells
    # assign workover_wells to workover_rigs based on depth capacity and distance between well and rig
    def assign_workover_wells(self, workover_wells, workover_rigs):
        workover_rig_assignments = {}
        workover_well_ids = [well['id'] for well in workover_wells]
        workover_rig_ids = [rig['name'] for rig in workover_rigs]
        workover_well_locations = [well['well_location'] for well in workover_wells]
        workover_rig_locations = [rig['rig_location'] for rig in workover_rigs]
        # workover_distance_matrix = cdist(workover_well_locations, workover_rig_locations, 'euclidean')
        workover_rig_locations = self.convert_string_to_tuple(workover_rig_locations)
        workover_well_locations = self.convert_string_to_tuple(workover_well_locations)
        first = np.array(workover_well_locations)
        second = np.array(workover_rig_locations)
        #print(workover_rig_locations)
        #print(workover_well_locations)
        workover_distance_matrix = cdist(first, second, 'euclidean')
        #print(workover_distance_matrix)
        workover_rig_assignments = {}
        if self.algorithm_type==1:
            
            workover_rig_assignments = self.assign_wells_to_rigs(workover_well_ids, workover_rig_ids,workover_distance_matrix)
        elif self.algorithm_type==2:
           
            workover_rig_assignments, workover_wells = self.allocate_wells_to_rigs(workover_rig_locations, workover_well_locations,workover_rigs,workover_wells)
                
        return workover_rig_assignments, workover_wells

    def assign_rigs(self, clusters, low_drilling_rigs, low_drilling_wells):
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

        return drilling_rig_assignments

    def distance_between_wells(self, well1, well2):
        x1, y1 = well1['well_location']
        x2, y2 = well2['well_location']
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def distance_between_all_wells(self, low_drilling_wells):
        distances = []

        for i, well1 in enumerate(low_drilling_wells):
            cluster = []
            for j, well2 in enumerate(low_drilling_wells):
                if i != j:
                    distance = self.distance_between_wells(well1, well2)
                    # print(distance)
                    if distance <= 30:
                        cluster.append(well2['name'])

            distances.append(cluster)
        # print(distances)
        flat_list = list(set([item for sublist in distances for item in sublist]))
        return flat_list

    def category(self):
        rig_dict = [rig.dict() for rig in self.rigs]
        well_dict = [well.dict() for well in self.wells]
        drilling_rigs = []
        workover_rigs = []
        low_drilling_rigs = []
        mid_drilling_rigs = []
        high_drilling_rigs = []
        for rig in rig_dict:
            if rig["rig_type"] == "Drilling" and rig["depth_capacity"]>= 1500 and rig["horsepower"] >= 1200:
                drilling_rigs.append(rig)
            elif rig["rig_type"] == "Workover" and rig["depth_capacity"] <= 1500 and rig["horsepower"]<=1200:
                workover_rigs.append(rig)
        drilling_wells = []
        workover_wells = []
        #print('drilling  rigs and workover rigs',drilling_rigs,workover_rigs)
        
        for well in well_dict:
            if well["well_type"] == "Drilling" and well["depth_capacity"] >= 1500:
                drilling_wells.append(well)
            elif well["well_type"] == "Workover" and well["depth_capacity"] <= 1500:
                workover_wells.append(well)
        #print('drilling wells and workover wells',drilling_wells,workover_wells)
        for rig in drilling_rigs:
            if 1200 <= rig['horsepower'] <= 1500:
                low_drilling_rigs.append(rig)

            elif 1500 <= rig['horsepower'] <= 3000:
                mid_drilling_rigs.append(rig)
                
            elif 3000 <= rig['horsepower'] <= 5000:
                high_drilling_rigs.append(rig)
                

        print('low drilling rigs', low_drilling_rigs)
        print('medium drilling rigs',mid_drilling_rigs)
        print('hig drilling rigs',high_drilling_rigs)
        #print(ultra_high_drilling_rigs)
        low_drilling_wells = []
        mid_drilling_wells = []
        high_drilling_wells = []
        # ultra_high_drilling_wells = []
        # print(drilling_wells)
        for well in drilling_wells:
            if 1500 <= well['depth_capacity'] <= 6000:
                low_drilling_wells.append(well)
            elif 6000 <= well['depth_capacity'] <= 10000:
                mid_drilling_wells.append(well)
            elif 10000 <= well['depth_capacity'] <= 20000:
                high_drilling_wells.append(well)
        #print('low drilling rigs', low_drilling_rigs)
        print('low drilling wells',low_drilling_wells)
        print('medium drilling wells',mid_drilling_wells)
        print('hig drilling wells',high_drilling_wells)
        if(self.algorithm_type == 1):
            
            drilling_rig_assignments = []
            workover_rig_assignments = []

            low_drilling_rig_assignment, low_drilling_wells=self.assign_low_drilling_wells(low_drilling_wells, low_drilling_rigs)
            medium_drilling_rig_assignment, mid_drilling_wells=self.assign_mid_drilling_wells(mid_drilling_wells, mid_drilling_rigs)
            high_drilling_rig_assignment, high_drilling_wells=self.assign_high_drilling_wells(high_drilling_wells, high_drilling_rigs)
            print("Drilling Rig Assignments:")
            drilling_rig_assignments.append(low_drilling_rig_assignment)
            drilling_rig_assignments.append(medium_drilling_rig_assignment)
            drilling_rig_assignments.append(high_drilling_rig_assignment)
            print(drilling_rig_assignments)
            print("\nWorkover Rig Assignments:")
            
            workover_rig_assignments, workover_wells=self.assign_workover_wells(workover_wells, workover_rigs)
            print(workover_rig_assignments)
            drilling_rig_assignments = reduce(lambda x, y: {**x, **y}, drilling_rig_assignments)

            # Define the workover rig assignments dictionary
            # workover_rig_assignments = {'Rig3': ['7'], 'Rig4': ['5', '9']}

            # Combine the drilling rig and workover rig assignments into a single dictionary
            
            combined_assignments = {**drilling_rig_assignments, **workover_rig_assignments}

            # Convert the values from strings to integers
            for rig, assignments in combined_assignments.items():
                combined_assignments[rig] = [int(x) for x in assignments]

            # Sort the keys in alphabetical order based on rig number
            result = {k: combined_assignments[k] for k in sorted(combined_assignments)}

            #print('result = ', result)
        elif(self.algorithm_type == 2):
            overall_rig_assignments = []
            # workover_rig_assignments = []
            #print("type 2..........................................")
            # print('for testing', low_drilling_rigs)
            flat_list = self.distance_between_all_wells(low_drilling_wells)
            print("cluster wells are", flat_list)
            print('low drilling wells after cluster', low_drilling_wells)
            print('low drilling rigs after cluster', low_drilling_rigs)
            rig_assignment = self.assign_rigs(flat_list, low_drilling_rigs, low_drilling_wells)
            print("cluster wells are", flat_list)
            print('low drilling wells after cluster', low_drilling_wells)
            print('low drilling rigs after cluster', low_drilling_rigs)



            low_drilling_rig_assignment, low_drilling_wells=self.assign_low_drilling_wells(low_drilling_wells, low_drilling_rigs)
            medium_drilling_rig_assignment, mid_drilling_wells=self.assign_mid_drilling_wells(mid_drilling_wells, mid_drilling_rigs)
            high_drilling_rig_assignment, high_drilling_wells=self.assign_high_drilling_wells(high_drilling_wells, high_drilling_rigs)
##            print('lowdrillingwells', low_drilling_rig_assignment)
##            print('mediumdrillingwells', medium_drilling_rig_assignment)
##            print('higdrillingwells', high_drilling_rig_assignment)
            #print("Drilling Rig Assignments:")
            workover_rig_assignments, workover_wells = self.assign_workover_wells(workover_wells, workover_rigs)
            # print('low_drilling_rig_assignment', low_drilling_rig_assignment)
            overall_rig_assignments.append(low_drilling_rig_assignment)
            overall_rig_assignments.append(medium_drilling_rig_assignment)
            overall_rig_assignments.append(high_drilling_rig_assignment)
            overall_rig_assignments.append(workover_rig_assignments)
            overall_rig_assignments = [rig for rig_list in overall_rig_assignments for rig in rig_list]
            # print('ss', overall_rig_assignments)
            overall_rig_assignments = sorted(overall_rig_assignments, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
            #print(overall_rig_assignments)
            #print("\noverall Rig Assignments:")
            #print(overall_rig_assignments)
            assigned_wells = {}
            for rig in overall_rig_assignments:
                for well in rig['assigned_wells']:
                    assigned_wells[well[4:]] = rig['name']
            result = {}
            for key, value in assigned_wells.items():
                if value not in result:
                    result[value] = [key]
                else:
                    result[value].append(key)
            #print('result = ', result)
            
        return result
class nextclosestwell:
    def __init__(self, distance, start):
        self.distance_matrix = distance
        self.start_city = start
        self.total_cities = len(distance)
        self.end_state = (1 << self.total_cities) - 1
        self.memo = [[None for _col in range(1 << self.total_cities)] for _row in range(self.total_cities)]

        self.shortest_path = []
        self.min_path_cost = float('inf')

    def solve(self):
        self.__initialize_memo()

        for num_element in range(3, self.total_cities + 1):

            for subset in self.__initiate_combination(num_element):

                if self.__is_not_in_subset(self.start_city, subset):
                    continue

                for next_city in range(self.total_cities):

                    if next_city == self.start_city or self.__is_not_in_subset(next_city, subset):
                        continue

                    subset_without_next_city = subset ^ (1 << next_city)
                    min_distance = float('inf')

                    for last_city in range(self.total_cities):

                        if last_city == self.start_city or \
                                last_city == next_city or \
                                self.__is_not_in_subset(last_city, subset):
                            continue

                        new_distance = \
                            self.memo[last_city][subset_without_next_city] + self.distance_matrix[last_city][next_city]

                        if new_distance < min_distance:
                            min_distance = new_distance

                    self.memo[next_city][subset] = min_distance

        self.__calculate_min_cost()
        self.__find_shortest_path()

    def __calculate_min_cost(self):
        for i in range(self.total_cities):

            if i == self.start_city:
                continue

            path_cost = self.memo[i][self.end_state]

            if path_cost < self.min_path_cost:
                self.min_path_cost = path_cost

    def __find_shortest_path(self):
        state = self.end_state

        for i in range(1, self.total_cities):
            best_index = -1
            best_distance = float('inf')

            for j in range(self.total_cities):

                if j == self.start_city or self.__is_not_in_subset(j, state):
                    continue

                new_distance = self.memo[j][state]

                if new_distance <= best_distance:
                    best_index = j
                    best_distance = new_distance

            self.shortest_path.append(best_index)
            state = state ^ (1 << best_index)

        self.shortest_path.append(self.start_city)
        self.shortest_path.reverse()

    def __initialize_memo(self):
        for destination_city in range(self.total_cities):

            if destination_city == self.start_city:
                continue

            self.memo[destination_city][1 << self.start_city | 1 << destination_city] = \
                self.distance_matrix[self.start_city][destination_city]

    def __initiate_combination(self, num_element):
        subset_list = []
        self.__initialize_combination(0, 0, num_element, self.total_cities, subset_list)
        return subset_list

    def __initialize_combination(self, subset, at, num_element, total_cities, subset_list):

        elements_left_to_pick = total_cities - at
        if elements_left_to_pick < num_element:
            return

        if num_element == 0:
            subset_list.append(subset)
        else:
            for i in range(at, total_cities):
                subset |= 1 << i
                self.__initialize_combination(subset, i + 1, num_element - 1, total_cities, subset_list)
                subset &= ~(1 << i)

    @staticmethod
    def __is_not_in_subset(element, subset):
        return ((1 << element) & subset) == 0
    
class Scheduler(object):

    def __init__(self,rigs,wells,schedulerStartTime,algorithm_type):
        self.rigs = rigs
        self.wells = wells
        self.schedulerStartTime = schedulerStartTime
        self.algorithm_type=algorithm_type
        
    def getRigName(self):
        return [rig.name for rig in self.rigs]

    def getRigmastupTime(self):
        return [rig.mastupTime for rig in self.rigs]
    
    def getRigmastdownTime(self):
        return [rig.mastdownTime for rig in self.rigs]
    
    def getWellProductionRate(self):
        return [well.productionRate for well in self.wells]
    
    def getWellStartTime(self):
        return [well.startTime for well in self.wells]

    def getWellEndTime(self):
        return [well.endTime for well in self.wells]
    
    def getWellWorkoverTime(self):
        return [well.workoverTime for well in self.wells]

    def getWellPriorities(self):
        return [well.priority for well in self.wells]

    def getWellLocation(self):
        return [well.well_location for well in self.wells]
    
    def getWellLossFactor(self):
        return [well.lossFactor for well in self.wells]
    
    def getRigLocation(self):
        return [rig.rig_location for rig in self.rigs]
    
    def getRigSpeed(self):
        return [rig.speed for rig in self.rigs]

    def getRigMaintance(self):
        return [rig.rig_maintance for rig in self.rigs]
    
    def getRigInitStatus(self):
        return [rig.rig_init_status for rig in self.rigs]
    
    def add_hours_to_now(self,hours):
        import datetime
        result = datetime.timedelta(hours=hours)
        return result
    
    def schedule(self, r_final,wells, rigs,t_opt,r_name):
##        print('final..............',r_final)
##        print(r_name)
##        print(rigs)
        wells_dict = []
        sorted_Wells=wells
        sorted_rigs=rigs
        schedulerStartTime=self.schedulerStartTime
        mastupTime=self.getRigmastupTime()
        mastdownTime=self.getRigmastdownTime()
        wellstartTime=self.getWellStartTime()
        #print(wellstartTime)
        wellendTime=self.getWellEndTime()
        #print(wellendTime)
        maintance=self.getRigMaintance()
        rig_state=self.getRigInitStatus()
        for j in range(len(r_final)):
##          s = date_function.today()
##          date =s.strftime("%d-%m-%Y %H:%M:%S.%f")
            #currentDate = datetime.strptime(date,"%d-%m-%Y %H:%M:%S.%f")
            state=rig_state[j]
            if state=='mastDown':
                currentDate = schedulerStartTime
                rigs=sorted_rigs
                # Get the next well to be processed
                r1=r_final[j]
                #print('r11 = ', r1)
                k=r_name[j][3:]
                #print('name...',k)
                rig=rigs[int(k)-1]
                #print('              ', rig)
                t_time=t_opt[j]
                while len(r1)>0 :
                    well = sorted_Wells[r1.pop(0)]
                    #print(well)
                    time=t_time.pop(0)
                    result=self.add_hours_to_now(time)
                    # Assign the well to the rig
                    # travel time from rig to well or well to well
                    if self.algorithm_type==1:
                        rig['assigned_wells'].append(well['id'])
                    begin=currentDate+result
                    w_startTime=well['startTime']
                    rig['arrivalTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['mastupStartTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    # Update the rig's processing time
                    rig['workoverTime']=well['workoverTime']
                    # Assign the well startTime to the rig
                    start1=begin+timedelta(hours=mastupTime[j])
                    rig['mastupEndTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['interventionStartTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    process_days=well['workoverTime']
                    endTime = start1+ timedelta(days=process_days)
                    rig['interventionEndTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['mastdownStartTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    mastendTime = start1+ timedelta(days=process_days)+timedelta(hours=mastdownTime[j])
                    # Assign the well endTime to the rig
                    rig['mastdownEndTime'].append(mastendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['maintanceStartTime'].append(mastendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    maintanceendTime=mastendTime+timedelta(hours=maintance[j])
                    rig['maintanceEndTime'].append(maintanceendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    currentDate=datetime.strptime(rig['maintanceEndTime'][-1], "%d-%m-%Y %H:%M:%S.%f")
                returnTime=endTime+self.add_hours_to_now(t_time.pop(0))
                rig['returnTime'].append(returnTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                temp = []
                #print('assigned wells = ', rig['assigned_wells'])
                for i in range(len(rig['assigned_wells'])):
                   
                    if i<len(rig['assigned_wells'])-1:
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'mastupStartTime':rig['mastupStartTime'][i],
                                 'mastupEndTime':rig['mastupEndTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'mastdownStartTime':rig['mastdownStartTime'][i],
                                 'mastdownEndTime':rig['mastdownEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i]})
                    if i==len(rig['assigned_wells'])-1:
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'mastupStartTime':rig['mastupStartTime'][i],
                                 'mastupEndTime':rig['mastupEndTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'mastdownStartTime':rig['mastdownStartTime'][i],
                                 'mastdownEndTime':rig['mastdownEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i],'returnTime': rig['returnTime'].pop(0)})                    
                #print("rig: "+str(j)+"--> "+str(temp))
                
                print(r_name[j]+"--> "+str(temp))
            else:
                currentDate = schedulerStartTime
                rigs=sorted_rigs
                # Get the next well to be processed
                r1=r_final[j]
                #print('r1 = ', r1)
                k=r_name[j][3:]
                #print('name...',k)
                rig=rigs[int(k)-1]
                #print(rig)
                t_time=t_opt[j]
                while len(r1)>0 :
                    well = sorted_Wells[r1.pop(0)]
                    #print(well)
                    time=t_time.pop(0)
                    result=self.add_hours_to_now(time)
                    # Assign the well to the rig
                    # travel time from rig to well or well to well
                    if self.algorithm_type==1:
                        rig['assigned_wells'].append(well['id'])
                    begin=currentDate+result
                    rig['arrivalTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    # Update the rig's processing time
                    rig['workoverTime']=well['workoverTime']
                    # Assign the well startTime to the rig
                    rig['interventionStartTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    process_days=well['workoverTime']
                    endTime = begin+ timedelta(days=process_days)
                    rig['interventionEndTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    # Assign the well endTime to the rig
                    rig['maintanceStartTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    maintanceendTime=endTime+timedelta(hours=maintance[j])
                    rig['maintanceEndTime'].append(maintanceendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    currentDate=datetime.strptime(rig['maintanceEndTime'][-1], "%d-%m-%Y %H:%M:%S.%f")
                returnTime=endTime+self.add_hours_to_now(t_time.pop(0))
                rig['returnTime'].append(returnTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                temp = []
                #print(rig)
                for i in range(len(rig['assigned_wells'])):
               
                    if i<len(rig['assigned_wells'])-1:
                        #print('plus')
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i]})
                    if i==len(rig['assigned_wells'])-1:
                        #print('minus')
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i],'returnTime': rig['returnTime'].pop(0)})                    
                #print("rig: "+str(j)+"--> "+str(temp))
                print(r_name[j]+"--> "+str(temp))
        pass
        
    def cost(self,w_1,d_1,r,f,Vwr,state,mastupTime,mastdownTime,maintanceTime):
        #test = df_mat_dist.sort_values(index, ascending=True)
        tw1=[]
        F1=[]
        Q1=[]
        productionRate=self.getWellProductionRate()
        Q = list(productionRate)
        loss_factor=self.getWellLossFactor()
        F=list(loss_factor)
        workover=self.getWellWorkoverTime()
        tw=list(workover)
        Ctad=15 # a flat fee for transport, assemply and disassembly
        cd= 0.072 # distance fee ecmp/h
        ct=2.16 # worktime fee ecmp/h
        #Vwr=30 # Velocity in km/h
        for i in w_1 :
            tw1.append(tw[i-1])
            F1.append(F[i-1])
            Q1.append(Q[i-1])
        R=[]
        C=[]
        K1=0
        tsi=[]
        tt=[]
        for m in range(len(r[f])):
            if state=="mastUp" :
                R.append(Q1[m]*F1[m]*73.23)
                K=8.5+((0.072*d_1[m])+(2.16*tw1[m]))
                C.append(K*73.23)
                T=(d_1[m]/Vwr)
                K1=K1+T+tw1[m]+maintanceTime
                tsi.append(K1)
                tt.append(T)
            else :
                R.append(Q1[m]*F1[m]*73.23)
                K=15+((0.072*d_1[m])+(2.16*tw1[m]))
                C.append(K*73.23)
                T=(d_1[m]/Vwr)
                K1=K1+T+tw1[m]+mastupTime+mastdownTime+maintanceTime
                tsi.append(K1)
                tt.append(T)
        Li=np.multiply(R,tsi)
        Tot_loss=np.sum(np.add(C,Li))
        return Tot_loss,tt,Li,C
    
    def solveNCW(self,r,sample,sample1,wellsDict,rigsDict,r_name):
        #print("solvencw")
        #print(r,sample,sample1,wellsDict,rigsDict,r_name)
        w1_opt=[]
        d_opt=[]
        t_opt=[]
        total_loss=[]
        sample3=[]
        rigs=rigsDict
        rig_state=self.getRigInitStatus()
        mastupTime=self.getRigmastupTime()
        mastdownTime=self.getRigmastdownTime()
        maintanceTime=self.getRigMaintance()
        Li_final=[]
        C_final=[]
        for f in range(len(r)) :
            sample3.append(sample[f])
            Loss=0
            sample4=[]
            Vwr=rigs[f]['speed']
            state=rig_state[f]
            global C
            global Li
            global tt
            global Tot_loss
            global w_opt
            global d1_opt
            global tt_opt
            global Min_loss
            for k in range(len(r[f])):
                start_city=k
                sample2=[]
                sample5=[]
                for x in r[f]:
                    sample2.append(sample1[x])
                distance_matrix = cdist(sample2, sample2, 'euclidean')
                tour = nextclosestwell(distance_matrix, start_city)
                tour.solve()
                w_1=tour.shortest_path
                sample4.append(sample2[w_1[0]])
                #print(sample3,sample4)
                distance=cdist(sample3,sample4,'euclidean')
                d_1=[]
                d_1.append(distance.tolist()[0][0])
                for j in range(len(r[f])-1):
                    d_1.append(distance_matrix[w_1[j]][w_1[j+1]])
                Tot_loss,tt,Li,C=self.cost(w_1,d_1,r,f,Vwr,state,mastupTime[f],mastdownTime[f],maintanceTime[f])
                if k==0 :
                  Min_loss=Tot_loss
                  w_opt=w_1
                  d1_opt=d_1
                  tt_opt=tt
                  sample5.append(sample2[w_opt[-1]])
                  #print(sample3,sample5)
                  distance_1=cdist(sample3,sample5,'euclidean')
                  d1_opt.append(distance_1.tolist()[0][0])
                elif Tot_loss<Min_loss :
                  Min_loss=Tot_loss
                  w_opt=w_1
                  d1_opt=d_1
                  tt_opt=tt
                  sample5.append(sample2[w_opt[-1]])
                  #print(sample3,sample5)
                  distance_1=cdist(sample3,sample5,'euclidean')
                  d1_opt.append(distance_1.tolist()[0][0])
                sample4=[]
            #print('Optimum well sequence and its Minimum total loss')
            #print(w_opt,d1_opt,Min_loss)
            w1_opt.append(w_opt)
            d_opt.append(d1_opt)
            tt_opt.append(d_opt[f][-1]/Vwr)
            t_opt.append(tt_opt)
            sample3=[]
            Li_final.append(Li)
            C_final.append(C)
            total_loss.append(Min_loss)
        #print(w1_opt)
        #print(d_opt)
        #print("travel times :", t_opt)    
        r_final=[]
        k=0
        for y in w1_opt :
            r1_opt=[]
            for i in y:
                r1_opt.append(r[k][i])
            k=k+1
            r_final.append(r1_opt) 
        print("optimal well sequence :", r_final)
        #print("distance sequence :", d_opt)
        self.schedule(r_final,wellsDict,rigsDict,t_opt,r_name)
        print("$ 73.23 per barrel of oil/patroleum")
        print('Well revenue Loss in US$:',Li_final)
        print('Rig cost in US$:',C_final)
        print('Rig wise total cost US$:',total_loss)
        print('total loss in US$:',np.sum(total_loss))
        pass
    
    def Convert(self,string):
        M=len(string)
        string=string[1:M-1]
        string.strip()
        li = list(string.split(","))
        return li
    def string_to_tuple(lists):
        result=[]
        for elem in lists:
            nums = elem.strip('()').split(',')
            nums = [float(num) for num in nums]
            result.append(tuple(nums))
        return result
    def distance_mat(self,rigs, wells):
        #print(rigs,wells)
        rigs_list=[]
        for elem in rigs:
            #nums = elem.strip('()').split(',')
            #nums = [float(num) for num in nums]
            rigs_list.append(tuple(elem))
        wells_list=[]
        for elem in rigs:
            #nums = elem.strip('()').split(',')
            #nums = [float(num) for num in nums]
            wells_list.append(tuple(elem))      
        distance_matrix = cdist(rigs_list, wells_list, 'euclidean')
        return distance_matrix

    def end_to_start_distance(self,rigs_dictionary, rigs):
        for i in range(len(rigs_dictionary)):
            distance_matrix = self.distance_mat([rigs_dictionary[i]['rig_location']], [rigs[i]])
            distance = ravel(distance_matrix).tolist()
            rigs_dictionary[i]['distances'].append(distance[0])
        return rigs_dictionary

    def early_completed(self,rigs_dictionary, well_dict,nearest):
        
        for i in range(len(well_dict)):
            if well_dict[i]['well_location'] == nearest:
                rigs_dictionary[0]['workoverTime'] += well_dict[i]['workoverTime']
        rigs_dictionary = sorted(rigs_dictionary, key=lambda x: (x['workoverTime']))
        return rigs_dictionary
    
    def allocate_wells_to_rigs(self,rigs, wells, rigs_dictionary, wells_dictionary):
        #print(rigs_dictionary)
        assigned_wells = []
        assigned_rigs = []
##        print('Welcome')
##        print(wells)
##        print(wells_dictionary)
##        print(rigs)
##        print('hai')
        while len(wells) > 0:
            for i in range(len(rigs)):
                
                result=[]
                for elem in wells:
                    
                    # nums = elem.strip('()').split(',')
                    # nums = [float(num) for num in nums]
                    result.append(tuple(elem))
##                print(wells)
                # print(result)
                #print(result1)
                #rigs_dictionary[0]['rig_location'] = [tuple(map(float, rigs_dictionary[0]['rig_location'].strip('()').split(',')))]
                #print(
                #print(tuple(rigs_dictionary[0]['rig_location']))
                ad = [tuple(rigs_dictionary[0]['rig_location'])]
        
                distance_matrix = cdist(ad, result, 'euclidean')#tuple(rigs_dictionary[0]['rig_location'])
##                print("hai")
##                print(distance_matrix)
                min_distance = float("inf")
                nearest_well = None
                for j in range(len(wells)):
                    if distance_matrix[0][j] < min_distance:
                        min_distance = distance_matrix[0][j]
                        nearest_well = j
                # for assigned wells
                for k in range(len(wells_dictionary)):
                    if wells[nearest_well] == wells_dictionary[k]['well_location']:
                        rigs_dictionary[0]['assigned_wells'].append(wells_dictionary[k]['id'])
##                print('minimum_distance, nearest well = ', min_distance, nearest_well)
##                print("hai")
                rigs_dictionary[0]['distances'].append(min_distance)
                rigs_dictionary[0]['rig_location'] = wells[nearest_well]
                rigs_dictionary = self.early_completed(rigs_dictionary, wells_dictionary, wells[nearest_well])
                wells.pop(nearest_well)
##                print(rigs_dictionary)
##                print('\n')
                if len(wells) == 0:
                    break
        rigs_dictionary = sorted(rigs_dictionary, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
        rigs_dictionary = self.end_to_start_distance(rigs_dictionary,rigs)
        #print(rigs_dictionary)
        return rigs_dictionary
    def well_assign(self):
        wells_location=self.getWellLocation()
        rigs_location=self.getRigLocation()
        rig_speed=self.getRigSpeed()
        rigname=self.getRigName()
        wellsDict = [well.dict() for well in self.wells]
        #print(wellsDict)
        rigsDict = [rig.dict() for rig in self.rigs]
        #print(rigsDict)
        c=list(rigs_location)
        c1=list(wells_location)
        file1=[]
        self.sample1=[]
        for i in c:
          #print(i)
          #k=self.Convert(i)
          file1.append(i)
        file2=[]
        for i in c1:
          #k=self.Convert(i)
          file2.append(i)
        sample = []
        for i in file1:
            sample.append((float(i[0]),float(i[1] )))
        #print(*[f"({w:.2f}, {h:.2f})" for w, h in sample], sep=', ')
        sample1 = []
        for i in file2:
            sample1.append((float(i[0]),float(i[1] )))
        if self.algorithm_type == 1:
            # Code for Round-robin method
            idx=classify(self.wells, self.rigs,rigname,self.algorithm_type)
            solution=idx.category()
            r1 = [[int(num) for num in sublist] for sublist in solution.values()]
            r_name= [str(sublist)  for sublist in solution.keys()]
            # print("Classification plus shortest distance selected")
        elif self.algorithm_type == 2:
            # Code for Classification plus shortest distance
            idx=classify(self.wells, self.rigs,rigname,self.algorithm_type)
            rigs_dict=idx.category()
            r1 = [[int(num)-1 for num in sublist] for sublist in rigs_dict.values()]
            r_name= [str(sublist)  for sublist in rigs_dict.keys()]
            # print('r', rigs_dict)
##            r1=[]
##            r_name=[]
##            for assign in rigs_dict:
##                b=[]
##                print(assign['assigned_wells'])
##                for w in assign['assigned_wells']:
##                    b.append(int(w))
##                r1.append(b)
##                r_name.append(assign['name'])
            print("Classification plus Round-robin method selected")
        else:
            # Invalid input
            print("Invalid algorithm type. Please enter 1 or 2.")
##        rig_pos=sample
##        well_pos=sample1
##        minimumlist = []
##        original_list = []
##        out = []
##        distance = cdist(sample1, sample, 'euclidean')
##        for i in range(len(well_pos)):
##          (m,i) = min((v,i) for i,v in enumerate(distance[i]))
##          # print('well',i+1,'---->','rig',minimumlist.index(min_lst)+1)
##          original_list.append(m)
##          output = (i,m)
##          out.append(output)
##          minimumlist.clear()
##        len_lst = []
##        for _ in out:
##          _ = list(_)
##          if _[1] not in len_lst:
##            len_lst.append(_[1])
##        # to create lists for rigs
##        lists = {}
##        for i in range(len(len_lst)):
##            lists[f"rig_{i}"] = []
##        for _ in range(len(out)):
##          lk = list(out[_])
##          rig = "rig_" + str(lk[0])
##          k = lists[rig]
##          k.append(_)
##          lists[rig] = k      
##        idx=classify(self.wells, self.rigs,rigname)
##        solution=idx.category()
##        r = [[int(num) for num in sublist] for sublist in solution.values()]
##        print(r)
##        r_name= [str(sublist)  for sublist in solution.keys()]
##        print(r_name)
        #print(r_name)
        #print("Rig wise well assignment :", r)
        # Create a dictionary with rigs as keys and lists as values
        my_dict = dict(zip(r_name, r1))

        # Remove empty lists and their respective rigs using dictionary comprehension
        my_dict = {k: v for k, v in my_dict.items() if v}

        # Convert dictionary back to separate lists
        r_name = list(my_dict.keys())
        r = list(my_dict.values())
##      result = {k:v for k,v in rigs_dict.items() if v}
##      r=[v  for  v in  result.values()]
##      r_name=[k  for  k in  result.keys()]
##        print(r)
##        print(r_name)
        return self.solveNCW(r,sample,sample1,wellsDict,rigsDict,r_name)        
if __name__ == "__main__":
    StartTime = input("enter scheduler StartTime in this format dd-mm-yyyy")
    algorithm_type = int(input("Enter the algorithm type (1 for Classification plus shortest distance, 2 for Round-robin method ): "))
    schedulerStartTime=datetime.strptime(StartTime, "%d-%m-%Y")
    #print(schedulerStartTime)
    rig1 = Rig("1","Rig1","Drilling", 9200,2600,10,15000,{'rig_location':[100 , 110],'rig_maintance':4,'rig_init_status':'mastUp', 'startTime':'04-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'})
    rig2 = Rig("2","Rig2","Drilling", 19260,4500,12,20000,{'rig_location':[110 , 115],'rig_maintance':4,'rig_init_status':'mastDown', 'startTime':'04-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'})
    rig3 = Rig("3","Rig3","Workover", 1400,1150,5,8000,{'rig_location':[150 , 190],'rig_maintance':4,'rig_init_status':'mastUp', 'startTime':'05-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'})
    rig4 = Rig("4","Rig4","Workover", 1300,1100,6,9000,{'rig_location':[100 , 200],'rig_maintance':4,'rig_init_status':'mastDown', 'startTime':'04-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'})
    
    # rig5 = Rig("5","Rig5","Workover", 1200,1160,5,7000,{'rig_location':'(100 , 110)','rig_maintance':4,'rig_init_status':'mastUp'})
    rig5 = Rig("5","Rig5","Drilling", 5200,1400,6,9000,{'rig_location':[100 , 120],'rig_maintance':4,'rig_init_status':'mastDown', 'startTime':'04-04-2023 00:00:00.00', 'endTime':'30-04-2023 00:00:00.00'})
    rig6 = Rig("6", "Rig6", "Drilling", 5300, 1400, 6, 9000,
               {'rig_location': [105, 125], 'rig_maintance': 4, 'rig_init_status': 'mastDown',
                'startTime': '04-04-2023 00:00:00.00', 'endTime': '30-04-2023 00:00:00.00'})

    # rig7 = Rig("7","Rig7","Drilling", 18000,5000,5,7000,{'rig_location':'(100 , 110)','rig_maintance':4,'rig_init_status':'mastUp'})

##    well1 = Well("0","well1","Drilling", 2000,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 2,'priority' : 2,'well_location':'(307 , 917)','lossFactor':0.24})
    well1 = Well('0', 'well1', 'Drilling', 5100, {'startTime':'04-04-2023','endTime':'14-04-2023', 'workoverTime': 2, 'priority': 4, 'well_location': [150 , 110], 'lossFactor': 0.26})
    well2 = Well('1', 'well2', 'Drilling', 9000, {'startTime':'05-04-2023','endTime':'19-04-2023', 'workoverTime': 3, 'priority': 1, 'well_location': [110 , 125], 'lossFactor': 0.14})
    well3 = Well('2', 'well3', 'Drilling', 5000, {'startTime':'04-04-2023','endTime':'18-04-2023', 'workoverTime': 2, 'priority': 5, 'well_location': [120 , 125], 'lossFactor': 0.38})
    well4= Well('3', 'well4', 'Drilling', 7642, {'startTime':'04-04-2023','endTime':'16-04-2023', 'workoverTime': 3, 'priority': 5, 'well_location': [115 , 120], 'lossFactor': 0.48})
    well5 = Well('4', 'well5', 'Drilling', 10219, {'startTime':'06-04-2023', 'endTime':'15-04-2023', 'workoverTime': 3, 'priority': 3, 'well_location': [125, 130], 'lossFactor': 0.11})
    well6 = Well('5', 'well6', 'Workover', 1200, {'startTime':'04-04-2023','endTime':'19-04-2023', 'workoverTime': 2, 'priority': 1, 'well_location': [130 , 145], 'lossFactor': 0.41})
    well7 = Well('6', 'well7', 'Drilling', 14637, {'startTime':'04-04-2023','endTime':'17-04-2023', 'workoverTime': 5, 'priority': 5, 'well_location': [123 , 135], 'lossFactor': 0.27})
    well8 = Well('7', 'well8', 'Workover', 1300, {'startTime':'05-04-2023','endTime':'14-04-2023', 'workoverTime': 4, 'priority': 5, 'well_location': [120 , 125], 'lossFactor': 0.23})
    well9 = Well('8', 'well9', 'Drilling', 8000, {'startTime':'04-04-2023','endTime':'13-04-2023', 'workoverTime': 2, 'priority': 1, 'well_location': [140 , 155], 'lossFactor': 0.17})
    well10 = Well('9', 'well10', 'Workover', 800, {'startTime':'07-04-2023','endTime':'24-04-2023', 'workoverTime': 4, 'priority': 5, 'well_location': [150 , 115], 'lossFactor': 0.1})
##    well10 = Well("9","well10","Workover",1450,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 4,'priority' : 10,'well_location':[52.33704737951449,24.50588349616796],'lossFactor':0.48})
    well11 = Well("10","well11","Drilling", 2250,{'startTime':'08-04-2023','endTime':'23-04-2023','workoverTime' : 3,'priority' : 6 ,'well_location':[120,114],'lossFactor':0.51})
    well12 = Well("11","well12","Workover", 1100,{'startTime':'04-04-2023','endTime':'26-04-2023', 'workoverTime' : 2,'priority' : 9,'well_location':[55,84.],'lossFactor':0.93})
    well13 = Well("12","well13","Workover", 1175,{'startTime':'04-04-2023','endTime':'28-04-2023', 'workoverTime' : 2,'priority' : 7,'well_location':[59,34],'lossFactor':0.77})
    well14 = Well("13","well14","Workover",1450,{'startTime':'05-04-2023','endTime':'28-04-2023','workoverTime' : 4,'priority' : 10,'well_location':[62,24],'lossFactor':0.48})
    scheduler = Scheduler(
        [rig1,rig2,rig3,rig4,rig5,rig6],
        [well1,well2,well3,well4,well5,well6,well7,well8,well9,well10,well11,well12,well13,well14],schedulerStartTime,algorithm_type)
    solution = scheduler.well_assign()
    pass

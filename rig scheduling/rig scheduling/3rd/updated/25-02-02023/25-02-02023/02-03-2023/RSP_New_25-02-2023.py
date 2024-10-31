import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datetime import date as date_function
import random
from Rig import Rig
from Well import Well
from scipy.spatial.distance import cdist
from numpy import array,ravel
import re

class classify(object):
    
    def __init__(self,wells,rigs,rigname):
        self.wells=wells
        self.rigs=rigs
        self.rigname=rigname
    def category(self):
        rig_dict = [rig.dict() for rig in self.rigs]
        well_dict = [well.dict() for well in self.wells]
        drilling_rigs = []
        workover_rigs = []
        for rig in rig_dict:
            if rig["rig_type"] == "Drilling" and rig["depth_capacity"]>= 1500 and rig["horsepower"]>= 1200:
                drilling_rigs.append(rig)
            elif rig["rig_type"] == "Workover" and rig["depth_capacity"] <= 1500 and rig["horsepower"]<=1200:
                workover_rigs.append(rig)
        drilling_wells = []
        workover_wells = []
        for well in well_dict:
            if well["well_type"] == "Drilling" and well["depth_capacity"] >= 1500:
                drilling_wells.append(well)
            elif well["well_type"] == "Workover" and well["depth_capacity"] <= 1500:
                workover_wells.append(well)
        drilling_rig_assignments = {}
        workover_rig_assignments = {}
        for well_name in drilling_wells:
            assigned = False
            for rig_name in drilling_rigs:
                if well_name["depth_capacity"] <= rig_name["depth_capacity"]:
                    drilling_rig_assignments[well_name["id"]] = rig_name["name"]
                    assigned = True
                    break
        for well_name in workover_wells:
            assigned = False
            for rig_name in workover_rigs:
                if well_name["depth_capacity"] <= rig_name["depth_capacity"]:
                    workover_rig_assignments[well_name["id"]] = rig_name["name"]
                    assigned = True
                    break
        print("Drilling Rig Assignments:")
        print(drilling_rig_assignments)
        print("\nWorkover Rig Assignments:")
        print(workover_rig_assignments)
        rig_order=[]
        for name in self.rigname:
            rig_order.append(name)
            
        rig_wise_allotted_well_ids = {}

        for rig_name in rig_order:
            rig_wise_allotted_well_ids[rig_name] = []

        for well_id, rig_name in drilling_rig_assignments.items():
            if rig_name != 'No available rig':
                rig_wise_allotted_well_ids[rig_name].append(well_id)

        for well_id, rig_name in workover_rig_assignments.items():
            rig_wise_allotted_well_ids[rig_name].append(well_id)

        return rig_wise_allotted_well_ids
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

    def __init__(self,rigs,wells,schedulerStartTime):
        self.rigs = rigs
        self.wells = wells
        self.schedulerStartTime = schedulerStartTime
            
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
    
    def schedule(self, r_final,wells, rigs,t_opt):
        wells_dict = []
        sorted_Wells=wells
        sorted_rigs=rigs
        schedulerStartTime=self.schedulerStartTime
        mastupTime=self.getRigmastupTime()
        mastdownTime=self.getRigmastdownTime()
        wellstartTime=self.getWellStartTime()
        wellendTime=self.getWellEndTime()
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
                rig=rigs[j]
                t_time=t_opt[j]
                while len(r1)>0 :
                    well = sorted_Wells[r1.pop(0)]
                    time=t_time.pop(0)
                    result=self.add_hours_to_now(time)
                    # Assign the well to the rig
                    # travel time from rig to well or well to well
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
                print("rig: "+str(j)+"--> "+str(temp))

            else:
                currentDate = schedulerStartTime
                rigs=sorted_rigs
                # Get the next well to be processed
                r1=r_final[j]
                rig=rigs[j]
                t_time=t_opt[j]
                while len(r1)>0 :
                    well = sorted_Wells[r1.pop(0)]
                    time=t_time.pop(0)
                    result=self.add_hours_to_now(time)
                    # Assign the well to the rig
                    # travel time from rig to well or well to well
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
                #print(rig['returnTime'])
                temp = []
                for i in range(len(rig['assigned_wells'])):
               
                    if i<len(rig['assigned_wells'])-1:
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i]})
                    if i==len(rig['assigned_wells'])-1:
                        temp.append({'rig_type':rig['rig_type'],'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'maintanceStartTime':rig['maintanceStartTime'][i],
                                 'maintanceEndTime':rig['maintanceEndTime'][i],'returnTime': rig['returnTime'].pop(0)})                    
                print("rig: "+str(j)+"--> "+str(temp))
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
    
    def solveNCW(self,r,sample,sample1,wellsDict,rigsDict):
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
                print(sample3,sample4)
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
                  print(sample3,sample5)
                  distance_1=cdist(sample3,sample5,'euclidean')
                  d1_opt.append(distance_1.tolist()[0][0])
                elif Tot_loss<Min_loss :
                  Min_loss=Tot_loss
                  w_opt=w_1
                  d1_opt=d_1
                  tt_opt=tt
                  sample5.append(sample2[w_opt[-1]])
                  print(sample3,sample5)
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
        print(w1_opt)
        print(d_opt)
        #print("travel times :", t_opt)    
        r_final=[]
        k=0
        for y in w1_opt :
            r1_opt=[]
            for i in y:
                r1_opt.append(r[k][i])
            k=k+1
            r_final.append(r1_opt) 
        #print("optimal well sequence :", r_final)
        #print("distance sequence :", d_opt)
        self.schedule(r_final,wellsDict,rigsDict,t_opt)
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
          k=self.Convert(i)
          file1.append(k)
        file2=[]
        for i in c1:
          k=self.Convert(i)
          file2.append(k)
        sample = []
        for i in file1:
            sample.append((int(i[0]),int(i[1] )))
        #print(*[f"({w:.2f}, {h:.2f})" for w, h in sample], sep=', ')
        sample1 = []
        for i in file2:
            sample1.append((int(i[0]),int(i[1] )))
        idx=classify(self.wells, self.rigs,rigname)
        solution=idx.category()
        r = [[int(num) for num in sublist] for sublist in solution.values()]
        print("Rig wise well assignment :", r)
       #rigs_dict = self.allocate_wells_to_rigs(rigs_location, wells_location,rigsDict,wellsDict)
        #print(rigs_dict)
        return self.solveNCW(r,sample,sample1,wellsDict,rigsDict)        

if __name__ == "__main__":
    StartTime = input("enter scheduler StartTime in this format dd-mm-yyyy")
    schedulerStartTime=datetime.strptime(StartTime, "%d-%m-%Y")
    #print(schedulerStartTime)
    rig1 = Rig("1","Rig1","Drilling", 2100,1600,10,15000,{'rig_location':'(599 , 160)','rig_maintance':4,'rig_init_status':'mastUp'})
    rig2 = Rig("2","Rig2","Drilling", 2260,1500,12,20000,{'rig_location':'(313 , 758)','rig_maintance':4,'rig_init_status':'mastDown'})
    rig3 = Rig("3","Rig3","Workover", 1100,750,5,8000,{'rig_location':'(145 , 226)','rig_maintance':4,'rig_init_status':'mastUp'})
    rig4 = Rig("4","Rig4","Workover", 1200,1000,6,9000,{'rig_location':'(313 , 758)','rig_maintance':4,'rig_init_status':'mastDown'})
    rig5 = Rig("5","Rig5","Workover", 1500,1200,5,7000,{'rig_location':'(145 , 226)','rig_maintance':4,'rig_init_status':'mastUp'})

    well1 = Well("0","well1","Drilling", 2000,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 2,'priority' : 2,'well_location':'(307 , 917)','lossFactor':0.24})
    well2 = Well("1","well2","Drilling", 2200,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 3,'priority' : 1 ,'well_location':'(741 , 293)','lossFactor':0.51})
    well3 = Well("2","well3","Workover", 1000,{'startTime' : '25-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 4,'well_location':'(299 , 880)','lossFactor':0.93})
    well4 = Well("3","well4","Workover", 1150,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 3,'well_location':'(313 , 573)','lossFactor':0.77})
    well5 = Well("4","well5","Workover", 1400,{'startTime' : '24-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 4,'priority' : 5,'well_location':'(370 , 606)','lossFactor':0.48})
    well6 = Well("5","well6","Drilling", 2050,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 2,'priority' : 8,'well_location':'(946 , 48)','lossFactor':0.24})
    well7 = Well("6","well7","Drilling", 2250,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 3,'priority' : 6 ,'well_location':'(376 , 278)','lossFactor':0.51})
    well8 = Well("7","well8","Workover", 1100,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 9,'well_location':'(353 , 276)','lossFactor':0.93})
    well9 = Well("8","well9","Workover", 1175,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 7,'well_location':'(318 , 854)','lossFactor':0.77})
    well10 = Well("9","well10","Workover",1450,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 4,'priority' : 10,'well_location':'(939 , 529)','lossFactor':0.48})
    well11 = Well("10","well11","Drilling", 2250,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 3,'priority' : 6 ,'well_location':'(376 , 278)','lossFactor':0.51})
    well12 = Well("11","well12","Workover", 1100,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 9,'well_location':'(353 , 276)','lossFactor':0.93})
    well13 = Well("12","well3","Workover", 1175,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023', 'workoverTime' : 2,'priority' : 7,'well_location':'(318 , 854)','lossFactor':0.77})
    well14 = Well("13","well14","Workover",1450,{'startTime' : '23-02-2023', 'endTime' : '10-03-2023','workoverTime' : 4,'priority' : 10,'well_location':'(939 , 529)','lossFactor':0.48})
    scheduler = Scheduler(
        [rig1,rig2,rig3,rig4,rig5],
        [well1,well2,well3,well4,well5,well6,well7,well8,well9,well10,well11,well12,well13,well14],schedulerStartTime,
    )
    solution = scheduler.well_assign()
    pass

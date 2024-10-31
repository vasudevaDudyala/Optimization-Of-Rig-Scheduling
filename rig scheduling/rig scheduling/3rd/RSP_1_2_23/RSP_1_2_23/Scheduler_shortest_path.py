import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datetime import date as date_function
import random
from Rig import Rig
from Well import Well
from scipy.spatial.distance import cdist
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

    def __init__(self,rigs,wells):
        self.rigs = rigs
        self.wells = wells 
        
    def getWellProductionRate(self):
        return [well.productionRate for well in self.wells]

    def getWellStartTime(self):
        return [well.startTime for well in self.wells]

    def getWellWorkoverTime(self):
        return [well.workoverTime for well in self.wells]

    def getWellPriorities(self):
        return [well.priority for well in self.wells]

    def getWellLocation(self):
        return [well.location for well in self.wells]
    
    def getWellLossFactor(self):
        return [well.lossFactor for well in self.wells]
    
    def getRigLocation(self):
        return [rig.location for rig in self.rigs]
    
    def getRigSpeed(self):
        return [rig.speed for rig in self.rigs]
    
    def Convert(self,string):
        M=len(string)
        string=string[1:M-1]
        string.strip()
        li = list(string.split(","))
        return li

    def solve(self,distance,start):
        self.__initialize_memo()
        self.distance_matrix = distance
        self.start_city = start
        self.total_cities = len(distance)
        self.end_state = (1 << self.total_cities) - 1
        self.memo = [[None for _col in range(1 << self.total_cities)] for _row in range(self.total_cities)]

        self.shortest_path = []
        self.min_path_cost = float('inf')
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
    
    # def hoursToDh(hours):
    #     d = mt.floor(hours/ (24))
    #     h = mt.floor(hours % (24) )
    #     return d,h
    
    def schedule(self, r_final,wells, rigs,t_opt):
        wells_dict = []
        self.Wells = wells
        self.rigs = rigs
        sorted_Wells=wells
        sorted_rigs=rigs
        for i in range(len(r_final)):
            s = date_function.today()
            date = s.strftime("%d-%m-%Y")
            currentDate = datetime.strptime(date, '%d-%m-%Y')
            rigs=sorted_rigs
            # Get the next well to be processed
            r=r_final[i]
            rig=rigs[i]
            t_time=t_opt[i]
            while len(r)>0 :
                well = sorted_Wells[r.pop(0)]
                time=t_time.pop(0)
                # Assign the well to the rig
                rig['assignedWells'].append(well['id'])
                # travel time from rig to well or well to well
                rig['travelTime'].append(time)
                # Update the rig's processing time
                rig['workoverTime'] += well['workoverTime']
                # Assign the well startTime to the rig
                rig['startTime'].append(currentDate.strftime("%d-%m-%Y"))
                process_days=rig['workoverTime']-1               
                endTime = datetime.strptime(well['startTime'], "%d-%m-%Y") + timedelta(days=process_days)

                # Assign the well endTime to the rig
                rig['endTime'].append(endTime.strftime("%d-%m-%Y"))                 
                currentDate=datetime.strptime(rig['endTime'][-1], "%d-%m-%Y")        
        print(rigs)
        travel_time = 1
        assign = []
        for rig in rigs:
            temp = []
            for i in range(len(rig['assignedWells'])):
                temp.append({'assignedWell': rig['assignedWells'][i],'travelTime': rig['travelTime'][i],'startTime': rig['startTime'][i], 'endTime': rig['endTime'][i]})
            assign.append(temp)
        for i in range(len(assign)):
            print("rig: "+str(i)+"--> "+str(assign[i]))
        pass

    def cost(self,w_1,d_1,r,f,Vwr):
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
            tw1.append(tw[i])
            F1.append(F[i])
            Q1.append(Q[i])
        R=[]
        C=[]
        K1=0
        tsi=[]
        tt=[]
        for m in range(len(r[f])):
            R.append(Q1[m]*F1[m])
            K=15+((0.072*d_1[m])+(2.16*tw1[m]))
            C.append(K)
            T=(d_1[m]/Vwr)
            K1=K1+T+tw1[m]
            tsi.append(K1)
            tt.append(T)
        Li=np.multiply(R,tsi)
        Tot_loss=np.sum(np.add(C,Li))
        return Tot_loss,tt
    
    def solveNCW(self,r,sample,sample1,wellsDict,rigsDict):
        w1_opt=[]
        d_opt=[]
        t_opt=[]
        total_loss=0
        sample3=[]
        rigs=rigsDict
        for f in range(len(r)) :
            sample3.append(sample[f])
            Loss=0

            sample4=[]
            Vwr=rigs[f]['speed']
            for k in range(len(r[f])):
                start_city=k
                sample2=[]
                sample4.append(sample1[k])
                for x in r[f]:
                    sample2.append(sample1[x])
                distance_matrix = cdist(sample2, sample2, 'euclidean')
                distance=cdist(sample3,sample4,'euclidean')
                tour = nextclosestwell(distance_matrix, start_city)
                tour.solve()
                w_1=tour.shortest_path
                d_1=[]
                d_1.append(distance.tolist()[0][0])
                for j in range(len(r[f])-1):
                    d_1.append(distance_matrix[w_1[j]][w_1[j+1]])
                Tot_loss,tt=self.cost(w_1,d_1,r,f,Vwr)
                if k==0 :
                  Min_loss=Tot_loss
                  w_opt=w_1
                  d1_opt=d_1
                  tt_opt=tt
                elif Tot_loss<Min_loss :
                  Min_loss=Tot_loss
                  w_opt=w_1
                  d1_opt=d_1
                  tt_opt=tt
                sample4=[]
            #print('Optimum well sequence and its Minimum total loss')
            #print(w_opt,d1_opt,Min_loss)
            w1_opt.append(w_opt)
            d_opt.append(d1_opt)
            t_opt.append(tt_opt)
            Loss+=Min_loss
            total_loss+=Loss
            sample3=[]
##        print(w1_opt)
##        print(d_opt)
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
        print('total loss',total_loss)
        pass
    
    def well_assign(self):
        well_location=self.getWellLocation()
        rig_location=self.getRigLocation()
        rig_speed=self.getRigSpeed()
        wellsDict = [well.dict() for well in self.wells]
        rigsDict = [rig.dict() for rig in self.rigs]
        c=list(rig_location)
        c1=list(well_location)
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
        #print(*[f"({w:.2f}, {h:.2f})" for w, h in sample1], sep=', ')
        rig_pos=sample
        well_pos=sample1
        minimumlist = []
        original_list = []
        out = []
        distance = cdist(sample1, sample, 'euclidean')
        for i in range(len(well_pos)):
          (m,i) = min((v,i) for i,v in enumerate(distance[i]))
          # print('well',i+1,'---->','rig',minimumlist.index(min_lst)+1)
          original_list.append(m)
          output = (i,m)
          out.append(output)
          minimumlist.clear()
        len_lst = []
        for _ in out:
          _ = list(_)
          if _[1] not in len_lst:
            len_lst.append(_[1])
        # to create lists for rigs
        lists = {}
        for i in range(len(len_lst)):
            lists[f"rig_{i}"] = []
        for _ in range(len(out)):
          lk = list(out[_])
          rig = "rig_" + str(lk[0])
          k = lists[rig]
          k.append(_)
          lists[rig] = k
        #print('rig0 = ',lists['rig_0'])
        #print('rig1 = ',lists['rig_1'])
        #print('rig2 = ',lists['rig_2'])
        rig0 = lists['rig_0']
        rig1 = lists['rig_1']
        rig2 = lists['rig_2']
        r=[rig0,rig1,rig2]
        #print(r)
        return self.solveNCW(r,sample,sample1,wellsDict,rigsDict)        

if __name__ == "__main__":
    rig1 = Rig("1","Rig-1",{'speed':10,'location':'(599 , 160)'})
    rig2 = Rig("2","Rig-2",{'speed':10,'location':'(313 , 758)'})
    rig3 = Rig("3","Rig-3",{'speed':10,'location':'(145 , 226)'})

    well1 = Well("1","well-1",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023','productionRate' : 30, 'workoverTime' : 2,'priority' : 2,'location':'(307 , 917)','lossFactor':0.24})
    well2 = Well("2","well-2",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023','productionRate' : 20, 'workoverTime' : 3,'priority' : 1 ,'location':'(741 , 293)','lossFactor':0.51})
    well3 = Well("3","well-3",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023', 'productionRate' : 40, 'workoverTime' : 2,'priority' : 4,'location':'(299 , 880)','lossFactor':0.93})
    well4 = Well("4","well-4",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023', 'productionRate' : 35, 'workoverTime' : 2,'priority' : 3,'location':'(313 , 573)','lossFactor':0.77})
    well5 = Well("5","well-5",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023', 'productionRate' : 25, 'workoverTime' : 4,'priority' : 5,'location':'(370 , 606)','lossFactor':0.48})
    well6 = Well("6","well-6",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023','productionRate' : 30, 'workoverTime' : 2,'priority' : 8,'location':'(946 , 48)','lossFactor':0.24})
    well7 = Well("7","well-7",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023','productionRate' : 20, 'workoverTime' : 3,'priority' : 6 ,'location':'(376 , 278)','lossFactor':0.51})
    well8 = Well("8","well-8",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023', 'productionRate' : 40, 'workoverTime' : 2,'priority' : 9,'location':'(353 , 276)','lossFactor':0.93})
    well9 = Well("9","well-9",{'startTime' : '1-02-2023', 'endTime' : '4-02-20233', 'productionRate' : 35, 'workoverTime' : 2,'priority' : 7,'location':'(318 , 854)','lossFactor':0.77})
    well10 = Well("10","well-10",{'startTime' : '1-02-2023', 'endTime' : '4-02-2023', 'productionRate' : 25, 'workoverTime' : 4,'priority' : 10,'location':'(939 , 529)','lossFactor':0.48})
    scheduler = Scheduler(
        [rig1,rig2,rig3],
        [well1,well2,well3,well4,well5,well6,well7,well8,well9,well10]
    )
    solution = scheduler.well_assign()
    pass

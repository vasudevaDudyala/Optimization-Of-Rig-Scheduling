import numpy as np
# import pandas as pd
from datetime import datetime, timedelta
# from datetime import date as date_function
# import random
from Rig import Rig
from Well import Well
from scipy.spatial.distance import cdist
from numpy import array, ravel
import re


class Scheduler(object):

    def __init__(self, rigs, wells, schedulerStartTime):
        self.rigs = rigs
        self.wells = wells
        self.schedulerStartTime = schedulerStartTime
            
    def getRigmastupTime(self):
        return [rig.mastupTime for rig in self.rigs]
    
    def getRigmastdownTime(self):
        return [rig.mastdownTime for rig in self.rigs]
    
    def getWellProductionRate(self):
        return [well.productionRate for well in self.wells]
    
    def getWellStartTime(self):
        return [well.startTime for well in self.wells]

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
    
    def add_hours_to_now(self,hours):
        import datetime
        result = datetime.timedelta(hours=hours)
        return result
    
    def schedule(self, r_final,wells, rigs,t_opt):
        # print('det',r_final,wells,rigs,t_opt)
        wells_dict = []
        sorted_Wells=wells
        sorted_rigs=rigs
        schedulerStartTime=self.schedulerStartTime
        mastupTime=self.getRigmastupTime()
        mastdownTime=self.getRigmastdownTime()
        for j in range(len(r_final)):
            currentDate = schedulerStartTime
            rigs=sorted_rigs
            # Get the next well to be processed
            r1=r_final[f"rig{j}"]
            # print(r1)
            rig=rigs[j]
            t_time=t_opt[j]
            # print('t_timeeeeeeeeeeeeeee',t_time)
            while len(r1)>0 :
                well = sorted_Wells[r1.pop(0)-1]
                time=t_time.pop(0)
                result=self.add_hours_to_now(time)
                # Assign the well to the rig
                # travel time from rig to well or well to well

                begin=currentDate+result
                rig['arrivalTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                rig['mastupStartTime'].append(begin.strftime("%d-%m-%Y %H:%M:%S.%f"))
                # Update the rig's processing time
                rig['workoverTime']=well['workoverTime']
                # Assign the well startTime to the rig
                if rigs[j]['mastupStatus'] == 'mastup':
                    start1 = begin
                    # print('innerlsdjflsjdldsflj', begin, mastupTime[j])
                    rig['mastupEndTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['interventionStartTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    process_days = well['workoverTime']
                    endTime = start1 + timedelta(days=process_days)
                    # print(endTime)
                    rig['interventionEndTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['mastdownStartTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    mastendTime = start1 + timedelta(days=process_days)
                    # print('mastentime   =   ', mastendTime)
                    # Assign the well endTime to the rig
                    rig['mastdownEndTime'].append(mastendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    currentDate = datetime.strptime(rig['mastdownEndTime'][-1], "%d-%m-%Y %H:%M:%S.%f")
                    # print('currentDate = ', currentDate)

                else:
                    start1=begin+timedelta(hours=mastupTime[j])
                    # print('innerlsdjflsjdldsflj', begin,mastupTime[j])
                    rig['mastupEndTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['interventionStartTime'].append(start1.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    process_days=well['workoverTime']
                    endTime = start1+ timedelta(days=process_days)
                    # print(endTime)
                    rig['interventionEndTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    rig['mastdownStartTime'].append(endTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    mastendTime = start1+ timedelta(days=process_days)+timedelta(hours=mastdownTime[j])
                    # print('mastentime   =   ', mastendTime)
                    # Assign the well endTime to the rig
                    rig['mastdownEndTime'].append(mastendTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
                    currentDate=datetime.strptime(rig['mastdownEndTime'][-1], "%d-%m-%Y %H:%M:%S.%f")
                    # print('currentDate = ', currentDate)
            returnTime = endTime+self.add_hours_to_now(t_time.pop(0))
            rig['returnTime'].append(returnTime.strftime("%d-%m-%Y %H:%M:%S.%f"))
        #print(rig['returnTime'])
        #print(rigs)
        travel_time = 1
        assign = []
        for rig in rigs:
            temp = []
            for i in range(len(rig['assigned_wells'])):
               
                if i<len(rig['assigned_wells'])-1:
                    temp.append({'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'mastupStartTime':rig['mastupStartTime'][i],
                                 'mastupEndTime':rig['mastupEndTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'mastdownStartTime':rig['mastdownStartTime'][i],'mastdownEndTime':rig['mastdownEndTime'][i]})
                if i==len(rig['assigned_wells'])-1:
                    temp.append({'assigned_well': rig['assigned_wells'][i],'arrivalTime': rig['arrivalTime'][i],'mastupStartTime':rig['mastupStartTime'][i],
                                 'mastupEndTime':rig['mastupEndTime'][i],'interventionStartTime': rig['interventionStartTime'][i],
                                 'interventionEndTime': rig['interventionEndTime'][i],'mastdownStartTime':rig['mastdownStartTime'][i],'mastdownEndTime':rig['mastdownEndTime'][i],'returnTime': rig['returnTime'].pop(0)})                    
            assign.append(temp)
        for i in range(len(rigs)):
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
            tw1.append(tw[i-1])
            F1.append(F[i-1])
            Q1.append(Q[i-1])
        R=[]
        C=[]
        K1=0
        tsi=[]
        tt=[]
        for m in range(len(r[f"rig{f}"])):
            R.append(Q1[m]*F1[m]*73.23)
            K=15+((0.072*d_1[m])+(2.16*tw1[m]))
            C.append(K*73.23)
            T=(d_1[m]/Vwr)
            K1=K1+T+tw1[m]
            tsi.append(K1)
            tt.append(T)
        Li=np.multiply(R,tsi)
        Tot_loss=np.sum(np.add(C,Li))
        return Tot_loss,tt,Li,C
    
    def solveNCW(self,wellsDict,rigsDict,rigs_dict):
        r={}
        for i in range(len(rigs_dict)):
            r[f"rig{i}"]=list(map(int, rigs_dict[i]['assigned_wells']))
        
##        rig0 = list(map(int, rigs_dict[0]['assigned_wells']))
##        rig1 = list(map(int, rigs_dict[1]['assigned_wells']))
##        rig2 = list(map(int, rigs_dict[2]['assigned_wells']))
##        r=[rig0,rig1,rig2]
        d={}
        for i in range(len(rigs_dict)):
            d[f"rig{i}"]=list(map(int, rigs_dict[i]['distances']))
        tt_opt=[]
        t_opt=[]
        Li_final=[]
        C_final=[]
        total_loss=[]
        d_opt=[]
        for f in range(len(r)):
            w_1=r[f"rig{f}"]
            d_1=d[f"rig{f}"][0:-1]
            Vwr=rigsDict[f]['speed']
            Tot_loss,tt,Li,C=self.cost(w_1,d_1,r,f,Vwr)
            tt.append(d[f"rig{f}"][-1]/Vwr)
            t_opt.append(tt)
            Li_final.append(Li)
            C_final.append(C)
            d_opt.append(d_1)
            total_loss.append(Tot_loss)
        self.schedule(r,wellsDict,rigsDict,t_opt)
        print("$ 73.23 per barrel of oil/patroleum")
        print('Well revenue Loss in US$:',Li_final)
        print('Rig cost in US$:',C_final)
        print('Rig wise total cost US$:',total_loss)
        print('total loss in US$:',np.sum(total_loss))
        pass
    
    def distance_mat(self,rigs, wells):
        distance_matrix = cdist(rigs, wells, 'euclidean')
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
        print('sdfhkhlassdflk',rigs,wells,rigs_dictionary,wells_dictionary)
        while len(wells) > 0:
            for i in range(len(rigs)):
                # print('remaining wells = ', wells)
                # print('performing rig', rigs_dictionary[0]['rig_location'])
                distance_matrix = cdist(array([rigs_dictionary[0]['rig_location']]), wells, 'euclidean')
                # print(distance_matrix)
                min_distance = float("inf")
                nearest_well = None
                for j in range(len(wells)):
                    if distance_matrix[0][j] < min_distance:
                        min_distance = distance_matrix[0][j]
                        nearest_well = j
                # for assigned wells
                # print(wells[nearest_well],nearest_well+1)
                for k in range(len(wells_dictionary)):
                    if wells[nearest_well] == wells_dictionary[k]['well_location']:
                        rigs_dictionary[0]['assigned_wells'].append(wells_dictionary[k]['id'])
                # print('minimum_distance, nearest well = ', min_distance, nearest_well)
                rigs_dictionary[0]['distances'].append(min_distance)
                rigs_dictionary[0]['rig_location'] = wells[nearest_well]
                rigs_dictionary = self.early_completed(rigs_dictionary, wells_dictionary, wells[nearest_well])
                wells.pop(nearest_well)
                # print(rigs_dictionary)
                # print('\n')
                if len(wells) == 0:
                    break
        # print('skdhfksadhkdsh', rigs_dictionary)
        rigs_dictionary = sorted(rigs_dictionary, key=lambda x: int(re.findall(r'\d+', x['name'])[0]))
        rigs_dictionary = self.end_to_start_distance(rigs_dictionary,rigs)
        print('the rig details : ', rigs_dictionary)
        return rigs_dictionary

    def well_assign(self):
        wells_location=self.getWellLocation()
        rigs_location=self.getRigLocation()
        rig_speed=self.getRigSpeed()
        wellsDict = [well.dict() for well in self.wells]
        #print(wellsDict)
        rigsDict = [rig.dict() for rig in self.rigs]
        #print(rigsDict)
        rigs_dict = self.allocate_wells_to_rigs(rigs_location, wells_location,rigsDict,wellsDict)
        #print(rigs_dict)
        return self.solveNCW(wellsDict,rigsDict,rigs_dict)        

if __name__ == "__main__":
    StartTime = "22-02-2023" #input("enter scheduler StartTime in this format dd-mm-yyyy")
    schedulerStartTime=datetime.strptime(StartTime, "%d-%m-%Y")
    #print(schedulerStartTime)
    # rig1 = Rig("1","Rig-1",{'rig_location': (15.491481, 78.48764)}, "mastup")
    # rig2 = Rig("2","Rig-2",{'rig_location': (15.484678, 78.484688)}, "mastdown")
    # rig3 = Rig("3","Rig-3",{'rig_location': (15.488546, 78.494026)}, "mastdown")
    rig1 = Rig("1", "Rig-1", {'rig_location': (599, 160)})
    rig2 = Rig("2", "Rig-2", {'rig_location': (313, 758)})
    rig3 = Rig("3", "Rig-3", {'rig_location': (145, 226)})
    # rig1 = Rig("1", "Rig-1", {'speed': 10, 'rig_location': '(599 , 160)'}, "mastup")
    # rig2 = Rig("2", "Rig-2", {'speed': 10, 'rig_location': '(313 , 758)'}, "mastdown")
    # rig3 = Rig("3", "Rig-3", {'speed': 10, 'rig_location': '(145 , 226)'}, "mastdown")

    # well1 = Well("1","well-1",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023','workoverTime' : 2,'priority' : 2,'well_location':(15.491019, 78.486007),'lossFactor':0.24})
    # well2 = Well("2","well-2",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023','workoverTime' : 2,'priority' : 1 ,'well_location':(15.494647, 78.491172),'lossFactor':0.51})
    # well3 = Well("3","well-3",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023', 'workoverTime' : 5,'priority' : 4,'well_location':(15.489348, 78.49147),'lossFactor':0.93})
    # well4 = Well("4","well-4",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023', 'workoverTime' : 2,'priority' : 3,'well_location':(15.483318, 78.49643),'lossFactor':0.77})
    # well5 = Well("5","well-5",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023', 'workoverTime' : 3,'priority' : 5,'well_location':(15.481215, 78.4868),'lossFactor':0.48})
    # well6 = Well("6","well-6",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023','workoverTime' : 3,'priority' : 8,'well_location':(15.484649, 78.476271),'lossFactor':0.24})
    # well7 = Well("7","well-7",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023','workoverTime' : 4,'priority' : 6 ,'well_location':(15.487176, 78.484016),'lossFactor':0.51})
    # well8 = Well("8","well-8",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023', 'workoverTime' : 4,'priority' : 9,'well_location':(15.48451, 78.485241),'lossFactor':0.93})
    # well9 = Well("9","well-9",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023', 'workoverTime' : 1,'priority' : 7,'well_location':(318 , 854),'lossFactor':0.77})
    # well10 = Well("10","well-10",{'startTime' : '3-02-2023', 'endTime' : '20-02-2023','workoverTime' : 5,'priority' : 10,'well_location':(939, 529),'lossFactor':0.48})

    well1 = Well("1", "well-1", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 2,
                                 'well_location': (307, 917), 'lossFactor': 0.24})
    well2 = Well("2", "well-2", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 3, 'priority': 1,
                                 'well_location': (741, 293), 'lossFactor': 0.51})
    well3 = Well("3", "well-3", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 4,
                                 'well_location': (299, 880), 'lossFactor': 0.93})
    well4 = Well("4", "well-4", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 3,
                                 'well_location': (313, 573), 'lossFactor': 0.77})
    well5 = Well("5", "well-5", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 4, 'priority': 5,
                                 'well_location': (370, 606), 'lossFactor': 0.48})
    well6 = Well("6", "well-6", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 8,
                                 'well_location': (946, 48), 'lossFactor': 0.24})
    well7 = Well("7", "well-7", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 3, 'priority': 6,
                                 'well_location': (376, 278), 'lossFactor': 0.51})
    well8 = Well("8", "well-8", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 9,
                                 'well_location': (353, 276), 'lossFactor': 0.93})
    well9 = Well("9", "well-9", {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 2, 'priority': 7,
                                 'well_location': (318, 854), 'lossFactor': 0.77})
    well10 = Well("10", "well-10",
                  {'startTime': '3-02-2023', 'endTime': '20-02-2023', 'workoverTime': 4, 'priority': 10,
                   'well_location': (939, 529), 'lossFactor': 0.48})

    scheduler = Scheduler(
        [rig1,rig2,rig3],
        [well1,well2,well3,well4,well5,well6,well7,well8,well9,well10],schedulerStartTime,
    )
    solution = scheduler.well_assign()

    pass

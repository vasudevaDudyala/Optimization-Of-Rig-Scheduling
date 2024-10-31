# import numpy as np
# import pandas as pd
# from datetime import datetime, timedelta
# from datetime import date as date_function
# import random
# from Rig import Rig
# from Well import Well
#
#
# class Scheduler(object):
#
#     def __init__(self,rigs,wells):
#         self.rigs = rigs
#         self.wells = wells
#         print(wells)
#
#     def getWellProductionRate(self):
#         return [well.productionRate for well in self.wells]
#
#     def getWellStartTime(self):
#         return [well.startTime for well in self.wells]
#
#     def getWellProcessingTime(self):
#         return [well.processingTime for well in self.wells]
#
#     def getWellPriorities(self):
#         return [well.priority for well in self.wells]
#
#     def priority(self):
#         priorities = self.getWellPriorities()
#         return [well.dict() for well in self.wells]
#
#     # def result(self,date,result,wells):
#     #     well_name = wells['name'].tolist()
#     #     process_time = wells['Processing time in days(ti)'].tolist()
#     #     release = wells['release_date'].tolist()
#     #     rigs = []
#     #     assigned_wells = []
#     #     start_date = []
#     #     finish_date = []
#     #     data = []
#
#         for i in range(len(result)):
#             for j in result[i]:
#                 rigs.append('rig' + str(i))
#                 assigned_wells.append(j)
#         for i in result:
#             fi = 0
#             for j in i:
#                 if fi == 0:
#                     k = well_name.index(j)
#                     fi = release[k]
#                     start_date.append(fi)
#                 k = well_name.index(j)
#                 process_days = process_time[k]
#                 next_date = datetime.strptime(str(fi), "%d-%m-%Y") + timedelta(days=process_days)
#                 full_datetime = "%d-%m-%Y"
#                 finished = next_date.strftime(full_datetime)
#                 fi = finished
#                 finish_date.append(finished)
#                 start_date.append(fi)
#             del start_date[-1]
#
#         update_start_date = []
#         update_finish_date = []
#         for i in range(len(start_date)):
#             s = datetime.strptime(start_date[i], '%d-%m-%Y')
#             f = datetime.strptime(finish_date[i], '%d-%m-%Y')
#             up_s = s.strftime("%Y-%m-%d")
#             up_f = f.strftime("%Y-%m-%d")
#             update_start_date.append(up_s)
#             update_finish_date.append(up_f)
#
#         df = pd.DataFrame(
#             {'Task': rigs, 'Start': update_start_date, 'Finish': update_finish_date, 'Resource': assigned_wells})
#         print(df)
#
#
#     def calculation(self, wells, rigs):
#
#         wells_dict = []
#         self.sortedWells = wells
#         self.rigs = rigs
#         print(self.sortedWells)
#         for i in self.sortedWells:
#             wells_dict.append(i)
#         print(wells_dict)
#         # sortedWells = sorted(wells, key=lam
#         # bda x: (x.priority))
#         currentDate = datetime.strptime(self.sortedWells[0]['startTime'], '%d-%m-%Y')
#
#         s = date_function.today()
#         date = s.strftime("%d-%m-%Y")
#         # Assign the wells to the rigs concurrently
#         while len(self.sortedWells) > 0:
#
#             # Get the next well to be processed
#             well = self.sortedWells.pop(0)
#             # print(datetime.strptime(well.endTime,'%Y-%m-%d'))
#             # Check if the well has been released
#             if datetime.strptime(well['endTime'], '%d-%m-%Y') <= currentDate:
#                 # Update the current date to the well's release date
#                 # currentDate = datetime.strptime(well.endTime, '%Y-%m-%d')
#                 # Find the rig with the shortest processing time
#                 rig = min(rigs, key=lambda x: x.processingTime)
#
#                 # Assign the well to the rig
#                 rig.assignedWells.append(well.id)
#
#                 # Update the rig's processing time
#                 rig.processingTime += well.processingTime
#                 # currentDate += timedelta(days=well['processing_time'])
#                 # print(currentDate)
#                 # print('%')
#             else:
#                 self.sortedWells.insert(0, well)
#                 # print(sortedWells)
#                 # print("welcome")
#                 if len(self.sortedWells) != 1:
#                     well = self.sortedWells.pop(1)
#                 else:
#                     well = self.sortedWells.pop(0)
#                 # Find the rig with the shortest processing time
#                 rig = min(rigs, key=lambda x: x['processingTime'])
#
#                 # Assign the well to the rig
#                 rig['assignedWells'].append(well['id'])
#
#                 # Update the rig's processing time
#                 rig['processingTime'] += well['processingTime']
#                 # currentDate += timedelta(days=well['processing_time'])
#                 # print(currentDate)
#                 # print('*')
#             rig = min(rigs, key=lambda x: x['processingTime'])
#             # print(rig['name'])
#             currentDate = datetime.strptime(date, '%d-%m-%Y')
#             # currentDate = ''
#             # print(timedelta(days=rig['processing_time']))
#             temp = str(timedelta(days=rig['processingTime']))
#             temp = temp.split()
#             # print(temp)
#             if len(temp) == 3:
#                 temp[0] = str(int(temp[0]) - 1)
#                 st = ' '.join([str(elem) for elem in temp])
#                 # currentDate = timedelta(days=st)
#                 currentDate += pd.to_timedelta(st)
#
#             else:
#                 currentDate += timedelta(days=rig['processingTime'])
#         result = []
#         for rig in rigs:
#             result.append(rig['assignedWells'])
#             print(f"{rig['name']}: {rig['assignedWells']}")
#
#         return result,rigs,wells_dict,date
#
#     def cost(self, date, rigs, wells):
#
#         print('inner rigs = ', rigs)
#         print('inner wells    =   ', wells)
#         total_loss = 0
#         current_date = datetime.strptime(date, '%d-%m-%Y')
#         for rig in rigs:
#             k = 0
#             # print(rig)
#             for w_1 in rig['assignedWells']:
#                 # print(w_1)
#
#                 for well in wells:
#                     if well['id'] == w_1:
#                         well_release_date = datetime.strptime(well['startTime'], '%d-%m-%Y')
#                         delay = (current_date - well_release_date).days
#                         loss = well['productionRate'] * (well['processingTime'] + delay)
#                         total_loss += loss
#                         temp = str(timedelta(days=well['processingTime']))
#                         # print(temp)
#                         temp = temp.split()
#                         # print(temp)
#                         if k == 0:
#                             temp[0] = str(int(temp[0]) - 1)
#                             # print(temp)
#                             st = ' '.join([str(elem) for elem in temp])
#                             # current_date = timedelta(days=st)
#                             current_date += pd.to_timedelta(st)
#
#                         else:
#                             current_date += timedelta(days=well['processingTime'])
#                             # print(current_date)
#                         # print(current_date)
#                         k += 1
#             # print(total_loss)
#             current_date = datetime.strptime(date, '%d-%m-%Y')
#         print(f'Total production loss: {total_loss}')
#
#         return total_loss
#
#     def solveHMTP(self):
#         print('pause1')
#         productionRatio = self.getWellProductionRate()
#         wellsDict = self.priority()
#         rigsDict = [rig.dict() for rig in self.rigs]
#         result, rigs, wells_dict, date = self.calculation(wellsDict, rigsDict)
#         print(date,rigs,wells_dict)
#         totalLoss = self.cost(date,rigs,wells_dict)
#         # df = self.result(date,result,wells_dict)
#         pass
#
#     def solve(self,method="HMTP"):
#         if method == "HMTP":
#             return self.solveHMTP()
#
#
# if __name__ == "__main__":
#     rig1 = Rig("1","Rig-1",{'speed':10})
#     rig2 = Rig("2","Rig-2",{'speed':10})
#     rig3 = Rig("3","Rig-3",{'speed':10})
#
#     well1 = Well("1","well-1",{'startTime' : '27-01-2023', 'endTime' : '30-01-2023','productionRate' : 60, 'processingTime' : 3,'priority' : 5})
#     well2 = Well("2","well-2",{'startTime' : '29-01-2023', 'endTime' : '30-01-2023','productionRate' : 40, 'processingTime' : 2,'priority' : 1 })
#     well3 = Well("3","well-3",{'startTime' : '28-01-2023', 'endTime' : '30-01-2023', 'productionRate' : 30, 'processingTime' : 2,'priority' : 4 })
#     scheduler = Scheduler(
#         [rig1,rig2,rig3],
#         [well1, well2, well3]
#     )
#     solution = scheduler.solve("HMTP")
#     # print(solution)
#
#     pass
a = 10
b = --a + a++ + a-- + ++a
print(b)
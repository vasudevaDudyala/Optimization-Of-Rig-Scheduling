import numpy as np
import pandas as pd
import datetime
import plotly.figure_factory as ff
from datetime import date
import plotly.express as px
import random


def ganntchart(rig,n,dates, resources):
      # print('all = ',rig,n,dates, resources)
      print(resources)
      res_list = []
      Resource = []
      for i in resources:
        for j in range(len(resources[i])):
          Resource.append(str(i))   #for Resource
          res_list.append(resources[i][j])  #for tasks

      current_list = []
      next_list = []
      fi = 0

      today = date.today().strftime('%y-%m-%d')
      current_list.append(today)
      #to find the start and finish dates
      for i in range(len(dates)):
        current_date = date.today()
        next_days = current_date + datetime.timedelta(days = dates[i])
        next = next_days.strftime('%y-%m-%d')
        fi = next
        current_list.append(fi)
        next_list.append(next)
        current_date = fi
      del current_list[-1]
      k = 0
      temp = []
      for i in resources:
        temp.append(k)
        k = k+len(resources[i])
      for i in temp:
        current_list[i] =  date.today().strftime('%y-%m-%d')
      df = pd.DataFrame({'Task':Resource,'Start':current_list,'Finish':next_list,'Resource' :res_list })
      print(df)
      r = lambda: random.randint(0, 255)
      colors = ['#%02X%02X%02X' % (r(), r(), r())]
      for i in range(1, df.Resource.nunique() + 1):
          colors.append('#%02X%02X%02X' % (r(), r(), r()))
      fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
      fig.write_html(r"C:\Users\reddy\Documents\college\projects\rig scheduling\rig scheduling\1st stage\rig gannts\method" +str(n) +' '+ str(rig)+'rigs'+ ".html")


# Total loss calculation for approximation technique 1
def app_total_loss(lists, wi_1, ti, pi):
    t = 0
    sums = []
    sum = 0
    tot_loss = 0
    for j in lists:
        for i in lists[j]:
            k = wi_1.index(i)
            sums.append(t + ti[k])
            sum = sum + ti[k] * pi[k]
        tot_loss = tot_loss + sum
        sum = 0
    print('sequence = ', lists)
    print('total loss = ', tot_loss)
    print('sums  = ', sums)
    return lists, tot_loss, sums


# # well allotment to rigs and calculation using approximation technique 2
def approx2(lists, wells, ti2, pi1):
    for i in lists:
        lists[i].reverse()
    sums = []
    t = 0
    sum = 0
    total_sum = 0
    for i in lists:
        for j in range(len(lists[i])):
            k = wells.index(lists[i][j])
            t = t + ti2[k]
            sums.append(t)
            s = t * pi1[k]
            sum = sum + s
        total_sum = total_sum + sum
        sum = 0
        t = 0
    print('sums = ', sums)
    print(lists, total_sum)
    return lists, total_sum, sums


# well allotment to rigs using approximation technique 1
def approx1(wells1, ti1, pi1):
    lists = {}
    ti2 = []
    for i in range(rig):
        lists[f"rig_{i + 1}"] = []
        rigs = list(lists.items())
    for i in range(len(rigs)):
        rigs[i] = list(rigs[i])
    temp = []
    ti = []
    wells = []
    for i in range(len(rigs)):
        rigs[i][1].append(wells1[0])
        temp.append(ti1[0])
        ti.append(ti1[0])
        wells.append(wells1[0])
        ti2.append(ti1[0])
        del ti1[0]
        del wells1[0]

    for i in range(len(ti1)):
        m = min(temp)
        ind = temp.index(m)
        sum = ti1[0] + m
        rigs[ind][1].append(wells1[0])
        wells.append(wells1[0])
        temp[ind] = sum
        ti.append(sum)
        ti2.append(ti1[0])
        del ti1[0]
        del wells1[0]
    # print(lists,wells,ti,pi1)
    return lists, wells, ti, pi1, ti2


# calculation of pi/ti ratio and data shuffle for ascending order
def ascratio(pi, ti):
    # print(pi,ti)
    rati = np.divide(pi, ti)
    ratio = rati.tolist()
    wells1 = []
    ti1 = []
    pi1 = []
    ratio1 = sorted(ratio)
    for i in ratio1:
        k = ratio.index(i)
        wells1.append(wi[k])
        ti1.append(ti[k])
        pi1.append(pi[k])
    return wells1, ti1, pi1


# calculation of pi/ti ratio and data shuffle for descending order
def descratio(pi, ti):
    # print(pi,ti)
    rati = np.divide(pi, ti)
    ratio = rati.tolist()
    wells1 = []
    ti1 = []
    pi1 = []
    ratio1 = sorted(ratio, reverse=True)
    for i in ratio1:
        k = ratio.index(i)
        wells1.append(wi[k])
        ti1.append(ti[k])
        pi1.append(pi[k])
    # print(wells1,ti1,pi1)
    return wells1, ti1, pi1


# well allotment to rigs
def shedule(wi, ti, pi):
    wells = wi
    # to create lists for rigs
    lists = {}
    for i in range(rig):
        lists[f"rig_{i + 1}"] = []
    rigs = list(lists.items())
    for i in range(len(rigs)):
        rigs[i] = list(rigs[i])
    wi_1 = []
    m = len(rigs) - 1  # no of rigs
    s = 0
    while len(wells) != 0:
        temp = lists['rig_' + str(s + 1)]
        temp.append(wells[0])
        sum = 0
        lists['rig_' + str(s + 1)]
        if (s == m):
            s = 0
        else:
            s = s + 1
        wi_1.append(wells[0])
        wells.pop(0)
    return lists, wi_1, ti, pi


# accessing parameters from input dataset
def divide(test1):
    wi = test1.iloc[:, 0]
    wi = wi.tolist()
    ti = test1.iloc[:, 1]
    ti = ti.tolist()
    pi = test1.iloc[:, 2]
    pi = pi.tolist()
    return wi, ti, pi


# total loss = revenue loss + rig cost
def total_loss(list, wi_1, ti, pi):
    sums = []
    up_ti = 0
    sum = 0
    total_loss = 0
    for j in list:
        for i in list[j]:
            k = wi_1.index(i)
            up_ti = up_ti + ti[k]
            sums.append(up_ti)
            loss = up_ti * pi[k]
            sum = sum + loss
        total_loss = total_loss + sum
        result = total_loss
        total_loss = 0
        up_ti = 0
    print('sequence = ', list)
    print('total loss = ', result)
    print('sums  = ', sums)
    return list, result, sums


def unavoidable_loss(ti_1, pi_1):
    Unavoid_loss = np.sum(np.multiply(ti_1, pi_1))
    return Unavoid_loss


def lowerbound():
    # Lower bound calculation
    # Unavoid_loss = unavoidable_loss()
    wi_1, ti_1, pi_1 = divide(data_set)
    Unavoid_loss = unavoidable_loss(pi_1, ti_1)
    B_9 = Unavoid_loss
    # wi_1,pi_1,ti_1 = divide(data_set)
    # descreasing values of pi/ti
    # ratio = []
    # print(pi_1,ti_1)
    # for i in range(len(pi_1)):
    #     ratio.append(ti_1[i]/pi_1[i])
    # print(ratio)
    ratio = np.array(pi_1) / np.array(ti_1)
    data_set['ratio'] = ratio.tolist()
    test_3 = data_set.sort_values('ratio', ascending=False)
    wi_3 = test_3.iloc[:, 0]
    wi_3 = wi_3.to_numpy()
    ti_3 = test_3.iloc[:, 1]
    ti_3 = ti_3.to_numpy()
    pi_3 = test_3.iloc[:, 2]
    pi_3 = pi_3.to_numpy()
    N = len(wi_3)
    r1 = []
    t_1 = []
    sum1 = 0
    Loss_r1 = 0
    for i in range(N):
        r1.append(wi_3[i])
        sum1 += ti_3[i]
        t_1.append(sum1)
        Loss_r1 += sum1 * pi_3[i]
    Total_loss = Loss_r1
    # print('lower bound = ', r1, t_1, Total_loss)
    B_1 = Total_loss
    LB = 1 / (2 * m) * ((m - 1) * B_9 + 2 * B_1)
    print('Lower bound:', LB)
    return LB

# "C:\Users\reddy\Documents\rig scheduling\1st stage\sample_datasets_100.csv"
# main function
data_set = pd.read_csv(r"C:\Users\reddy\Documents\college\projects\rig scheduling\rig scheduling\1st stage\Dataset.csv")  # read input data file

# print(" 1 : ASCENDING METHOD  2 : DESCENDING METHOD 3:APPROXIMATION METHOD1 4:APPROXIMATION METHOD2")

for i in range(18):
    rig = int(input('Enter no of rigs'))  # no of rigs
    m = rig
    print('1 : ASCENDING METHOD  2 : DESCENDING METHOD 3:APPROXIMATION METHOD1 4:APPROXIMATION METHOD2')
    n = int(input('enter your choice'))
    # Ascending order well arrange
    if n == 1:
        lowerbound()
        asc = data_set.sort_values('Productivity in barrels per day', ascending=True)
        wi, ti, pi = divide(asc)
        lists, wi_1, ti, pi = shedule(wi, ti, pi)
        seq_list, result, sums = total_loss(lists, wi_1, ti, pi)
        ganntchart(rig,n,sums, lists)
    # descending order well arrange
    elif n == 2:
        lowerbound()
        desc = data_set.sort_values('Productivity in barrels per day', ascending=False)
        wi, ti, pi = divide(desc)
        lists, wi_1, ti, pi = shedule(wi, ti, pi)
        lists, result, sums = total_loss(lists, wi_1, ti, pi)
        ganntchart(rig,n,sums, lists)
    # Approximation method 1
    elif n == 3:
        lowerbound()
        desc = data_set.sort_values('Productivity in barrels per day', ascending=False)
        wi, ti, pi = divide(desc)

        wells1, ti1, pi1 = descratio(pi, ti)
        lists, wells, ti, pi1, ti2 = approx1(wells1, ti1, pi1)
        lists, tot_loss, sums = app_total_loss(lists, wells, ti, pi1)
        ganntchart(rig,n,sums, lists)

        # Approximation method 2
    elif n == 4:
        lowerbound()
        asc = data_set.sort_values('Productivity in barrels per day', ascending=True)
        wi, ti, pi = divide(asc)
        wells1, ti1, pi1 = ascratio(pi, ti)
        lists, wells, ti, pi1, ti2 = approx1(wells1, ti1, pi1)
        lists, total_sum, sums = approx2(lists, wells, ti2, pi1)
        ganntchart(rig,n,sums, lists)

    else:
        print('Enter above four methods only')
    print("\n")

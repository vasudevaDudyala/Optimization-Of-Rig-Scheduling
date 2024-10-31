import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datetime import date as date_function
import plotly.figure_factory as ff
import plotly.express as px
import random


def ganntchart(n, wells, result):
    well_name = wells['name'].tolist()
    process_time = wells['processing_time'].tolist()
    release = wells['release_date'].tolist()
    rigs = []
    assigned_wells = []
    start_date = []
    finish_date = []
    data = []

    for i in range(len(result)):
        for j in result[i]:
            rigs.append('rig'+str(i))
            assigned_wells.append(j)
    print('resultttt',result)
    for i in result:
        fi = 0
        for j in i:
            if fi == 0:
                k = well_name.index(j)
                fi = release[k]
                start_date.append(fi)
            k = well_name.index(j)
            process_days = process_time[k]
            next_date = datetime.strptime(str(fi), "%d-%m-%Y") + timedelta(days=process_days)
            full_datetime = "%d-%m-%Y"
            finished = next_date.strftime(full_datetime)
            fi = finished
            finish_date.append(finished)
            start_date.append(fi)
        del start_date[-1]

    update_start_date = []
    update_finish_date = []
    for i in range(len(start_date)):
        s = datetime.strptime(start_date[i], '%d-%m-%Y')
        f = datetime.strptime(finish_date[i], '%d-%m-%Y')
        up_s = s.strftime("%Y-%m-%d")
        up_f = f.strftime("%Y-%m-%d")
        update_start_date.append(up_s)
        update_finish_date.append(up_f)

    df = pd.DataFrame({'Task': rigs, 'Start': update_start_date, 'Finish': update_finish_date, 'Resource': assigned_wells})
    print(df)
    r = lambda: random.randint(0, 255)
    colors = ['#%02X%02X%02X' % (r(), r(), r())]
    for i in range(1, df.Resource.nunique() + 1):
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
    fig = ff.create_gantt(df, colors=colors,index_col='Resource', show_colorbar=True,
                      group_tasks=True)
    fig.write_html(r"C:\Users\reddy\Documents\rig scheduling\2nd stage\rig gannts\method" + str(n) + 'rigs' + ".html")


def cost(rigs, wells, date):

    print('inner rigs = ',rigs)
    print('inner wells    =   ',wells)
    total_loss = 0
    current_date = datetime.strptime(date, '%d-%m-%Y')
    for rig in rigs:
        k = 0
        print('rigs = ',rig)
        for w_1 in rig['assigned_wells']:
            # print(w_1)

            for well in wells:
                if well['name'] == w_1:
                    well_release_date = datetime.strptime(well['release_date'], '%d-%m-%Y')
                    delay = (current_date - well_release_date).days
                    loss = well['production_rate'] * (well['processing_time'] + delay)
                    total_loss += loss
                    temp = str(timedelta(days=well['processing_time']))
                    # print(temp)
                    temp = temp.split()
                    # print(temp)
                    if k == 0:
                        temp[0] = str(int(temp[0]) - 1)
                        # print(temp)
                        st = ' '.join([str(elem) for elem in temp])
                        # current_date = timedelta(days=st)
                        current_date += pd.to_timedelta(st)

                    else:
                        current_date += timedelta(days=well['processing_time'])
                        # print(current_date)
                    # print(current_date)
                    k += 1
        # print(total_loss)
        current_date = datetime.strptime(date, '%d-%m-%Y')
    print(f'Total production loss: {total_loss}')

    return total_loss


def calculation(wells,rigs):

    print(wells,rigs)
    sorted_wells = sorted(wells, key=lambda x: (x['priority']))
    # print(sorted_wells)
    # print('pause1')
    # Set the current date to the earliest release date
    current_date = datetime.strptime(sorted_wells[0]['release_date'], '%d-%m-%Y')
    s = date_function.today()
    date = s.strftime("%d-%m-%Y")
    # Assign the wells to the rigs concurrently
    while len(sorted_wells) > 0:
        # Get the next well to be processed
        well = sorted_wells.pop(0)
        # print(datetime.strptime(well['release_date'],'%Y-%m-%d'))
        # Check if the well has been released
        if datetime.strptime(well['release_date'], '%d-%m-%Y') <= current_date:
            # Update the current date to the well's release date
            # current_date = datetime.strptime(well['release_date'], '%Y-%m-%d')
            # Find the rig with the shortest processing time
            rig = min(rigs, key=lambda x: x['processing_time'])

            # Assign the well to the rig
            rig['assigned_wells'].append(well['name'])

            # Update the rig's processing time
            rig['processing_time'] += well['processing_time']
            # current_date += timedelta(days=well['processing_time'])
            # print(current_date)
            # print('%')
        else:
            sorted_wells.insert(0, well)
            # print(sorted_wells)
            # print("welcome")
            if len(sorted_wells) != 1:
                well = sorted_wells.pop(1)
            else:
                well = sorted_wells.pop(0)
            # Find the rig with the shortest processing time
            rig = min(rigs, key=lambda x: x['processing_time'])

            # Assign the well to the rig
            rig['assigned_wells'].append(well['name'])

            # Update the rig's processing time
            rig['processing_time'] += well['processing_time']
            # current_date += timedelta(days=well['processing_time'])
            # print(current_date)
            # print('*')
        rig = min(rigs, key=lambda x: x['processing_time'])
        # print(rig['name'])
        current_date = datetime.strptime(date, '%d-%m-%Y')
        # current_date = ''
        # print(timedelta(days=rig['processing_time']))
        temp = str(timedelta(days=rig['processing_time']))
        temp = temp.split()
        # print(temp)
        if len(temp) == 3:
            temp[0] = str(int(temp[0]) - 1)
            st = ' '.join([str(elem) for elem in temp])
            # current_date = timedelta(days=st)
            current_date += pd.to_timedelta(st)

        else:
            current_date += timedelta(days=rig['processing_time'])
    result = []
    for rig in rigs:
        result.append(rig['assigned_wells'])
        print(f"{rig['name']}: {rig['assigned_wells']}")

    return result,rigs,wells,date


def sort_string(wells_list):
    s = []
    for i in range(len(wells_list)):
        string = ""
        for j in wells_list[i]:
            if j.isdigit():
                string += j
        s.append(int(string))
        del string
    print(s)
    return s


def priority(wells, production_rate, release_date, processing_time):
    well_names = []
    wells_list = []
    for i in wells:
        wells_list.append(i)
    s = sort_string(wells_list)
    sort_wells = sorted(s)
    priorities = []
    for i in sort_wells:
        k = s.index(i) + 1
        priorities.append(k)
    for i in sort_wells:
        well_names.append('well '+str(i))
    well_df = pd.DataFrame(
        {'name': well_names,
         'priority': priorities,
         'release_date': release_date,
         'processing_time' : processing_time,
         'production_rate' : production_rate
         })
    wells_dict = well_df.to_dict('records')
    return wells_dict


def sort(ratio):
    print('ratio=' ,ratio)
    sor_ratio = sorted(ratio, reverse=True)
    wi1 = []
    ti1 = []
    pi1 = []
    di1 = []
    rati = []
    for i in sor_ratio:
        k = ratio.index(i)
        wi1.append(well_name[k])
        ti1.append(processing_time[k])
        pi1.append(production_rate[k])
        di1.append(due_date[k])
        del ratio[k]
        rati.append(ratio)
        ratio.insert(k, 0)
    return wi1, ti1, di1, sor_ratio


def ratio1(production_rate):
    rati = []
    for i in production_rate:
        rati.append(i)

    # ratio = []
    # for i in range(len(production_rate)):
    #     ratio.append(production_rate[i])
    return rati


def ratio2(pi, ti):
    rati = np.divide(pi, ti)
    ratio = rati.tolist()
    return ratio


def ratio3(pi, ti):
    rati = np.multiply(pi, ti)
    ratio = rati.tolist()
    return ratio


def divide(well_df):
    name = well_df.iloc[:, 0]
    well_name = name.tolist()
    pi = well_df.iloc[:, 1]
    production_rate = pi.tolist()
    ti = well_df.iloc[:, 2]
    processing_time = ti.tolist()
    di = well_df.iloc[:, 3]
    release_date = di.tolist()
    Di = well_df.iloc[:, 4]
    due_date = Di.tolist()
    return well_name, production_rate, processing_time, release_date, due_date

def files(rig_df):

    rigs_dict = rig_df.to_dict('records')
    for i in rigs_dict:
        i['assigned_wells'] = []
    return rigs_dict


well_df = pd.read_csv(r'C:\Users\reddy\Documents\rig scheduling\2nd stage\wells.csv')
# well_df = pd.read_csv(r"C:\Users\reddy\Documents\rig scheduling\2nd stage\wells - Copy.csv")
rig_df = pd.read_csv(r'C:\Users\reddy\Documents\rig scheduling\2nd stage\rigs.csv')

print('1: HMPT TECHNIQUE (pi)    2 : HMPT TECHNIQUE (pi/ti)    3 : HMPT TECHNIQUE (pi*ti)')
for i in range(3):
    n = int(input('Enter any one method'))
    if n == 1:
        rigs_dict = files(rig_df)
        well_name, production_rate, processing_time, release_date, due_date = divide(well_df)
        rati = ratio1(production_rate)
        wi1, ti1, di1, sor_ratio = sort(rati)
        well_dict = priority(wi1,production_rate, release_date, processing_time)
        print('well_dict',well_dict)
        result, rigs, wells, date = calculation(well_dict, rigs_dict)
        print('rigsssss = ',rigs)
        print(date)
        print(wells)
        print(rigs)

        total_loss = cost(rigs, wells, date)
        ganntchart(n,well_df,result)

    elif n == 2:
        rigs_dict = files(rig_df)
        well_name, production_rate, processing_time, release_date, due_date = divide(well_df)
        rati = ratio2(production_rate,processing_time)
        wi1, ti1, di1, sor_ratio = sort(rati)
        well_dict = priority(wi1, production_rate, release_date, processing_time)
        result, rigs, wells,date = calculation(well_dict, rigs_dict)
        total_loss = cost(rigs, wells, date)
        ganntchart(n, well_df, result)
        print(total_loss)
    elif n == 3:
        rigs_dict = files(rig_df)
        well_name, production_rate, processing_time, release_date, due_date = divide(well_df)
        rati = ratio3(production_rate,processing_time)
        wi1, ti1, di1, sor_ratio = sort(rati)
        well_dict = priority(wi1, production_rate, release_date, processing_time)
        result, rigs, wells, date = calculation(well_dict, rigs_dict)
        total_loss = cost(rigs, wells, date)
        ganntchart(n, well_df, result)
        print(total_loss)
    else:
        print('Enter above methods only .')
    print('\n')

from datetime import datetime,timedelta
import pandas as pd

rigs = [{'name': 'Rig 1', 'capacity': 1, 'processing_time': 5, 'assigned_wells': ['well 3', 'well 6']}, {'name': 'Rig 2', 'capacity': 1, 'processing_time': 4, 'assigned_wells': ['well 2']}, {'name': 'Rig 3', 'capacity': 1, 'processing_time': 5, 'assigned_wells': ['well 7', 'well 8', 'well 5']}, {'name': 'Rig 4', 'capacity': 1, 'processing_time': 3, 'assigned_wells': ['well 1', 'well 10']}, {'name': 'Rig 5', 'capacity': 1, 'processing_time': 3, 'assigned_wells': ['well 9', 'well 4']}]
wells = [{'name': 'well 1', 'priority': 5, 'release_date': '01-01-2023', 'processing_time': 1, 'production_rate': 10}, {'name': 'well 2', 'priority': 2, 'release_date': '01-01-2023', 'processing_time': 4, 'production_rate': 30}, {'name': 'well 3', 'priority': 1, 'release_date': '01-01-2023', 'processing_time': 2, 'production_rate': 40}, {'name': 'well 4', 'priority': 10, 'release_date': '01-01-2023', 'processing_time': 1, 'production_rate': 1}, {'name': 'well 5', 'priority': 3, 'release_date': '04-01-2023', 'processing_time': 2, 'production_rate': 30}, {'name': 'well 6', 'priority': 8, 'release_date': '01-01-2023', 'processing_time': 3, 'production_rate': 5}, {'name': 'well 7', 'priority': 4, 'release_date': '01-01-2023', 'processing_time': 2, 'production_rate': 20}, {'name': 'well 8', 'priority': 9, 'release_date': '01-01-2023', 'processing_time': 1, 'production_rate': 2}, {'name': 'well 9', 'priority': 6, 'release_date': '01-01-2023', 'processing_time': 2, 'production_rate': 10}, {'name': 'well 10', 'priority': 7, 'release_date': '01-01-2023', 'processing_time': 2, 'production_rate': 10}]
total_loss = 0
date = '01-01-2023'
current_date = datetime.strptime(date, '%d-%m-%Y')
for rig in rigs:
    k = 0
    # print(rig)
    for w_1 in rig['assigned_wells']:
        # print(w_1)

        for well in wells:
            if well['name'] == w_1:
                well_release_date = datetime.strptime(well['release_date'], '%d-%m-%Y')
                delay = (current_date - well_release_date).days
                loss = well['production_rate'] * (well['processing_time'] + delay)
                total_loss += loss
                print(total_loss)
                temp = str(timedelta(days=well['processing_time']))
                print(temp)
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


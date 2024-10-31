import datetime
import random
import pandas as pd
from datetime import timedelta,date
today = date.today()
names = []
pi = []
ti = []
di = []
Di = []
for i in range(5):

    n = int(input('enter the range'))
    for i in range(n):
        name = i+1
        production_rate = random.randint(10,50)
        processing_time = random.randint(1, 5)

        release_date = date.today()
        if (n % 3 == 0):
            release_date += timedelta(days=4)
        due_date = random.randint(1,5)
        names.append('well '+str(name))
        pi.append(production_rate)
        ti.append(processing_time)
        di.append(release_date)
        Di.append(due_date)
        
    dict = dict(names = names, production_rate=pi, processing_time=ti, release_date=di, due_date=Di)
    df = pd.DataFrame(dict)

    df.to_csv(r'C:\Users\reddy\Documents\rig scheduling\random generator values\hmpt_datasets\sample_hmpt_' +str(n)+'.csv')
    print(df)
    names.clear()
    pi.clear()
    ti.clear()
    di.clear()
    Di.clear()
    del dict

import random
import pandas as pd
pi = []
ti = []
for i in range(5):

    n = int(input('enter the range'))
    for i in range(n):
        processing_time = random.randint(1,20)
        production_rate = random.randint(40, 150)
        pi.append(processing_time)
        ti.append(production_rate)

    dict = dict(processing_time = pi, productivity_barrels_per_day=ti)
    df = pd.DataFrame(dict)
    print(df)

    df.to_csv(r'C:\Users\reddy\Documents\rig scheduling\random generator values\general_datasets\sample_datasets_' +str(n)+'.csv')
    pi.clear()
    ti.clear()
    del dict

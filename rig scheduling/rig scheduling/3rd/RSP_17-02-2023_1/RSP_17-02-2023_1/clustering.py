import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Generate random well and rig locations
num_wells = 1000
num_rigs = 20
# Set the seed for reproducibility
np.random.seed(123)

wells_lat = np.random.uniform(low=40, high=45, size=num_wells)
wells_lon = np.random.uniform(low=-80, high=-75, size=num_wells)
wells_df = pd.DataFrame({'lat': wells_lat, 'lon': wells_lon})

rigs_lat = np.random.uniform(low=40, high=45, size=num_rigs)
rigs_lon = np.random.uniform(low=-80, high=-75, size=num_rigs)
rigs_df = pd.DataFrame({'lat': rigs_lat, 'lon': rigs_lon})

# Convert latitudes and longitudes to radians
wells_rad = np.radians(wells_df[['lat', 'lon']].values)
rigs_rad = np.radians(rigs_df[['lat', 'lon']].values)

# Compute distances between wells and rigs using the Haversine formula
lat1 = wells_rad[:, 0]
lat2 = rigs_rad[:, 0]
lon1 = wells_rad[:, 1]
lon2 = rigs_rad[:, 1]
dlat = lat2 - lat1
dlon = lon2 - lon1
a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
c = 2 * np.arcsin(np.sqrt(a))
distances = 6371 * c

# Perform clustering
num_clusters = len(rigs_df)
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(distances)

well_clusters = kmeans.labels_

for i in range(num_clusters):
    cluster_wells = np.where(well_clusters == i)[0]
    print(f"Wells assigned to Cluster {i+1}:")
    for well_index in cluster_wells:
        print(f"({wells_df.iloc[well_index]['lat']}, {wells_df.iloc[well_index]['lon']})")
    print()  # print an empty line to separate the clusters

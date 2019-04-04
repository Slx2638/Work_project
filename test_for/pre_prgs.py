import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
ss = StandardScaler()

food_file = 'food_data.csv'

food_list = []
name_list = []
with open(food_file,encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    food_header = next(csv_reader)
    del food_header[0]
    for row in csv_reader:
        name_list.append(row[0])
        del row[0]
        food_list.append(row)

SSE = []
SCORES = []
CHANGE = []
food_array = np.array(food_list)
#z-score
df = preprocessing.scale(food_array)
# print(df)
X = range(2,45)
for k in X:
    estimator = KMeans(n_clusters=k)
    estimator.fit(df)
    SSE.append(estimator.inertia_)
    SCORES.append(silhouette_score(df,estimator.labels_,metric='euclidean'))
    CHANGE.append(
        sum(
            np.min(
                cdist(df, estimator.cluster_centers_, metric='euclidean'), axis=1)
            / df.shape[0])
    )


plt.xlabel("k")
plt.figure(1)
plt.ylabel("手肘")
plt.plot(X,SSE,'bx-')
plt.figure(2)
plt.ylabel('轮廓系数')
plt.plot(X,SCORES,'bx-')
plt.figure(3)
plt.ylabel("平均畸变程度")
plt.plot(X,CHANGE,'bx-')
plt.show()

# kmodel = KMeans(n_clusters=37, n_jobs=6)
#
# print(kmodel.fit_predict(df))




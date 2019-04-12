import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



df = pd.read_csv('food_data.csv', encoding='utf-8')
nutrient_list = df.columns.tolist()[1:] # 食物营养素名称列表
print(nutrient_list)
#
# # str1 = input("第一种食物")
# # str2 = input("第二种食物")
#
df1 = df.loc[df['食物名称(100g)'] == '小麦'].drop(['食物名称(100g)'],axis=1)
df2 = df.loc[df['食物名称(100g)'] == '花卷']
str1_number = np.array(df1).tolist()[0] # 营养素含量数值列表

print(str1_number)
str2_number = np.array(df2).tolist()[0]

print(pd.Series(df1))

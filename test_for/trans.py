import pandas as pd

data = pd.read_excel('food.xls','Food Nutrition',index_col=0)
data.to_csv('food_data.csv',encoding='utf-8')

import pandas as pd


df = pd.read_csv('HR.csv')
# print(df) #dataframe 类型数据集

# print(df.mean()) #求各列的均值 series形式

# print(df['column_name'].mean()) #均值
# df['column_name'].median() 中位数
# df['column_name'].quantile(q=0.25)  四分位数
# df['column_name'].mode()  众数


# df.std() 标准差
# df.var() 方差



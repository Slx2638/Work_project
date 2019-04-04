import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import csv
import re
import wx
from numpy import *
import matplotlib.pyplot as plt
from pylab import mpl
from matplotlib.font_manager import _rebuild

_rebuild() 

mpl.rcParams['font.sans-serif'] = ['SimHei']
# gui
app = wx.App()
frame = wx.Frame(None, title="食物查询", pos=(100, 200), size=(600, 450))

search_text = wx.TextCtrl(frame, pos=(5, 5), size=(400, 24))
search_button = wx.Button(frame, label="查询", pos=(440, 5), size=(50, 24))
content_text= wx.TextCtrl(frame,pos = (5,39),size = (400,200),style = wx.TE_MULTILINE)
foodname_text = wx.TextCtrl(frame, pos=(5, 260), size=(400, 24))
show_button = wx.Button(frame, label="查看食物营养元素", pos=(440, 260), size=(130, 24))

food_data = []
food_file = 'food_data.csv'
with open(food_file,encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    food_header = next(csv_reader)
    for row in csv_reader:
        food_data.append(row)

food_data = np.array(food_data)

def search_food(evevt):
    i = 0
    index_list = []
    food_list = []
    search_content = search_text.GetValue()
    while(i < food_data.shape[0]):
        if re.findall(search_content,str(food_data[i][0])):
            index_list.append(i)
        i += 1
    if len(index_list) != 0:
        for i in index_list:
            food_content = []
            for j in range(food_data.shape[1]):
                food_content.append(food_data[i][j])
            food_list.append(pd.Series(food_content))
    else:
        content_text.SetValue('not found')
    food_df = pd.DataFrame(food_list)
    food_df.columns = food_header
    index_content = food_df['食物名称(100g)'].tolist()
    def show_list(list):
        str = '查询到的食物：' + '\n'
        for i in range(len(list)):
            str += list[i] + '\n'
        return str
    content_text.SetValue(str(show_list(index_content)))

def show_food(evevt):
    i = 0
    index_list = []
    food_list = []
    search_content = foodname_text.GetValue()
    while(i < food_data.shape[0]):
        if search_content == str(food_data[i][0]):
            index_list.append(i)
        i += 1
    if len(index_list) != 0:
        for i in index_list:
            food_content = []
            for j in range(food_data.shape[1]):
                food_content.append(food_data[i][j])
            food_list.append(pd.Series(food_content))
    else:
        content_text.SetValue('not found')
    plt.cla()
    food_df = pd.DataFrame(food_list)
    food_df.columns = food_header
    # print(food_df)    #DataFrame
    index_content = food_df['食物名称(100g)'].tolist()
    food_df = food_df.T
    food_df.columns = index_content
    food_df = food_df.drop(['食物名称(100g)'])
    nutrition_list = food_df.index.tolist()
    food_df = food_df[index_content[0]].astype(int)
    food_dict = food_df.tolist()
    food_dict = [int(item)for item in food_dict]

    f_a = np.arange(len(nutrition_list))
    for i in range(len(food_dict)):
        plt.text(food_dict[i]+10,f_a[i], food_dict[i],ha='center', va='bottom', fontsize=11)

    plt.title(index_content[0])
    plt.xlabel('含量/100g')
    plt.ylabel('营养元素种类')
    plt.xlim(0,1000)
    food_df.plot(kind='barh')



search_button.Bind(wx.EVT_BUTTON,search_food)
show_button.Bind(wx.EVT_BUTTON,show_food)

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)



frame.Show()
app.MainLoop()


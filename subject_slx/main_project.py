#coding=utf-8
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import numpy as np
import xlwt

import pandas as pd
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


def spy():
	from urllib import request
	class Spider():
		food_id = 1
		kind_parttern = '<span class="text-muted">(.*)</span>'
		root_partten = '<table class="cstable" width="680" style="text-align:center;">([\s\S]*?)</table>'
		nutrition_partten = '<a class="bblue" href="pen.asp([\s\S]*?)</a>'
		number_parttern = '<td width="16%">(.*)<span class="bgray">'
		unit_parttern = '<span class="bgray">(.*)</span>'

		workbook = xlwt.Workbook(encoding='utf-8')
		worksheet = workbook.add_sheet('Food Nutrition')
		row0 = ['食物名称(100g)',
				'热量(kcal)', '硫胺素(mg)', '钙(mg)',
				'蛋白质(g)', '核黄素(mg)', '镁(mg)',
				'脂肪(g)', '烟酸(mg)', '铁(mg)',
				'碳水化合物(g)', '维生素C(mg)', '锰(mg)',
				'膳食纤维(g)', '维生素E(mg)', '锌(mg)',
				'维生素A(ug)', '胆固醇(mg)', '铜(mg)',
				'胡萝卜素(ug)', '钾(mg)', '磷(mg)',
				'视黄醇当量(ug)', '钠(mg)', '硒(mg)', ]
		for i in range(0, len(row0)):
			worksheet.write(0, i, row0[i])
		#获取html
		def __fetch_content(self):
			url_old = 'https://yingyang.supfree.net/wochuo.asp?id='
			url = url_old + str(self.__class__.food_id)
			r = request.urlopen(url)
			htmls = r.read()
			htmls = str(htmls, encoding='gb2312')
			self.__class__.food_id += 1
			if self.__class__.food_id == 1298:
				self.__class__.food_id += 1
			return htmls
		#处理html
		def __analysis(self, htmls, y):
			root_htmls = re.findall(Spider.root_partten, htmls)
			food_name = re.findall(Spider.kind_parttern, htmls)
			anchors = []
			for html in root_htmls:
				nutrition = re.findall(Spider.nutrition_partten, html)
				number = re.findall(Spider.number_parttern, html)
				unit = re.findall(Spider.unit_parttern, html)
				anchor = {'nutrition': nutrition, 'number': number, 'unit': unit}
				anchors.append(anchor)
			food_list = []
			food_list.append(food_name[0])
			for i in range(24):
				food_list.append(anchors[0]['number'][i])
			self.__write_excel(y, food_list)

		def __write_excel(self, y, f_list):
			for i in range(len(f_list)):
				self.worksheet.write(y, i, f_list[i])

		def go(self):
			for i in range(1439):
				htmls = self.__fetch_content()
				self.__analysis(htmls, i + 1)
			self.workbook.save('food.xls')

	spider = Spider()
	spider.go()

	data = pd.read_excel('food.xls', 'Food Nutrition', index_col=0)
	data.to_csv('food_data.csv', encoding='utf-8')


def f_search():
	import pandas as pd
	import csv
	import re
	import wx
	import matplotlib.pyplot as plt
	from pylab import mpl
	from matplotlib.font_manager import _rebuild
	#中文
	_rebuild()
	mpl.rcParams['font.sans-serif'] = ['SimHei']
	app = wx.App()

	frame = wx.Frame(None, title="食物查询", pos=(100, 200), size=(600, 450))
	search_text = wx.TextCtrl(frame, pos=(5, 5), size=(400, 24))
	search_button = wx.Button(frame, label="查询", pos=(440, 5), size=(50, 24))
	content_text = wx.TextCtrl(frame, pos=(5, 39), size=(400, 200), style=wx.TE_MULTILINE)
	foodname_text = wx.TextCtrl(frame, pos=(5, 260), size=(400, 24))
	show_button = wx.Button(frame, label="查看食物营养元素", pos=(440, 260), size=(130, 24))

	food_data = []
	food_file = 'food_data.csv'
	with open(food_file, encoding='utf-8') as csvfile:
		csv_reader = csv.reader(csvfile)
		food_header = next(csv_reader)
		for row in csv_reader:
			food_data.append(row)

	food_data = np.array(food_data)
	#模糊搜索
	def search_food(evevt):
		i = 0
		index_list = []
		food_list = []
		search_content = search_text.GetValue()
		while (i < food_data.shape[0]):
			if re.findall(search_content, str(food_data[i][0])):
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
	#具体数据
	def show_food(evevt):
		i = 0
		index_list = []
		food_list = []
		search_content = foodname_text.GetValue()
		while (i < food_data.shape[0]):
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
		food_dict = [int(item) for item in food_dict]

		f_a = np.arange(len(nutrition_list))
		for i in range(len(food_dict)):
			plt.text(food_dict[i] + 10, f_a[i], food_dict[i], ha='center', va='bottom', fontsize=11)

		plt.title(index_content[0])
		plt.xlabel('含量/100g')
		plt.ylabel('营养元素种类')
		food_df.plot(kind='barh')

	search_button.Bind(wx.EVT_BUTTON, search_food)
	show_button.Bind(wx.EVT_BUTTON, show_food)

	pd.set_option('display.unicode.ambiguous_as_wide', True)
	pd.set_option('display.unicode.east_asian_width', True)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)

	frame.Show()
	app.MainLoop()


def selectfile():
	global filename
	filename=filedialog.askopenfilename()
	print(filename)


def clu():
	top = Toplevel()
	top.title('聚类分析')
	top.geometry('200x200')
	Label(top,text='', width=5).grid(column=1, row=1)
	Label(top,text='', width=5).grid(column=1, row=2)
	Label(top,text='', width=5).grid(column=2, row=1)
	Label(top,text='', width=5).grid(column=2, row=2)
	Button(top, text='导入文件',width=15,command=selectfile).grid(row=3,column=2,padx=1,pady=1)
	Button(top, text='聚类',width=15,command=clust).grid(row=4,column=2,padx=1,pady=1)


def clust():
	global df
	df = pd.read_csv(filename,encoding='utf-8')
	#zscore
	df1 = df.drop(['食物名称(100g)'],axis=1)
	data = scale(df1)

	# dlen = len(df1)
	# n_cluster = int(np.sqrt(dlen))
	global n_cluster
	n_cluster = 38

	km = KMeans(n_clusters=n_cluster,random_state=0)
	km.fit(data)
	# centers = km.cluster_centers_  #聚类中心
	labels = km.labels_
	df['label'] = labels
	df.to_csv('clu_result.csv', index=False)
	df.columns
	return df


def show_result():
	from tkinter import ttk
	top = Toplevel()
	top.title('查看类别')
	top.geometry('300x200')
	tarea = Label(top,text='输入类别数：')
	tarea.grid(column=0, row=1)
	number = StringVar()
	numberChosen = ttk.Combobox(top, width=12, textvariable=number)
	numberChosen['values'] = list(range(n_cluster))  # 下拉列表
	numberChosen.current(0)
	global n
	def show_msg(*args):
		n=numberChosen.get()
		print('class:',number)
		tmp_df = df.loc[df.label == int(n),]
		newwindow = Toplevel()
		newwindow.title('数据', )
		# 创建表格
		tree_date = ttk.Treeview(newwindow,height=30)
		# 定义列
		tree_date['columns'] = list(tmp_df.columns)
		tree_date.pack()
		vbar = ttk.Scrollbar(newwindow, orient=VERTICAL, command=tree_date.yview)
		tree_date.configure(yscrollcommand=vbar.set)
		tree_date.grid(row=0, column=0, sticky=NSEW)
		vbar.grid(row=0, column=1, sticky=NS)
		# 列宽度
		w = 1600
		for col in tmp_df.columns:
			tree_date.column(str(col), width=int(w/(len(tmp_df.columns)+3)))
			tree_date.heading(str(col), text=col)
		# 表格添加数据
		for i in range(len(tmp_df)):
			data = tuple(list(tmp_df.iloc[i,]))
			tree_date.insert('', i, text=i, values=data)
		newwindow.mainloop()
	numberChosen.bind("<<ComboboxSelected>>", show_msg)
	numberChosen.grid(column=3, row=1)


def apply_search():
	top = Toplevel()
	top.title('营养素查询')
	top.geometry('300x150')
	tarea = Label(top, text='输入营养素名称：')
	tarea.grid(column=0, row=1)
	v1 = StringVar()
	search_text = Entry(top,textvariable=v1,width=10)
	search_text.grid(row=2,column=0,padx=1,pady=1)
	global nutrient
	def query(*args):
		nutrient = search_text.get()
		try:
			col=[c for c in df.columns if nutrient in c]
			if len(col)>0:
				col=col[0]
			tmp_df = df[df[col]>0].sort_values(by=col,ascending=False)#筛选

			cols = [df.columns[0],col]
			tmp_df = tmp_df[cols]
			tmp_df = tmp_df.reset_index(drop=True)
		except:
			tmp_df=pd.DataFrame()
		newwindow = Toplevel()
		newwindow.title('数据', )
		newwindow.geometry('640x480')
		tree_date = ttk.Treeview(newwindow, height=30)
		# 定义列
		tree_date['columns'] = list(tmp_df.columns)
		tree_date.pack()
		vbar = ttk.Scrollbar(newwindow, orient=VERTICAL, command=tree_date.yview)
		tree_date.configure(yscrollcommand=vbar.set)
		tree_date.grid(row=0, column=0, sticky=NSEW)
		vbar.grid(row=0, column=1, sticky=NS)
		# 设置列宽度
		w = 640
		for col in tmp_df.columns:
			tree_date.column(str(col), width=int(w / (len(tmp_df.columns) + 3)))
			tree_date.heading(str(col), text=col)
		if len(tmp_df) == 0:
			tree_date.insert('end', '0 results')
		else:
			for i in range(len(tmp_df)):
				data = tuple(list(tmp_df.iloc[i,]))
				tree_date.insert('', i, text=i, values=data)
		newwindow.mainloop()
	Button(top, text='查询', command=query).grid(row=2, column=1, padx=1, pady=1)


def main():
	root = Tk()
	root.geometry('400x300')

	Label(text='',width=8).grid(column=1,row=1)
	Label(text='',width=8).grid(column=1,row=2)
	Label(text='',width=8).grid(column=1,row=3)
	Label(text='',width=8).grid(column=1,row=4)
	Label(text='',width=8).grid(column=1,row=5)
	Button(root, text='查询数据', fg='red', width=30, underline=4, command=f_search).grid(column=4, row=3)
	Button(root, text='聚类分析', fg='red', width=30, underline=4, command=clu).grid(column=4, row=4)
	Button(root, text='查看类别', fg='red', width=30, underline=4, command=show_result).grid(column=4, row=5)
	Button(root, text='应用查询', fg='red', width=30, underline=4, command=apply_search).grid(column=4, row=6)
	Button(root, text='爬取数据', fg='red', width=30, underline=4, command=spy).grid(column=4, row=7)
	mainloop()

if __name__ == '__main__':
	main()
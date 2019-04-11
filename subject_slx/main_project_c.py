#coding=utf-8
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import numpy as np
import xlwt

import pandas as pd
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
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
	import csv
	import re
	import wx
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
	Button(top, text='导入文件',width=15,command=selectfile).grid(row=3,column=2,padx=1,pady=1)
	Button(top, text='聚类',width=15,command=clust_pre).grid(row=4,column=2,padx=1,pady=1)

#手肘轮廓图
def draw():
	from sklearn.metrics import silhouette_score
	SSE = []
	SCORES = []
	X = range(2, 40)
	for k in X:
		estimator = KMeans(n_clusters=k)
		estimator.fit(data)
		SSE.append(estimator.inertia_)
		SCORES.append(silhouette_score(data, estimator.labels_, metric='euclidean'))

	plt.xlabel("k")
	plt.figure(1)
	plt.ylabel("手肘")
	plt.plot(X, SSE, 'bx-')
	plt.figure(2)
	plt.ylabel('轮廓系数')
	plt.plot(X, SCORES, 'bx-')

flag_1 = False
flag_2 = False
flag_3 = False
flag_4 = False
flag_5 = False
flag_6 = False
flag_7 = False
flag_8 = False
flag_9 = False
flag_10 = False
flag_11 = False
flag_12 = False
flag_13 = False
flag_14 = False
flag_15 = False
flag_16 = False
flag_17 = False
flag_18 = False
flag_19 = False
flag_20 = False
flag_21 = False
flag_22 = False
flag_23 = False
flag_24 = False

def clust_pre():
	top = Toplevel()
	top.title("聚类准备")
	top.geometry("700x400")

	global list_content
	list_content = []
	nutrient_list = ['热量(kcal)', '硫胺素(mg)', '钙(mg)',
					 '蛋白质(g)', '核黄素(mg)', '镁(mg)',
					 '脂肪(g)', '烟酸(mg)', '铁(mg)',
					 '碳水化合物(g)', '维生素C(mg)', '锰(mg)',
					 '膳食纤维(g)', '维生素E(mg)', '锌(mg)',
					 '维生素A(ug)', '胆固醇(mg)', '铜(mg)',
					 '胡萝卜素(ug)', '钾(mg)', '磷(mg)',
					 '视黄醇当量(ug)', '钠(mg)', '硒(mg)', ]

	lab = ttk.Label(top, text='请选择需要的营养元素：')
	lab.grid(row=0, columnspan=3)
	Button(top, text='画图确定k值', width=15, command=draw).grid(row=6, column=0, padx=1, pady=1)
	Label(top, text='输入k值', width=15).grid(column=0, row=7)
	var = StringVar()
	k_var = Entry(top, textvariable = var)
	k_var.grid(column=0, row=8)

	global df
	df = pd.read_csv(filename, encoding='utf-8')

	def click_1():
		global flag_1
		flag_1 = not flag_1
		if flag_1:
			list_content.append(nutrient_list[0])
		else:
			list_content.remove(nutrient_list[0])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_2():
		global flag_2
		flag_2 = not flag_2
		if flag_2:
			list_content.append(nutrient_list[1])
		else:
			list_content.remove(nutrient_list[1])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_3():
		global flag_3
		flag_3 = not flag_3
		if flag_3:
			list_content.append(nutrient_list[2])
		else:
			list_content.remove(nutrient_list[2])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_4():
		global flag_4
		flag_4 = not flag_4
		if flag_4:
			list_content.append(nutrient_list[3])
		else:
			list_content.remove(nutrient_list[3])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_5():
		global flag_5
		flag_5 = not flag_5
		if flag_5:
			list_content.append(nutrient_list[4])
		else:
			list_content.remove(nutrient_list[4])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_6():
		global flag_6
		flag_6 = not flag_6
		if flag_6:
			list_content.append(nutrient_list[5])
		else:
			list_content.remove(nutrient_list[5])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_7():
		global flag_7
		flag_7 = not flag_7
		if flag_7:
			list_content.append(nutrient_list[6])
		else:
			list_content.remove(nutrient_list[6])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_8():
		global flag_8
		flag_8 = not flag_8
		if flag_8:
			list_content.append(nutrient_list[7])
		else:
			list_content.remove(nutrient_list[7])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_9():
		global flag_9
		flag_9 = not flag_9
		if flag_9:
			list_content.append(nutrient_list[8])
		else:
			list_content.remove(nutrient_list[8])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_10():
		global flag_10
		flag_10 = not flag_10
		if flag_10:
			list_content.append(nutrient_list[9])
		else:
			list_content.remove(nutrient_list[9])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_11():
		global flag_11
		flag_11 = not flag_11
		if flag_11:
			list_content.append(nutrient_list[10])
		else:
			list_content.remove(nutrient_list[10])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_12():
		global flag_12
		flag_12 = not flag_12
		if flag_12:
			list_content.append(nutrient_list[11])
		else:
			list_content.remove(nutrient_list[11])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_13():
		global flag_13
		flag_13 = not flag_13
		if flag_13:
			list_content.append(nutrient_list[12])
		else:
			list_content.remove(nutrient_list[12])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_14():
		global flag_14
		flag_14 = not flag_14
		if flag_14:
			list_content.append(nutrient_list[13])
		else:
			list_content.remove(nutrient_list[13])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_15():
		global flag_15
		flag_15 = not flag_15
		if flag_15:
			list_content.append(nutrient_list[14])
		else:
			list_content.remove(nutrient_list[14])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_16():
		global flag_16
		flag_16 = not flag_16
		if flag_16:
			list_content.append(nutrient_list[15])
		else:
			list_content.remove(nutrient_list[15])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_17():
		global flag_17
		flag_17 = not flag_17
		if flag_17:
			list_content.append(nutrient_list[16])
		else:
			list_content.remove(nutrient_list[16])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_18():
		global flag_18
		flag_18 = not flag_18
		if flag_18:
			list_content.append(nutrient_list[17])
		else:
			list_content.remove(nutrient_list[17])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_19():
		global flag_19
		flag_19 = not flag_19
		if flag_19:
			list_content.append(nutrient_list[18])
		else:
			list_content.remove(nutrient_list[18])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_20():
		global flag_20
		flag_20 = not flag_20
		if flag_20:
			list_content.append(nutrient_list[19])
		else:
			list_content.remove(nutrient_list[19])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_21():
		global flag_21
		flag_21 = not flag_21
		if flag_21:
			list_content.append(nutrient_list[20])
		else:
			list_content.remove(nutrient_list[20])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_22():
		global flag_22
		flag_22 = not flag_22
		if flag_22:
			list_content.append(nutrient_list[21])
		else:
			list_content.remove(nutrient_list[21])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_23():
		global flag_23
		flag_23 = not flag_23
		if flag_23:
			list_content.append(nutrient_list[22])
		else:
			list_content.remove(nutrient_list[22])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)
	def click_24():
		global flag_24
		flag_24 = not flag_24
		if flag_24:
			list_content.append(nutrient_list[23])
		else:
			list_content.remove(nutrient_list[23])
		global df1
		global data
		df1 = df.drop(['食物名称(100g)'], axis=1)
		df1 = df1.loc[:, list_content]
		data = scale(df1)


		# 多选框
	frm = ttk.Frame(top)
	ttk.Checkbutton(frm, text='热量(kcal)', command=click_1).grid(row=0)
	ttk.Checkbutton(frm, text='硫胺素(mg)', command=click_2).grid(row=0, column=1)
	ttk.Checkbutton(frm, text='钙(mg)', command=click_3).grid(row=0, column=2)
	ttk.Checkbutton(frm, text='蛋白质(g)', command=click_4).grid(row=0, column=3)
	ttk.Checkbutton(frm, text='核黄素(mg)', command=click_5).grid(row=0, column=4)
	ttk.Checkbutton(frm, text='镁(mg)', command=click_6).grid(row=0, column=5)
	ttk.Checkbutton(frm, text='脂肪(g)', command=click_7).grid(row=1)
	ttk.Checkbutton(frm, text='烟酸(mg)', command=click_8).grid(row=1, column=1)
	ttk.Checkbutton(frm, text='铁(mg)', command=click_9).grid(row=1, column=2)
	ttk.Checkbutton(frm, text='碳水化合物(g)', command=click_10).grid(row=1, column=3)
	ttk.Checkbutton(frm, text='维生素C(mg)', command=click_11).grid(row=1, column=4)
	ttk.Checkbutton(frm, text='锰(mg)', command=click_12).grid(row=1, column=5)
	ttk.Checkbutton(frm, text='膳食纤维(g)', command=click_13).grid(row=2)
	ttk.Checkbutton(frm, text='维生素E(mg)', command=click_14).grid(row=2, column=1)
	ttk.Checkbutton(frm, text='锌(mg)', command=click_15).grid(row=2, column=2)
	ttk.Checkbutton(frm, text='维生素A(ug)', command=click_16).grid(row=2, column=3)
	ttk.Checkbutton(frm, text='胆固醇(mg)', command=click_17).grid(row=2, column=4)
	ttk.Checkbutton(frm, text='铜(mg)', command=click_18).grid(row=2, column=5)
	ttk.Checkbutton(frm, text='胡萝卜素(ug)', command=click_19).grid(row=3)
	ttk.Checkbutton(frm, text='钾(mg)', command=click_20).grid(row=3, column=1)
	ttk.Checkbutton(frm, text='磷(mg)', command=click_21).grid(row=3, column=2)
	ttk.Checkbutton(frm, text='视黄醇当量(ug)', command=click_22).grid(row=3, column=3)
	ttk.Checkbutton(frm, text='钠(mg)', command=click_23).grid(row=3, column=4)
	ttk.Checkbutton(frm, text='硒(mg)', command=click_24).grid(row=3, column=5)
	frm.grid(row=4)

	def clust():
		global n_cluster
		n_cluster = int(k_var.get())
		km = KMeans(n_clusters=n_cluster, random_state=0)
		km.fit(data)
		# centers = km.cluster_centers_  #聚类中心
		labels = km.labels_
		df['label'] = labels
		df.to_csv('clu_result_c.csv', index=False)
		return df

	Button(top, text='聚类', width=15, command=clust).grid(row=10, column=0, padx=1, pady=1)

	top.mainloop()

def show_result():

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
	var = StringVar()
	search_text = Entry(top,textvariable=var,width=10)
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
		newwindow.geometry('640x640')
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
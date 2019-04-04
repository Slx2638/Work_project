from tkinter import filedialog
from tkinter import *
from urllib import request
import xlwt
import re
import numpy as np
from numpy import *
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


def eu_dist(v1,v2):
	dist = sum([(x1-x2)**2 for x1,x2 in zip(v1,v2)])
	return dist

def crit_dist(v_data,centers):
	dists = 0
	for v in v_data:
		for c in centers:
			dists+= eu_dist(v,c)
	return dists

#聚类
def clust():
	global df
	df = pd.read_csv(filename,encoding='utf-8')
	df.head(2)
	#zscore
	df1 = df.drop(['食物名称(100g)'],axis=1)
	
	data = scale(df1)
	dlen = len(df1)
	global n_cluster
	best_n = 0
	best_crit = 10000000
	# for n_cluster in range(3,int(np.sqrt(dlen))):
	for n_cluster in range(3,10):
		# print(n_cluster)
		data1=data[0:int(dlen/3),]
		data2=data[int(dlen/3):2*int(dlen/3),]
		data3=data[2*int(dlen/3):,]

		crits = []
		for k in range(3):
			if k==0:
				v_data = data3
				c_data = np.vstack((data1,data2))
			elif k==1:
				v_data = data2
				c_data = np.vstack((data1,data3))
			elif k==2:
				v_data = data1
				c_data = np.vstack((data2,data3))

			km = KMeans(n_clusters=n_cluster, random_state=0)
			km.fit(c_data)
			centers = km.cluster_centers_
			labels = km.labels_

			crit = crit_dist(v_data,centers)
			crits.append(crit)
		if np.mean(crits) <best_crit:
			best_n = n_cluster
			best_crit = np.mean(crits)
			# clu_dists.append((n_cluster,np.mean(crits)))


	# n_cluster = int(np.sqrt(dlen))
	print('最优类别数目为：', best_n)
	n_cluster = best_n
	km = KMeans(n_clusters=best_n, random_state=0)
	km.fit(data)
	centers = km.cluster_centers_
	labels = km.labels_


	# 数据标签加入原始数据
	df['label'] = labels

	# 数据（带有类别）结果写入本地文件
	df.to_csv('聚类结果.csv', index=False)

	print(df.head(1))
	df.columns

	pca = PCA()
	ndf = df.drop(['食物名称(100g)','热量(kcal)'], axis=1)
	pca.fit(ndf)
	print(pca.explained_variance_ratio_)
	vols = pca.transform(ndf)[::, 0]
	vols.shape

	# 画图
	plt.scatter(vols, df1.iloc[:, 1], marker='.', c=labels)
	len(vols)
	plt.show()

	return df


def selectfile():
	global filename
	filename=filedialog.askopenfilename()

#查询数据
def f_search():
	import pandas as pd
	import csv
	import re
	import wx
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
		plt.xlim(0, 1000)
		food_df.plot(kind='barh')

	search_button.Bind(wx.EVT_BUTTON, search_food)
	show_button.Bind(wx.EVT_BUTTON, show_food)

	pd.set_option('display.unicode.ambiguous_as_wide', True)
	pd.set_option('display.unicode.east_asian_width', True)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)

	frame.Show()
	app.MainLoop()





def show2():
	pass

def clu():
	top = Toplevel()
	top.title('聚类分析')
	top.geometry('300x200')
	# v1 = StringVar()
	# e1 = Entry(top,textvariable=v1,width=10)
	# e1.grid(row=1,column=0,padx=1,pady=1)
	# Button(root, text="文件", command=selectPath)
	Label(top,text='', width=5).grid(column=1, row=1)
	Label(top,text='', width=5).grid(column=1, row=2)
	Label(top,text='', width=5).grid(column=2, row=1)
	Label(top,text='', width=5).grid(column=2, row=2)
	Button(top, text='导入',width=15,command=selectfile).grid(row=3,column=2,padx=1,pady=1)
	Button(top, text='聚类',width=15,command=clust).grid(row=4,column=2,padx=1,pady=1)


#聚类结果查询
def show_sk():
	# print('chakan:',df.head(1))
	top = Toplevel()
	top.title('查看类别')
	top.geometry('200x200')
	# v1 = StringVar()
	# e1 = Entry(top,textvariable=v1,width=10)
	# e1.grid(row=1,column=0,padx=1,pady=1)
	# Button(root, text="文件", command=selectPath)
	# Button(top, text='导入',command=selectfile).grid(row=1,column=1,padx=1,pady=1)
	# Button(top, text='聚类',command=clust).grid(row=2,column=1,padx=1,pady=1)

	from tkinter import ttk
	tarea = Label(top,text='clust:')
	tarea.grid(column=0, row=1)
	number = StringVar()
	numberChosen = ttk.Combobox(top, width=12, textvariable=number)
	numberChosen['values'] = list(range(n_cluster))  # 下拉列表
	numberChosen.current(0)  # 下标
	global v
	def show_msg(*args):
		v=numberChosen.get()
		print('class:',v)
		tmp_df = df.loc[df.label == int(v),]
		newwindow = Toplevel()
		newwindow.title('数据', )
		# newwindow.geometry('640x480')
		w = newwindow.winfo_screenwidth()
		h = newwindow.winfo_screenheight()
		newwindow.geometry("%dx%d" % (w, h))

		text1 = Text(newwindow, width=w, height=h)


		colnames = ' '.join(tmp_df.columns) + '\n'
		text1.insert('end',colnames)
		for i in range(len(tmp_df)):
			data = ' '.join([str(x) for x in list(tmp_df.iloc[i,])])
			print(i,data)
			text1.insert('end', data+'\n')
		text1.pack()

	numberChosen.bind("<<ComboboxSelected>>", show_msg)

	numberChosen.grid(column=1, row=1)



def main():
	root = Tk()
	root.geometry('400x300')

	Label(text='',width=8).grid(column=1,row=1)
	Label(text='',width=8).grid(column=1,row=2)
	Label(text='',width=8).grid(column=1,row=3)
	Label(text='',width=8).grid(column=1,row=4)
	Label(text='',width=8).grid(column=1,row=5)
	Button(root, text='查询数据',fg='red',width=30,	underline=4, command=f_search).grid(column=4, row=3)
	Button(root, text='聚类分析',fg='red',width=30,	underline=4, command=clu).grid(column=4, row=4)
	Button(root, text='查看类别',fg='red',width=30,	underline=4, command=show_sk).grid(column=4, row=5)
	Button(root, text='应用查询',fg='red',width=30,	underline=4, command=show2).grid(column=4, row=6)
	Button(root, text='爬取数据', fg='red', width=30, underline=4, command=f_search).grid(column=4, row=7)
	mainloop()

if __name__ == '__main__':
	main()
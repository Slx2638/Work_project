# tkinter复选框操作
import tkinter as tk

root = tk.Tk()
root.title('问卷调查')
root.geometry('600x600')  # 设置窗口大小

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


list_content = []



nutrient_list = ['热量(kcal)', '硫胺素(mg)', '钙(mg)',
				'蛋白质(g)', '核黄素(mg)', '镁(mg)',
				'脂肪(g)', '烟酸(mg)', '铁(mg)',
				'碳水化合物(g)', '维生素C(mg)', '锰(mg)',
				'膳食纤维(g)', '维生素E(mg)', '锌(mg)',
				'维生素A(ug)', '胆固醇(mg)', '铜(mg)',
				'胡萝卜素(ug)', '钾(mg)', '磷(mg)',
				'视黄醇当量(ug)', '钠(mg)', '硒(mg)', ]

def click_1():
    global flag_1
    flag_1 = not flag_1
    if flag_1:
        list_content.append(nutrient_list[0])
    else:
        list_content.remove(nutrient_list[0])
def click_2():
    global flag_2
    flag_2 = not flag_2
    if flag_2:
        list_content.append(nutrient_list[1])
    else:
        list_content.remove(nutrient_list[1])
def click_3():
    global flag_3
    flag_3 = not flag_3
    if flag_3:
        list_content.append(nutrient_list[2])
    else:
        list_content.remove(nutrient_list[2])
def click_4():
    global flag_4
    flag_4 = not flag_4
    if flag_4:
        list_content.append(nutrient_list[3])
    else:
        list_content.remove(nutrient_list[3])
def click_5():
    global flag_5
    flag_5 = not flag_5
    if flag_5:
        list_content.append(nutrient_list[4])
    else:
        list_content.remove(nutrient_list[4])
def click_6():
    global flag_6
    flag_6 = not flag_6
    if flag_6:
        list_content.append(nutrient_list[5])
    else:
        list_content.remove(nutrient_list[5])
def click_7():
    global flag_7
    flag_7 = not flag_7
    if flag_7:
        list_content.append(nutrient_list[6])
    else:
        list_content.remove(nutrient_list[6])
def click_8():
    global flag_8
    flag_8 = not flag_8
    if flag_8:
        list_content.append(nutrient_list[7])
    else:
        list_content.remove(nutrient_list[7])
def click_9():
    global flag_9
    flag_9 = not flag_9
    if flag_9:
        list_content.append(nutrient_list[8])
    else:
        list_content.remove(nutrient_list[8])
def click_10():
    global flag_10
    flag_10 = not flag_10
    if flag_10:
        list_content.append(nutrient_list[9])
    else:
        list_content.remove(nutrient_list[9])
def click_11():
    global flag_11
    flag_11 = not flag_11
    if flag_11:
        list_content.append(nutrient_list[10])
    else:
        list_content.remove(nutrient_list[10])
def click_12():
    global flag_12
    flag_12 = not flag_12
    if flag_12:
        list_content.append(nutrient_list[11])
    else:
        list_content.remove(nutrient_list[11])
def click_13():
    global flag_13
    flag_13 = not flag_13
    if flag_13:
        list_content.append(nutrient_list[12])
    else:
        list_content.remove(nutrient_list[12])
def click_14():
    global flag_14
    flag_14 = not flag_14
    if flag_14:
        list_content.append(nutrient_list[13])
    else:
        list_content.remove(nutrient_list[13])
def click_15():
    global flag_15
    flag_15 = not flag_15
    if flag_15:
        list_content.append(nutrient_list[14])
    else:
        list_content.remove(nutrient_list[14])
def click_16():
    global flag_16
    flag_16 = not flag_16
    if flag_16:
        list_content.append(nutrient_list[15])
    else:
        list_content.remove(nutrient_list[15])
def click_17():
    global flag_17
    flag_17 = not flag_17
    if flag_17:
        list_content.append(nutrient_list[16])
    else:
        list_content.remove(nutrient_list[16])
def click_18():
    global flag_18
    flag_18 = not flag_18
    if flag_18:
        list_content.append(nutrient_list[17])
    else:
        list_content.remove(nutrient_list[17])
def click_19():
    global flag_19
    flag_19 = not flag_19
    if flag_19:
        list_content.append(nutrient_list[18])
    else:
        list_content.remove(nutrient_list[18])
def click_20():
    global flag_20
    flag_20 = not flag_20
    if flag_20:
        list_content.append(nutrient_list[19])
    else:
        list_content.remove(nutrient_list[19])
def click_21():
    global flag_21
    flag_21 = not flag_21
    if flag_21:
        list_content.append(nutrient_list[20])
    else:
        list_content.remove(nutrient_list[20])
def click_22():
    global flag_22
    flag_22 = not flag_22
    if flag_22:
        list_content.append(nutrient_list[21])
    else:
        list_content.remove(nutrient_list[21])
def click_23():
    global flag_23
    flag_23 = not flag_23
    if flag_23:
        list_content.append(nutrient_list[22])
    else:
        list_content.remove(nutrient_list[22])
def click_24():
    global flag_24
    flag_24 = not flag_24
    if flag_24:
        list_content.append(nutrient_list[23])
    else:
        list_content.remove(nutrient_list[23])

lab = tk.Label(root, text='请选择需要的营养元素：')
lab.grid(row=0, columnspan=3, sticky=tk.W)

# 多选框
frm = tk.Frame(root)
tk.Checkbutton(frm, text='热量(kcal)', command=click_1).grid(row=0)
ck2 = tk.Checkbutton(frm, text='硫胺素(mg)', command=click_2)
ck3 = tk.Checkbutton(frm, text='钙(mg)', command=click_3)
ck4 = tk.Checkbutton(frm, text='蛋白质(g)', command=click_4)
ck5 = tk.Checkbutton(frm, text='核黄素(mg)', command=click_5)
ck6 = tk.Checkbutton(frm, text='镁(mg)', command=click_6)
ck7 = tk.Checkbutton(frm, text='脂肪(g)', command=click_7)
ck8 = tk.Checkbutton(frm, text='烟酸(mg)', command=click_8)
ck9 = tk.Checkbutton(frm, text='铁(mg)', command=click_9)
ck10 = tk.Checkbutton(frm, text='碳水化合物(g)', command=click_10)
ck11 = tk.Checkbutton(frm, text='维生素C(mg)', command=click_11)
ck12 = tk.Checkbutton(frm, text='锰(mg)', command=click_12)
ck13 = tk.Checkbutton(frm, text='膳食纤维(g)', command=click_13)
ck14 = tk.Checkbutton(frm, text='维生素E(mg)', command=click_14)
ck15 = tk.Checkbutton(frm, text='锌(mg)', command=click_15)
ck16 = tk.Checkbutton(frm, text='维生素A(ug)', command=click_16)
ck17 = tk.Checkbutton(frm, text='胆固醇(mg)', command=click_17)
ck18 = tk.Checkbutton(frm, text='铜(mg)', command=click_18)
ck19 = tk.Checkbutton(frm, text='胡萝卜素(ug)', command=click_19)
ck20 = tk.Checkbutton(frm, text='钾(mg)', command=click_20)
ck21 = tk.Checkbutton(frm, text='磷(mg)', command=click_21)
ck22 = tk.Checkbutton(frm, text='视黄醇当量(ug)', command=click_22)
ck23 = tk.Checkbutton(frm, text='钠(mg)', command=click_23)
ck24 = tk.Checkbutton(frm, text='硒(mg)', command=click_24)



ck2.grid(row=0, column=1)
ck3.grid(row=0, column=2)
ck4.grid(row=0,column=3)
ck5.grid(row=0, column=4)
ck6.grid(row=0, column=5)
ck7.grid(row=1)
ck8.grid(row=1, column=1)
ck9.grid(row=1, column=2)
ck10.grid(row=1, column=3)
ck11.grid(row=1, column=4)
ck12.grid(row=1, column=5)
ck13.grid(row=2)
ck14.grid(row=2, column=1)
ck15.grid(row=2, column=2)
ck16.grid(row=2, column=3)
ck17.grid(row=2, column=4)
ck18.grid(row=2, column=5)
ck19.grid(row=3)
ck20.grid(row=3, column=1)
ck21.grid(row=3, column=2)
ck22.grid(row=3, column=3)
ck23.grid(row=3, column=4)
ck24.grid(row=3, column=5)
frm.grid(row=4)

root.mainloop()

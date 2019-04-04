# import urllib
# import re
# from bs4 import BeautifulSoup

import math

print(math.sqrt(1400))
import wx
import tkinter

# import wx
#
# app = wx.App()
# frame = wx.Frame(None, title="Gui Test Editor", pos=(1000, 200), size=(500, 400))
#
# path_text = wx.TextCtrl(frame, pos=(5, 5), size=(350, 24))
# open_button = wx.Button(frame, label="打开", pos=(370, 5), size=(50, 24))
# save_button = wx.Button(frame, label="保存", pos=(430, 5), size=(50, 24))
# frame.Show()
# app.MainLoop()


# top = tkinter.Tk()
# top.mainloop()


# class Fecth_ccontent():
#     page = 1
#     url = 'http://www.zou114.com/nutrient/y' + str(page) +'.html'
#     text = urllib.request.urlopen(url).read()
#
#     soup = BeautifulSoup(text,'html.parser')
#     def __get_content(self):
#         all_content = self.soup.find_all(attrs={'class':'nrbnr'})   #食物名称、营养元素的html class对象
#
#         food_content = self.__analysis_content(all_content)
#         print(food_content)
#
#     def __analysis_content(self,all_content):
#         food_content = str(all_content)
#         name_list = re.findall('<font color="red">(.*)</font>',food_content)
#         nutrition_biao = re.findall('<li class="lgr">(.*)</li>',food_content)
#         food_list = []
#         food_list.append(name_list[0])
#         for j in range(24):
#             number = re.findall('[0-9]{1,}[.]+[0-9]{1,}',nutrition_biao[j])
#             if number == []:
#                 number = ['0']
#             food_list.append(number[0])
#         return food_list
#
#     def run(self):
#         self.__get_content()
#
# f = Fecth_ccontent()
# f.run()






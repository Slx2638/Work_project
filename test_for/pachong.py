from urllib import request
import re
import xlwt
import pandas as pd


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


data = pd.read_excel('food.xls','Food Nutrition',index_col=0)
data.to_csv('food_data.csv',encoding='utf-8')
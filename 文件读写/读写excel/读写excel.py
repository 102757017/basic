
# coding: utf-8

# In[1]:

#!/usr/bin/python

import xlwings as xls
xls.__version__


# # 打开Excel程序，默认设置：程序可见，并新建一个工作簿

# In[2]:

app = xls.App(visible=True,add_book=True)


# # 再新建一个工作簿

# In[3]:

wb = app.books.add()


# # app.books是可迭代对象，显示目前所有的工作簿

# In[4]:

print(app.books)


# In[5]:

app.books[0]


# In[6]:

app.books["工作簿1"]


# # 关闭工作薄

# In[7]:

app.books["工作簿2"].close()


# # 打开一个现存的工作薄

# In[8]:

wb=app.books.open('test.xlsx')


# # 显示工作薄内所有sheet

# In[9]:

wb.sheets
for sht in app.books["test.xlsx"].sheets:
    print(sht)


# # 获取单元格内文本

# In[10]:

print("文本内容：",wb.sheets["QA"]['A2'].value)
print("文本内容：",wb.sheets["QA"]['$A$2'].value)
#背景色
print("背景颜色：",wb.sheets["QA"]['A2'].color)
print("行高：",wb.sheets["QA"]['A2'].row_height)
print("列宽：",wb.sheets["QA"]['A2'].column_width)
print("字体:",wb.sheets["QA"]['A2'].api.Font.Name)



print("字体大小:",wb.sheets["QA"]['A2'].api.Font.size)
print("字体颜色：",wb.sheets["QA"]['A2'].api.Font.Color)
#设置颜色为(255,0,0)
wb.sheets["QA"]['A2'].api.Font.Color=0x0000ff
# -4108 水平居中。 -4131 靠左，-4152 靠右。
wb.sheets["QA"]['A2'].api.HorizontalAlignment = -4108
# -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。
wb.sheets["QA"]['A2'].api.VerticalAlignment = -4130


# In[11]:

wb.sheets["QA"]['F17:H17'].value


# In[12]:

wb.sheets["QA"]['F17:H18'].value


# # 得到指定单元格所在的合并单元格的Range

# In[13]:

#判断range范围内是否有合并单元格
print(wb.sheets["QA"]['A2:A3'].api.MergeCells)

#合并单元格的range
wb.sheets["QA"]['A2'].api.MergeArea.Address


# # 搜索文本
# 当查找到指定查找区域的末尾时，本方法将环绕至区域的开始继续搜索。发生环绕后，为停止查找，可保存第一次找到的单元格地址，然后测试下一个查找到的单元格地址是否与其相同。

# In[14]:

rng=wb.sheets["QA"].api.UsedRange.Find("单元格")
if rng==None:
    print("未搜索到该字符串")
else:
    #保存第一个搜索结果的地址，防止无限循环
    firstaddress = rng.Address
    print(firstaddress)
    rng = wb.sheets["QA"].api.UsedRange.FindNext(rng)
    while rng.Address!= firstaddress:
        print(rng.Address)
        rng = wb.sheets["QA"].api.UsedRange.FindNext(rng)


# # 获取表格中的形状

# In[15]:

wb.sheets["QA"].shapes


# # 文本框

# In[16]:

shape0=wb.sheets["QA"].shapes[0]
print("name:",shape0.name)
#读取shape的value有以下几种方法
print("value:",shape0.api.OLEFormat.Object.Text)
print("value:",shape0.api.TextFrame2.TextRange.Text)
#print("value:",shape0.api.TextFrame.Characters.Text)
print("type:",shape0.type)
print("heigh:",shape0.height)
print("width:",shape0.width)
print("允许文本溢出形状:",shape0.api.TextFrame.VerticalOverflow)


# # 复制一个sheet（此处用到了vba的函数，api后面可以使用任意vba函数）

# In[17]:

wb.sheets["QA"].api.Copy()


# # 更改sheet的名称（此处用到了vba的函数，api后面可以使用任意vba函数）

# In[18]:

app.books[2].sheets[0].api.Name="QA2"


# # 图片

# In[19]:

shape1=app.books[2].sheets["QA2"].shapes[1]
print("name:",shape1.name)
print("type:",shape1.type)
print("heigh:",shape1.height)
print("width:",shape1.width)
print("距离左边的距离:",shape1.left)
print("距离顶端的距离:",shape1.left)

#添加图片
app.books[2].sheets["QA2"].pictures.add(r'C:\Users\hewei\Pictures\a.png')

#删除图片
shape1.delete()


# # 修改单元格内文本

# In[20]:

app.books[2].sheets["QA2"]['T19'].value="否"


# # 进行一组数据的赋值时默认是按行进行赋值

# In[21]:

app.books[2].sheets["QA2"]['A24'].value=[1, 2, 3,4]


# # 按列进行赋值需要添加transpose参数

# In[22]:

app.books[2].sheets["QA2"]['A25'].options(transpose=True).value=[1, 2, 3,4]


# # 保存工作簿

# In[23]:

app.books[2].save("复制的工作表.xlsx")


# # 转换文件格式
# | 名称                              | 值   | 说明                   | 扩展名 |
# | :-------------------------------- | :--- | :--------------------- | :----- |
# | **xlCSV**                         | 6    | CSV                    | *.csv  |
# | **xlExcel8**                      | 56   | Excel 97-2003 工作簿   | *.xls  |
# | **xlOpenXMLWorkbook**             | 51   | Open XML 工作簿        | *.xlsx |
# | **xlOpenXMLWorkbookMacroEnabled** | 52   | 启用 Open XML 工作簿宏 | *.xlsm |
# | **xlTextMac**                     | 19   | Macintosh 文本         | *.txt  |
# | **xlTextMSDOS**                   | 21   | MSDOS 文本             | *.txt  |
# | **xlTextWindows**                 | 20   | Windows 文本           | *.txt  |
# | **xlXMLSpreadsheet**              | 46   | XML 电子表格           | *.xml  |

# In[24]:

import os
import sys
os.chdir(sys.path[0])
app.books[2].api.SaveAs( "复制的工作表",46)


# # 关闭excel

# In[25]:

app.books[2].close()
app.quit()
app.kill()


# In[ ]:




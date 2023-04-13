# --* coding=utf-8 *--
import base64
from io import StringIO, BytesIO
import xlwt
import pymongo
from pymongo import MongoClient
import gridfs
import os
import matplotlib.pyplot as plt
import matplotlib.image as iming
import bson.binary
import numpy as np

def storage_pics(path):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    myset = db.originalPics
    # path = 'aistudio-发票数据集/test'
    files = os.listdir(path)
    for file in files:
        file_name = path + "\\" + file
        print(file_name)
        f = file.split('.')
        imgtmp = open(file_name, 'rb')
        img = base64.b64encode(imgtmp.read())
        myset.insert_one({"name": f[0], "type": f[1], "img_base64": img})

    print("导入数据库成功")


def storage_invoice_approval(datas):
    print('正在将发票数据导入mondb里')
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    for d in range(len(datas)):

            if (datas[d]['InvoiceDate'] == '2016年06月12日' and datas[d]['PurchasserName'] == '深圳市购机汇网络有限公司' and datas[d]['AmountInFiguers'] <= '2700'):
                my_set.insert_one(
                     {
                          "InvoiceDate": datas[d]['InvoiceDate'],
                          "SellerRegisterNum": datas[d]['SellerRegisterNum'],
                          "PurchasserName": datas[d]['PurchasserName'],
                          "SellerName": datas[d]['SellerName'],
                          "AmountInFiguers": datas[d]['AmountInFiguers'],
                          "InvoiceName":datas[d]['InvoiceName'],
                          "InvoiceImgType": datas[d]['InvoiceImgType'],
                          "Approval": '通过'

                     }
                )
            else:
                my_set.insert_one(
                    {
                        "InvoiceDate": datas[d]['InvoiceDate'],
                        "SellerRegisterNum": datas[d]['SellerRegisterNum'],
                        "PurchasserName": datas[d]['PurchasserName'],
                        "SellerName": datas[d]['SellerName'],
                        "AmountInFiguers": datas[d]['AmountInFiguers'],
                        "InvoiceName":datas[d]['InvoiceName'],
                        "InvoiceImgType": datas[d]['InvoiceImgType'],
                        "Approval": '不通过'

                    }
                )

    print("导入成功")


def mongodb_to_excel():
    print('正在将发票数据从mongodb放入excel中')
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    print('正在写入数据！')
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('增值税发票内容登记', cell_overwrite_ok=True)
    # 创建样式对象，初始化样式
    style = xlwt.XFStyle()
    alignment = xlwt.Alignment()
    # 设置水平居中对齐
    alignment.horz = 2
    # 为样式创建字体
    font = xlwt.Font()
    # 设置字体
    font.name = 'Calibri'
    # 字体大小
    font.height = 200
    style.font = font
    style.alignment = alignment
    title = ['开票日期', '发票名称', '纳税人识别号', '购买方名称', '卖方名称', '购买金额', '审批状态']
    for i in range(len(title)):
        sheet.col(i).width = 7777
        sheet.write(0, i, title[i],style)

    num = 0
    for x in my_set.find():
        sheet.write(num + 1, 0, x['InvoiceDate'], style)
        sheet.write(num + 1, 1, x['InvoiceName'], style)
        sheet.write(num + 1, 2, x['SellerRegisterNum'], style)
        sheet.write(num + 1, 3, x['PurchasserName'], style)
        sheet.write(num + 1, 4, x['SellerName'], style)
        sheet.write(num + 1, 5, x['AmountInFiguers'], style)
        sheet.write(num + 1, 6, x['Approval'], style)
        num = num + 1
    print('excel生成成功')
    # 插入审批状态比例
    sheet.write(num + 1, 0, "审批状态", style)
    sheet.write(num + 1, 1, "总数量", style)
    sheet.write(num + 2, 0, '通过', style)
    sheet.write(num + 2, 1, pass_num(), style)
    sheet.write(num + 3, 0, '不通过', style)
    sheet.write(num + 3, 1, unpass_num(), style)
    sheet.write(num + 4, 0, '转人工', style)
    sheet.write(num + 4, 1, person_num(), style)
    sheet.write(num + 5, 0, "all", style)
    sheet.write(num + 5, 1, all_num(), style)
    book.save('testb.xlsx')


# 统计发票总数量
def all_num():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    count = my_set.estimated_document_count()
    print(count)
    return count


# 统计“通过”的发票数量
def pass_num():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    count = my_set.count_documents({'Approval': '通过'})
    print(count)
    return count

# 统计‘不通过’的发票数量
def unpass_num():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    count = my_set.count_documents({'Approval': '不通过'})
    print(count)
    return count

# 统计转人工的发票数量
def person_num():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    count = my_set.count_documents({'Approval': '转人工'})
    print(count)
    return count








# --* coding=utf-8 *--
import base64
from io import StringIO, BytesIO

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
                my_set.insert_one(# TODO:把save(datas)的数据插入放到这里
                     {
                          "InvoiceDate": datas[d]['InvoiceDate'],
                          "SellerRegisterNum": datas[d]['SellerRegisterNum'],
                          "PurchasserName": datas[d]['PurchasserName'],
                          "SellerName": datas[d]['SellerName'],
                          "AmountInFiguers": datas[d]['AmountInFiguers'],
                          "Approval": '通过'

                     }
                )
            else:
                my_set.insert_one(# TODO:把save(datas)的数据插入放到这里
                    {
                        "InvoiceDate": datas[d]['InvoiceDate'],
                        "SellerRegisterNum": datas[d]['SellerRegisterNum'],
                        "PurchasserName": datas[d]['PurchasserName'],
                        "SellerName": datas[d]['SellerName'],
                        "AmountInFiguers": datas[d]['AmountInFiguers'],
                        "Approval": '不通过'

                    }
                )

    print("导入成功")




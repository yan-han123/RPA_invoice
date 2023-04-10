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

def delete():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    myset1 = db.originalPics
    myset1.drop()
    myset2 = db.invoice_approval
    myset2.drop()

if __name__ == '__main__':
    delete()

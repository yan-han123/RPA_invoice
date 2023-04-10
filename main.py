# encoding:utf-8
import requests
import base64
import os
import xlwt
import datetime
import urllib
from PIL import Image
from io import BytesIO
import json
import pandas as pd
import storage


    # 获取发票正文内容
def get_context(pic):
    print('正在获取图片正文内容！')
    data = {}
    try:
        request_url ="https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?access_token="
            # 二进制方式打开图片文件
        img_file = pic
        im = Image.open(img_file)
        (x, y) = im.size

        max_size = 2000

        if max(im.size) > max_size:
            scale_factor = max_size / max(im.size)
            new_size = tuple(int(dim * scale_factor) for dim in im.size)
            im = im.resize(new_size, resample=Image.LANCZOS)
            im.save(pic, format='JPEG', optimize=True, quality=70)
        f = open(pic, 'rb')
        img = base64.b64encode(f.read())
        print(len(img))
            # if len(img) > 4 * 1024 * 1024:
            #     img = urllib.parse.quote_plus(img)
        params = {"image": img}

            # 这里需要替换成自己的access_token
        access_token = '24.28996d3cf44704a4c04759df066806ed.2592000.1683466812.282335-32066502'
            # access_token = '24.18919bfddfe2e9eaafa5adafbc009fdd.2592000.1652961349.282335-24520345'
        request_url = request_url+ access_token
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'close'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # print(response.json())
            json1 = response.json()
            data['SellerRegisterNum'] = json1['words_result']['SellerRegisterNum']
            data['InvoiceDate'] = json1['words_result']['InvoiceDate']
            data['PurchasserName'] = json1['words_result']['PurchaserName']
            data['SellerName'] = json1['words_result']['SellerName']
            data['AmountInFiguers'] = json1['words_result']['AmountInFiguers']
            # print(data['AmountInFiguers'])

        print('正文内容获取成功！')
        return data

    except Exception as e:
        print(e)
    return data

    # 定义生成图片路径的函数
def pics(path):
    print('正在生成图片路径')
    # 生成一个空列表用于存放图片路径
    pics = []
        # 遍历文件夹，找到后缀为jpg和png的文件，整理之后加入列表
    for filename in os.listdir(path):
        if filename.endswith('jpg') or filename.endswith('png'):
            pic = path + '/' + filename
            pics.append(pic)
    print('图片路径生成成功！')
    return pics

def datas(pics):
    datas = []
    for p in pics:
        data = get_context(p)
        datas.append(data)
    return datas

    # 定义一个写入将数据excel表格的函数
def data_save(datas):
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
    title = ['开票日期', '纳税人识别号', '购买方名称', '卖方名称', '购买金额', '审批状态']
    for i in range(len(title)):
        sheet.col(i).width = 7777
        sheet.write(0, i, title[i],style)
    for d in range(len(datas)):
        for j in range(5):
            sheet.write(d + 1, 0, datas[d]['InvoiceDate'],style)
            sheet.write(d + 1, 1, datas[d]['SellerRegisterNum'],style)
            sheet.write(d + 1, 2, datas[d]['PurchasserName'],style)
            sheet.write(d + 1, 3, datas[d]['SellerName'],style)
            sheet.write(d + 1, 4, datas[d]['AmountInFiguers'],style)
            if (datas[d]['InvoiceDate'] == '2016年06月12日' and datas[d]['PurchasserName'] == '深圳市购机汇网络有限公司' and datas[d]['AmountInFiguers'] <= '2700'):
               sheet.write(d + 1, 5, '通过', style)
            else:
                sheet.write(d + 1, 5, '不通过', style)

    print('数据写入成功！')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    book.save(now+'增值税发票.xls')

def main():
    print('开始执行！！！')

    # 这是你发票的存放地址，自行更改
    path = 'aistudio-发票数据集/test'

    Pics = pics(path)
    Datas = datas(Pics)
    #data_save(Datas)
    storage.storage_invoice_approval(Datas)
    #content = self.get_context('aistudio-发票数据集/b/b0.jpg')
    #print(content)
    storage.storage_pics(path)
    print('执行结束！')

if __name__ == '__main__':
    # 请输入你的API Ke
    main()
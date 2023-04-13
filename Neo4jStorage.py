import pandas as pd
import py2neo
from py2neo import Node, Graph, Relationship, NodeMatcher
import pymongo
#
# # TODO: 使用你自己的用户名和密码
# graph = Graph('http://localhost:7474', auth=("neo4j", "xc13579246810"))
# 清除neo4j中原有的结点等所有信息
# graph.delete_all()


# 创建节点
# def CreateNode(graph, my_set):
#
#    for x in my_set.find():
#        r_value = graph.nodes.match(label="SellerName", name=x['SellerName']).first()
#        l_value = graph.nodes.match(label="PurchasserName", name=x['PurchasserName']).first()
#        if r_value is None:
#            node1 = Node(label="SellerName", name=x['SellerName'])
#            graph.create(node1)
#        if l_value is None:
#            node2 = Node(label="PurchasserName", name=x['PurchasserName'])
#            graph.create(node2)
#
def invoice_create_relationship():

    # # TODO: 使用你自己的用户名和密码
    graph = Graph('http://localhost:7474', auth=("neo4j", "xc13579246810"))
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    for x in my_set.find():
        node_name = Node("SellerName", name=x['SellerName'])
        node_name1 = Node("PurchasserName",name=x['PurchasserName'])
        matcher = NodeMatcher(graph)
        nodelist = list(matcher.match("SellerName", name=x['SellerName']))
        nodelist1 = list(matcher.match("PurchasserName",name=x['PurchasserName']))
        if len(nodelist) > 0 :
            node_name = nodelist[0]
        else:
            graph.create(node_name)
        if len(nodelist1) > 0 :
            node_name1 = nodelist1[0]
        else:
            graph.create(node_name1)
        query = "MATCH (p:SellerName {name: $payer}), (q:PurchasserName {name: $payee}) " \
                "CREATE (p)-[r:attribute {InvoiceName: $InvoiceName, amount: $amount, SellerRegisterNum: $SellerRegisterNum, time: $time}]->(q)"
        graph.run(query, payer=x['SellerName'], payee=x['PurchasserName'], InvoiceName=x['InvoiceName'], amount=x['AmountInFiguers'], SellerRegisterNum=x['SellerRegisterNum'], time=x['InvoiceDate'])

def delete():
    # # TODO: 使用你自己的用户名和密码
    graph = Graph('http://localhost:7474', auth=("neo4j", "xc13579246810"))
    graph.delete_all()


def neo4j_relationship():
    # # TODO: 使用你自己的用户名和密码
    graph = Graph('http://localhost:7474', auth=("neo4j", "xc13579246810"))
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.RPA_invoice  # 连接到RPA_invoice数据库
    my_set = db.invoice_approval
    graph.delete_all()
    # 整理数据
    # CreateNode()
    invoice_create_relationship()




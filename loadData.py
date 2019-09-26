from faker import Faker
import argparse
import json
import csv
import random
from OrderTables import order,getParentNames,getAllColumnNames
import pandas as pd
import itertools
import math
import time

fake = Faker()



def parse():
    parser = argparse.ArgumentParser(description='add the args')
    parser.add_argument('templateJson')
    parser.add_argument('testCasesCount',type=int)
    args = parser.parse_args()
    return args

def init(template):
    headersFieldNames = getHeaderFields(template)
    headerTypeDefsMap = getHeaderTypeDef(template)
    return headersFieldNames,headerTypeDefsMap

def loadTemplate(args):
    template = {}
    with open(args.templateJson) as jsonfile:
        template = json.load(jsonfile)
    return template

def getHeaderFields(template):
    headerFieldNames = []
    for i in template["headerFields"]:
        headerFieldNames.append((list(i.keys())[0]))
    return headerFieldNames

def getHeaderTypeDef(template):
    headerFieldsJson = dict()
    for i in template["headerFields"]:
        key = (list(i.keys())[0])
        headerFieldsJson[key] = i[key]
    return headerFieldsJson

def generateDataSampleFromTemplate(headersFieldNames,headerTypeDefsMap):
    switcher = {
        "email" : fake.email(),
        "name" : fake.name(),
        "address": fake.address(),
        "text": fake.text(),
        "country": fake.country(),
        "int": random.randint(100,2000),
        "float": str(random.randint(100,2000)) + "." + str(random.randint(100,2000) ),
        "credit_card_number": fake.credit_card_number()
    }
    data = []  
    for key in headersFieldNames:
       data.append(switcher.get(headerTypeDefsMap[key]))
    return data

def getHeaderInfo(tableDef):
    typeDefmap = {}
    for attribute in tableDef:
        for info in attribute:
            if isinstance(attribute[info],str):
                typeDefmap[info] = attribute[info]
    return typeDefmap

def fillDataForParent(headerInfo,testCasesCount,tableName):
    headersFieldNames = [*headerInfo]
    csvData = []
    csvData.append(headersFieldNames)
    for i in range(testCasesCount):
        csvData.append(generateDataSampleFromTemplate(headersFieldNames,headerInfo))

    with open(tableName+'.csv', 'w',newline='') as csvFile:
        writer = csv.writer(csvFile,delimiter='$')
        writer.writerows(csvData)
    csvFile.close()

def isParent(table):
    for attribute in table:
        if 'info' in attribute and 'parent' in attribute['info']:
            return False
    return True

def fillDataForChild(table,tableOrder,tableName,testCasesCount,headerInfo):
    # print(tableName)
    parents = getParentNames(table,tableOrder)
    data = []
    keyColumnNames = []

    for parent in parents:
        df = pd.read_csv(str(parent['table'])+'.csv',delimiter='$')
        uniqueValues = df[str(parent["attribute"])].unique()
        # print(uniqueValues)
        data.append(uniqueValues)
        keyColumnNames.append(parent['currentAttributeName'])
    # print(data,keyColumnNames)
    allData = pd.DataFrame(list(itertools.product(*data)),columns=keyColumnNames).head(math.floor(testCasesCount/2))
    allColumnNames = getAllColumnNames(table)
    # print(allColumnNames,keyColumnNames)
    nonKeyColumns = [i for i in allColumnNames if i not in keyColumnNames or keyColumnNames.remove(i)]

    nonKeyData = []
    for i in range(math.floor(testCasesCount/2)):
        nonKeyData.append(generateDataSampleFromTemplate(nonKeyColumns,headerInfo))
    nonKeyDataDf = pd.DataFrame(nonKeyData)
    for i in range(len(nonKeyColumns)):
       allData[nonKeyColumns[i]] = nonKeyDataDf[i]
    # print(allData)
    df.to_csv(tableName+'.csv',sep='$',index=False)
    return

def generateFakeData(args):
    template = loadTemplate(args)
    tableOrder,tablePositionMap = order(template)
    for position in tableOrder:
        tableName = tablePositionMap[position]
        table = template["Tables"][tableName]
        headerInfo = getHeaderInfo(table)
        if(isParent(table)):
            fillDataForParent(headerInfo,args.testCasesCount,tableName)
        else:
            fillDataForChild(table,tablePositionMap,tableName,args.testCasesCount,headerInfo)
        
    # print(tablePositionMap,tableOrder)


    
if __name__ == "__main__":
    args = parse()
    start = time.time()
    generateFakeData(args)
    end = time.time()
    print(end-start)

import json
from topologicalSort import Graph

def getParents(table,tableNames):
    parents = []
    for attribute in table:
         if 'info' in attribute and 'parent' in attribute['info']:
             parents.append(tableNames.index(attribute['info']['parent']['table']))
    return parents

def getParentNames(table,tableNames):
    parents = []
    for attribute in table:
         if 'info' in attribute and 'parent' in attribute['info']:
             parent = attribute['info']['parent']
             for i in attribute:
                 if isinstance(attribute[i],str):
                     parent['currentAttributeName'] = i
             parents.append(parent)
    return parents

def getAllColumnNames(table):
    columnNames = []
    for attribute in table:
        for i in attribute:
            if isinstance(attribute[i],str):
                columnNames.append(i)
    return columnNames


def combinations(arr): 
    n = len(arr) 
    indices = [0 for i in range(n)] 
  
    while (1): 
        for i in range(n): 
            print(arr[i][indices[i]], end = " ") 
        print() 

        next = n - 1
        while (next >= 0 and 
              (indices[next] + 1 >= len(arr[next]))): 
            next-=1

        if (next < 0): 
            return
 
        indices[next] += 1
  
        for i in range(next + 1, n): 
            indices[i] = 0
  
def order(template):
    Tables = template["Tables"]
    tableNames = [*Tables]
    g = Graph(len(tableNames))

    for table in Tables:
        parents = getParents(Tables[table],tableNames)
        currentNode = tableNames.index(table)
        for parent in parents:
            g.addEdge(parent,currentNode)

    return g.topologicalSort(),tableNames

    






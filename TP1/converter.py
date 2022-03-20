from genericpath import exists
import ply.lex as lex
import sys
import re

header = []
dicLines = []

class ListIntervalFunction:
    def __init__(self, name, size, function):
        self.name = name
        self.size = size
        self.function = function

class ListFixedFunction:
    def __init__(self, name, size, function):
        self.name = name
        self.size = size
        self.function = function

class ListInterval:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class ListFixed:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Identifier:
    def __init__(self, name):
        self.name = name

tokens = ["ID", "LISTF", "LISTI", "LISTFFUNC", "LISTIFUNC"]
# ID -> Identificadores
# LISTF -> Lista com tamanho fixo
# LISTI -> Lista com intervalo de tamanho
# LISTFFUNC -> Lista com tamanho fixo com função aplicada
# LISTIFUNC -> Lista com intervalo de tamanho com funcão aplicada

def t_LISTIFUNC(t):
    r'([^,]+)\{\d+\,(\d+)\}\:\:([^,]+)'
    regex = r'([^,]+)\{\d+\,(\d+)\}\:\:([^,]+)'
    result = re.compile(regex).search(t.value)
    obj = ListIntervalFunction(result.group(1), result.group(2), result.group(3))
    header.append(obj)

def t_LISTFFUNC(t):
    r'([^,]+)\{(\d+)\}\:\:([^,]+)'
    regex = r'([^,]+)\{(\d+)\}\:\:([^,]+)'
    result = re.compile(regex).search(t.value)
    obj = ListFixedFunction(result.group(1), result.group(2), result.group(3))
    header.append(obj)

def t_LISTI(t):
    r'([^,]+)\{\d+\,(\d+)\}'
    regex = r'([^,]+)\{\d+\,(\d+)\}'
    result = re.compile(regex).search(t.value)
    obj = ListInterval(result.group(1), result.group(2))
    header.append(obj)

def t_LISTF(t):
    r'([^,]+)\{(\d+)\}'
    regex = r'([^,]+)\{(\d+)\}'
    result = re.compile(regex).search(t.value)
    obj = ListFixed(result.group(1), result.group(2))
    header.append(obj)

def t_ID(t):
    r'([^,]+)'
    regex = r'([^,]+)'
    result = re.compile(regex).search(t.value)
    obj = Identifier(result.group(1))
    header.append(obj)

# carateres a ignorar
t_ignore = '\n\t, '

def t_error(t):
    print(f"ERROR: Illegal character '{t.value[0]}' at position ({t.lineno}, {t.lexpos})")
    t.lexer.skip(1)

# analisador léxico
lexer = lex.lex()

def lineParser(lineList):
    i = 0
    dic = {}
    for column in header:
        if type(column) == Identifier:
            dic[column.name] = lineList[i]
            i = i + 1
        elif type(column) == ListFixed:
            temp = []
            for j in range(column.size):
                temp.append(int(lineList[i]))
                i = i + 1
            dic[column.name] = temp
        elif type(column) == ListInterval:
            temp = []
            for j in range(column.size):
                if lineList[i] != '':
                    temp.append(int(lineList[i]))
                i = i + 1
            dic[column.name] = temp
        elif type(column) == ListIntervalFunction:
            temp = []
            soma = 0
            for j in range(int(column.size)):
                if lineList[i] != '':
                    temp.append(int(lineList[i]))
                    soma = soma + temp[-1]
                i = i + 1
            dic[column.name] = temp
            nameKey = column.name + '_' + column.function
            if column.function == 'sum':
                dic[nameKey] = soma
            elif column.function == 'media':
                dic[nameKey] = soma / len(temp)
        elif type(column) == ListFixedFunction:
            temp = []
            soma = 0
            for j in range(int(column.size)):
                temp.append(int(lineList[i]))
                soma = soma + temp[-1]
                i = i + 1
            dic[column.name] = temp
            nameKey = column.name + '_' + column.function
            if column.function == 'sum':
                dic[nameKey] = soma
            elif column.function == 'media':
                dic[nameKey] = soma / len(temp)            
    dicLines.append(dic)

def readCSV():
    fileName = sys.argv[1]
    if exists(fileName):
        file = open(fileName, 'r', encoding='utf_8')
        firstLine = file.readline()
        firstLine = firstLine.strip()
        lexer.input(firstLine)
        for tok in lexer:
            pass
        for line in file:
            regex = r'([^,\n\t]*)(,|\n|\t)?'
            lineList = []
            for match in re.finditer(regex, line):
                lineList.append(match.group(1))
            if lineList[-1] == '\n':
                lineList = lineList[:-1]
            lineParser(lineList)
        file.close()   
    else:
        print("Couldn't read CSV file.")

def writeJSON():
    fileName = sys.argv[2]
    file = open(fileName, 'w', encoding='utf_8')
    strFile = "[\n"
    for entry in dicLines:
        infoString = "\t{\n"
        for info in entry:
            if isinstance(entry[info], list):
                listString = '['
                for element in entry[info]:
                    listString += str(element) + ','
                listString = listString[:-1] + ']'
                infoString += "\t\t\"" + info + "\": " + listString + ",\n"
            elif isinstance(entry[info], (int, float)):
                infoString += "\t\t\"" + info + "\": " + str(entry[info]) + ",\n"
            else:
                infoString += "\t\t\"" + info + "\": \"" + str(entry[info]) + "\",\n"
        infoString = infoString[:-2] + "\n"
        infoString += ("\t},\n")
        strFile += infoString
    strFile = strFile[:-2] + "\n]\n"
    file.write(strFile)
    file.close()

readCSV()
writeJSON()     
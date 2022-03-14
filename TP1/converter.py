from genericpath import exists
from re import T
import ply.lex as lex
import sys
import csv
import json

# def readCSV():
#     print(sys.argv[1])
#     if exists(sys.argv[1]):
#         file = open(sys.argv[1])
#         print("teste")
#         for row in file:
#             print(row)
#     else:
#         print("Couldn't read CSV file.")
        

# readCSV()


tokens = ["CA", "CF", "VG", "NUM", "FA", "ID"]
# CA -> Chaveta aberta
# CF -> Chaveta fechada
# VG -> Vírgula
# NUM -> Números
# FA -> Funções de Agregação
# ID -> Identificadores


t_CA = r'\{'
t_CF = r'\}'
t_VG = r','

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FA(t):
    r'::\w+'
    return t

def t_ID(t):
    r'[a-zA-ZÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ_][\w/]*'
    return t

# carateres a ignorar
t_ignore = '\n\t '

def t_error(t):
    print(f"ERROR: Illegal character '{t.value[0]}' at position ({t.lineno}, {t.lexpos})")
    t.lexer.skip(1)

# analisador léxico
lexer = lex.lex()


for line in sys.stdin:
    lexer.input(line)
    for tok in lexer:
        print(tok)
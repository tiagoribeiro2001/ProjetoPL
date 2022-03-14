from genericpath import exists
from re import T
import ply.lex as lex
import ply.yacc as yacc
import sys
import csv
import json

tokens = ["COMA", "LBRACE", "RBRACE", "DCOLON", "INT", "ID"]
# VG -> Vírgula
# CA -> Chaveta aberta
# CF -> Chaveta fechada
# DP -> Dois pontos (::)
# NUM -> Número
# ID -> Identificadores

t_COMA = r','
t_LBRACE = r'{'
t_RBRACE = r'}'
t_DCOLON = r'::'

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][\w/]*'
    return t

# carateres a ignorar
t_ignore = '\n\t '

def t_error(t):
    print(f"ERROR: Illegal character '{t.value[0]}' at position ({t.lineno}, {t.lexpos})")
    t.lexer.skip(1)

# analisador léxico
lexer = lex.lex()

def p_language(p):
    '''
    language : expression
                | interval
                | size
                | function
                | empty
    '''
    print(p[1])

def p_expression(p):
    '''
    expression : ID COMA
    '''
    p[0] = p[1]

def p_interval(p):
    '''
    interval : LBRACE INT COMA INT RBRACE
    '''
    p[0] = (p[2], p[4])

def p_size(p):
    '''
    size : LBRACE INT RBRACE
    '''
    p[0] = p[2]

def p_function(p):
    '''
    function : DCOLON ID
    '''
    p[0] = p[2]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

parser = yacc.yacc()

def readCSV():
    fileName = sys.argv[1]
    if exists(fileName):
        file = open(fileName)
        firstLine = file.readline()
        parser.parse(firstLine)
    else:
        print("Couldn't read CSV file.")

readCSV()        

# for line in sys.stdin:
#     lexer.input(line)
#     for tok in lexer:
#         print(tok)
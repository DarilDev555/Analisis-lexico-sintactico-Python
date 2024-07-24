import ply.lex as lex
from prettytable import PrettyTable

# resultado del analisis
resultado_lexema = []
estado = True
lineaError = 0

# Palabras Reservadas
reservada = (
    'INCLUDE',
    'USING',
    'NAMESPACE',
    'STD',
    'COUT',
    'CIN',
    'GET',
    'CADENA',
    'RETURN',
    'VOID',
    'INT',
    'ENDL',
    'ROBOT',  # Añadido Robot
)

tokens = reservada + (
    'IDENTIFICADOR',
    'ENTERO',
    'ASIGNAR',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'POTENCIA',
    'MODULO',
    'MINUSMINUS',
    'PLUSPLUS',
    'AND',
    'OR',
    'NOT',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORQUE',
    'MAYORIGUAL',
    'IGUAL',
    'DISTINTO',
    'NUMERAL',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAIZQ',
    'LLADER',
    'PUNTOCOMA',
    'COMA',
    'COMDOB',
    'MAYORDER',
    'MAYORIZQ',
    'PUNTO',
        # Añadido PUNTO
)

# Reglas de Expresiones Regulares para token de Contexto simple
t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'
t_ASIGNAR = r'='
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOCOMA = r';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'
t_PUNTO = r'\.'  # Regla para PUNTO

def t_ROBOT(t):
    r'Robot'
    return t

def t_INCLUDE(t):
    r'include'
    return t

def t_USING(t):
    r'using'
    return t

def t_NAMESPACE(t):
    r'namespace'
    return t

def t_STD(t):
    r'std'
    return t

def t_COUT(t):
    r'cout'
    return t

def t_CIN(t):
    r'cin'
    return t

def t_GET(t):
    r'get'
    return t

def t_ENDL(t):
    r'endl'
    return t

def t_SINO(t):
    r'else'
    return t

def t_SI(t):
    r'if'
    return t

def t_RETURN(t):
   r'return'
   return t

def t_VOID(t):
   r'void'
   return t

def t_MIENTRAS(t):
    r'while'
    return t

def t_PARA(t):
    r'for'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t

def t_CADENA(t):
   r'\"?(\w+ \ *\w*\d* \ *)\"?'
   return t

def t_NUMERAL(t):
    r'\#'
    return t

def t_PLUSPLUS(t):
    r'\+\+'
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_MAYORDER(t):
    r'<<'
    return t

def t_MAYORIZQ(t):
    r'>>'
    return t

def t_DISTINTO(t):
    r'!='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_comments_ONELine(t):
        r'\/\/(.)*\n'
        t.lexer.lineno += 1
        print("Comentario de una linea")
t_ignore =' \t'

# Variable global para almacenar el último token inválido
ultimo_error = None

def t_error(t):
    global ultimo_error, lineaError
    global estado
    # Formatear los datos del token inválido
    if estado:
        ultimo_error = " Error Lexico token no valido en Linea {:4} Valor {:16} ".format(str(t.lineno), str(t.value[0]))
        lineaError = int(t.lineno)
        estado = False
    # Saltar el token inválido
    t.lexer.skip(1)

# Prueba de ingreso
def prueba(data):
    errorEstado = True
    global estado
    estado = True
    global ultimo_error, lineaError
    ultimo_error = ""
    tabla2 = PrettyTable()
    tabla2.field_names = ["Linea", "Tipo", "Valor", "Posicion"]
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        if tok.type in reservada or tok.type in tokens:
            try:
                nada = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos))
            except:
                continue
    return ultimo_error, lineaError

# instanciamos el analizador lexico
analizador = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("ingrese: ")
        resultado_lexema = prueba(data)
        for item in resultado_lexema:
            print(item)

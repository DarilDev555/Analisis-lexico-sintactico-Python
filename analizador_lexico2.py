# -- coding: latin-1 --

import re
import io

# Definir los patrones para los TOKENS
tokens = [
    ('UNCOMENTARIO', r'//.*', 'barras'), # Comentario de una linea
    ('SEPARADOR', r'\(', 'parentesis de apertura'), # Parentesis de apertura
    ('SEPARADOR', r'\)', 'parentesis de cierre'), # Parentesis de cierre
    ('SEPARADOR', r'\{', 'llave de apertura'),
    ('SEPARADOR', r'\}', 'llave de cierre'),
    ('SEPARADOR', r'\[', 'corchete de apertura'),
    ('SEPARADOR', r'\]', 'corchete de cierre'), # Corchete de cierre
    ('CLAVE', r'out', 'out'), ('CLAVE', r'println', 'println'),('DATO', r'int', 'int'),
    ('SIMBOLO', r'=', 'igual'), # Asignacion
    ('DATO', r'String', 'String'), # tipo de dato
    ('DATO', r'float', 'float'),
    ('DATO', r'char', 'char'),
    ('DATO', r'boolean', 'boolean'),
    ('DATO', r'long', 'long'),
    ('DATO', r'boolean', 'boolean'),
    ('NUMERO', r'\d+', 'digito'), # Numeros
    ('SEPARADOR', r';','punto y coma'), # Punto y coma
    ('CLAVE', r'System', 'System'), ('CLAVE', r'class','class'), # Palabras clave
    ('CLAVE', r'main','main'), # Palabras clave
    ('Palabra Reservada', r'Robot','Robot'), # Palabras clave
    ('CLAVE', r'public','public'), # Palabras clave
    ('CLAVE', r'private','private'), # Palabras clave
    ('CLAVE', r'static','static'), # Palabras clave
    ('CLAVE', r'args','args'), # Palabras clave
    ('CLAVE', r'true','true'), # Palabras clave
    ('CLAVE', r'false','false'), # Palabras clave
    ('CLAVE', r'void','void'), # Palabras clave
    ('METODO', r'base','metodo base'), # Palabras clave
    ('METODO', r'cuerpo','metodo cuerpo'), # Palabras clave
    ('METODO', r'garra','metodo garra'), # Palabras clave
    ('CADENA', r'"[^"]*"','cadenas de texto'), # Cadenas de texto
    ('SEPARADOR', r',', 'coma'), # Coma
    ('SIMBOLO', r'\.', 'punto'), # Punto
    ('OP_LOGICO', r'&&', 'and'), # Operadores logicos
    ('OP_LOGICO', r'\|\|', 'or'), # Operadores logicos
    ('OP_RELACIONAL', r'==', 'igual'), # Operadores relacionales
    ('OP_RELACIONAL', r'!=', 'diferente'), # Operadores relacionales
    ('OP_RELACIONAL', r'<=', 'menor o igual que'), # Operadores relacionales
    ('OP_RELACIONAL', r'>=', 'mayor o igual que'), # Operadores relacionales
    ('OP_RELACIONAL', r'<', 'menor que'), # Operadores relacionales
    ('OP_RELACIONAL', r'>', 'mayor que'), # Operadores relacionales
    ('OP_INCDEC', r'\+\+', 'operadores de incremento'), # Incremento/Decremento
    ('ARITMETICO', r'\+', 'suma'), # Operadores aritmeticos
    ('ARITMETICO', r'-', 'resta'), # Operadores aritmeticos
    ('ARITMETICO', r'\*', 'multiplicacion'), # Operadores aritmeticos
    ('ARITMETICO', r'/', 'division'), # Operadores aritmeticos
    ('OP_INCDEC', r'--', 'operadores de decremento'), # Incremento/Decremento
    ('VARIABLE', r'[A-Za-z_][A-Za-z0-9_]+', 'variable'), # Identificadores
]

# Funcion principal del analizador lexico
def lex2(input_string):
    tokens_found = []
    line_number = 1 # Contador de linea inicializado en 1
    # Iterar a traves de la cadena de entrada
    while input_string:
        match = None # Buscar el token coincidente en la entrada
        for token_name, pattern, description in tokens:
            regex = re.compile('^' + pattern)
            match = regex.search(input_string)
            if match:
                value = match.group(0)
                # tokens_found.append((token_name, value, description))
                input_string = input_string[match.end():]
                break
        # Si no se encuentra ningun token, se agrega el valor a una lista especial con informacion de linea
        if not match:
            # Eliminar espacios en blanco y caracteres no validos
            invalid_value = re.search(r'^\S+', input_string)
            if invalid_value:
                value = invalid_value.group(0)
                tokens_found.append(('INVALIDO', value, 'valor no compatible, linea ' + str(line_number)))
            input_string = input_string[1:]
        if input_string.startswith('\n'):
            line_number += 1
            input_string = input_string[1:]
    return tokens_found

# Ejemplo de uso MAIN

def analizar_lexico( code2 ):
    code = code2

    tokens = lex2(code)

    # Guardar la tabla en un string
    output = io.StringIO()
    # output.write("---------------------------------------------------------------------\n")
    for token_type, value, description in tokens:
        output.write(f"|{token_type:<15}| {value:<20}| {description:<28}|\n")
        break
        # output.write("---------------------------------------------------------------------\n")

    # Obtener el contenido del string
    result = output.getvalue()

    # Cerrar el objeto StringIO
    output.close()

    # Imprimir el resultado
    return (result)

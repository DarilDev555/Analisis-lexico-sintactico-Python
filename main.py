import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QColor
from PyQt5.QtCore import Qt
import ply.lex as lex
from prettytable import PrettyTable

from vista.home import *
from analizador_lexico import *
from analizador_sintactico import *

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QMainWindow, QFileDialog, QApplication
import subprocess
import shutil

class Simbolo:
    def __init__(self, nombre, tipo, valor, parametros, num_parametros, valor_maximo, valor_minimo):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.parametros = parametros
        self.num_parametros = num_parametros
        self.valor_maximo = valor_maximo
        self.valor_minimo = valor_minimo

    def __eq__(self, other):
        return (self.nombre, self.tipo, self.valor, self.parametros, self.num_parametros, self.valor_maximo, self.valor_minimo) == \
            (other.nombre, other.tipo, other.valor, self.parametros, other.num_parametros, other.valor_maximo, other.valor_minimo)

    def __hash__(self):
        return hash((self.nombre, self.tipo, self.valor, self.parametros, self.num_parametros, self.valor_maximo, self.valor_minimo))


lista_simbolos = []


class Main(QMainWindow):
    """ Clase principal de nuestra app """
    def __init__(self):
        """ Inicializamos nuestra app """
        QMainWindow.__init__(self)

        # Instanciamos nuestra ventana widget home
        self.home = Ui_home()
        self.home.setupUi(self)

        # Ajustar el tamaño del editor
        self.home.tx_ingreso.setFixedHeight(250)
        self.home.tx_sintactico.setFixedHeight(350)

        # Eventos
        self.home.bt_archivo.clicked.connect(self.ev_importar)
        self.home.pushButton.clicked.connect(self.ev_exportar)
        self.home.bt_analizar.clicked.connect(self.ev_analizar)
        
    def ev_sintactico(self):
        '''
        Manejo de análisis gramático
        :return: 
        '''
        # limpiamos el campo
        self.home.tx_sintactico.setText('')
        # Obtenemos los datos ingresados
        datos = self.home.tx_ingreso.toPlainText().strip()

        # analizamos la gramática de los datos ingresados
        resultado_sintactico, resultado_errorLineas = prueba_sintactica(datos)
        cadena = ''

        # Armamos la cadena a mostrar
        for item in resultado_sintactico:
            cadena += item + "\n"
        # mostramos en pantalla
        self.home.tx_sintactico.setText(cadena)

        # Resaltar en rojo las líneas con errores
        self.resaltar_errores(resultado_errorLineas)

    def resaltar_errores(self, error_lineas):
        """
        Resalta en rojo las líneas con errores en tx_ingreso.
        :param error_lineas: List of line numbers with errors
        """
        cursor = self.home.tx_ingreso.textCursor()
        formato = QTextCharFormat()
        formato.setBackground(QColor(Qt.red))

        for linea in error_lineas:
            # Mueve el cursor al inicio del texto
            cursor.movePosition(QTextCursor.Start)
            # Mueve el cursor a la línea con error
            for _ in range(linea - 1):
                cursor.movePosition(QTextCursor.Down)

            # Selecciona la línea completa
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            # Aplica el formato de resaltado
            cursor.setCharFormat(formato)
    
    def tabla_simbolos(self):
        analizador = lex.lex()
        analizador.input(self.home.tx_ingreso.toPlainText())
        lista_simbolos.clear()
        while True:
            tok = analizador.token()
            if not tok:
                break
            else:
                
                simbolo = None
                if tok.value == 'Robot':
                    simbolo = Simbolo('Robot', "Palabra Reservada", 'Null', 'Null', 'Null', 'Null', 'Null')
                elif tok.value == 'garra':
                    simbolo = Simbolo(tok.value, "Metodo", 'Numerico', 'Si', '1', '180', '0')
                elif tok.value == 'base':
                    simbolo = Simbolo(tok.value, "Metodo", 'Numerico', 'Si', '1', '360', '0')
                elif tok.value == 'cuerpo':
                    simbolo = Simbolo(tok.value, "Metodo", 'Numerico', 'Si', '1', '90', '0')
                elif tok.value == 'inicio':
                    simbolo = Simbolo(tok.value, "Metodo", 'Null', 'Null', 'Null', 'Null', 'Null')
                elif tok.value == 'detener':
                    simbolo = Simbolo(tok.value, "Metodo", 'Null', 'Null', 'Null', 'Null', 'Null')
                elif tok.value == 'velocidad':
                    simbolo = Simbolo(tok.value, "Metodo", 'Numerico', 'Si', '1', '1000', '0')
                elif tok.value == 'repetir':
                    simbolo = Simbolo(tok.value, "Metodo", 'Numerico', 'Si', '1', '1000', '0')
                elif tok.type == 'IDENTIFICADOR':
                    simbolo = Simbolo(tok.value, "Identificador", 'Null', 'Null', 'Null', 'Null', 'Null')
                
                if simbolo and simbolo not in lista_simbolos:
                    lista_simbolos.append(simbolo)


            
    def ev_importar(self):
        '''
        Manejo de subir archivo 
        :return: 
        '''
        dlg = QFileDialog()

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                data = f.read().strip()
                if data:
                    self.home.tx_ingreso.setPlainText(data+"\n")


    def ev_exportar(self):
        '''
        Manejo de exportación de contenido del editor a un archivo
        :return: 
        '''
        # Mostrar un diálogo para seleccionar la ubicación y el nombre del archivo de destino
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if fileName:
            # Obtener el texto del editor
            text = self.home.tx_ingreso.toPlainText()
            
            # Escribir el texto en el archivo seleccionado
            with open(fileName, 'w') as file:
                file.write(text)

    def ev_lexico(self):
        '''
        Manejo de análisis de expresión lexemas
        :return: 
        '''
        # limpiamos el campo
        self.home.tx_sintactico.setText('')
        # Obtenemos los datos ingresados
        datos = self.home.tx_ingreso.toPlainText().strip()
        # analizamos la lexemas de los datos ingresados
        self.home.tx_sintactico.setText(prueba(datos))

    def ev_analizar(self):
        estadoLexico = False
        estadoSintactico = False
        estadoSemantico = False
        resultado_errorLineas = []

        # Analisis Lexico
        # print("analizar")

        # limpiamos el campo
        self.home.tx_sintactico.setText('')
        # Obtenemos los datos ingresados
        datos = self.home.tx_ingreso.toPlainText().strip()

        # mostramos en pantalla
        error, lineaError = prueba(datos)
        self.home.tx_sintactico.setPlainText(error)
        self.resaltar_errores([lineaError])
        estadoLexico = error == ''

        if estadoLexico:
            self.despintar_texto()
            self.home.tx_sintactico.setText('')
            # Obtenemos los datos ingresados
            datos = self.home.tx_ingreso.toPlainText().strip()
            # analizamos la gramática de los datos ingresados
            resultado_sintactico, resultado_errorLineas = prueba_sintactica(datos)
            cadena = ''
            # Armamos la cadena a mostrar
            for item in resultado_sintactico:
                cadena += item + "\n"
            # mostramos en pantalla
            self.home.tx_sintactico.setText(cadena)
            # Resaltar en rojo las líneas con errores
            self.resaltar_errores(resultado_errorLineas)
            self.tabla_simbolos()
            # imprime tabla de simbolos
            self.imprimir_simbolos()
            estadoSintactico = self.home.tx_sintactico.toPlainText() == ''

        if estadoSintactico:
            self.despintar_texto()
            estadoSemantico = self.analizador_semantico()

        if estadoSemantico:
            datos = self.home.tx_ingreso.toPlainText().strip()
            intermediate_code = self.generate_intermediate_code(datos)
            self.print_intermediate_code(intermediate_code)
            # 
            data_section = self.generate_data_section(intermediate_code)
            code_section = """
CODE_SEG SEGMENT
ASSUME CS: CODE_SEG, DS:DATA_SEG
    MOV DX, 06H
    MOV AL, 10000000B;port A=output/ mode 0, PORT B=output/ mode 0 ,port C=output
    OUT DX, AL 
START:
            """
            code_section += self.convert_to_asm(intermediate_code)

            code_section += """
CODE_SEG    ENDS
END  START
            """
            with open("output.asm", "w") as file:
                file.write(data_section)
                file.write(code_section)
                
            shutil.copy("output.asm", "C:/DOSBox-0.73/Tasm/codigo.asm")
                
            p = subprocess.run("C:/DOSBox-0.73/dosbox.exe")
            
            exit_code = p.returncode

            print("Código ensamblador generado en output.asm")





    def analizador_semantico(self):
        """
        Realiza el análisis semántico sobre el contenido de tx_ingreso.
        """
        texto = self.home.tx_ingreso.toPlainText().strip().split('\n')
        simbolos_declarados = {}
        errores = []

        # Paso 1: Verificación de variables declaradas repetidas
        for i, linea in enumerate(texto, 1):
            if 'Robot' in linea:
                partes = linea.split()
                if len(partes) == 2:
                    nombre_var = partes[1]
                    if nombre_var in simbolos_declarados:
                        errores.append(f"Error: Variable '{nombre_var}' declarada repetidamente en la línea {i}")
                    else:
                        simbolos_declarados[nombre_var] = i

        # Paso 2: Verificación de uso de variables no declaradas
        for i, linea in enumerate(texto, 1):
            partes = linea.split()
            if len(partes) > 1 and '=' in linea:
                nombre_var = partes[0].strip().split('.')[0]
                if nombre_var not in simbolos_declarados:
                    errores.append(f"Error: Variable '{nombre_var}' no declarada usada en la línea {i}")
            elif len(partes) == 1:
                nombre_var = partes[0].strip().split('.')[0]
                if nombre_var not in simbolos_declarados:
                    errores.append(f"Error: Variable '{nombre_var}' no declarada usada en la línea {i}")

        # verifica metodos con y sin atributos
        for i, linea in enumerate(texto, 1):
            partes = linea.split()
            for parte in partes:
                if ('inicio' in parte or 'detener' in parte) and len(partes) > 1:
                    errores.append(f"Error: Método '{parte}' no debe llevar atributos en la línea {i}")
                if ('garra' in parte or 'base' in parte or 'cuerpo' in parte or 'velocidad' in parte or 'repetir' in parte) and len(partes) == 1:
                    errores.append(f"Error: Método '{parte}' debe llevar atributos en la línea {i}")

        # Paso 3: Verificación de atributos dentro de los rangos permitidos
        for i, linea in enumerate(texto, 1):
            if '=' in linea:
                partes = linea.split('=')
                nombre_var = partes[0].strip()
                if '.' in nombre_var:
                    var, attr = nombre_var.split('.')
                    valor = int(partes[1].strip())
                    if attr == 'garra' and (valor < 0 or valor > 180):
                        errores.append(f"Error: Valor de 'garra' fuera de rango en la línea {i}")
                    elif attr == 'cuerpo' and (valor < 0 or valor > 90):
                        errores.append(f"Error: Valor de 'cuerpo' fuera de rango en la línea {i}")
                    elif attr == 'base' and (valor < 0 or valor > 360):
                        errores.append(f"Error: Valor de 'base' fuera de rango en la línea {i}")
                    elif attr == 'velocidad' and (valor < 0 or valor > 1000):
                        errores.append(f"Error: Valor de 'velocidad' fuera de rango en la línea {i}")
                    elif attr == 'repetir' and (valor < 0 or valor > 1000):
                        errores.append(f"Error: Valor de 'repetir' fuera de rango en la línea {i}")
                    

        # Mostrar errores en el campo de texto sintáctico
        if errores:
            self.home.tx_sintactico.setText('\n'.join(errores))
            return False
        else:
            self.home.tx_sintactico.setText("Análisis completado sin errores.")
            return True


    def imprimir_simbolos(self):
        """
        Imprime la lista de símbolos en una tabla.
        """
        tabla = PrettyTable()
        tabla.field_names = ["Nombre", "Tipo", "Valor", "Parámetros", "Num Parámetros", "Valor Máximo", "Valor Mínimo"]

        for simbolo in lista_simbolos:
            tabla.add_row([simbolo.nombre, simbolo.tipo, simbolo.valor, simbolo.parametros, simbolo.num_parametros, simbolo.valor_maximo, simbolo.valor_minimo])

        print(tabla)

    def despintar_texto(self):
        """
        Elimina cualquier formato aplicado al texto.
        """
        cursor = self.home.tx_ingreso.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
    
    def generate_intermediate_code(self, source_code):
        # Dividimos el código fuente en líneas
        lines = source_code.strip().split('\n')

        # Inicializamos la tabla de código intermedio
        intermediate_code = []

        # Contador de memoria para las declaraciones de robots
        memory_counter = 1

        # Patrón para coincidir con la declaración del robot y las instrucciones
        robot_pattern = re.compile(r'Robot\s+(\w+)')
        instruction_pattern = re.compile(r'(\w+)\.(\w+)\s*=\s*(\d+)|(\w+)\.(\w+)')

        # Diccionario para almacenar las memorias de cada robot
        robot_memories = {}

        # Pasada única: procesar declaraciones de robots y sus instrucciones
        for line in lines:
            robot_match = robot_pattern.match(line.strip())
            instruction_match = instruction_pattern.match(line.strip())

            if robot_match:
                # Capturamos el identificador del robot y asignamos una memoria única
                robot_id = robot_match.group(1)
                mem_id = f'mem{memory_counter}'
                robot_memories[robot_id] = mem_id
                intermediate_code.append(['Cargar', 'Robot', '', mem_id])
                intermediate_code.append(['Crear', mem_id, '', robot_id])
                memory_counter += 1
            elif instruction_match:
                if instruction_match.group(1) and instruction_match.group(2) and instruction_match.group(3):
                    # Caso de asignación: robot_id.var = value
                    robot_id = instruction_match.group(1)
                    var = instruction_match.group(2)
                    value = instruction_match.group(3)
                    intermediate_code.append(['Cargar', value, '', 'ax'])
                    intermediate_code.append(['Llamar', var, robot_id, ''])
                elif instruction_match.group(4) and instruction_match.group(5):
                    # Caso de llamada a método: robot_id.method
                    robot_id = instruction_match.group(4)
                    method = instruction_match.group(5)
                    intermediate_code.append(['Llamar', method, robot_id, ''])

        return intermediate_code

    def print_intermediate_code(self, intermediate_code):
        # Crear la tabla con PrettyTable
        tabla_intermedia = PrettyTable()
        tabla_intermedia.field_names = ["Op", "Dir1", "Dir2", "Res"]

        for row in intermediate_code:
            tabla_intermedia.add_row(row)

        print(tabla_intermedia)

    def generate_data_section(self, quadruples):
        objects = set()
        for quad in quadruples:
            op, dir1, dir2, res = quad
            if op == "Crear":
                objects.add(res)
        
        data_section = "\nDATA_SEG SEGMENT\n"
        data_section += "    PORTA EQU 00H\n    PORTB EQU 02H\n    PORTC EQU 04H\n    Config EQU 06H\n"
        for obj in objects:
            data_section += f"    {obj} DW 00000000b\n" 
        data_section += "DATA_SEG ENDS\n"
        
        return data_section

    def cambiar_estado(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return estados[0]
        elif estado_motor == estados[0]:
            return estados[1]
        elif estado_motor == estados[1]:
            return estados[2]
        elif estado_motor == estados[2]:
            return estados[3]
        elif estado_motor == estados[3]:
            return estados[0]

    def cambiar_estado_reversa(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return estados[0]
        elif estado_motor == estados[3]:
            return estados[2]
        elif estado_motor == estados[2]:
            return estados[1]
        elif estado_motor == estados[1]:
            return estados[0]
        elif estado_motor == estados[0]:
            return estados[3]    
    
    def base(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return " \nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return " \nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return " \nMOV al, 00000011b\nOUT DX,AL"
        elif estado_motor == estados[2]:
            return " \nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[3]:
            return " \nMOV al, 00001100b\nOUT DX,AL"
    
    def base_r(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return " \nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return " \nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return " \nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[2]:
            return " \nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[3]:
            return " \nMOV al, 00000011b\nOUT DX,AL"
        
    def cuerpo(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return " \nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return " \nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return ""
        elif estado_motor == estados[2]:
            return ""
        elif estado_motor == estados[3]:
            return ""
        
    def cuerpo_r(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return " \nMOV al, 00000000b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return " \nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return " \nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[2]:
            return " \nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[3]:
            return " \nMOV al, 00000000b\nOUT DX,AL"
        
    def garra(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return "\nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return "\nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return "\nMOV al, 00000011b\nOUT DX,AL"
        elif estado_motor == estados[2]:
            return "\nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[3]:
            return "\nMOV al, 00001100b\nOUT DX,AL"
        
    def garra_r(self, estado_motor):
        estados = ["00001100b", "00000110b", "00000011b", "00001001b"]
        if estado_motor == "00000000b":
            return "\nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[0]:
            return "\nMOV al, 00001001b\nOUT DX,AL"
        elif estado_motor == estados[1]:
            return "\nMOV al, 00001100b\nOUT DX,AL"
        elif estado_motor == estados[2]:
            return "\nMOV al, 00000110b\nOUT DX,AL"
        elif estado_motor == estados[3]:
            return "\nMOV al, 00000011b\nOUT DX,AL"
    
    def convert_to_asm(self, internal_code):
        quads_repetir = []
        cuantas_veces = 0
        estado_motor_base = "00000000b"
        estado_motor_cuerpo = "00000000b"
        estado_motor_garra = "00000000b"
        estado_grados_base = 0
        estado_grados_cuerpo = 0
        estado_grados_garra = 0
        ax = 0
        NE = 0
        delays = 0
        asm_code = ""
        for quad in internal_code:
            op_n, dir1_n, dir2_n, res_n = quad
            if op_n == "Llamar" and dir1_n == "inicio":
                escribir = False
                quad_anterior = None
                for quad_2 in internal_code:
                    if "repetir" in quad_2:
                        cuantas_veces = int(quad_anterior[1])
                        break
                    if escribir:
                        quads_repetir.append(quad_2)
                    if "inicio" in quad_2:
                        escribir = True
                    quad_anterior = quad_2
                    
                    
                print(quads_repetir)    
        for _ in range(cuantas_veces):
            for quad in quads_repetir:
                op, dir1, dir2, res = quad
                if op == "Cargar" and dir1 == "Robot":
                    continue
                elif op == "Cargar":
                    if res == "ax":
                        ax = 0
                        ax = int(dir1)
                elif op == "Llamar":
                    if dir1 == "velocidad ax":
                        continue
                    elif dir1 == "detener":
                        continue
                    elif dir1 == "base":
                        aux = ax - estado_grados_base
                        print(f'Base = {estado_grados_base}')
                        if aux == 0:
                            continue
                        elif aux > 0:
                            giros = aux // 45
                            for _ in range(giros):
                                estado_grados_base += 45
                                asm_code += "MOV DX, PORTA\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.base(estado_motor_base) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_base = self.cambiar_estado(estado_motor_base)
                            estado_grados_base = ax
                            ax = 0
                        elif aux < 0:
                            giros = (aux * -1) // 45
                            for _ in range(giros):
                                estado_grados_base -= 45
                                asm_code += "MOV DX, PORTA\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.base_r(estado_motor_base) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_base = self.cambiar_estado_reversa(estado_motor_base)
                            estado_grados_base = ax
                            ax = 0
                    elif dir1 == "cuerpo":
                        aux = ax - estado_grados_cuerpo
                        print(f'Cuerpo = {estado_grados_cuerpo}')
                        if aux == 0:
                            continue
                        elif aux > 0:
                            giros = aux // 45
                            for _ in range(giros):
                                estado_grados_cuerpo += 45
                                asm_code += "MOV DX, PORTB\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.cuerpo(estado_motor_cuerpo) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_cuerpo = self.cambiar_estado(estado_motor_cuerpo)
                            estado_grados_cuerpo = ax
                            ax = 0
                        elif aux < 0:
                            giros = (aux * -1) // 45
                            for _ in range(giros):
                                estado_grados_cuerpo -= 45
                                asm_code += "MOV DX, PORTB\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.cuerpo_r(estado_motor_cuerpo) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_cuerpo = self.cambiar_estado_reversa(estado_motor_cuerpo)
                            estado_grados_cuerpo = ax
                            ax = 0
                    elif dir1 == "garra":
                        aux = ax - estado_grados_garra
                        print(f'Garra = {estado_grados_garra}')
                        if aux == 0:
                            continue
                        elif aux > 0:
                            giros = aux // 45
                            for _ in range(giros):
                                estado_grados_garra += 45
                                asm_code += "MOV DX, PORTC\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.garra(estado_motor_garra) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_garra = self.cambiar_estado(estado_motor_garra)
                            estado_grados_garra = ax
                            ax = 0
                        elif aux < 0:
                            giros = (aux * -1) // 45
                            for _ in range(giros):
                                estado_grados_garra -= 45
                                asm_code += "MOV DX, PORTC\n"
                                asm_code += f"MOV CX, 0ffffh\ndelay_{delays}:\nLOOP delay_{delays}\n"
                                asm_code += self.garra_r(estado_motor_garra) + "\n"
                                NE += 1
                                delays += 1
                                estado_motor_garra = self.cambiar_estado_reversa(estado_motor_garra)
                            estado_grados_garra = ax
                            ax = 0
                    elif dir1 == "repetir":
                        asm_code += "dec bx\ncmp bx,0d\njne inicio\n"
                else:
                    asm_code += f"; Unknown operation: {op}\n"
        return asm_code



def iniciar():
    # Instanciamos nuestra app por defecto, esto no cambia
    app = QApplication(sys.argv)

    # Instanciamos nuestra ventana
    ventana = Main()
    # Mostramos nuestra app
    ventana.show()

    # Controlamos el cierre de la app
    sys.exit(app.exec_())


if __name__ == '__main__':
    iniciar()


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, *args):
        super().__init__(*args)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.setFont(QFont("Courier", 1))  # Aquí puedes ajustar el tamaño de la fuente

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)




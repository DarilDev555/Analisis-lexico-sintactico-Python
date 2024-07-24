quadruples = [
    ("Crear", "mem1", "", "r1"),
    ("Llamar", "iniciar", "", "r1"),
    ("Cargar", "180", "", "ax"),
    ("Llamar", "base", "", "r1"),
    ("Cargar", "45", "", "ax"),
    ("Llamar", "cuerpo", "", "r1"),
    ("Cargar", "180", "", "ax"),
    ("Llamar", "garra", "", "r1"),
    ("Cargar", "0", "", "ax"),
    ("Llamar", "garra", "", "r1"),
    ("Cargar", "90", "", "ax"),
    ("Llamar", "cuerpo", "", "r1"),
    ("Cargar", "0", "", "ax"),
    ("Llamar", "base", "", "r1"),
    ("Cargar", "90", "", "ax"),
    ("Llamar", "cuerpo", "", "r1"),
    ("Cargar", "10", "", "cx"),
    ("Llamar", "repetir", "", "r1"),
    ("Llamar", "detener", "", "r1"),
]

def generate_data_section(quadruples):
    objects = set()
    for quad in quadruples:
        op, dir1, dir2, res = quad
        if op == "Crear":
            objects.add(res)
    
    data_section = "DATA SEGMENT\n"
    for obj in objects:
        data_section += f"{obj} DW 0\n" 
    data_section += "DATA ENDS\n"
    
    return data_section

def convert_to_asm(quad):
    op, dir1, dir2, res = quad
    asm_code = ""
    
    if op == "Cargar":
        asm_code = f"MOV {res}, {dir1}\n"
    elif op == "Crear":
        asm_code = f"; Crear {res} (equivalente a inicializar {dir1} como {res})\n"
        asm_code += f"MOV {res}, {dir1}\n" 
    elif op == "Llamar":
        asm_code = f"CALL {dir1}_{res}\n"
    else:
        asm_code = f"; Unknown operation: {op}\n"

    return asm_code

data_section = generate_data_section(quadruples)

code_section = """
CODE SEGMENT
ASSUME CS:CODE, DS:DATA
START:
"""

for quad in quadruples:
    code_section += convert_to_asm(quad)

code_section += """
MOV AX, 4C00h
INT 21h
CODE ENDS
END START
"""
with open("output.asm", "w") as file:
    file.write(data_section)
    file.write(code_section)

print("Código ensamblador generado en output.asm")

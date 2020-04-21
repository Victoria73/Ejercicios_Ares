
import re 

expresion_titulo = "^[a-zA-ZáéíóúÁÉÍÓÚñÑ 0-9]{2,30}$"
expresion_paginas = "^[0-9,.]{1,6}$"
expresion_precio = "^[0-9,.]{1,6}$"

def validar_titulo(titulo):
    validador =re.compile(expresion_titulo)
    return validador.match(titulo)


def validar_paginas(paginas):
    validador = re.compile(expresion_paginas)
    return validador.match(paginas)
    
    
def validar_precio(precio): 
    validador = re.compile(expresion_precio)
    return validador.match(precio)  
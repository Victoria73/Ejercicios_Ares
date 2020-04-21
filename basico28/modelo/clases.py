

class Libro():
    
    def __init__(self):
        self.titulo = ""
        self.precio = 0.0
        self.paginas = 0
        self.digital = False
        self.tapa = "blanda"
        self.envio = "standar"
        self.id = 0
        self.imagen = ""


# o esta es otra opcion
'''
def __init__(self, titulo = "", paginas = 0, precio = 0.0,\
                  digital = False, tapa = "blanda", envio = "standar", id = 0):
        self.titulo = titulo
        self.paginas = paginas
        self.precio = precio
        self.digital = digital
        self.tapa = tapa
        self.envio = envio
        self.id = id
'''
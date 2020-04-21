'''
Created on Mar 30, 2020

@author: aressancho
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from ventanas import ventana_principal, ventana_registrar_libro,\
ventana_listado_libros, ventana_list_widget, ventana_table_widget,\
    ventana_editar_libro, boton_registrar_libro, ventana_ver_detalles_libro
import sys
from modelo.clases import Libro
from modelo import operaciones_bd
from PyQt5.Qt import QMessageBox, QTableWidget, QTableWidgetItem, QPushButton,\
    QMainWindow, QFileDialog, QPixmap, QLabel
from _functools import partial
from tkinter import *
import shutil
from pathlib import Path
from validadores.validadores_libro import validar_paginas
from validadores import validadores_libro
from modelo.operaciones_bd import borrar_libro, obtener_libro_por_id






#inicio definicion funciones

def registrar_libro():
    libro = Libro()
    libro.titulo = ui_registrar_libro.entrada_titulo.text()
    libro.titulo = libro.titulo.strip()#strip elimina espacios en blanco
    libro.paginas = ui_registrar_libro.entrada_paginas.text()
    libro.paginas = libro.paginas.strip()
    libro.precio = ui_registrar_libro.entrada_precio.text()
    libro.precio = libro.precio.strip()
    
    resultado_validar_titulo = validadores_libro.validar_titulo(libro.titulo)
    if resultado_validar_titulo == None :
        ui_registrar_libro.label_error_titulo.setText("<font color = 'red'>Titulo incorrecto<\font>")
        return
    else :
        ui_registrar_libro.label_error_titulo.clear()
           
    resultado_validar_paginas = validadores_libro.validar_paginas(libro.paginas)
    if resultado_validar_paginas == None :
        ui_registrar_libro.label_error_paginas.setText("<font color = 'red'>Paginas incorrecto<\font>")
        return
    else :
        ui_registrar_libro.label_error_paginas.clear()    
    try:
        resultado_validar_precio = validadores_libro.validar_precio(libro.precio)
        if resultado_validar_precio == None :
            ui_registrar_libro.label_error_precio.setText("<font color = 'red'>Precio incorrecto<\font>")
            return
        else :
            ui_registrar_libro.label_error_precio.clear()
    except Exception as a:
        print(a)
    
    libro.paginas = ui_registrar_libro.entrada_paginas.text()
    libro.precio = ui_registrar_libro.entrada_precio.text()
    if ui_registrar_libro.checkbox_digital.isChecked():
        libro.digital = True 
        
    indice_seleccionado = ui_registrar_libro.combo_tapa.currentIndex()
    libro.tapa = ui_registrar_libro.combo_tapa.itemText(indice_seleccionado)
    
    if ui_registrar_libro.radio_estandar.isChecked():
        libro.envio = "estandar"
    if ui_registrar_libro.radio_urgente.isChecked():
        libro.envio = "urgente"
    if ui_registrar_libro.radio_prioritario.isChecked():
        libro.envio = "prioritario"
    
    id_generado = operaciones_bd.registro_libro(libro)
    
    ruta_imagen = "temporal/imagen.jpg"
    objeto_path = Path(ruta_imagen)
    existe = objeto_path.is_file()
    if existe :
        ruta_imagen_destino = "imagenes/" + str(id_generado) + ".jpg"
        shutil.move("temporal/imagen.jpg",ruta_imagen_destino)
    
    QMessageBox.about(MainWindow,"Info","Registro de libro OK")
    
def seleccionar_imagen():
    archivo = QFileDialog.getOpenFileName(MainWindow)
    print(archivo)
    ruta_archivo = archivo[0]
    shutil.copy(ruta_archivo,"temporal/imagen.jpg")
    pixmap = QPixmap("temporal/imagen.jpg") 
    ui_registrar_libro.label_imagen.setPixmap(pixmap)
    ancho_label_imagen = ui_registrar_libro.label_imagen.width()
    pixmap_redim = pixmap.scaledToWidth(ancho_label_imagen)
    ui_registrar_libro.label_imagen.setPixmap(pixmap_redim)

def cambio_imagen():
    archivo = QFileDialog.getOpenFileName(MainWindow)
    ruta_archivo = archivo[0]
    shutil.copy(ruta_archivo,"temporal/imagen.jpg")
    pixmap = QPixmap("temporal/imagen.jpg") 
    ui_ventana_editar_libro.label_imagen.setPixmap(pixmap)
    ancho_label_imagen = ui_ventana_editar_libro.label_imagen.width()
    pixmap_redim = pixmap.scaledToWidth(ancho_label_imagen)
    ui_ventana_editar_libro.label_imagen.setPixmap(pixmap_redim)

    
def mostar_registro_libro():

    ui_registrar_libro.setupUi(MainWindow)
    ui_registrar_libro.boton_registrar_libro.clicked.connect(registrar_libro)
    ui_registrar_libro.boton_seleccionar_archivo.clicked.connect(seleccionar_imagen)
    ui_registrar_libro.label_error_titulo.clear()
    ui_registrar_libro.label_error_paginas.clear()
    ui_registrar_libro.label_error_precio.clear()
    
    
def mostrar_listado_libros():
    ui_listar_libros.setupUi(MainWindow)
    lista_resultado = operaciones_bd.obtener_libros()
    texto = ""
    for l in lista_resultado:
        texto += "id: " + str(l[0]) + " titulo: " + l[1] + " paginas: " + str(l[2])+ "\n"
            
    ui_listar_libros.listado_libros.setText(texto)
    
def mostrar_list_widget():
    global lista_resultado
    ui_ventana_list_widget.setupUi(MainWindow)
    lista_resultado = operaciones_bd.obtener_libros()
    for l in lista_resultado:
        ui_ventana_list_widget.list_widget_libros.addItem(l[1] + " paginas: " + str(l[2])+ " precio: " + "\n")

    ui_ventana_list_widget.list_widget_libros.itemClicked.connect(mostrar_registro)

def mostrar_registro():
    indice_seleccionado = ui_ventana_list_widget.list_widget_libros.currentRow()
    texto = ""
    texto += "titulo " + lista_resultado[indice_seleccionado][1] + "\n"
    texto += "paginas " + str(lista_resultado[indice_seleccionado][2]) + "\n"
    #texto += "precio" + str(lista_resultado[indice_seleccionado][3]) + "\n"
    QMessageBox.about(MainWindow, "Info ", "mostrar informacion del elemento " + str(indice_seleccionado ) + "\n" + texto)

def mostrar_table_widget():
    ui_ventana_table_widget.setupUi(MainWindow)
    fila = 0
    
    libros = operaciones_bd.obtener_libros()
    for l in libros :
        ui_ventana_table_widget.tabla_libros.insertRow(fila)
        '''celda = QTableWidgetItem(str(l[0]))
        ui_ventana_table_widget.tabla_libros.setItem(fila,0,celda)
        celda = QTableWidgetItem(str(l[1]))
        ui_ventana_table_widget.tabla_libros.setItem(fila,1,celda)
        celda = QTableWidgetItem(str(l[2]))
        ui_ventana_table_widget.tabla_libros.setItem(fila,2,celda)
        celda = QTableWidgetItem(str(l[3]))
        ui_ventana_table_widget.tabla_libros.setItem(fila,3,celda)
        '''
        columna_indice = 0
        for valor in l:
            if columna_indice == 4:
                if valor == 0:
                    valor ="No"
                else :
                    valor = "Si"    
                
            celda = QTableWidgetItem(str(valor))
            ui_ventana_table_widget.tabla_libros.setItem(fila,columna_indice,celda)
            columna_indice += 1
            #despues de meter llos datos en la fila, creamos un boton de borrar
        boton_ver_detalles = QPushButton("Ver detalles")
        boton_ver_detalles.clicked.connect(partial(cargar_ver_detalle,l[0]))
        ui_ventana_table_widget.tabla_libros.setCellWidget(fila,3,boton_ver_detalles)
           
        boton_borrar = QPushButton("borrar")
        boton_borrar.clicked.connect(partial(borrar_libro,l[0]))
        ui_ventana_table_widget.tabla_libros.setCellWidget(fila,5,boton_borrar)
                
        boton_editar = QPushButton("Editar")
        boton_editar.clicked.connect(partial(editar_libro,l[0]))
        ui_ventana_table_widget.tabla_libros.setCellWidget(fila,6,boton_editar)
        
        label_miniatura = QLabel()
        ruta_imagen = "imagenes/" + str(l[0]) + ".jpg"
        objeto_path = Path(ruta_imagen)
        existe = objeto_path.is_file()
        if existe :
            
            pixmap = QPixmap("imagenes/" + str(l[0]) + ".jpg")
            pixmap_redim =pixmap.scaledToHeight(40)
            label_miniatura.setPixmap(pixmap_redim)
            ui_ventana_table_widget.tabla_libros.setCellWidget(fila,4,label_miniatura)
            
        fila += 1

def cargar_ver_detalle(id):
    QMessageBox.about(MainWindow,"Info"," Ver detalles de id: " + str(id))
    ui_ventana_ver_detalles_libro.setupUi(MainWindow)
    libro = operaciones_bd.obtener_libro_por_id(id)
    
    ui_ventana_ver_detalles_libro.entrada_titulo.setText(libro.titulo)
    ui_ventana_ver_detalles_libro.entrada_paginas.setText(str(libro.paginas))
    ui_ventana_ver_detalles_libro.entrada_precio.setText(str(libro.precio))
    
    if libro.digital :   
        ui_ventana_ver_detalles_libro.checkbox_digital.setChecked(True)
        
    ui_ventana_ver_detalles_libro.entrada_combo.setCurrentText(libro.tapa)
    
    if libro.envio == "estandar":
        ui_ventana_ver_detalles_libro.entrada_estandar.setChecked(True)
    elif libro.envio == "urgente":
        ui_ventana_ver_detalles_libro.entrada_urgente.setChecked(True)
    elif libro.envio == "prioritario":
        ui_ventana_ver_detalles_libro.entrada_prioritario.setChecked(True)
    
    
    ruta_imagen_destino = "imagenes/" + str(libro.id) + ".jpg"
    pixmap = QPixmap(ruta_imagen_destino)
    ancho_label_imagen = ui_ventana_ver_detalles_libro.label_imagen.width()
    pixmap_redim = pixmap.scaledToWidth(ancho_label_imagen)
    ui_ventana_ver_detalles_libro.label_imagen.setPixmap(pixmap_redim)
    
    
    
    
    
            
def editar_libro(id):
    QMessageBox.about(MainWindow,"Info"," vas a editar el registro de id: " + str(id))
    ui_ventana_editar_libro.setupUi(MainWindow)
    
    libro_a_editar = operaciones_bd.obtener_libro_por_id(id)
    
    ui_ventana_editar_libro.entrada_titulo.setText(libro_a_editar.titulo)
    ui_ventana_editar_libro.label_error_titulo.clear()
    
    ui_ventana_editar_libro.entrada_paginas.setText(str(libro_a_editar.paginas))
    ui_ventana_editar_libro.label_error_paginas.clear()
    
    
    ui_ventana_editar_libro.entrada_precio.setText(str(libro_a_editar.precio))
    ui_ventana_editar_libro.label_error_precio.clear()
    
    ui_ventana_editar_libro.checkbox_digital.setChecked(libro_a_editar.digital)
    ui_ventana_editar_libro.entrada_combo.setCurrentText(libro_a_editar.tapa)
    if libro_a_editar.envio == "estandar":
        ui_ventana_editar_libro.entrada_estandar.setChecked(True)
    elif libro_a_editar.envio == "urgente":
        ui_ventana_editar_libro.entrada_urgente.setChecked(True)
    elif libro_a_editar.envio == "prioritario":
        ui_ventana_editar_libro.entrada_prioritario.setChecked(True)
    
    
    ruta_imagen_destino = "imagenes/" + str(id) + ".jpg"
    pixmap = QPixmap(ruta_imagen_destino)
    ui_ventana_editar_libro.label_imagen.setPixmap(pixmap)
    ui_ventana_editar_libro.boton_seleccionar_archivo.clicked.connect(cambio_imagen)
    
    ui_ventana_editar_libro.boton_registrar_cambiar_libro.clicked.connect(partial(guardar_cambios_libro,libro_a_editar.id))
    
def guardar_cambios_libro(id):
    
    libro_guardar_cambios = Libro()
    libro_guardar_cambios.titulo = ui_ventana_editar_libro.entrada_titulo.text()
    
    resultado_validar_titulo = validadores_libro.validar_titulo(libro_guardar_cambios.titulo)
    if resultado_validar_titulo == None :
        ui_ventana_editar_libro.label_error_titulo.setText("<font color = 'red'>Titulo incorrecto<\font>")
        return
    else :
        ui_ventana_editar_libro.label_error_titulo.clear()
    
            
    libro_guardar_cambios.paginas = ui_ventana_editar_libro.entrada_paginas.text()
    resultado_validar_paginas = validadores_libro.validar_paginas(libro_guardar_cambios.paginas)
    if resultado_validar_paginas == None :
        ui_ventana_editar_libro.label_error_paginas.setText("<font color = 'red'>Paginas incorrecto<\font>")
        return
    else :
        
        ui_ventana_editar_libro.label_error_paginas.clear()
    
    
    libro_guardar_cambios.precio = ui_ventana_editar_libro.entrada_precio.text()
    resultado_validar_precio = validadores_libro.validar_precio(libro_guardar_cambios.precio)
    if resultado_validar_precio == None :
        ui_ventana_editar_libro.label_error_precio.setText("<font color = 'red'>Precio incorrecto<\font>")
        return
    else :
        ui_ventana_editar_libro.label_error_precio.clear()

        
    
    if ui_ventana_editar_libro.checkbox_digital.isChecked():
        libro_guardar_cambios.digital = True 
    indice_seleccionado = ui_ventana_editar_libro.entrada_combo.currentIndex()
    libro_guardar_cambios.tapa = ui_ventana_editar_libro.entrada_combo.itemText(indice_seleccionado)
    if ui_ventana_editar_libro.entrada_estandar.isChecked():
        libro_guardar_cambios.envio = "estandar"
    if ui_ventana_editar_libro.entrada_urgente.isChecked():
        libro_guardar_cambios.envio = "urgente"
    if ui_ventana_editar_libro.entrada_prioritario.isChecked():
        libro_guardar_cambios.envio = "prioritario"
    
    ruta_imagen = "temporal/imagen.jpg"
    objeto_path = Path(ruta_imagen)
    existe = objeto_path.is_file()
    if existe :
        ruta_imagen_destino = "imagenes/" + str(id) + ".jpg"
        shutil.move("temporal/imagen.jpg",ruta_imagen_destino)
    
    
    libro_guardar_cambios.id = id
    
    
    
    
    QMessageBox.about(MainWindow, "Info","guardar cambios sobre el registro id:  " + str(id))
    operaciones_bd.guardar_cambios_libro(libro_guardar_cambios)
    
    mostrar_table_widget()
    
            
def borrar_libro(id):
    res = QMessageBox.question(MainWindow,"Info","va a borrar un registro de id: " + str(id))
    if res == QMessageBox.Yes:
        operaciones_bd.borrar_libro(id)
        mostrar_table_widget()
    
    
def mostrar_inicio():
    ui.setupUi(MainWindow)

#fin definicion funciones


#inicio aplicacion principal:

app = QtWidgets.QApplication(sys.argv)#linea obligatoria para usar pyqt5
MainWindow = QtWidgets.QMainWindow()#crear una ventana principal con pyqt5

ui = ventana_principal.Ui_ventana_principal()#creo el interfaz definido por ventana_principal.py
#que es el archivo generado desde la consola a partir
#del archivo de diseño ventana_principal.ui
ui_registrar_libro = ventana_registrar_libro.Ui_ventana_registrar_libro()#lo mismo pero para registrar libro
ui_listar_libros = ventana_listado_libros.Ui_ventana_listado_libros()#lo mismo pero para listar libros
ui_ventana_list_widget = ventana_list_widget.Ui_MainWindow()
ui_ventana_table_widget = ventana_table_widget.Ui_MainWindow()
ui_ventana_editar_libro = ventana_editar_libro.Ui_MainWindow()
ui_ventana_ver_detalles_libro = ventana_ver_detalles_libro.Ui_MainWindow()

ui.setupUi(MainWindow)
#todo lo que tiene el interfaz de la ventana principal lo pongo en el
#MainWindow
#asignar las funciones a los submenús
ui.submenu_insertar_libro.triggered.connect(mostar_registro_libro)
ui.submenu_listar_libros.triggered.connect(mostrar_listado_libros)
ui.submenu_inicio.triggered.connect(mostrar_inicio)
ui.submenu_widget_libro.triggered.connect(mostrar_list_widget)
ui.submenu_table_libro.triggered.connect(mostrar_table_widget)

MainWindow.show()#mostrar la ventana principal de pyqt5
sys.exit(app.exec_())#cerrar la aplicacion cuando se cierra la ventana MainWindow

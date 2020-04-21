'''
El procedimiento con base de datos es :
1- conectar 
2- operar
3- desconectar

@author: EXPERISIT
'''

import mysql.connector
from modelo.clases import Libro
from modelo import constantes_sql, clases

def conectar():
    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        database = "bd_libros"
        )
    return conexion


def registro_libro(libro):
    sql = constantes_sql.SQL_INSERCION_LIBRO
    conexion = conectar()
    cursor = conexion.cursor()
    
    valores_a_insertar = (libro.titulo, libro.paginas, libro.precio, libro.digital, libro.tapa, libro.envio, libro.imagen)
    cursor.execute(sql,valores_a_insertar)
    conexion.commit()     #para subir archivos
    id_generado = cursor.lastrowid
    conexion.disconnect() #para desconnectar
    return id_generado

def obtener_libros():
    sql = constantes_sql.SQL_SELECT_LIBROS
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql)
    lista_resultado = cursor.fetchall()
    conexion.disconnect()
    return lista_resultado  

def borrar_libro(id_libro):
    sql = constantes_sql.SQL_BORRAR_LIBROS
    conexion = conectar()
    cursor = conexion.cursor()
    val = (id_libro,)
    cursor.execute(sql,val)
    conexion.commit()     #para subir archivos
    conexion.disconnect()
    
def obtener_libro_por_id(id): 
    sql = constantes_sql.SQL_OBTENER_LIBRO_ID
    conexion = conectar()
    cursor = conexion.cursor()
    val = (id,)
    cursor.execute(sql,val)
    resultado = cursor.fetchone()
    conexion.disconnect()
    
    libro = clases.Libro()
    libro.id = resultado[0]
    libro.titulo = resultado[1]
    libro.paginas = resultado[2]
    libro.precio = float(resultado[3])
    libro.digital = resultado[4]
    libro.tapa = resultado[5]
    libro.envio = resultado[6]
    libro.imagen = resultado[7]
    
    
    return libro

def guardar_cambios_libro(libro_a_guardar_cambios):
    sql = constantes_sql.SQL_GUARDAR_CAMBIOS_LIBRO
    conexion = conectar()
    cursor = conexion.cursor()
    val = (libro_a_guardar_cambios.titulo, libro_a_guardar_cambios.paginas, libro_a_guardar_cambios.precio, libro_a_guardar_cambios.digital, libro_a_guardar_cambios.tapa, libro_a_guardar_cambios.envio, libro_a_guardar_cambios.imagen, libro_a_guardar_cambios.id)
    
    cursor.execute(sql,val)
    conexion.commit()
    conexion.disconnect()
    
    
    
    
       
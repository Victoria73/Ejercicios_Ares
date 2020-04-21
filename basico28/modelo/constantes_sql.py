
SQL_INSERCION_LIBRO = "INSERT INTO `tabla_libros` (`id`, `titulo`, `paginas`, `precio`, `digital`, `tapa`, `envio`, `imagen`) VALUES (NULL, %s , %s , %s, %s , %s , %s, %s);"

SQL_SELECT_LIBROS = "SELECT id, titulo, paginas  FROM tabla_libros"

SQL_BORRAR_LIBROS = "DELETE FROM tabla_libros WHERE id = %s;"

SQL_OBTENER_LIBRO_ID = "SELECT * FROM tabla_libros WHERE id = %s;"

SQL_GUARDAR_CAMBIOS_LIBRO = "UPDATE tabla_libros SET titulo = %s,paginas = %s, precio = %s,digital = %s, tapa = %s, envio = %s, imagen = %s WHERE id = %s;"
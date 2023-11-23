productos = {
    1: {"nombre": "Martillo", "precio": 14.99, "tipo": "herramienta"},
    2: {"nombre": "Destornillador Phillips", "precio": 7.99, "tipo": "herramienta"},
    3: {"nombre": "Sierra Eléctrica", "precio": 79.99, "tipo": "herramienta"},
    4: {"nombre": "Caja de Herramientas Completa", "precio": 99.99, "tipo": "herramienta"},
    5: {"nombre": "Nivel de Burbuja", "precio": 9.99, "tipo": "herramienta"},
    
    6: {"nombre": "Batería Externa", "precio": 24.99, "tipo": "accesorio"},
    7: {"nombre": "Soporte para Teléfono", "precio": 14.99, "tipo": "accesorio"},
    8: {"nombre": "Cargador de Coche USB", "precio": 19.99, "tipo": "accesorio"},
    9: {"nombre": "Funda Resistente para Teléfono", "precio": 12.99, "tipo": "accesorio"},
    10: {"nombre": "Auriculares Inalámbricos", "precio": 29.99, "tipo": "accesorio"},
    
    11: {"nombre": "Cámara de Seguridad", "precio": 89.99, "tipo": "electrónica"},
    12: {"nombre": "Smart TV 4K", "precio": 499.99, "tipo": "electrónica"},
    13: {"nombre": "Reproductor de Blu-ray", "precio": 69.99, "tipo": "electrónica"},
    14: {"nombre": "Altavoz Bluetooth", "precio": 39.99, "tipo": "electrónica"},
    15: {"nombre": "Tableta Gráfica", "precio": 129.99, "tipo": "electrónica"},
    
    16: {"nombre": "Licuadora", "precio": 49.99, "tipo": "electrodoméstico"},
    17: {"nombre": "Aspiradora Robótica", "precio": 199.99, "tipo": "electrodoméstico"},
    18: {"nombre": "Horno Tostador", "precio": 89.99, "tipo": "electrodoméstico"},
    19: {"nombre": "Batidora de Mano", "precio": 29.99, "tipo": "electrodoméstico"},
    20: {"nombre": "Cafetera Programable", "precio": 69.99, "tipo": "electrodoméstico"},
    
    21: {"nombre": "Silla de Oficina Ergonómica", "precio": 129.99, "tipo": "mueble"},
    22: {"nombre": "Mesa de Escritorio", "precio": 79.99, "tipo": "mueble"},
    23: {"nombre": "Lámpara de Pie", "precio": 49.99, "tipo": "mueble"},
    24: {"nombre": "Estantería Modular", "precio": 69.99, "tipo": "mueble"},
    25: {"nombre": "Sofá Reclinable", "precio": 399.99, "tipo": "mueble"},
    
    26: {"nombre": "Manta Suave", "precio": 19.99, "tipo": "ropa"},
    27: {"nombre": "Set de Toallas", "precio": 29.99, "tipo": "ropa"},
    28: {"nombre": "Alfombra Shaggy", "precio": 39.99, "tipo": "ropa"},
    29: {"nombre": "Cojines Decorativos", "precio": 14.99, "tipo": "ropa"},
    30: {"nombre": "Cortinas Opacas", "precio": 24.99, "tipo": "ropa"}
}

#crea una nueva ventana de registrar productos en la que del lado derecho se visualizara una tabla dividida por columnas en la que se vera el id del producto, su nombre, precio y tipo, del lado izquierdo se veran unos index para ingresar esos datos, exepto el id, ese se agrega automaticamente con un id libre, debajo los botones de agregar y modificar, con ese boton se agregara un nuevo producto con los datos ingresados, si se da click en algun producto de la tabla de la izquierda los datos de ese producto se ponen en los index y se bloquea el boton agregar, se deja modificar los datos del producto seleccionado y al dar click en modificar se modifica el producto seleccionado con los datos ingresados
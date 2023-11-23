import tkinter as tk
from tkinter import ttk

class RegistroProductos(tk.Toplevel):
    def __init__(rprod, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rprod.title("Registrar Producto")
        rprod.geometry("720x520")
        rprod.resizable(False, False)

        rprod.productos = productos
        rprod.producto_seleccionado = None

        lbl_id = tk.Label(rprod, text="ID:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_id = ttk.Entry(rprod, state="readonly")
        rprod.entry_id.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre = tk.Label(rprod, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_nombre = ttk.Entry(rprod)
        rprod.entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        lbl_precio = tk.Label(rprod, text="Precio:")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_precio = ttk.Entry(rprod)
        rprod.entry_precio.grid(row=2, column=1, padx=10, pady=10)

        lbl_tipo = tk.Label(rprod, text="Tipo:")
        lbl_tipo.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_tipo = ttk.Entry(rprod)
        rprod.entry_tipo.grid(row=3, column=1, padx=10, pady=10)

        rprod.btn_agregar = ttk.Button(rprod, text="Agregar", command=rprod.agregar_producto)
        rprod.btn_agregar.grid(row=4, column=0, columnspan=2, pady=10)

        rprod.btn_modificar = ttk.Button(rprod, text="Modificar", command=rprod.modificar_producto, state="disabled")
        rprod.btn_modificar.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(rprod, text="Volver", command=rprod.volver).grid(row=6, column=0, columnspan=2, pady=10)

        rprod.lista_productos = tk.Listbox(rprod, font=("DejaVu Sans", 10), selectmode=tk.SINGLE, width=50)
        rprod.lista_productos.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(rprod, orient="vertical", command=rprod.lista_productos.yview)
        scrollbar.grid(row=0, column=2, rowspan=8, sticky="nse")
        rprod.lista_productos.config(yscrollcommand=scrollbar.set)
        rprod.lista_productos.bind("<ButtonRelease-1>", rprod.cargar_producto_seleccionado)
        rprod.entry_nombre.bind("<KeyRelease>", rprod.habilitar_modificar)

        rprod.actualizar_lista_productos()

        
    def bloquear_botones(rprod):
        if rprod.producto_seleccionado:
            rprod.btn_agregar.config(state="disabled")
            rprod.btn_modificar.config(state="active")
        else:
            rprod.btn_agregar.config(state="active")
            rprod.btn_modificar.config(state="disabled")


    def agregar_producto(rprod):
        nombre = rprod.entry_nombre.get()
        precio = float(rprod.entry_precio.get())
        tipo = rprod.entry_tipo.get()

        nuevo_id = max(rprod.productos.keys()) + 1

        rprod.productos[nuevo_id] = {"nombre": nombre, "precio": precio, "tipo": tipo}

        rprod.actualizar_lista_productos()

        rprod.limpiar_campos_entrada()
        
        rprod.bloquear_botones()

    def modificar_producto(rprod):
        if rprod.producto_seleccionado:
            nombre = rprod.entry_nombre.get()
            precio = float(rprod.entry_precio.get())
            tipo = rprod.entry_tipo.get()
            rprod.productos[rprod.producto_seleccionado]["nombre"] = nombre
            rprod.productos[rprod.producto_seleccionado]["precio"] = precio
            rprod.productos[rprod.producto_seleccionado]["tipo"] = tipo

            rprod.actualizar_lista_productos()

            rprod.limpiar_campos_entrada()

            rprod.bloquear_botones()

    def cargar_producto_seleccionado(rprod, event):
        seleccion = rprod.lista_productos.curselection()
        if seleccion:
            index = seleccion[0]
            id_producto = int(rprod.lista_productos.get(index).split(" - ")[0])
            producto = rprod.productos[id_producto]

            rprod.entry_id.config(state="normal")
            rprod.entry_id.delete(0, tk.END)
            rprod.entry_id.insert(0, str(id_producto))
            rprod.entry_id.config(state="readonly")

            rprod.entry_nombre.delete(0, tk.END)
            rprod.entry_nombre.insert(0, producto["nombre"])

            rprod.entry_precio.delete(0, tk.END)
            rprod.entry_precio.insert(0, producto["precio"])

            rprod.entry_tipo.delete(0, tk.END)
            rprod.entry_tipo.insert(0, producto["tipo"])

            rprod.habilitar_modificar()

            rprod.bloquear_botones()

    def habilitar_modificar(rprod, event=None):
        if rprod.lista_productos.curselection() and rprod.entry_nombre.get() != "":
            rprod.producto_seleccionado = int(rprod.entry_id.get())
            rprod.btn_modificar.config(state="active")
        else:
            rprod.producto_seleccionado = None
            rprod.btn_modificar.config(state="disabled")
        rprod.bloquear_botones()

    def actualizar_lista_productos(rprod):
        rprod.lista_productos.delete(0, tk.END)

        for id_producto, producto_info in rprod.productos.items():
            rprod.lista_productos.insert(tk.END, f"{id_producto} - {producto_info['nombre']} - {producto_info['precio']:.2f}")

    def limpiar_campos_entrada(rprod):
        rprod.entry_id.config(state="normal")
        rprod.entry_id.delete(0, tk.END)
        rprod.entry_id.config(state="readonly")
        rprod.entry_nombre.delete(0, tk.END)
        rprod.entry_precio.delete(0, tk.END)
        rprod.entry_tipo.delete(0, tk.END)

    def volver(cproduct):
        cproduct.grab_release()
        cproduct.destroy()
        cproduct.master.deiconify()
import tkinter as tk
from tkinter import ttk

class RegistroProductos(tk.Toplevel):
    def __init__(rprod, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rprod.title("Registrar Producto")
        rprod.geometry("720x520")
        rprod.resizable(False, False)

        rprod.productos = productos
        rprod.producto_seleccionado = None

        lbl_id = tk.Label(rprod, text="ID:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_id = ttk.Entry(rprod, state="readonly")
        rprod.entry_id.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre = tk.Label(rprod, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_nombre = ttk.Entry(rprod)
        rprod.entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        lbl_precio = tk.Label(rprod, text="Precio:")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_precio = ttk.Entry(rprod)
        rprod.entry_precio.grid(row=2, column=1, padx=10, pady=10)

        lbl_tipo = tk.Label(rprod, text="Tipo:")
        lbl_tipo.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        rprod.entry_tipo = ttk.Entry(rprod)
        rprod.entry_tipo.grid(row=3, column=1, padx=10, pady=10)

        rprod.btn_agregar = ttk.Button(rprod, text="Agregar", command=rprod.agregar_producto)
        rprod.btn_agregar.grid(row=4, column=0, columnspan=2, pady=10)

        rprod.btn_modificar = ttk.Button(rprod, text="Modificar", command=rprod.modificar_producto, state="disabled")
        rprod.btn_modificar.grid(row=5, column=0, columnspan=2, pady=10)
        
        rprod.btn_eliminar = ttk.Button(rprod, text="Eliminar", command=rprod.eliminar_producto, state="disabled")
        rprod.btn_eliminar.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(rprod, text="Volver", command=rprod.volver).grid(row=7, column=0, columnspan=2, pady=10)

        rprod.lista_productos = tk.Listbox(rprod, font=("DejaVu Sans", 10), selectmode=tk.SINGLE, width=50)
        rprod.lista_productos.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(rprod, orient="vertical", command=rprod.lista_productos.yview)
        scrollbar.grid(row=0, column=2, rowspan=8, sticky="nse")
        rprod.lista_productos.config(yscrollcommand=scrollbar.set)
        rprod.lista_productos.bind("<ButtonRelease-1>", rprod.cargar_producto_seleccionado)
        rprod.entry_nombre.bind("<KeyRelease>", rprod.habilitar_modificar)

        rprod.actualizar_lista_productos()

        
    def bloquear_botones(rprod):
        if rprod.producto_seleccionado:
            rprod.btn_agregar.config(state="disabled")
            rprod.btn_modificar.config(state="active")
            rprod.btn_eliminar.config(state="active")
        else:
            rprod.btn_agregar.config(state="active")
            rprod.btn_modificar.config(state="disabled")
            rprod.btn_eliminar.config(state="disabled")


    def agregar_producto(rprod):
        nombre = rprod.entry_nombre.get()
        precio = float(rprod.entry_precio.get())
        tipo = rprod.entry_tipo.get()

        nuevo_id = max(rprod.productos.keys()) + 1

        rprod.productos[nuevo_id] = {"nombre": nombre, "precio": precio, "tipo": tipo}

        rprod.actualizar_lista_productos()

        rprod.limpiar_campos_entrada()
        
        rprod.bloquear_botones()

    def modificar_producto(rprod):
        if rprod.producto_seleccionado:
            nombre = rprod.entry_nombre.get()
            precio = float(rprod.entry_precio.get())
            tipo = rprod.entry_tipo.get()
            rprod.productos[rprod.producto_seleccionado]["nombre"] = nombre
            rprod.productos[rprod.producto_seleccionado]["precio"] = precio
            rprod.productos[rprod.producto_seleccionado]["tipo"] = tipo

            rprod.actualizar_lista_productos()

            rprod.limpiar_campos_entrada()

            rprod.bloquear_botones()

    def eliminar_producto(rprod):
        if rprod.producto_seleccionado:
            del rprod.productos[rprod.producto_seleccionado]
            rprod.actualizar_lista_productos()
            rprod.limpiar_campos_entrada()
            rprod.bloquear_botones()


    def cargar_producto_seleccionado(rprod, event):
        seleccion = rprod.lista_productos.curselection()
        if seleccion:
            index = seleccion[0]
            id_producto = int(rprod.lista_productos.get(index).split(" - ")[0])
            producto = rprod.productos[id_producto]

            rprod.entry_id.config(state="normal")
            rprod.entry_id.delete(0, tk.END)
            rprod.entry_id.insert(0, str(id_producto))
            rprod.entry_id.config(state="readonly")

            rprod.entry_nombre.delete(0, tk.END)
            rprod.entry_nombre.insert(0, producto["nombre"])

            rprod.entry_precio.delete(0, tk.END)
            rprod.entry_precio.insert(0, producto["precio"])

            rprod.entry_tipo.delete(0, tk.END)
            rprod.entry_tipo.insert(0, producto["tipo"])

            rprod.habilitar_modificar()

            rprod.bloquear_botones()

    def habilitar_modificar(rprod, event=None):
        if rprod.lista_productos.curselection() and rprod.entry_nombre.get() != "":
            rprod.producto_seleccionado = int(rprod.entry_id.get())
            rprod.btn_modificar.config(state="active")
            rprod.btn_eliminar.config(state="active")
        else:
            rprod.producto_seleccionado = None
            rprod.btn_modificar.config(state="disabled")
            rprod.btn_eliminar.config(state="disabled")
        rprod.bloquear_botones()

    def actualizar_lista_productos(rprod):
        rprod.lista_productos.delete(0, tk.END)

        for id_producto, producto_info in rprod.productos.items():
            rprod.lista_productos.insert(tk.END, f"{id_producto} - {producto_info['nombre']} - {producto_info['precio']:.2f}")

    def limpiar_campos_entrada(rprod):
        rprod.entry_id.config(state="normal")
        rprod.entry_id.delete(0, tk.END)
        rprod.entry_id.config(state="readonly")
        rprod.entry_nombre.delete(0, tk.END)
        rprod.entry_precio.delete(0, tk.END)
        rprod.entry_tipo.delete(0, tk.END)

    def volver(cproduct):
        cproduct.grab_release()
        cproduct.destroy()
        cproduct.master.deiconify()

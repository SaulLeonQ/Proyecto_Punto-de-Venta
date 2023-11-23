import tkinter as tk
from tkinter import ttk

class ConsultarProducto(tk.Toplevel):
    def __init__(cproduct, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cproduct.title("Consultar Producto")
        cproduct.geometry("450x320")
        cproduct.resizable(False, False)

        cproduct.productos = productos

        cproduct.entry_busqueda = ttk.Entry(cproduct, font=("DejaVu Sans", 12))
        cproduct.entry_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        cproduct.lista_productos = tk.Listbox(cproduct, font=("DejaVu Sans", 10), selectmode=tk.SINGLE, width=50)
        cproduct.lista_productos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Button(cproduct, text="Volver", command=cproduct.volver).grid(row=2, column=0, pady=10)

        scrollbar = ttk.Scrollbar(cproduct, orient="vertical", command=cproduct.lista_productos.yview)
        scrollbar.grid(row=1, column=0, sticky="nse")
        cproduct.lista_productos.config(yscrollcommand=scrollbar.set)

        cproduct.entry_busqueda.bind("<KeyRelease>", cproduct.actualizar_lista)

    def actualizar_lista(cproduct, event):
        busqueda = cproduct.entry_busqueda.get().lower()
        cproduct.lista_productos.delete(0, tk.END)

        for id_producto, producto_info in cproduct.productos.items():
            nombre = producto_info["nombre"].lower()
            if busqueda in nombre:
                cproduct.lista_productos.insert(tk.END, f"{nombre} - ${producto_info['precio']:.2f} - {producto_info['cantidad']}")

    def volver(cproduct):
        cproduct.grab_release()
        cproduct.destroy()
        cproduct.master.deiconify()
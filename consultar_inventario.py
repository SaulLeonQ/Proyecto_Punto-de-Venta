import tkinter as tk
from tkinter import ttk

class ConsultarInventario(tk.Toplevel):
    def __init__(conin, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conin.title("Consultar Inventario")
        conin.geometry("660x480")
        conin.resizable(False, False)

        conin.productos = productos

        conin.entry_busqueda = ttk.Entry(conin, font=("DejaVu Sans", 12))
        conin.entry_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        conin.tree = ttk.Treeview(conin, columns=("ID", "Nombre", "Cantidad"), show="headings", height=15)
        conin.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        conin.tree.heading("ID", text="ID", command=lambda: conin.sort_column("ID"))
        conin.tree.heading("Nombre", text="Nombre", command=lambda: conin.sort_column("Nombre"))
        conin.tree.heading("Cantidad", text="Cantidad", command=lambda: conin.sort_column("Cantidad"))

        ttk.Button(conin, text="Volver", command=conin.volver).grid(row=2, column=0, pady=10)

        scrollbar = ttk.Scrollbar(conin, orient="vertical", command=conin.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="nse")
        conin.tree.config(yscrollcommand=scrollbar.set)

        conin.entry_busqueda.bind("<KeyRelease>", conin.actualizar_lista)
        conin.actualizar_lista()

    def actualizar_lista(conin, event=None):
        busqueda = conin.entry_busqueda.get().lower()

        for item in conin.tree.get_children():
            conin.tree.delete(item)

        for id_producto, producto_info in conin.productos.items():
            nombre = producto_info["nombre"].lower()
            if busqueda in nombre:
                conin.tree.insert("", "end", values=(id_producto, producto_info["nombre"], producto_info["cantidad"]))

    def volver(conin):
        conin.grab_release()
        conin.destroy()
        conin.master.deiconify()

    def sort_column(conin, column):
        data = [(conin.tree.set(child, "ID"), conin.tree.set(child, "Nombre"), conin.tree.set(child, "Cantidad"))
                for child in conin.tree.get_children("")]
        
        if column == "ID":
            data.sort(key=lambda x: int(x[0]))
        elif column == "Nombre":
            data.sort(key=lambda x: x[1])
        elif column == "Cantidad":
            data.sort(key=lambda x: int(x[2]))

        for item in conin.tree.get_children():
            conin.tree.delete(item)

        for item in data:
            conin.tree.insert("", "end", values=item)

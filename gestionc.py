import tkinter as tk
from tkinter import ttk
from clientesdepruebaporquenuncavoyatenerbasededatos import clientes

class GestionC(tk.Toplevel):
    def __init__(gesc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gesc.title("Gestión de Clientes")
        gesc.geometry("400x330")
        gesc.resizable(False, False)
       
        ttk.Label(gesc, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        gesc.id_entry = ttk.Entry(gesc, state="disabled")
        gesc.id_entry.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        ttk.Label(gesc, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        gesc.nombre_entry = ttk.Entry(gesc, width=15)
        gesc.nombre_entry.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        gesc.agregar_btn = ttk.Button(gesc, text="Agregar", command=gesc.agregar_cliente)
        gesc.agregar_btn.grid(row=2, column=0, padx=5, pady=5)

        gesc.modificar_btn = ttk.Button(gesc, text="Modificar", command=gesc.modificar_cliente, state="disabled")
        gesc.modificar_btn.grid(row=3, column=0, padx=5, pady=5)

        gesc.eliminar_btn = ttk.Button(gesc, text="Eliminar", command=gesc.eliminar_cliente, state="disabled")
        gesc.eliminar_btn.grid(row=4, column=0, padx=5, pady=5)

        gesc.clientes_listbox = tk.Listbox(gesc, selectmode=tk.SINGLE)
        gesc.clientes_listbox.grid(row=0, column=3, columnspan=4, rowspan=6, pady=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(gesc, orient="vertical", command=gesc.clientes_listbox.yview)
        scrollbar.grid(row=0, column=6, rowspan=6, sticky="nse")
        gesc.clientes_listbox.config(yscrollcommand=scrollbar.set)
        gesc.clientes_listbox.bind("<<ListboxSelect>>", gesc.mostrar_datos_cliente)

        ttk.Button(gesc, text="Volver", command=gesc.volver).grid(row=5, column=0, pady=10)
        gesc.actualizar_lista_clientes()


    def agregar_cliente(gesc):
        ultimo_id = max(clientes.keys(), default=0)
        nuevo_id = ultimo_id + 1

        nuevo_cliente = {
            "id": nuevo_id,
            "nombre": gesc.nombre_entry.get()
        }
        clientes[nuevo_cliente["id"]] = nuevo_cliente
        gesc.actualizar_lista_clientes()
        gesc.limpiar_campos()


    def modificar_cliente(gesc):
        cliente_id = int(gesc.id_entry.get().split(":")[0])
        clientes[cliente_id]["nombre"] = gesc.nombre_entry.get()
        gesc.actualizar_lista_clientes()
        gesc.limpiar_campos()


    def eliminar_cliente(gesc):
        cliente_id = int(gesc.id_entry.get().split(":")[0])
        del clientes[cliente_id]
        gesc.actualizar_lista_clientes()
        gesc.limpiar_campos()

    def mostrar_datos_cliente(gesc, event):
        seleccion = gesc.clientes_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            cliente_seleccionado = gesc.clientes_listbox.get(index)
            cliente_id, cliente_nombre = cliente_seleccionado.split(":")
            gesc.id_entry.config(state="normal")
            gesc.id_entry.delete(0, tk.END)
            gesc.id_entry.insert(0, cliente_id)
            gesc.id_entry.config(state="disabled")
            gesc.nombre_entry.delete(0, tk.END)
            gesc.nombre_entry.insert(0, cliente_nombre.strip())
            gesc.modificar_btn.config(state="normal")
            gesc.eliminar_btn.config(state="normal")
            gesc.agregar_btn.config(state="disabled")

    def actualizar_lista_clientes(gesc):
        gesc.clientes_listbox.delete(0, tk.END)
        for cliente_id, cliente_data in clientes.items():
            gesc.clientes_listbox.insert(tk.END, f"{cliente_id}: {cliente_data['nombre']}")

    def limpiar_campos(gesc):
        gesc.id_entry.config(state="normal")
        gesc.id_entry.delete(0, tk.END)
        gesc.id_entry.config(state="disabled")
        gesc.nombre_entry.delete(0, tk.END)
        gesc.modificar_btn.config(state="disabled")
        gesc.eliminar_btn.config(state="disabled")
        gesc.agregar_btn.config(state="normal")

    def volver(gesc):
        gesc.grab_release()
        gesc.destroy()
        gesc.master.deiconify()

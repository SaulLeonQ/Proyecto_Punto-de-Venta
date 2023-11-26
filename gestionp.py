import tkinter as tk
from tkinter import ttk
from proveedoresdepruebaporquechenuncavaahacerlabasededatos import proveedores

class GestionP(tk.Toplevel):
    def __init__(gesp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gesp.title("Gestión de Proveedores")
        gesp.geometry("520x370")
        gesp.resizable(False, False)

        ttk.Label(gesp, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        gesp.id_entry = ttk.Entry(gesp, state="disabled")
        gesp.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(gesp, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        gesp.nombre_entry = ttk.Entry(gesp, width=15)
        gesp.nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(gesp, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        gesp.telefono_entry = ttk.Entry(gesp, width=15)
        gesp.telefono_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        gesp.agregar_btn = ttk.Button(gesp, text="Agregar", command=gesp.agregar_proveedor)
        gesp.agregar_btn.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        gesp.modificar_btn = ttk.Button(gesp, text="Modificar", command=gesp.modificar_proveedor, state="disabled")
        gesp.modificar_btn.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        gesp.eliminar_btn = ttk.Button(gesp, text="Eliminar", command=gesp.eliminar_proveedor, state="disabled")
        gesp.eliminar_btn.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        gesp.proveedores_listbox = tk.Listbox(gesp, selectmode=tk.SINGLE, width=30)
        gesp.proveedores_listbox.grid(row=0, column=3, columnspan=4, rowspan=8, pady=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(gesp, orient="vertical", command=gesp.proveedores_listbox.yview)
        scrollbar.grid(row=0, column=7, rowspan=8, sticky="nse")
        gesp.proveedores_listbox.config(yscrollcommand=scrollbar.set)
        gesp.proveedores_listbox.bind("<<ListboxSelect>>", gesp.mostrar_datos_proveedor)

        ttk.Button(gesp, text="Volver", command=gesp.volver).grid(row=7, column=0, pady=10, columnspan=2)
        gesp.actualizar_lista_proveedores()

    def agregar_proveedor(gesp):
        ultimo_id = max(proveedores.keys(), default=0)
        nuevo_id = ultimo_id + 1

        nuevo_proveedor = {
            "id": nuevo_id,
            "nombre": gesp.nombre_entry.get(),
            "telefono": gesp.telefono_entry.get()
        }
        proveedores[nuevo_proveedor["id"]] = nuevo_proveedor
        gesp.actualizar_lista_proveedores()
        gesp.limpiar_campos()

    def modificar_proveedor(gesp):
        proveedor_id = int(gesp.id_entry.get())
        proveedores[proveedor_id]["nombre"] = gesp.nombre_entry.get()
        proveedores[proveedor_id]["telefono"] = gesp.telefono_entry.get()
        gesp.actualizar_lista_proveedores()
        gesp.limpiar_campos()

    def eliminar_proveedor(gesp):
        proveedor_id = int(gesp.id_entry.get())
        del proveedores[proveedor_id]
        gesp.actualizar_lista_proveedores()
        gesp.limpiar_campos()

    def mostrar_datos_proveedor(gesp, event):
        seleccion = gesp.proveedores_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            proveedor_seleccionado = gesp.proveedores_listbox.get(index)
            proveedor_info = proveedor_seleccionado.split(":")
            proveedor_id = proveedor_info[0].strip()
            gesp.id_entry.config(state="normal")
            gesp.id_entry.delete(0, tk.END)
            gesp.id_entry.insert(0, proveedor_id)
            gesp.id_entry.config(state="disabled")
            if len(proveedor_info) > 1:
                rest = ':'.join(proveedor_info[1:]).strip().split(":")
                proveedor_nombre = rest[0].strip()
                proveedor_telefono = rest[1].strip() if len(rest) > 1 else ""
                gesp.nombre_entry.delete(0, tk.END)
                gesp.nombre_entry.insert(0, proveedor_nombre)
                gesp.telefono_entry.delete(0, tk.END)
                gesp.telefono_entry.insert(0, proveedor_telefono)
            else:
                gesp.nombre_entry.delete(0, tk.END)
                gesp.telefono_entry.delete(0, tk.END)
            gesp.modificar_btn.config(state="normal")
            gesp.eliminar_btn.config(state="normal")
            gesp.agregar_btn.config(state="disabled")

    def actualizar_lista_proveedores(gesp):
        gesp.proveedores_listbox.delete(0, tk.END)
        for proveedor_id, proveedor_data in proveedores.items():
            gesp.proveedores_listbox.insert(tk.END, f"{proveedor_id}: {proveedor_data['nombre']} : {proveedor_data['telefono']}")

    def limpiar_campos(gesp):
        gesp.id_entry.config(state="normal")
        gesp.id_entry.delete(0, tk.END)
        gesp.id_entry.config(state="disabled")
        gesp.nombre_entry.delete(0, tk.END)
        gesp.telefono_entry.delete(0, tk.END)
        gesp.modificar_btn.config(state="disabled")
        gesp.eliminar_btn.config(state="disabled")
        gesp.agregar_btn.config(state="normal")

    def volver(gesp):
        gesp.grab_release()
        gesp.destroy()
        gesp.master.deiconify()


import tkinter as tk
from tkinter import ttk, messagebox
from usuariosdepruebaporquenotengobasededatos import usuarios

class GestionU(tk.Toplevel):
    def __init__(gesu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gesu.title("Gestión de Usuarios")
        gesu.geometry("540x420")
        gesu.resizable(False, False)

        ttk.Label(gesu, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        gesu.id_entry = ttk.Entry(gesu, state="disabled")
        gesu.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(gesu, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        gesu.nombre_entry = ttk.Entry(gesu, width=15)
        gesu.nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(gesu, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        gesu.contraseña_entry = ttk.Entry(gesu, show="*", width=15)
        gesu.contraseña_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(gesu, text="Confirmar Contraseña:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        gesu.confirmar_contraseña_entry = ttk.Entry(gesu, show="*", width=15)
        gesu.confirmar_contraseña_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        gesu.agregar_btn = ttk.Button(gesu, text="Agregar", command=gesu.agregar_usuario)
        gesu.agregar_btn.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        gesu.modificar_btn = ttk.Button(gesu, text="Modificar", command=gesu.modificar_usuario, state="disabled")
        gesu.modificar_btn.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        gesu.eliminar_btn = ttk.Button(gesu, text="Eliminar", command=gesu.eliminar_usuario, state="disabled")
        gesu.eliminar_btn.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        gesu.usuarios_listbox = tk.Listbox(gesu, selectmode=tk.SINGLE, width=20)
        gesu.usuarios_listbox.grid(row=0, column=3, columnspan=4, rowspan=8, pady=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(gesu, orient="vertical", command=gesu.usuarios_listbox.yview)
        scrollbar.grid(row=0, column=7, rowspan=8, sticky="nse")
        gesu.usuarios_listbox.config(yscrollcommand=scrollbar.set)
        gesu.usuarios_listbox.bind("<<ListboxSelect>>", gesu.mostrar_datos_usuario)

        ttk.Button(gesu, text="Volver", command=gesu.volver).grid(row=7, column=0, pady=10, columnspan=2)
        gesu.actualizar_lista_usuarios()

    def agregar_usuario(gesu):
        if gesu.contraseña_entry.get() != gesu.confirmar_contraseña_entry.get():
            messagebox.showwarning("Error", "Las contraseñas no coinciden. Por favor, inténtelo de nuevo.")
            return

        ultimo_id = max([usuario["ID"] for usuario in usuarios], default=0)
        nuevo_id = ultimo_id + 1

        nuevo_usuario = {
            "ID": nuevo_id,
            "nombre": gesu.nombre_entry.get(),
            "contraseña": gesu.contraseña_entry.get(),
            "tipo": "vendedor"
        }
        usuarios.append(nuevo_usuario)
        gesu.actualizar_lista_usuarios()
        gesu.limpiar_campos()

    def modificar_usuario(gesu):
        usuario_id = int(gesu.id_entry.get())
        for usuario in usuarios:
            if usuario["ID"] == usuario_id:
                usuario["nombre"] = gesu.nombre_entry.get()
                usuario["contraseña"] = gesu.contraseña_entry.get()
                break
        gesu.actualizar_lista_usuarios()
        gesu.limpiar_campos()

    def eliminar_usuario(gesu):
        usuario_id = int(gesu.id_entry.get())
        usuario_tipo = next((usuario["tipo"] for usuario in usuarios if usuario["ID"] == usuario_id), None)

        if usuario_tipo == "administrador":
            messagebox.showwarning("Error", "No se puede eliminar a un usuario administrador.")
        else:
            usuarios[:] = [usuario for usuario in usuarios if usuario["ID"] != usuario_id]
            gesu.actualizar_lista_usuarios()
            gesu.limpiar_campos()

    def mostrar_datos_usuario(gesu, event):
        seleccion = gesu.usuarios_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            usuario_seleccionado = gesu.usuarios_listbox.get(index)
            usuario_info = usuario_seleccionado.split(":")
            usuario_id = int(usuario_info[0].strip())
            gesu.id_entry.config(state="normal")
            gesu.id_entry.delete(0, tk.END)
            gesu.id_entry.insert(0, usuario_id)
            gesu.id_entry.config(state="disabled")
            if len(usuario_info) > 1:
                rest = ':'.join(usuario_info[1:]).strip().split(":")
                usuario_nombre = rest[0].strip()
                usuario_contraseña = rest[1].strip() if len(rest) > 1 else ""
                gesu.nombre_entry.delete(0, tk.END)
                gesu.nombre_entry.insert(0, usuario_nombre)
                gesu.contraseña_entry.delete(0, tk.END)
                gesu.contraseña_entry.insert(0, usuario_contraseña)
                gesu.confirmar_contraseña_entry.delete(0, tk.END)
                gesu.confirmar_contraseña_entry.insert(0, usuario_contraseña)
            else:
                gesu.nombre_entry.delete(0, tk.END)
                gesu.contraseña_entry.delete(0, tk.END)
                gesu.confirmar_contraseña_entry.delete(0, tk.END)
            gesu.modificar_btn.config(state="normal")
            gesu.eliminar_btn.config(state="normal")
            gesu.agregar_btn.config(state="disabled")

    def actualizar_lista_usuarios(gesu):
        gesu.usuarios_listbox.delete(0, tk.END)
        for usuario in usuarios:
            gesu.usuarios_listbox.insert(tk.END, f"{usuario['ID']}: {usuario['nombre']}")

    def limpiar_campos(gesu):
        gesu.id_entry.config(state="normal")
        gesu.id_entry.delete(0, tk.END)
        gesu.id_entry.config(state="disabled")
        gesu.nombre_entry.delete(0, tk.END)
        gesu.contraseña_entry.delete(0, tk.END)
        gesu.confirmar_contraseña_entry.delete(0, tk.END)
        gesu.modificar_btn.config(state="disabled")
        gesu.eliminar_btn.config(state="disabled")
        gesu.agregar_btn.config(state="normal")

    def volver(gesu):
        gesu.grab_release()
        gesu.destroy()
        gesu.master.deiconify()
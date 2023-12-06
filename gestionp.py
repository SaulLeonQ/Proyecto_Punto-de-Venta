import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

db_parametros = {
    'dbname': 'posbd',
    'user': 'electrogalgos',
    'password': 'tengomiedo',
    'host': 'projectparra.cyhwcmck3mea.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
class GestionP(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gestión de Proveedores")
        self.geometry("735x420")
        self.resizable(False, False)

        ttk.Label(self, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = ttk.Entry(self, state="disabled")
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(self, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.nombre_entry = ttk.Entry(self, width=15)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        ttk.Label(self, text="Contacto:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.contacto_entry = ttk.Entry(self, width=15)
        self.contacto_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")


        ttk.Label(self, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.telefono_entry = ttk.Entry(self, width=15)
        self.telefono_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        self.agregar_btn = ttk.Button(self, text="Agregar", command=self.agregar_proveedor)
        self.agregar_btn.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.modificar_btn = ttk.Button(self, text="Modificar", command=self.modificar_proveedor, state="disabled")
        self.modificar_btn.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        self.eliminar_btn = ttk.Button(self, text="Eliminar", command=self.eliminar_proveedor, state="disabled")
        self.eliminar_btn.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        self.proveedores_listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=55)
        self.proveedores_listbox.grid(row=0, column=3, columnspan=4, rowspan=8, pady=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.proveedores_listbox.yview)
        scrollbar.grid(row=0, column=7, rowspan=8, sticky="nse")
        self.proveedores_listbox.config(yscrollcommand=scrollbar.set)
        self.proveedores_listbox.bind("<<ListboxSelect>>", self.mostrar_datos_proveedor)

        ttk.Button(self, text="Volver", command=self.volver).grid(row=7, column=0, pady=10, columnspan=2)
        self.actualizar_lista_proveedores()

    def agregar_proveedor(self):
        nombre = self.nombre_entry.get()
        contacto = self.contacto_entry.get()
        telefono = self.telefono_entry.get()  # Obtener el texto del Entry
        self.telefono_entry.delete(0, tk.END)

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            # Insertar en la base de datos
            cursor.execute("INSERT INTO proveedores (proveedor_nombre, proveedor_contacto, proveedor_telefono) VALUES (%s,%s,%s) RETURNING proveedor_id",
                           (nombre, contacto, telefono))
            proveedor_id = cursor.fetchone()[0]
            connection.commit()

            self.actualizar_lista_proveedores()
            self.limpiar_campos()
            self.mostrar_mensaje("Proveedor agregado con ID: {}".format(proveedor_id))

        except psycopg2.Error as e:
            print("Error al agregar proveedor:", e)

        finally:
            if connection:
                connection.close()
            
    def modificar_proveedor(self):
        proveedor_id = self.id_entry.get()
        nombre = self.nombre_entry.get()
        contacto = self.contacto_entry.get()
        telefono = self.telefono_entry.get()

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            cursor.execute("UPDATE proveedores SET proveedor_nombre = %s,proveedor_contacto = %s, proveedor_telefono = %s WHERE proveedor_id = %s",
                           (nombre, contacto, telefono, proveedor_id))

            connection.commit()

            self.actualizar_lista_proveedores()
            self.limpiar_campos()
            self.mostrar_mensaje("Proveedor modificado")

        except psycopg2.Error as e:
            print("Error al modificar proveedor:", e)
        
    def eliminar_proveedor(self):
        proveedor_id = self.id_entry.get()

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            cursor.execute("DELETE FROM proveedores WHERE proveedor_id = %s", (proveedor_id,))

            connection.commit()

            self.actualizar_lista_proveedores()
            self.limpiar_campos()
            self.mostrar_mensaje("Proveedor eliminado")

        except psycopg2.Error as e:
            print("Error al eliminar proveedor:", e)

        finally:
            if connection:
                connection.close()
       
    def mostrar_datos_proveedor(self, event):
     try:
        seleccionado = self.proveedores_listbox.curselection()

        if seleccionado:
            # Obtener el proveedor seleccionado
            proveedor_seleccionado = self.proveedores_listbox.get(seleccionado)

            # Dividir la información del proveedor
            partes = proveedor_seleccionado.split(", ")
            
            # Extraer los valores de las partes
            id_proveedor = partes[0].split(": ")[1]
            nombre = partes[1].split(": ")[1]
            contacto = partes[2].split(": ")[1]
            telefono = partes[3].split(": ")[1]

            # Actualizar las cajas de texto
            self.id_entry.config(state="normal")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, id_proveedor)
            self.id_entry.config(state="disabled")
            
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, nombre)
            
            self.contacto_entry.delete(0, tk.END)
            self.contacto_entry.insert(0, contacto)
            
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, telefono)

            # Habilitar los botones de modificar y eliminar
            self.modificar_btn.config(state="normal")
            self.eliminar_btn.config(state="normal")
            self.agregar_btn.config(state="disabled")

     except Exception as e:
        print("Error al obtener datos del proveedor:", e)

     finally:
        # Siempre cerrar la conexión después de usarla
        if 'connection' in locals() and connection:
            connection.close()

       
    def actualizar_lista_proveedores(self):
     def obtener_proveedores():
        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            # Consultar todos los datos de proveedores
            cursor.execute("SELECT * FROM proveedores")
            return cursor.fetchall()

        except psycopg2.Error as e:
            print("Error al obtener proveedores:", e)
            return None

        finally:
            if connection:
                connection.close()
     self.proveedores_listbox.delete(0, tk.END)
     proveedores = obtener_proveedores()
     if proveedores:
        for proveedor in proveedores:
            info_proveedor = f"ID: {proveedor[0]}, Nombre: {proveedor[1]}, Contacto: {proveedor[2]}, Teléfono: {proveedor[3]}"
            self.proveedores_listbox.insert(tk.END, info_proveedor)


    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Mensaje", mensaje)   

    def limpiar_campos(gesp):
        gesp.id_entry.config(state="normal")
        gesp.id_entry.delete(0, tk.END)
        gesp.id_entry.config(state="disabled")
        gesp.nombre_entry.delete(0, tk.END)
        gesp.telefono_entry.delete(0, tk.END)
        gesp.contacto_entry.delete(0, tk.END)
        gesp.modificar_btn.config(state="disabled")
        gesp.eliminar_btn.config(state="disabled")
        gesp.agregar_btn.config(state="normal")

    def volver(gesp):
        gesp.grab_release()
        gesp.destroy()
        gesp.master.deiconify()


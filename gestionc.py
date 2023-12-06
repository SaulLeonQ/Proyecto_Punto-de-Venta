import tkinter as tk
from tkinter import ttk, messagebox
from clientesdepruebaporquenuncavoyatenerbasededatos import clientes
import psycopg2

db_parametros = {
    'dbname': 'posbd',
    'user': 'electrogalgos',
    'password': 'tengomiedo',
    'host': 'projectparra.cyhwcmck3mea.us-east-2.rds.amazonaws.com',
    'port': '5432',
}

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
        nombre_cliente = gesc.nombre_entry.get()

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            cursor.execute("INSERT INTO cliente (cliente_nombre) VALUES (%s) RETURNING cliente_id;", (nombre_cliente,))
            nuevo_id = cursor.fetchone()[0]

            connection.commit()

            gesc.actualizar_lista_clientes()
            gesc.limpiar_campos()
            gesc.mostrar_mensaje("Cliente agregado con ID: {}".format(nuevo_id))


        except psycopg2.Error as e:
            print("Error al agregar cliente:", e)
        finally:
            if connection:
                connection.close()


    def modificar_cliente(gesc):
        cliente_id = gesc.id_entry.get()
        nombre_cliente = gesc.nombre_entry.get()

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            cursor.execute("UPDATE cliente SET cliente_nombre = %s WHERE cliente_id = %s;", (nombre_cliente, cliente_id))
            connection.commit()
            gesc.actualizar_lista_clientes()
            gesc.limpiar_campos()
            gesc.mostrar_mensaje("Cliente modificado")

        except psycopg2.Error as e:
            print("Error al modificar cliente:", e)
        finally:
            if connection:
                connection.close()


    def eliminar_cliente(gesc):
        cliente_id = gesc.id_entry.get()

        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            cursor.execute("DELETE FROM cliente WHERE cliente_id = %s", (cliente_id,))

            connection.commit()

            gesc.actualizar_lista_clientes()
            gesc.limpiar_campos()
            gesc.mostrar_mensaje("Cliente eliminado")

        except psycopg2.Error as e:
            print("Error al eliminar cliente:", e)

        finally:
            if connection:
                connection.close()

    def mostrar_datos_cliente(gesc, event):
     try:
        seleccionado = gesc.clientes_listbox.curselection()

        if seleccionado:
            # Obtener el proveedor seleccionado
            proveedor_seleccionado = gesc.clientes_listbox.get(seleccionado)

            # Dividir la información del proveedor
            partes = proveedor_seleccionado.split(", ")
            
            # Extraer los valores de las partes
            cliente_id = partes[0].split(": ")[1]
            cliente_nombre = partes[1].split(": ")[1]

            # Actualizar las cajas de texto
            gesc.id_entry.config(state="normal")
            gesc.id_entry.delete(0, tk.END)
            gesc.id_entry.insert(0, cliente_id)
            gesc.id_entry.config(state="disabled")
            
            gesc.nombre_entry.delete(0, tk.END)
            gesc.nombre_entry.insert(0, cliente_nombre)

            # Habilitar los botones de modificar y eliminar
            gesc.modificar_btn.config(state="normal")
            gesc.eliminar_btn.config(state="normal")
            gesc.agregar_btn.config(state="disabled")

     except Exception as e:
        print("Error al obtener datos del proveedor:", e)

     finally:
        # Siempre cerrar la conexión después de usarla
        if 'connection' in locals() and connection:
            connection.close()

    def actualizar_lista_clientes(gesc):
     def obtener_clientes():
        try:
            connection = psycopg2.connect(**db_parametros)
            cursor = connection.cursor()

            # Consultar todos los datos de proveedores
            cursor.execute("SELECT * FROM cliente")
            return cursor.fetchall()

        except psycopg2.Error as e:
            print("Error al obtener cliente:", e)
            return None

        finally:
            if connection:
                connection.close()
     gesc.clientes_listbox.delete(0, tk.END)
     clientes = obtener_clientes()
     if clientes:
        for clientes in clientes:
            info_cliente = f"ID: {clientes[0]}, Nombre: {clientes[1]}"
            gesc.clientes_listbox.insert(tk.END, info_cliente)

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

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Mensaje", mensaje)  

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from datetime import datetime
from registrosdecomprasporquenotengobasededatos import registros_compras
from registrosdeventasporqueelchenuncavaahacerlabasededatosmellevalaverga import registros_ventas
from clientesdepruebaporquenuncavoyatenerbasededatos import clientes
from proveedoresdepruebaporquechenuncavaahacerlabasededatos import proveedores

class Reportes(tk.Toplevel):
    def __init__(vrep, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vrep.title("Registros")
        vrep.geometry("730x430")
        vrep.resizable(False, False)
        style = ThemedStyle(vrep)
        style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=18,font=("DejaVu Sans",12))
        style.configure('FrameA.TFrame',background="#f2f2f2")
        style.configure('LabelQ.TLabel',background="#f2f2f2")
        vrep.productos = productos
        vrep.proveedores = proveedores

        vrep.frame = ttk.Frame(vrep,width=220,height=160, style="FrameA.TFrame")
        vrep.frame.place(x=504,y=0)
        vrep.frame.configure()
        
        btn_volver = ttk.Button(vrep, text="Volver", command=vrep.volver)
        btn_registros_compras = ttk.Button(vrep, text="Registros de Compras", command=vrep.mostrar_registros_compras)
        btn_registros_ventas = ttk.Button(vrep, text="Registros de Ventas", command=vrep.mostrar_registros_ventas)
        
    
        vrep.tabla_inferior = ttk.Treeview(vrep, columns=("ID", "Fecha", "Producto", "Proveedor", "Cantidad", "Total"))
        vrep.tabla_inferior.heading("#0", text="ID", anchor=tk.W)
        vrep.tabla_inferior.column("#0", width=0, stretch=tk.NO)
        vrep.tabla_inferior.heading("ID", text="ID")
        vrep.tabla_inferior.column("ID", width=25, minwidth=25, stretch=tk.NO)
        vrep.tabla_inferior.heading("Fecha", text="Fecha", command=lambda: vrep.column_sort("Fecha", False))
        vrep.tabla_inferior.column("Fecha", width=150, minwidth=150, stretch=tk.NO)
        vrep.tabla_inferior.heading("Producto", text="Producto", command=lambda: vrep.column_sort("Producto", False))
        vrep.tabla_inferior.column("Producto", width=150, minwidth=150, stretch=tk.NO)
        vrep.tabla_inferior.heading("Proveedor", text="Proveedor", command=lambda: vrep.column_sort("Proveedor", False))
        vrep.tabla_inferior.column("Proveedor", width=150, minwidth=150, stretch=tk.NO)
        vrep.tabla_inferior.heading("Cantidad", text="Cantidad", command=lambda: vrep.column_sort("Cantidad", False))
        vrep.tabla_inferior.column("Cantidad", width=125, minwidth=125, stretch=tk.NO)
        vrep.tabla_inferior.heading("Total", text="Total", command=lambda: vrep.column_sort("Total", False))
        vrep.tabla_inferior.column("Total", width=100, minwidth=100, stretch=tk.NO)
        for col in vrep.tabla_inferior["columns"]:
            vrep.tabla_inferior.heading(col, text=col, anchor=tk.W)
            vrep.tabla_inferior.column(col, anchor=tk.W, width=vrep.tabla_inferior.column(col, "width"))
            vrep.tabla_inferior.heading(col, command=lambda c=col: vrep.column_sort(c, False))
            vrep.tabla_inferior.heading(col, text=col, anchor=tk.W)
            vrep.tabla_inferior.heading(col, command=lambda c=col: vrep.column_sort(c, False))
            vrep.tabla_inferior.bind("<B1-Motion>", lambda event: "break")


        vrep.label_reporte = ttk.Label(vrep, text="Reporte del día",style="LabelQ.TLabel")
        vrep.label_ventas_brutas = ttk.Label(vrep, text="Ventas brutas: ",style="LabelQ.TLabel")
        vrep.label_compras_brutas = ttk.Label(vrep, text="Compras brutas: ",style="LabelQ.TLabel")
        vrep.label_total = ttk.Label(vrep, text="Total: ",style="LabelQ.TLabel")
        vrep.label_ventas_totales = ttk.Label(vrep, text="Ventas totales: ",style="LabelQ.TLabel")
        vrep.label_compras_totales = ttk.Label(vrep, text="Compras totales: ",style="LabelQ.TLabel")

        btn_volver.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        btn_registros_compras.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        btn_registros_ventas.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        vrep.tabla_inferior.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        vrep.scrollbar_vertical = ttk.Scrollbar(vrep, command=vrep.tabla_inferior.yview)
        vrep.scrollbar_vertical.grid(row=5, column=3, sticky='nse')
        vrep.tabla_inferior.configure(yscrollcommand=vrep.scrollbar_vertical.set)

        vrep.label_reporte.place(x=572,y=10)
        vrep.label_ventas_brutas.place(x=529,y=40)
        vrep.label_compras_brutas.place(x=516,y=60)
        vrep.label_total.place(x=586,y=80)
        vrep.label_ventas_totales.place(x=525,y=100)
        vrep.label_compras_totales.place(x=512,y=120)

        vrep.ventas_brutas, vrep.compras_brutas, vrep.ventas_totales, vrep.compras_totales = vrep.calcular_totales()
        vrep.actualizar_etiquetas_totales()

    def volver(vrep):
        style = ThemedStyle(vrep)
        style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=12,font=("DejaVu Sans",20))
        vrep.grab_release()
        vrep.destroy()
        vrep.master.deiconify()

    def mostrar_registros_compras(vrep):
        vrep.limpiar_tabla(vrep.tabla_inferior)

        vrep.cambiar_encabezados_tabla_inferior(["ID", "Fecha", "Producto", "Proveedor", "Cantidad", "Total"])
        for compra in registros_compras:
            id_venta = compra.get("Id_Venta", "")
            fecha = compra.get("fecha", "")
            id_producto = compra.get("id_producto", "")
            id_proveedor = compra.get("id_proveedor", "")
            cantidad = compra.get("cantidad", "")
            total = compra.get("total", "")

            nombre_producto = vrep.productos.get(id_producto, {}).get("nombre", f"Producto {id_producto}")
            nombre_proveedor = vrep.proveedores.get(id_proveedor, {}).get("nombre", f"Proveedor {id_proveedor}")

            vrep.tabla_inferior.insert("", tk.END, values=(id_venta, fecha, nombre_producto, nombre_proveedor, cantidad, total))

    def mostrar_registros_ventas(vrep):
        vrep.limpiar_tabla(vrep.tabla_inferior)

        vrep.cambiar_encabezados_tabla_inferior(["ID", "Fecha", "Producto", "Cliente", "Cantidad", "Total"])
        for venta in registros_ventas:
            id_venta = venta.get("Id_Venta", "")
            fecha = venta.get("fecha", "")
            id_producto = venta.get("id_producto", "")
            id_cliente = venta.get("id_cliente", "")
            cantidad = venta.get("cantidad", "")
            total = venta.get("total", "")

            nombre_producto = vrep.productos.get(id_producto, {}).get("nombre", f"Producto {id_producto}")
            nombre_cliente = clientes.get(id_cliente, {}).get("nombre", f"Cliente {id_cliente}")

            vrep.tabla_inferior.insert("", tk.END, values=(id_venta, fecha, nombre_producto, nombre_cliente, cantidad, total))


    def limpiar_tabla(vrep, tabla):
        for item in tabla.get_children():
            tabla.delete(item)


    def cambiar_encabezados_tabla_inferior(vrep, encabezados):
        for col in vrep.tabla_inferior["columns"]:
            vrep.tabla_inferior.heading(col, text="", anchor=tk.W)

        for i, encabezado in enumerate(encabezados):
            vrep.tabla_inferior.heading(vrep.tabla_inferior["columns"][i], text=encabezado, anchor=tk.W)

    def column_sort(vrep, col, reverse):
        items = [(vrep.tabla_inferior.set(k, col), k) for k in vrep.tabla_inferior.get_children("")]
        
        if col == "Fecha":
            items = [(vrep.convertir_fecha(vrep.tabla_inferior.set(k, col)), k) for k in vrep.tabla_inferior.get_children("")]
            items.sort(reverse=not reverse)
        else:
            items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            vrep.tabla_inferior.move(k, "", index)

    def convertir_fecha(vrep, fecha_str):
        return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    
    def calcular_totales(vrep):
        fecha_actual = datetime.now().date()

        ventas_brutas = 0
        compras_brutas = 0
        ventas_totales = set()
        compras_totales = set()

        for venta in registros_ventas:
            fecha_venta = datetime.strptime(venta.get("fecha", ""), "%Y-%m-%d %H:%M:%S").date()
            if fecha_venta == fecha_actual:
                ventas_brutas += float(venta.get("total", ""))
                ventas_totales.add(venta.get("Id_Venta", ""))

        for compra in registros_compras:
            fecha_compra = datetime.strptime(compra.get("fecha", ""), "%Y-%m-%d %H:%M:%S").date()
            if fecha_compra == fecha_actual:
                compras_brutas += float(compra.get("total", ""))
                compras_totales.add(compra.get("Id_Venta", ""))

        total = ventas_brutas - compras_brutas

        return ventas_brutas, compras_brutas, len(ventas_totales), len(compras_totales)

    def actualizar_etiquetas_totales(vrep):
        vrep.label_ventas_brutas["text"] = f"Ventas brutas: {vrep.ventas_brutas}"
        vrep.label_compras_brutas["text"] = f"Compras brutas: {vrep.compras_brutas}"
        vrep.label_total["text"] = f"Total: {vrep.ventas_brutas - vrep.compras_brutas}"
        vrep.label_ventas_totales["text"] = f"Ventas totales: {vrep.ventas_totales}"
        vrep.label_compras_totales["text"] = f"Compras totales: {vrep.compras_totales}"

    def limpiar_tabla(vrep, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cambiar_encabezados_tabla_inferior(vrep, encabezados):
        for col in vrep.tabla_inferior["columns"]:
            vrep.tabla_inferior.heading(col, text="", anchor=tk.W)

        for i, encabezado in enumerate(encabezados):
            vrep.tabla_inferior.heading(vrep.tabla_inferior["columns"][i], text=encabezado, anchor=tk.W)



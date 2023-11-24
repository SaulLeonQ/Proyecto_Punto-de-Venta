import tkinter as tk
from tkinter import ttk
from datetime import datetime
from registrosdecomprasporquenotengobasededatos import registros_compras
from proveedoresdepruebaporquechenuncavaahacerlabasededatos import proveedores

class RestablecerInventario(tk.Toplevel):
    def __init__(rinv, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rinv.title("Restablecer Inventario")
        rinv.geometry("300x400")
        rinv.resizable(False, False)

        rinv.productos = productos
        rinv.proveedores = proveedores

        rinv.fecha_var = tk.StringVar()
        rinv.producto_var = tk.StringVar()
        rinv.proveedor_var = tk.StringVar()
        rinv.cantidad_var = tk.StringVar()
        rinv.total_var = tk.StringVar()

        rinv.configurar_interfaz()

    def configurar_interfaz(rinv):
        lbl_fecha = tk.Label(rinv, text="Fecha:")
        lbl_fecha.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_fecha = ttk.Entry(rinv, textvariable=rinv.fecha_var, state="readonly")
        entry_fecha.grid(row=0, column=1, padx=10, pady=10)
        rinv.fecha_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        lbl_producto = tk.Label(rinv, text="Producto:")
        lbl_producto.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        rinv.combo_producto = ttk.Combobox(rinv, textvariable=rinv.producto_var, state="readonly")
        rinv.combo_producto.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        rinv.combo_producto.bind("<<ComboboxSelected>>", rinv.seleccionar_producto)

        lbl_proveedor = tk.Label(rinv, text="Proveedor:")
        lbl_proveedor.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_proveedor = ttk.Entry(rinv, textvariable=rinv.proveedor_var, state="readonly")
        entry_proveedor.grid(row=2, column=1, padx=10, pady=10)

        lbl_cantidad = tk.Label(rinv, text="Cantidad:")
        lbl_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_cantidad = ttk.Entry(rinv, textvariable=rinv.cantidad_var)
        entry_cantidad.grid(row=3, column=1, padx=10, pady=10)

        lbl_total = tk.Label(rinv, text="Total:")
        lbl_total.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_total = ttk.Entry(rinv, textvariable=rinv.total_var)
        entry_total.grid(row=4, column=1, padx=10, pady=10)

        btn_confirmar = ttk.Button(rinv, text="Confirmar", command=rinv.confirmar)
        btn_confirmar.grid(row=5, column=0, columnspan=2, pady=10)

        btn_volver = ttk.Button(rinv, text="Volver", command=rinv.volver)
        btn_volver.grid(row=6, column=0, columnspan=2, pady=10)

        rinv.lista_productos = [(f"{id_producto} - {producto['nombre']}") for id_producto, producto in rinv.productos.items()]
        rinv.combo_producto["values"] = rinv.lista_productos

    def seleccionar_producto(rinv, event):
        selected_product_id = int(rinv.combo_producto.get().split(" - ")[0])
        rinv.producto_var.set(selected_product_id)
    
        proveedor_id = rinv.productos[selected_product_id]["proveedor"]

        proveedor_nombre = next((proveedor["nombre"] for proveedor in rinv.proveedores.values() if proveedor["id"] == proveedor_id), "")

        rinv.proveedor_var.set(proveedor_nombre)

        rinv.selected_proveedor_id = proveedor_id

    def confirmar(rinv):
        try:
            cantidad = int(rinv.cantidad_var.get())
            total = float(rinv.total_var.get())
            id_producto = int(rinv.producto_var.get())
            id_proveedor = rinv.selected_proveedor_id
        except ValueError:
            tk.messagebox.showerror("Error", "La cantidad y el total deben ser números.")
            return

        if id_producto not in rinv.productos:
            tk.messagebox.showerror("Error", "Producto no encontrado.")
            return
        
        id_venta = len(registros_compras) + 1

        rinv.productos[id_producto]["cantidad"] += cantidad

        registro = {
            "Id_Venta": id_venta,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id_producto": id_producto,
            "id_proveedor": id_proveedor,
            "cantidad": cantidad,
            "total": total
        }
        registros_compras.append(registro)

        rinv.producto_var.set("")
        rinv.proveedor_var.set("")
        rinv.cantidad_var.set("")
        rinv.total_var.set("")
    
        rinv.fecha_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def volver(rinv):
        rinv.grab_release()
        rinv.destroy()
        rinv.master.deiconify()
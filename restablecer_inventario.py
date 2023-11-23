import tkinter as tk
from tkinter import ttk
from datetime import datetime
from registrosdecomprasporquenotengobasededatos import registros_compras
from proveedoresdepruebaporquechenuncavaahacerlabasededatos import proveedores

class RestablecerInventario(tk.Toplevel):
    def __init__(self, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Restablecer Inventario")
        self.geometry("300x400")
        self.resizable(False, False)

        self.productos = productos
        self.proveedores = proveedores

        self.fecha_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        self.proveedor_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.total_var = tk.StringVar()

        self.configurar_interfaz()

    def configurar_interfaz(self):
        lbl_fecha = tk.Label(self, text="Fecha:")
        lbl_fecha.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_fecha = ttk.Entry(self, textvariable=self.fecha_var, state="readonly")
        entry_fecha.grid(row=0, column=1, padx=10, pady=10)
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        lbl_producto = tk.Label(self, text="Producto:")
        lbl_producto.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.combo_producto = ttk.Combobox(self, textvariable=self.producto_var, state="readonly")
        self.combo_producto.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.combo_producto.bind("<<ComboboxSelected>>", self.seleccionar_producto)

        lbl_proveedor = tk.Label(self, text="Proveedor:")
        lbl_proveedor.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_proveedor = ttk.Entry(self, textvariable=self.proveedor_var, state="readonly")
        entry_proveedor.grid(row=2, column=1, padx=10, pady=10)

        lbl_cantidad = tk.Label(self, text="Cantidad:")
        lbl_cantidad.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_cantidad = ttk.Entry(self, textvariable=self.cantidad_var)
        entry_cantidad.grid(row=3, column=1, padx=10, pady=10)

        lbl_total = tk.Label(self, text="Total:")
        lbl_total.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        entry_total = ttk.Entry(self, textvariable=self.total_var)
        entry_total.grid(row=4, column=1, padx=10, pady=10)

        btn_confirmar = ttk.Button(self, text="Confirmar", command=self.confirmar)
        btn_confirmar.grid(row=5, column=0, columnspan=2, pady=10)

        btn_volver = ttk.Button(self, text="Volver", command=self.volver)
        btn_volver.grid(row=6, column=0, columnspan=2, pady=10)

        self.lista_productos = [(f"{id_producto} - {producto['nombre']}") for id_producto, producto in self.productos.items()]
        self.combo_producto["values"] = self.lista_productos

    def seleccionar_producto(self, event):
        selected_product_id = int(self.combo_producto.get().split(" - ")[0])
        self.producto_var.set(selected_product_id)
    
        proveedor_id = self.productos[selected_product_id]["proveedor"]
    
        proveedor_nombre = next((proveedor["nombre"] for proveedor in self.proveedores if proveedor["id"] == proveedor_id), "")
    
        self.proveedor_var.set(proveedor_nombre)
        
        self.selected_proveedor_id = proveedor_id



    def confirmar(self):
        try:
            cantidad = int(self.cantidad_var.get())
            total = float(self.total_var.get())
            id_producto = int(self.producto_var.get())
            id_proveedor = self.selected_proveedor_id
        except ValueError:
            tk.messagebox.showerror("Error", "La cantidad y el total deben ser números.")
            return

        if id_producto not in self.productos:
            tk.messagebox.showerror("Error", "Producto no encontrado.")
            return
        
        id_venta = len(registros_compras) + 1

        self.productos[id_producto]["cantidad"] += cantidad

        registro = {
            "Id_Venta": id_venta,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id_producto": id_producto,
            "id_proveedor": id_proveedor,
            "cantidad": cantidad,
            "total": total
        }
        registros_compras.append(registro)

        self.producto_var.set("")
        self.proveedor_var.set("")
        self.cantidad_var.set("")
        self.total_var.set("")
    
        self.fecha_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def volver(self):
        self.grab_release()
        self.destroy()
        self.master.deiconify()
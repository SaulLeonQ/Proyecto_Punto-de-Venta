import tkinter as tk
from tkinter import ttk
from ventas_recibo import VentasRecibo


class VentasPago(tk.Toplevel):
    def __init__(vpago, master, productos_seleccionados):
        super().__init__(master)
        vpago.title("Pagar")
        vpago.geometry("600x320")
        vpago.resizable(False, False)

        vpago.productos_seleccionados = productos_seleccionados
        vpago.total_dinero = 0.0

        frame_top = ttk.Frame(vpago)
        frame_top.pack(side="top", expand=True, anchor="n")

        frame_lista = ttk.Frame(frame_top)
        frame_lista.pack(side="left", expand=True, anchor="nw", pady=10)
        
        frame_labels =ttk.Frame(frame_top)
        frame_labels.pack(side="right", expand=True, anchor="ne", pady=10)

        scrollbar_lista = ttk.Scrollbar(frame_lista)
        scrollbar_lista.pack(side="right", fill="y")

        vpago.lista_productos = tk.Listbox(frame_lista, yscrollcommand=scrollbar_lista.set, width=40, height=10)
        vpago.lista_productos.pack(side="left", expand=True)
        scrollbar_lista.config(command=vpago.lista_productos.yview)

        frame_botones_dinero = ttk.Frame(vpago)
        frame_botones_dinero.pack(side="top", pady=10, anchor="nw")
        ttk.Button(frame_botones_dinero, width=5, text="$500", command=lambda: vpago.sumar_dinero(500)).grid(row=0, column=0, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$200", command=lambda: vpago.sumar_dinero(200)).grid(row=0, column=1, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$100", command=lambda: vpago.sumar_dinero(100)).grid(row=0, column=2, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$50", command=lambda: vpago.sumar_dinero(50)).grid(row=0, column=3, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$20", command=lambda: vpago.sumar_dinero(20)).grid(row=0, column=4, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$10", command=lambda: vpago.sumar_dinero(10)).grid(row=1, column=0, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$5", command=lambda: vpago.sumar_dinero(5)).grid(row=1, column=1, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$2", command=lambda: vpago.sumar_dinero(2)).grid(row=1, column=2, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$1", command=lambda: vpago.sumar_dinero(1)).grid(row=1, column=3, padx=2, pady=5)
        ttk.Button(frame_botones_dinero, width=5, text="$0.50", command=lambda: vpago.sumar_dinero(0.50)).grid(row=1, column=4, padx=2, pady=5)

        vpago.total = 0.0
        vpago.subtotal = 0.0

        vpago.label_subtotal = tk.Label(frame_labels, text="Subtotal: $0.00")
        vpago.label_subtotal.pack(pady=10)

        vpago.label_total = tk.Label(frame_labels, text="Total: $0.00")
        vpago.label_total.pack(pady=10)

        vpago.label_pago_efectivo = tk.Label(frame_labels, text="Pago en efectivo: $0.00")
        vpago.label_pago_efectivo.pack(pady=10)

        vpago.boton_pagar = ttk.Button(frame_labels, text="Pagar", command=vpago.pagar)
        vpago.boton_pagar.pack(side="left", padx=10)
        vpago.boton_cancelar = ttk.Button(frame_labels, text="Cancelar", command=vpago.destroy)
        vpago.boton_cancelar.pack(side="left", padx=10)

        vpago.actualizar_lista_productos()


    def pagar(vpago):
        ventas_recibo = VentasRecibo(
            vpago,
            productos_seleccionados=vpago.productos_seleccionados,
            total_dinero=vpago.total_dinero,
            subtotal=vpago.subtotal,
            total=vpago.total,
            productos=vpago.master.productos
        )
        ventas_recibo.transient(vpago)
        ventas_recibo.grab_set()


    def actualizar_lista_productos(vpago):
        vpago.lista_productos.delete(0, tk.END)

        for producto, info in vpago.productos_seleccionados.items():
            cantidad = info["cantidad"]
            nombre_producto = vpago.master.productos[producto]["nombre"]
            precio = info["precio"]
            vpago.lista_productos.insert(tk.END, f"{nombre_producto} - {cantidad} - Precio: ${precio:.2f}")


        vpago.subtotal = sum(info["cantidad"] * info["precio"] for info in vpago.productos_seleccionados.values())
        vpago.total = vpago.subtotal

        vpago.label_subtotal.config(text=f"Subtotal: ${vpago.subtotal:.2f}")
        vpago.label_total.config(text=f"Total: ${vpago.total:.2f}")
        vpago.label_pago_efectivo.config(text=f"Pago en efectivo: ${vpago.total_dinero:.2f}")
 
        if vpago.total_dinero >= vpago.total:
            vpago.boton_pagar.config(state='active')

        else:
            vpago.boton_pagar.config(state='disable')

    def sumar_dinero(vpago, monto):
        vpago.total_dinero += monto
        vpago.actualizar_lista_productos()



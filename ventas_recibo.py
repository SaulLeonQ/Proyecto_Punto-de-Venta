import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class VentasRecibo(tk.Toplevel):
    def __init__(vrecibo, master, productos_seleccionados, total_dinero, subtotal, total, productos):
        super().__init__(master)
        vrecibo.title("Recibo")
        vrecibo.geometry("500x650")
        vrecibo.resizable(False, False)

        style = ThemedStyle(vrecibo)
        style.set_theme("clam")
        style.configure('EstiloA.TLabel', background="#f2f2f2")
        style.configure('EstiloB.TButton', width=12,font=("DejaVu Sans",15))

        frame_productos = ttk.Frame(vrecibo)
        frame_productos.pack(side="left", fill="y", expand=True, anchor="nw", pady=10)
        
        frame_venta = ttk.Frame(vrecibo)
        frame_venta.pack(side="left", expand=True, anchor="sw",pady=10)

        frame_botones = ttk.Frame(vrecibo)
        frame_botones.pack(side="right", expand=True,pady=10)

        canvas = tk.Canvas(frame_productos)
        canvas.pack(fill="both", expand=True)
        canvas.configure(bg="#f2f2f2")

        canvas2 = tk.Canvas(frame_productos)
        canvas2.pack(fill="both", expand=True)
        canvas2.configure(bg="#f2f2f2")

        vrecibo.mostrar_productos(canvas, productos_seleccionados, productos)

        ttk.Label(canvas2, style="EstiloA.TLabel", text="Número de venta:").grid(row=0, column=0, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text="Subtotal:").grid(row=1, column=0, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text="Total:").grid(row=2, column=0, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text="Efectivo:").grid(row=3, column=0, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text="Cambio:").grid(row=4, column=0, pady=5)

        numero_venta = 1 
        subtotal = subtotal
        total = total
        efectivo = total_dinero
        cambio = efectivo - total

        ttk.Label(canvas2, style="EstiloA.TLabel", text=numero_venta).grid(row=0, column=1, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text=f"${subtotal:.2f}").grid(row=1, column=1, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text=f"${total:.2f}").grid(row=2, column=1, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text=f"${efectivo:.2f}").grid(row=3, column=1, pady=5)
        ttk.Label(canvas2, style="EstiloA.TLabel", text=f"${cambio:.2f}").grid(row=4, column=1, pady=5)

        ttk.Button(frame_botones, style="EstiloB.TButton", text="Anular venta", command=vrecibo.Anular).pack(pady=40)
        ttk.Button(frame_botones, style="EstiloB.TButton", text="Cerrar", command=vrecibo.cerrar_recibo).pack(pady=40)


    def mostrar_productos(vrecibo, canvas, productos_seleccionados, productos):
        row_counter = 1
        for producto, info in productos_seleccionados.items():
            cantidad = info["cantidad"]
            nombre_producto = productos[producto]["nombre"]
            precio = info["precio"]

            ttk.Label(canvas, style="EstiloA.TLabel",text=f"{nombre_producto} - {cantidad} - Precio: ${precio:.2f}").grid(row=row_counter, column=0, columnspan=2, pady=5)
            row_counter += 1


    def Anular(vrecibo):
        vrecibo.destroy()

    def cerrar_recibo(vrecibo):
        vrecibo.destroy()


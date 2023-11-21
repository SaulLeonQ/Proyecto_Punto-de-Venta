import tkinter as tk
from tkinter import ttk, PhotoImage
from ttkthemes import ThemedStyle
from ventas_pago import VentasPago
from productosdepruebaporquesigosinbasededatos import productos


class VentanaProductos(tk.Toplevel):
    def __init__(vventas, productos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vventas.title("Lista de Productos")
        vventas.geometry("900x600")
        vventas.resizable(False, False)
        vventas.configure(bg="#f2f2f2")

        style = ThemedStyle(vventas)
        style.set_theme("clam")
        style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=12,font=("DejaVu Sans",10))

        vventas.imgMenu = PhotoImage(file="resources/menu.png").subsample(8,8)

        vventas.espacio_superior = tk.Frame(vventas, height=100, bg="light gray")
        vventas.espacio_superior.pack(fill="x")

        vventas.espacio_izquierdo = tk.Frame(vventas, width=150, bg="light gray")
        vventas.espacio_izquierdo.pack(side="left", fill="y")
        vventas.btn_cerrar = ttk.Button(vventas, image=vventas.imgMenu, command=vventas.cerrar_ventana)
        vventas.btn_cerrar.place(x=10,y=10)

        
        vventas.canvas = tk.Canvas(vventas)
        vventas.canvas.pack(side="left", fill="both", expand=True)
        vventas.canvas.configure(bg="#f2f2f2")
        vventas.scrollbar = ttk.Scrollbar(vventas, command=vventas.canvas.yview, orient="vertical", style="TScrollbar")
        vventas.scrollbar.pack(side="left", fill="y")
        vventas.canvas.configure(yscrollcommand=vventas.scrollbar.set)


        vventas.canvas_totales = tk.Canvas(vventas, bg="light gray", height=50)
        vventas.canvas_totales.pack(side="bottom", fill="x",anchor="se")

        vventas.canvas_totales.label_total_productos = tk.Label(vventas.canvas_totales, text=f"Total Productos: 0")
        vventas.canvas_totales.label_total_productos.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        vventas.canvas_totales.label_total_precio = tk.Label(vventas.canvas_totales, text=f"Subtotal Precio: $0.00")
        vventas.canvas_totales.label_total_precio.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        vventas.canvas_productos = tk.Canvas(vventas, width=400, bg="#f2f2f2")
        vventas.canvas_productos.pack(side="right", fill="both", expand=True)
        vventas.scrollbar_productos = ttk.Scrollbar(vventas, command=vventas.canvas_productos.yview, orient="vertical", style="TScrollbar")
        vventas.scrollbar_productos.pack(side="right", fill="y")
        vventas.canvas_productos.configure(yscrollcommand=vventas.scrollbar_productos.set)
        vventas.frame_productos = tk.Frame(vventas.canvas_productos, bg="#f2f2f2")
        vventas.canvas_productos.create_window((0, 0), window=vventas.frame_productos, anchor="nw")

        vventas.frame = tk.Frame(vventas.canvas, bg="#f2f2f2")
        vventas.canvas.create_window((0, 0), window=vventas.frame, anchor="nw")

        vventas.productos = productos

        vventas.frame.bind("<Configure>", vventas.frame_conf)

        tipos = set(prod_info["tipo"] for prod_info in productos.values())
        vventas.botones_tipos = []
        col = 0
        row = 0
        for tipo in tipos:
            padx_left = 150 if col == 0 else 10
            boton_tipo = ttk.Button(vventas.espacio_superior, text=tipo, command=lambda t=tipo: vventas.crear_botones(t))
            boton_tipo.grid(row=row, column=col, padx=(padx_left, 10), pady=10)
            vventas.botones_tipos.append(boton_tipo)
            col += 1
            if col > 4:
                col = 0
                row += 1
                vventas.altura(row)


        vventas.botones_productos = []
        vventas.productos_seleccionados = {}

    def crear_botones(vventas,stipo):
        for boton in vventas.botones_productos:
            boton.grid_forget()
        row = 0
        col = 0
        for producto_id, producto_info in vventas.productos.items():
            if producto_info["tipo"] == stipo:
                nombre_producto = producto_info["nombre"]
                precio_producto = producto_info["precio"]
                boton = ttk.Button(vventas.frame, text=nombre_producto, width=20, command=lambda idp=producto_id, pp=precio_producto: agregar_producto(idp,pp))
                boton.grid(row=row, column=col, padx=10, pady=10)
                vventas.botones_productos.append(boton)
                col += 1
                if col > 1:
                    col = 0
                    row += 1

        def agregar_producto(id_producto,precio_producto):
            if id_producto in vventas.productos_seleccionados:
                vventas.productos_seleccionados[id_producto]["cantidad"] += 1
            else:
                vventas.productos_seleccionados[id_producto] = {"cantidad": 1, "precio": precio_producto}

            vventas.actualizar_lista_productos()

    def actualizar_lista_productos(vventas):
        for widget in vventas.canvas_productos.winfo_children():
            widget.destroy()
        
        for widget in vventas.canvas_totales.winfo_children():
            widget.destroy()

        total_productos = 0
        total_precio = 0.0
        row = 0
        for producto_id, info in vventas.productos_seleccionados.items():
            cantidad = info["cantidad"]
            precio_unitario = info["precio"]
            total_productos += cantidad
            total_precio += cantidad * precio_unitario
            
            nombre_producto = vventas.productos[producto_id]["nombre"]

            label_producto = tk.Label(vventas.canvas_productos, text=f"{nombre_producto}: {cantidad}")
            label_producto.grid(row=producto_id, column=0, padx=10, pady=5, sticky="w")

            boton_restar = ttk.Button(vventas.canvas_productos, text="-",width=4, command=lambda pid=producto_id: restar_producto(pid))
            boton_restar.grid(row=producto_id, column=1, padx=5, pady=5, sticky="w")
            row += 1

        label_total_productos = tk.Label(vventas.canvas_totales, text=f"Total Productos: {total_productos}")
        label_total_productos.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        row+=1

        label_total_precio = tk.Label(vventas.canvas_totales, text=f"Subtotal Precio: ${total_precio:.2f}")
        label_total_precio.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        row+=1

        boton_pagar = ttk.Button(vventas.canvas_totales, text="Pagar", command=vventas.pagar)
        boton_pagar.grid(row=row, column=0, padx=10, pady=5, sticky="w")



        def restar_producto(producto_id):
            if producto_id in vventas.productos_seleccionados:
                vventas.productos_seleccionados[producto_id]["cantidad"] -= 1
                if vventas.productos_seleccionados[producto_id]["cantidad"] <= 0:
                    del vventas.productos_seleccionados[producto_id]
                vventas.actualizar_lista_productos()

        
        vventas.frame_productos.update()


    def frame_conf(vventas, event):
        vventas.canvas.configure(scrollregion=vventas.canvas.bbox("all"))

    def altura(vventas,r):
        altura_anterior = vventas.espacio_superior.winfo_height()
        nueva_altura = altura_anterior + r * 80
        vventas.espacio_superior.config(height=nueva_altura)
        vventas.geometry(f"900x{500 + nueva_altura}")

    def cerrar_ventana(vventas):
        vventas.grab_release()
        vventas.destroy()
        vventas.master.deiconify()
    
    def pagar(vventas):
        ventana_pago = VentasPago(vventas, productos_seleccionados=vventas.productos_seleccionados)
        ventana_pago.transient(vventas)
        ventana_pago.grab_set()



if __name__ == "__main__":
    root = tk.Tk()
    ventana = VentanaProductos(root, productos)
    root.mainloop()

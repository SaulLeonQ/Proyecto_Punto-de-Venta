import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from productosdepruebaporquesigosinbasededatos import productos


class VentanaProductos(tk.Toplevel):
    def __init__(vventas, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vventas.root = root
        vventas.root.title("Lista de Productos")
        vventas.root.geometry("800x600")
        vventas.root.resizable(False, False)
        vventas.root.configure(bg="#f2f2f2")

        style = ThemedStyle(vventas.root)
        style.set_theme("clam")
        style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=12,font=("DejaVu Sans",10))

        vventas.espacio_superior = tk.Frame(vventas.root, height=100, bg="light gray")
        vventas.espacio_superior.pack(fill="x")

        vventas.espacio_derecho = tk.Frame(vventas.root, width=400, bg="light gray")
        vventas.espacio_derecho.pack(side="right", fill="y")
        vventas.espacio_derecho.label_total_productos = tk.Label(vventas.espacio_derecho, text=f"Total Productos: 0")
        vventas.espacio_derecho.label_total_productos.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        vventas.espacio_derecho.label_total_precio = tk.Label(vventas.espacio_derecho, text=f"Total Precio: $0.00")
        vventas.espacio_derecho.label_total_precio.grid(row=2, column=0, padx=10, pady=5, sticky="w")


        vventas.espacio_izquierdo = tk.Frame(vventas.root, width=150, bg="light gray")
        vventas.espacio_izquierdo.pack(side="left", fill="y")

        vventas.canvas = tk.Canvas(vventas.root)
        vventas.canvas.pack(side="left", fill="both", expand=True)
        vventas.canvas.configure(bg="#f2f2f2")
        vventas.scrollbar = ttk.Scrollbar(vventas.root, command=vventas.canvas.yview, orient="vertical", style="TScrollbar")
        vventas.scrollbar.pack(side="right", fill="y")
        vventas.canvas.configure(yscrollcommand=vventas.scrollbar.set)

        vventas.frame = tk.Frame(vventas.canvas, bg="#f2f2f2")
        vventas.canvas.create_window((0, 0), window=vventas.frame, anchor="nw")

        vventas.productos = productos

        vventas.frame.bind("<Configure>", vventas.frame_conf)

        tipos = set(prod_info["tipo"] for prod_info in productos.values())
        vventas.botones_tipos = []
        col = 0
        row = 0
        for tipo in tipos:
            padx_left = 190 if col == 0 else 10
            boton_tipo = ttk.Button(vventas.espacio_superior, text=tipo, command=lambda t=tipo: vventas.crear_botones(t))
            boton_tipo.grid(row=row, column=col, padx=(padx_left, 10), pady=10)
            vventas.botones_tipos.append(boton_tipo)
            col += 1
            if col > 2:
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

        def agregar_producto(nombre_producto,precio_producto):
            if nombre_producto in vventas.productos_seleccionados:
                vventas.productos_seleccionados[nombre_producto]["cantidad"] += 1
            else:
                vventas.productos_seleccionados[nombre_producto] = {"cantidad": 1, "precio": precio_producto}

            vventas.actualizar_lista_productos()

    def actualizar_lista_productos(vventas):
        for widget in vventas.espacio_derecho.winfo_children():
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

            label_producto = tk.Label(vventas.espacio_derecho, text=f"{nombre_producto}: {cantidad}")
            label_producto.grid(row=producto_id, column=0, padx=10, pady=5, sticky="w")

            boton_restar = ttk.Button(vventas.espacio_derecho, text="-",width=4, command=lambda pid=producto_id: restar_producto(pid))
            boton_restar.grid(row=producto_id, column=1, padx=5, pady=5, sticky="w")
            row += 1

        label_total_productos = tk.Label(vventas.espacio_derecho, text=f"Total Productos: {total_productos}")
        label_total_productos.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        row+=1

        label_total_precio = tk.Label(vventas.espacio_derecho, text=f"Total Precio: ${total_precio:.2f}")
        label_total_precio.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        def restar_producto(producto_id):
            if producto_id in vventas.productos_seleccionados:
                vventas.productos_seleccionados[producto_id]["cantidad"] -= 1
                if vventas.productos_seleccionados[producto_id]["cantidad"] <= 0:
                    del vventas.productos_seleccionados[producto_id]
                vventas.actualizar_lista_productos()

        
        vventas.espacio_derecho.update()

    def frame_conf(vventas, event):
        vventas.canvas.configure(scrollregion=vventas.canvas.bbox("all"))

    def altura(vventas,r):
        altura_anterior = vventas.espacio_superior.winfo_height()
        nueva_altura = altura_anterior + r * 80
        vventas.espacio_superior.config(height=nueva_altura)
        vventas.root.geometry(f"800x{500 + nueva_altura}")

if __name__ == "__main__":
    root = tk.Tk()
    ventana = VentanaProductos(root, productos)
    root.mainloop()
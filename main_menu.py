import tkinter as tk
from ventas import VentanaProductos
from tkinter import ttk,PhotoImage
from ttkthemes import ThemedStyle
from productosdepruebaporquesigosinbasededatos import productos


class MenuPrincipal(tk.Toplevel):
    def __init__(mmenu, usuario, tipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mmenu.title("Sesión de {}".format(usuario))
        mmenu.geometry("600x420")
        mmenu.resizable(False, False)

        style = ThemedStyle(mmenu)
        style.set_theme("clam")
        style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=12,font=("DejaVu Sans",20))        

        #CREACION DE LAS IMAGENES Y LABELS
        mmenu.imgRegProd = PhotoImage(file="resources/caja.png").subsample(8,8)
        mmenu.imgRestInv = PhotoImage(file="resources/carga-de-camiones.png").subsample(8,8)
        mmenu.imgConsInv = PhotoImage(file="resources/cajas.png").subsample(8,8)
        mmenu.imgComVent = PhotoImage(file="resources/carrito-de-compras.png").subsample(8,8)
        mmenu.imgReporte = PhotoImage(file="resources/porcentaje.png").subsample(8,8)
        mmenu.imgConsProd = PhotoImage(file="resources/busqueda.png").subsample(8,8)

        mmenu.Logo = PhotoImage(file="resources/Easyplus_Logo.png")

        lbllogo = tk.Label(mmenu, image=mmenu.Logo)
        lblRegProd = tk.Label(mmenu, text="Registrar Producto",foreground='black',font=("DejaVu Sans", 12))
        lblRestInv = tk.Label(mmenu, text="Restablecer Inventario",foreground='black',font=("DejaVu Sans", 12))
        lblConsInv = tk.Label(mmenu, text="Consultar Inventario",foreground='black',font=("DejaVu Sans", 12))
        lblComVent = tk.Label(mmenu, text="Comenzar Venta",foreground='black',font=("DejaVu Sans", 12))
        lblReporte = tk.Label(mmenu, text="Reportes",foreground='black',font=("DejaVu Sans", 12))
        lblConsProd = tk.Label(mmenu, text="Consultar Producto",foreground='black',font=("DejaVu Sans", 12))

        #CREACION DE BOTONES
        btCerrarSesion = ttk.Button(mmenu, text="Cerrar Sesión", style='TButton', command=mmenu.cerrar_sesion)
        btRegProd = ttk.Button(mmenu, image=mmenu.imgRegProd, style='TButton') #command=verificacion
        btRestInv = ttk.Button(mmenu, image=mmenu.imgRestInv, style='TButton') #command=verificacion
        btConsInv = ttk.Button(mmenu, image=mmenu.imgConsInv, style='TButton') #command=verificacion
        btComVent = ttk.Button(mmenu, image=mmenu.imgComVent, style='TButton', command=mmenu.ventas) #command=ventas
        btReporte = ttk.Button(mmenu, image=mmenu.imgReporte, style='TButton') #command=verificacion
        btConsProd = ttk.Button(mmenu, image=mmenu.imgConsProd, style='TButton') #command=verificacion


        #ACTIVACION DE BOTONES POR PERMISOS
        if tipo=="administrador":
            btReporte.config(state='active')
            btConsInv.config(state='active')
            btRestInv.config(state='active')
            btRegProd.config(state='active')
        else:
            btReporte.config(state='disable')
            btConsInv.config(state='disable')
            btRestInv.config(state='disable')
            btRegProd.config(state='disable')


        #POSICIONAMIENTO DE ELEMENTOS
        btCerrarSesion.place(x=1, y=1)

        btRegProd.place(x=57,y=70)
        lblRegProd.place(x=22,y=150)

        btRestInv.place(x=57,y=180)
        lblRestInv.place(x=7,y=260)

        btConsInv.place(x=57,y=290)
        lblConsInv.place(x=15,y=370)

        btComVent.place(x=482,y=70)
        lblComVent.place(x=452,y=150)

        btReporte.place(x=482,y=180)
        lblReporte.place(x=482,y=260)

        btConsProd.place(x=482,y=290)
        lblConsProd.place(x=442,y=370)

        lbllogo.place(x=210,y=120)

    def cerrar_sesion(mmenu):
        mmenu.grab_release()
        mmenu.destroy()
        mmenu.master.deiconify()

        


    def ventas(mmenu):
            ventana_principal = VentanaProductos(productos, mmenu)
            ventana_principal.grab_set()
            mmenu.withdraw()
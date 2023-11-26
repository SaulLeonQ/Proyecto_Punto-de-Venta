import tkinter as tk
from ventas import VentanaProductos
from consultar_producto import ConsultarProducto
from restablecer_inventario import RestablecerInventario
from registro_producto import RegistroProductos
from consultar_inventario import ConsultarInventario
from reportes import Reportes
from gestionc import GestionC
from gestionp import GestionP
from gestionu import GestionU
from tkinter import ttk,PhotoImage
from ttkthemes import ThemedStyle
from productosdepruebaporquesigosinbasededatos import productos


class MenuPrincipal(tk.Toplevel):
    def __init__(mmenu, usuario, tipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mmenu.title("Sesión de {}".format(usuario))
        mmenu.geometry("610x600")
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
        mmenu.imgConProd = PhotoImage(file="resources/busqueda.png").subsample(8,8)
        mmenu.imgUsuario = PhotoImage(file="resources/usuarios.png").subsample(8,8)
        mmenu.imgCliente = PhotoImage(file="resources/clientes.png").subsample(8,8)
        mmenu.imgProveed = PhotoImage(file="resources/proveedores.png").subsample(8,8)
        mmenu.imgSalir = PhotoImage(file="resources/menu.png").subsample(8,8)

        mmenu.Logo = PhotoImage(file="resources/Easyplus_Logo.png")

        lbllogo = tk.Label(mmenu, image=mmenu.Logo)
        lblRegProd = tk.Label(mmenu, text="Registrar Producto",foreground='black',font=("DejaVu Sans", 12))
        lblRestInv = tk.Label(mmenu, text="Restablecer Inventario",foreground='black',font=("DejaVu Sans", 12))
        lblGestC = tk.Label(mmenu, text="Gestion de Clientes",foreground='black',font=("DejaVu Sans", 12))
        lblGestP = tk.Label(mmenu, text="Gestion de Proveedores",foreground='black',font=("DejaVu Sans", 12))
        lblGestU = tk.Label(mmenu, text="Gestion de Usuarios",foreground='black',font=("DejaVu Sans", 12))
        lblComVent = tk.Label(mmenu, text="Comenzar Venta",foreground='black',font=("DejaVu Sans", 12))
        lblReporte = tk.Label(mmenu, text="Reportes",foreground='black',font=("DejaVu Sans", 12))
        lblConsProd = tk.Label(mmenu, text="Consultar Producto",foreground='black',font=("DejaVu Sans", 12))
        lblConsInv = tk.Label(mmenu, text="Consultar Inventario",foreground='black',font=("DejaVu Sans", 12))
        lblCerrar = tk.Label(mmenu, text="Cerrar Sesion",foreground='black',font=("DejaVu Sans", 12))

        #CREACION DE BOTONES
        btCerrarSesion = ttk.Button(mmenu, image=mmenu.imgSalir, style='TButton', command=mmenu.cerrar_sesion)
        btRegProd = ttk.Button(mmenu, image=mmenu.imgRegProd, style='TButton', command=mmenu.registrar_producto)
        btRestInv = ttk.Button(mmenu, image=mmenu.imgRestInv, style='TButton', command=mmenu.restablecer_inventario)
        btGestionC = ttk.Button(mmenu, image=mmenu.imgCliente, style='TButton', command=mmenu.gestionC)
        btGestionP = ttk.Button(mmenu, image=mmenu.imgProveed, style='TButton', command=mmenu.gestionP)
        btGestionU = ttk.Button(mmenu, image=mmenu.imgUsuario, style='TButton', command=mmenu.gestionU)
        btComVent = ttk.Button(mmenu, image=mmenu.imgComVent, style='TButton', command=mmenu.ventas)
        btReporte = ttk.Button(mmenu, image=mmenu.imgReporte, style='TButton', command=mmenu.reportes)
        btConsProd = ttk.Button(mmenu, image=mmenu.imgConProd, style='TButton', command=mmenu.consultar_producto)
        btConsInv = ttk.Button(mmenu, image=mmenu.imgConsInv, style='TButton', command=mmenu.consultar_inventario)


        #ACTIVACION DE BOTONES POR PERMISOS
        if tipo=="administrador":
            btReporte.config(state='active')
            btGestionC.config(state='active')
            btGestionU.config(state='active')
            btGestionP.config(state='active')
            btRestInv.config(state='active')
            btRegProd.config(state='active')
        else:
            btReporte.config(state='disable')
            btGestionC.config(state='disable')
            btGestionU.config(state='disable')
            btGestionP.config(state='disable')
            btRestInv.config(state='disable')
            btRegProd.config(state='disable')


        #POSICIONAMIENTO DE ELEMENTOS
        btCerrarSesion.place(x=200, y=280)

        btRegProd.place(x=57,y=50)
        lblRegProd.place(x=22,y=130)

        btRestInv.place(x=57,y=160)
        lblRestInv.place(x=7,y=240)

        btGestionC.place(x=57,y=270)
        lblGestC.place(x=16,y=350)

        btGestionP.place(x=57,y=380)
        lblGestP.place(x=0,y=460)

        btConsInv.place(x=57,y=490)
        lblConsInv.place(x=13,y=570)

        btComVent.place(x=482,y=50)
        lblComVent.place(x=452,y=130)

        btReporte.place(x=482,y=160)
        lblReporte.place(x=482,y=240)

        btConsProd.place(x=482,y=270)
        lblConsProd.place(x=442,y=350)

        btGestionU.place(x=482,y=380)
        lblGestU.place(x=439,y=460)

        btCerrarSesion.place(x=482,y=490)
        lblCerrar.place(x=462,y=570)

        lbllogo.place(x=220,y=190)

    def cerrar_sesion(mmenu):
        mmenu.grab_release()
        mmenu.destroy()
        mmenu.master.deiconify()

    def ventas(mmenu):
        ventana_principal = VentanaProductos(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def gestionC(mmenu):
        ventana_principal = GestionC(mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def gestionP(mmenu):
        ventana_principal = GestionP(mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def gestionU(mmenu):
        ventana_principal = GestionU(mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def registrar_producto(mmenu):
        ventana_principal = RegistroProductos(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()
    
    def restablecer_inventario(mmenu):
        ventana_principal = RestablecerInventario(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def reportes(mmenu):
        ventana_principal = Reportes(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def consultar_producto(mmenu):
        ventana_principal = ConsultarProducto(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()

    def consultar_inventario(mmenu):
        ventana_principal = ConsultarInventario(productos, mmenu)
        ventana_principal.grab_set()
        mmenu.withdraw()
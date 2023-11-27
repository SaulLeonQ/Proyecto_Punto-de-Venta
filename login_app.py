import tkinter as tk
from tkinter import messagebox,ttk,PhotoImage
from ttkthemes import ThemedStyle
import psycopg2


from main_menu import MenuPrincipal

#IMPLEMENTACION DE BD
db_parametros = {
    'dbname': 'bidoodkhl2srw9thnh6n',
    'user': 'ug8l8c6wm3ggrmnn4xx1',
    'password': 'boo9ZRBIYS6WttHzvrjF0uB9JEVuS4',
    'host': 'bidoodkhl2srw9thnh6n-postgresql.services.clever-cloud.com',
    'port': '50013',
}

# VERIFICACION DEL USUARIO
def verificacion():
    usuario = eusuario.get()
    contraseña = econtraseña.get()

    connection = None 
    cursor = None

    try:
        # Conectar a la base de datos
        connection = psycopg2.connect(**db_parametros)
        cursor = connection.cursor()

        # Consulta SQL para verificar al usuario en la tabla de administradores
        cursor.execute("SELECT * FROM administrador WHERE admin_usuario = %s AND admin_contra = %s", (usuario, contraseña))
        result_admin = cursor.fetchone()

        # Consulta SQL para verificar al usuario en la tabla de clientes si no se encontró en administradores
        if not result_admin:
            cursor.execute("SELECT * FROM vendedor WHERE vendedor_usuario = %s AND vendedor_contra = %s", (usuario, contraseña))
            result_vendedor = cursor.fetchone()

        if result_admin:
            tipo = "administrador"
            tipoU = result_admin[0]
            ventana_principal = MenuPrincipal(usuario, tipo)
            ventana_principal.grab_set()
            ventana.withdraw()

        elif result_vendedor:
            tipoU = result_vendedor[0]
            ventana_principal = MenuPrincipal(usuario, tipoU, ventana)
            ventana_principal.grab_set()  
            ventana.withdraw()


        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión a la base de datos: {str(e)}")

    finally:
        # Cerrar cursor y conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()


#CREACION DE LA VENTANA
ventana = tk.Tk()
ventana.title("Log-in")

ventana.geometry("300x450")
ventana.resizable(False, False)

#IMAGEN
Logo = PhotoImage(file="resources/Easyplus_Logo.png")

#EVENTOS DE LOS ENTRYS
def eusuario_click(event):
    if eusuario.get() == defteuduario:
        eusuario.delete(0, tk.END)
        eusuario.config(foreground='black')

def eusuario_focus_out(event):
    if not eusuario.get():
        eusuario.insert(0, defteuduario)
        eusuario.config(foreground='grey')

defteuduario = "Usuario"

def econtraseña_click(event):
    if econtraseña.get() == defteconstraseña:
        econtraseña.delete(0, tk.END)
        econtraseña.config(foreground='black',show="*")

def econtraseña_focus_out(event):
    if not econtraseña.get():
        econtraseña.insert(0, defteconstraseña)
        econtraseña.config(foreground='grey', show="")
defteconstraseña = "Contraseña"


#EDICION DEL ESTILO
style = ThemedStyle(ventana)
style.set_theme("clam")
style.configure('TButton',borderwidth=1,relief="flat",background="#f2f2f2", width=12,font=("DejaVu Sans",20))
style.configure('TEntry',relief="flat",padding=(5,5,5,5))


#ENTRYS, BOTON E IMAGEN
eusuario = ttk.Entry(ventana, style='TEntry',foreground='grey',font=("DejaVu Sans", 20),width=12)
eusuario.insert(0, defteuduario)
eusuario.bind("<FocusIn>", eusuario_click)
eusuario.bind("<FocusOut>", eusuario_focus_out)

econtraseña = ttk.Entry(ventana, style='TEntry',foreground='grey',font=("DejaVu Sans", 20),width=12)
econtraseña.insert(0, defteconstraseña)
econtraseña.bind("<FocusIn>", econtraseña_click)
econtraseña.bind("<FocusOut>", econtraseña_focus_out)

btlogin = ttk.Button(ventana, text="Iniciar sesión", command=verificacion, style='TButton')

lbllogo = tk.Label(ventana, image=Logo)

lbllogo.place(x=50,y=0)
eusuario.place(x=42,y=210)
econtraseña.place(x=42,y=260)
btlogin.place(x=42,y=350)

ventana.mainloop()
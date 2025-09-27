import tkinter as tk
from tkinter import messagebox
import json
import time
# import os, sys

##variables globales
users = {}
user_number = None
user = None
formato_fecha = "%d/%m/%y %H:%M:%S"
##colores para cada frame
bg_color = "#ad01ca"
lbl_color = "#780986"
lbl_txt_color = "#fae4ff"
btn_color = "#fdf2ff"
btn_txt_color = "#51005c"
entry_color = "#fdf2ff"
entry_txt_color = "#51005c"
##COLECCION DE CONTRASEÑAS INSEGURAS
contraseña_insegura = {"1234", "admin", "ADMIN", "4321", "password","PASSWORD", "123456", "QWERTY", "qwerty", "abcd", "abcde", "ABCD", "ABCDE"}
"""
##RECORDATORIO: VOLVER A PONER EL ICONO
--> GUARDAR EL TIEMPO DEL MOMENTO DE LA TRANSACCION (DEPOSITO, TRANSFERENCIA Y RETIRO)
--> AGG NOTI DE DEPOSITO Y RETIRO (POSIBLE BORRAR ACTIVIDAD RECIENTE)
--> LIMITE DE AHORRO (POSIBLE)
--> LIMITE DE RETIRO DIARIO 
--> VACIAR ACTIVIDAD RECIENTE PARA CADA USUARIO
--> REVISAR ERROR DE LISTA VACIA AL CERRAR SESION
--> MODULAR EL CODIGO
--> USUARIO DE MINIMO 4 MAXIMO 12 CARACTERES
--> CONTRASENA DE MINIMO 8 MAXIMO 12 CARACTERES
--> OPCION DE TRANSFERIR ENTRE USUARIOS REGISTRADOS
--> VERFICADOR DE CONTRASENAS INSEGURAS USANDO UN CONJUNTO {}
--> GENERAR PDF CON EL HISTORIAL DE CADA USUARIO 
--> DOCUMENTAR EL CODIGO
--> AGREGAR OPCION DE AJUSTES (BORRAR USUARIO, CAMBIAR TEMA, ...)

"""

##FUNCIONES GENERALES
def closeApp():
    """Guardar los datos y cerrar el programa.
    """
    if messagebox.askokcancel("Salir", "¿Seguro que quieres cerrar el programa?"):
        home.destroy()
        saveData()

def loginBtn():
    """Boton para iniciar sesion.
    """
    global user_number
    if user_number == 0:
        respuesta = messagebox.askyesno("Advertencia", "No hay usuarios registrados, vamos a registarte")
        if respuesta == True:
            home_frame.pack_forget()
            sign_up_frame.pack(fill="both", expand=True)
            
        else:
            quit()
    else:
        home_frame.pack_forget()
        login_frame.pack(fill="both", expand=True)

def signUpBtn():
    """Boton para registrar un nuevo usuario.
    """
    home_frame.pack_forget()
    sign_up_frame.pack(fill="both", expand=True)
    
def deleteUserBtn():
    """Boton para eliminar usuario ya existente.
    """
    home_frame.pack_forget()
    delete_user_frame.pack(fill="both", expand=True)

def closeBtn():
    """Boton para salir y guardar los datos.
    """
    if messagebox.askokcancel("Salir", "¿Seguro que quieres cerrar el programa?"):
        saveData()
        home.destroy()
    

def login():
    """Funcion para autenticar usuarios e iniciar sesion.
    
    Se solicita el usuario y contraseña y despues se comprueba si: 
    -->  EL usuario y contraseña existen
    """
    global users, username, user
    user = userIn.get()
    password = passwordIn.get()
    username = user
    print(f"El usuario {username} inicio sesion.") 
    if user in users and users[user]["password"] == password:
        userIn.delete(0, "end")
        passwordIn.delete(0, "end")
        login_frame.pack_forget() 
        user_profile_frame.pack(fill="both", expand=True)
        login_message.config(text=f"Bienvenido {user}!")
        user_info.config(text=f"Saldo disponible: {users[user]["dinero"]}")
        for actividad in users[user]["actividad_reciente"]:
            actividad_reciente.config(text=f"Actividad reciente:\n{actividad}", font=("Arial", 8))
            print(f"Actividad reciente de {user}: {actividad}")
    else:
        messagebox.showinfo("Credenciales invalidas", "Usuario o contraseña incorrectos")

def sign_up():
    """Funcion para crear un nuevo usuario.
    """
    global users, user_number
    user = set_user.get()
    password = set_password.get()
    user_length = len(user)
    password_length = len(password)
    
    if user in users:
        messagebox.showinfo("Usuario ya registrado", "El usuario que ingresaste ya existe")
        set_user.delete(0, "end")
    elif user == "":
        messagebox.showinfo("Usuario no valido", "No ingresaste un nombre de usuario")
    elif user_length < 4:
        messagebox.showinfo("Usuario no valido", "El nombre de usuario debe tener al menos 4 caracteres")
    elif  password == "":
        messagebox.showinfo("Contraseña no valida", "Por favor, crea una contraseña")
    elif password_length < 4:
        messagebox.showinfo("Contraseña no valida", "La contraseña debe tener al menoso 4 caracteres")
    elif password in contraseña_insegura or password == user:
        messagebox.showinfo("Contraseña no valida", "La contraseña ingresada es insegura, por favor escribe otra.")
        set_password.delete(0, "end")
    else:
        fecha_transaccion = time.strftime(formato_fecha)
        users[user] = {"password": password, "dinero": 0, "actividad_reciente": [f"{fecha_transaccion}: Cuenta creada"]}
        print(users)
        messagebox.showinfo("Registro completado", "Usuario registrado exitosamente")
        set_user.delete(0, "end")
        set_password.delete(0, "end")
        sign_up_frame.pack_forget()
        home_frame.pack(fill="both", expand=True)
        saveData()
        loadData()
        user_number = len(users)
        user_message.config(text=f"Hay {user_number} usuario(s) registrado(s)")

def deleteUser():
    """Funcion para eliminar usuarios existentes.
    """ 
    global user_number
    user = delete_user_in.get()
    if user in users:
        del_confirm = messagebox.askyesno("Confirmacion de eliminacion.", f"Estas seguro que deseas eliminar el usuario {user}")
        if del_confirm == True:
            users.pop(user)
            messagebox.showwarning("Usuario eliminado", f"Se ha eliminado el usuario {user}")
            delete_user_in.delete(0, "end")
            user_number = len(users)
            user_message.config(text=f"Hay {user_number} usuario(s) registrado(s)")
            saveData()
            loadData()
        else:
            delete_user_in.delete(0,"end")
    else:
        messagebox.showwarning("Error de usuario", f"El usuario {user} no existe")

def depositar():
    """Funcion para el boton para abrir la pantalla de deposito.
    """
    user_profile_frame.pack_forget()
    depositar_frame.pack(fill="both", expand=True)

def realizarDeposito():
    """Funcion para realizar el deposito.
    """
    intento_deposito = False
    while not intento_deposito:
        value = float(depositar_cantidad.get())
        dinero = value
        if dinero <= 0:
            messagebox.showerror("Operacion invalida", "El monto minimo de deposito es de 1 peso.")
            break
        else:
            fecha_transaccion = time.strftime(formato_fecha)
            messagebox.showinfo("Transaccion exitosa!", f"Haz depositado {dinero} peso(s)")
            users[user]["dinero"] = users[user]["dinero"] + dinero
            users[user]["actividad_reciente"].append(f"{fecha_transaccion}: Deposito de {dinero} pesos")
            saveData()
            loadData()
            #depositar_frame.pack_forget()
            #user_profile_frame.pack(fill="both", expand=True)
            user_info.config(text=f"Tienes {users[user]["dinero"]} pesos disponibles en tu cuenta")
            depositar_cantidad.delete(0, "end")
        
            for actividad in users[user]["actividad_reciente"]:
                actividad_reciente.config(text=f"Actividad reciente:\n{actividad}", font=("Arial", 8))  
            break  
    

def retirar(): 
    """Funcion para el boton de abrir la pantalla de retiro.
    """
    user_profile_frame.pack_forget()
    retirar_frame.pack(fill="both", expand=True)

def realizarRetiro():
    """Funcion para retirar la cantidad de dinero que el usuario ingrese.
    """
    intento_retiro = False
    while not intento_retiro:
        value = retirar_cantidad.get()
        dinero = float(value)
        # if str(value): #tampoco sirve lol
        #     messagebox.showerror("Operacion invalida", "Por favor ingrese datos NUMERICOS VALIDOS")
        #     break
        # else:
        #     dinero = int(value)
        
        # if dinero == str(): ##no sirve xd
        #     messagebox.showerror("Operacion invalida", "Por favor ingrese datos NUMERICOS VALIDOS")
        #     intento_retiro = False
        #     retirar_cantidad.delete(0, "end")
        
        if dinero <= 0:
            messagebox.showinfo("Informacion invalida", "El retiro minimo es de $1")
            break
        else:
            if dinero > users[user]["dinero"]:
                messagebox.showinfo("Fondos insuficientes", f"No tienes dinero suficiente para retirar esta cantidad\nTienes ${users[user]["dinero"]} disponibles")
                retirar_cantidad.delete(0, "end")
                break
            else:
                fecha_transaccion = time.strftime(formato_fecha)
                messagebox.showinfo("Transaccion exitosa!", f" Haz retirado {dinero} peso(s)")
                users[user]["dinero"] = users[user]["dinero"] - dinero
                users[user]["actividad_reciente"].append(f"{fecha_transaccion}:Retiro de ${dinero}.")
                saveData()
                loadData()
                # retirar_frame.pack_forget()
                # user_profile_frame.pack(fill="both", expand=True)
                user_info.config(text=f"Tienes ${users[user]["dinero"]} disponibles en tu cuenta ")
                retirar_cantidad.delete(0, "end")
                for actividad in users[user]["actividad_reciente"]:
                    actividad_reciente.config(text=f"Actividad reciente:\n{actividad}", font=("Arial", 8))
                break

def transferir():
    """Funcion para el boton de transferir dinero entre usuarios.
    """
    user_profile_frame.pack_forget()
    transferir_frame.pack(fill="both", expand=True)

def realizarTransferencia():
    """Funcion para realizar la transferencia al usuario ingresado.
    """
    global users, user
    userT = transferir_user.get()
    print(userT)
    if userT not in users:
        messagebox.showerror("Informacion invalida", f"El usuario {userT} no existe")
    elif userT == user:
        transferir_user.delete(0, "end")
        messagebox.showerror("Informacion invalida", "No te puedes transferir a ti mismo")
    else:
        intento_transferir = False
        while not intento_transferir:
            userT = transferir_user.get()
            cantidad = float(transferir_cantidad.get())
            dinero = cantidad
            dineroU = users[user]["dinero"]
            dineroUT = users[userT]["dinero"]
            print(f"El dinero del usuario {userT} es: ","$", dineroUT)
            print(dineroU)
            if dinero <= 0:
                messagebox.showerror("Informacion invalida", "El monto minimo para transferir es de $1")
                transferir_cantidad.delete(0, "end")
                dinero = None
                cantidad = None
            elif dinero > users[user]["dinero"]:
                transferir_cantidad.delete(0, "end")
                dinero = None
                cantidad = None
                messagebox.showerror("Fondos insuficientes", f"No tienes suficiente dinero para realizar la transferencia!\nDinero disponible {users[user]["dinero"]}")
            elif dinero <= dineroU:
                fecha_transaccion = time.strftime(formato_fecha)
                users[userT]["dinero"] = users[userT]["dinero"] + dinero
                users[user]["dinero"] -= dinero
                users[userT]["actividad_reciente"].append(f"{fecha_transaccion}: Dinero recibido de {user}: {dinero}")
                users[user]["actividad_reciente"].append(f"{fecha_transaccion}: Transferencia de {dinero} a {userT}")
                saveData()
                loadData()
                user_info.config(text=f"Tienes ${users[user]["dinero"]} disponible en tu cuenta")
                transferir_user.delete(0,"end")
                transferir_cantidad.delete(0, "end")
                messagebox.showinfo("Transaccion exitosa!", f"Haz transferido {dinero} a {userT}")
                print(f"El dinero del usuario {userT} ahora es: ","$", users[userT]["dinero"])
                for actividad in users[user]["actividad_reciente"]:
                    actividad_reciente.config(text=f"Actividad reciente:\n{actividad}")
                intento_transferir = True
            else:
                messagebox.showerror("Informacion invalida", "Por favor, ingrese datos NUMERICOS validos")
                transferir_cantidad.delete(0, "end")
                cantidad = None
                cantidad = None

def signOut(): 
    """Funcion para el boton de cerrar sesion.
    """
    user_profile_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)
    users[user]["actividad_reciente"] = [users[user]["actividad_reciente"][-1]]  
    saveData()
    loadData()

def backR():
    """Boton para regresar a home desde el menu de registro.
    """
    set_user.delete(0, "end")
    set_password.delete(0, "end")
    home_frame.pack(fill="both", expand=True)
    sign_up_frame.pack_forget()
    
def backI():
    """ Boton para regresar a home desde el menu de inicio de sesion.
    """
    userIn.delete(0, "end")
    passwordIn.delete(0, "end")
    home_frame.pack(fill="both", expand=True)
    login_frame.pack_forget()
    
def backRe():
    """Boton para regresar al perfil de usuario desde el menu de retirar.
    """
    retirar_cantidad.delete(0, "end")
    user_profile_frame.pack(fill="both", expand=True)
    retirar_frame.pack_forget()
    
def backDel():
    """ Boton para regresar a home desde el menu de eliminar usuario.
    """
    delete_user_in.delete(0, "end")
    home_frame.pack(fill="both", expand=True)
    delete_user_frame.pack_forget()
    
def backDe():
    """ Boton para regresar al perfil de usuario desde el menu de deposito.
    """
    depositar_cantidad.delete(0, "end")
    user_profile_frame.pack(fill="both", expand=True)
    depositar_frame.pack_forget()

def backTr():
    """Boton para cerrar el menu de transferencia y regresar al perfil de usuario.
    """
    transferir_user.delete(0, "end")
    transferir_cantidad.delete(0, "end")
    user_profile_frame.pack(fill="both", expand=True)
    transferir_frame.pack_forget()

##FUNCIONES PARA GUARDAR Y CARGAR DATOS DEL USUARIO
def saveData():
    """Funcion para guardar informacion de los usuarios almacenada en el diccionario de {users}.
    """
    global users, users_number 
    with open("users.json", "w") as archivo: ##Crear archivo con nombre "users", w = writte (escribir)
            json.dump(users, archivo) ##Tomar elemento y hacerlo un archivo (debe estar en w)
            #print("Datos guardados exitosamente.") ##Mensaje de aviso [prueba]

def loadData():
    """Funcion para cargar los datos al programa desde el JSON generado con saveData().
    """
    global users, users_number
    try: ##Hacer intento para abrir el archivo
        with open("users.json", "r") as archivo: ##Abrir el archivo "users.json", "r" = read (leer)
            users = json.load(archivo) ##Asignar los datos del archivo a una variable
            users_number = len(users) ##Simplemente revisar el numero de usuarios
            #print("Datos cargados exitosamente") ##Mensaje de aviso [prueba]
            #print(users) ##Revisar que datos hay [prueba]
    except FileNotFoundError: ##Mandar un error de tipo FileNotFoundError, solo es un manejo de errores por usar try
        print("No se encontró el archivo, iniciando con datos predeterminados.") ##Aviso
        users = {} ##Cargar datos en caso de no encontrar el archivo

def getTime():
    """Funcion para obtener la hora actual [en desarrollo xd].
    """
    print("XD")

loadData() ##Cargar los datos 

# def ruta_recurso(rel_path):
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, rel_path)

##INICIO DE PROGRAMA EN VENTANA
home = tk.Tk()
home.title("Inicio")
home.geometry("800x600")
home.resizable(False, False)
home.configure(bg=bg_color)
home.tk.call('tk', 'scaling', 3.0)
home.protocol("WM_DELETE_WINDOW", closeApp)
home.iconbitmap("icono.ico")

user_number = len(users)

##homeFrame
home_frame = tk.Frame(home, bg=bg_color)
home_frame.pack_propagate(False)
home_frame.pack(fill="both", expand=True)
home.protocol("WM_DELETE_WINDOW", closeApp)

# img = tk.PhotoImage(file="img.png")
# lbl_img = tk.Label(home_frame, image=img)
# lbl_img.pack(side="left")
#img.pack(side="left")
welcome_mensaje = tk.Label(home_frame, text=f"¡Hola, bienvenido a MiCajita de ahorro!", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
welcome_mensaje.pack(pady=10)
# user_message = tk.Label(home_frame, text=f"Hay {user_number} usuario(s) registrado(s).", font=("Arial", 10), bg=lbl_color, fg=lbl_txt_color)
# user_message.pack(pady=10)
if(user_number == 0):
    user_message = tk.Label(home_frame, text="No hay usuarios registrados", font=("Arial", 10), bg=lbl_color, fg=lbl_txt_color)
    user_message.pack(pady=10)
else: 
    user_message = tk.Label(home_frame, text="¿Quien va a usar el programa?", font=("Arial", 10), bg=lbl_color, fg=lbl_txt_color)
    user_message.pack(pady=10)

##Botones para el menu de inicio (home)
login_btn_home = tk.Button(home_frame, text="Iniciar sesion", command=loginBtn, width=16, bg=btn_color, fg=btn_txt_color)
login_btn_home.pack(pady=10)

signUp_btn_home = tk.Button(home_frame, text="Registrarse", command=signUpBtn, width=16, bg=btn_color, fg=btn_txt_color)
signUp_btn_home.pack(pady=10)

##Opcion para eliminar a un usuario
delete_user_btn = tk.Button(home_frame, text="Eliminar usuario", command=deleteUserBtn, width=16, bg=btn_color, fg=btn_txt_color)
delete_user_btn.pack(pady=10)

close_btn_home = tk.Button(home_frame, text="Salir", command=closeBtn, width=16, bg=btn_color, fg=btn_txt_color)
close_btn_home.pack(pady=10)

##LOGIN FRAME
login_frame = tk.Frame(home, bg=bg_color)
login_frame.pack_propagate(False)
login_frame.pack_forget()

login_screen = tk.Label(login_frame, text="Vamos a iniciar sesion!", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
login_screen.pack(pady=10)
# Crear un Entry para texto
user_indication = tk.Label(login_frame, text="Usuario:", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
user_indication.pack(pady=5)
userIn = tk.Entry(login_frame, font=("Arial", 12), bg=entry_color, fg=entry_txt_color)
userIn.pack()

password_indication = tk.Label(login_frame, text="Contraseña:", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
password_indication.pack(pady=5)
passwordIn = tk.Entry(login_frame, font=("Arial", 12), show="*", bg=entry_color, fg=entry_txt_color)
passwordIn.pack()

login_Btn = tk.Button(login_frame, text="Iniciar sesion", command=login, bg=btn_color, fg=btn_txt_color, width=14)
login_Btn.pack(pady=10)

backI = tk.Button(login_frame, text="Regresar", command=backI, width=14, bg=btn_color, fg=btn_txt_color)
backI.pack(pady=10)

##SIGN UP FRAME##################################################################################################
sign_up_frame = tk.Frame(home, bg=bg_color)
sign_up_frame.pack_propagate(False)
sign_up_frame.pack_forget()

sing_up_message = tk.Label(sign_up_frame, text="Vamos a registrarte!", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
sing_up_message.pack(pady=10)
set_user_lbl = tk.Label(sign_up_frame, text="Crea el nombre de usuario: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
set_user_lbl.pack(pady=10)
set_user = tk.Entry(sign_up_frame, font=("Arial", 12), bg=entry_color, fg=entry_txt_color)
set_user.pack(pady=10)
set_password_lbl = tk.Label(sign_up_frame, text="Crea tu contraseña: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
set_password_lbl.pack(pady=5)
set_password = tk.Entry(sign_up_frame, font=("Arial", 12), show="*", bg=entry_color, fg=entry_txt_color)
set_password.pack(pady=5)

sign_up_btn = tk.Button(sign_up_frame, text="Registrarse", command=sign_up, width="10", bg=btn_color, fg=btn_txt_color)
sign_up_btn.pack(pady=10)

backR = tk.Button(sign_up_frame, text="Regresar", command=backR,width="10", bg=btn_color, fg=btn_txt_color)
backR.pack(pady=10)

############################################################################################################################
##DELETE USER FRAME
delete_user_frame = tk.Frame(home, bg=bg_color)
delete_user_frame.pack_propagate(False)
delete_user_frame.pack_forget()

delete_user_lbl = tk.Label(delete_user_frame, text="Vas a eliminar a un usuario", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
delete_user_lbl.pack(pady=10)
delete_user_txt = tk.Label(delete_user_frame, text="Ingresa el usuario a eliminar: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
delete_user_txt.pack(pady=10)
delete_user_in = tk.Entry(delete_user_frame, font=("Arial", 12), bg=entry_color, fg=entry_txt_color)
delete_user_in.pack(pady=10)
confirm_delete_user = tk.Button(delete_user_frame, text="Eliminar", command=deleteUser, bg=btn_color, fg=btn_txt_color)
confirm_delete_user.pack(pady=10)
back_delete = tk.Button(delete_user_frame, text="Regresar", command=backDel, bg=btn_color, fg=btn_txt_color)
back_delete.pack(pady=10)

##USER PROFILE FRAME
username = user

user_profile_frame = tk.Frame(home, bg=bg_color)
login_message = tk.Label(user_profile_frame, text=f"¡Hola {username}, bienvenido a MiAhorro!", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
login_message.pack(pady=10)

user_info = tk.Label(user_profile_frame, text=f"Tienes ___ pesos disponibles en tu cuenta ", bg=lbl_color, fg=lbl_txt_color)
user_info.pack(pady=10) 
##Opcion depositar
depositar_btn = tk.Button(user_profile_frame, text="Depositar", command=depositar, width=16, bg=btn_color, fg=btn_txt_color)
depositar_btn.pack(pady=10)

##Opcion retirar
retirar_btn = tk.Button(user_profile_frame, text="Retirar", command=retirar, width=16, bg=btn_color, fg=btn_txt_color)
retirar_btn.pack(pady=10)

#opcion transferir
transferir_btn = tk.Button(user_profile_frame, text="Transferir", command=transferir, width=16, bg=btn_color, fg=btn_txt_color )
transferir_btn.pack(pady=10)

##Opcion cerrar sesion
cerrar_sesion = tk.Button(user_profile_frame, text="Cerrar sesion", command=signOut, width=16, bg=btn_color, fg=btn_txt_color)
cerrar_sesion.pack(pady=10)

##Actividad reciente
actividad_reciente = tk.Label(user_profile_frame, text="Actividad reciente: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
actividad_reciente.pack(pady=10)

##DEPOSITAR FRAME
depositar_frame = tk.Frame(home, bg=bg_color)
depositar_frame.pack_propagate(False)
depositar_frame.pack_forget()

##Entradas y botones
depositar_lbl = tk.Label(depositar_frame, text="Vas a depositar", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
depositar_lbl.pack(pady=10)
depositar_txt = tk.Label(depositar_frame, text="Cantidad a depositar: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
depositar_txt.pack(pady=10)

depositar_cantidad = tk.Entry(depositar_frame, font=("Arial", 14), bg=entry_color, fg=entry_txt_color)
depositar_cantidad.pack(pady=10)

confirmar = tk.Button(depositar_frame, text="Depositar", command=realizarDeposito, width=10, bg=btn_color, fg=btn_txt_color)
confirmar.pack(pady=10)

backDe = tk.Button(depositar_frame, text="Regresar", command=backDe, width=10, bg=btn_color, fg=btn_txt_color)
backDe.pack(pady=10)

##RETIRAR FRAME
retirar_frame = tk.Frame(home, bg=bg_color)
retirar_frame.pack_propagate(False)
retirar_frame.pack_forget()

##Entradas y botones
retirar_lbl = tk.Label(retirar_frame, text="Vas a retirar", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
retirar_lbl.pack(pady=10)
retirar_txt = tk.Label(retirar_frame, text="Cantidad a retirar: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
retirar_txt.pack(padx=10)

retirar_cantidad = tk.Entry(retirar_frame, font=("Arial", 12), bg=entry_color, fg=entry_txt_color)
retirar_cantidad.pack(pady=10)

confirmar_r = tk.Button(retirar_frame, text="Retirar", command=realizarRetiro, width=16, bg=btn_color, fg=btn_txt_color)
confirmar_r.pack(pady=10)

backRe = tk.Button(retirar_frame, text="Regresar", command=backRe, width=16, bg=btn_color, fg=btn_txt_color)
backRe.pack(pady=10)

#TRANSFERIR FRAME
transferir_frame = tk.Frame(home, bg=bg_color)
transferir_frame.pack_propagate(False)
transferir_frame.pack_forget()

#entradas y botones
transferir_lbl = tk.Label(transferir_frame, text="Vas a transferir!", font=("Arial", 14), bg=lbl_color, fg=lbl_txt_color)
transferir_lbl.pack(pady=10)
transferir_txt = tk.Label(transferir_frame, text="Ingresa el usuario al que deseas transferir: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
transferir_txt.pack(pady=10)
transferir_user = tk.Entry(transferir_frame, font=("Arial", 12), bg=entry_color, fg=entry_txt_color)
transferir_user.pack(pady=10)
transferir_cantidad_txt = tk.Label(transferir_frame, text="Ingresa la cantidad a transferir: ", font=("Arial", 8), bg=lbl_color, fg=lbl_txt_color)
transferir_cantidad_txt.pack(pady=10)
transferir_cantidad = tk.Entry(transferir_frame, font=("Arial", 12), width=16, bg=entry_color, fg=entry_txt_color)
transferir_cantidad.pack(pady=10)
confirmar_transferir = tk.Button(transferir_frame, text="Transferir", command=realizarTransferencia, width=16, bg=btn_color, fg=btn_txt_color)
confirmar_transferir.pack(pady=10)
backTr = tk.Button(transferir_frame, text="Regresar", command=backTr, width=16, bg=btn_color, fg=btn_txt_color)
backTr.pack(pady=10)

home.mainloop() ##FIN del programa
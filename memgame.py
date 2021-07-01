''' =============================================================
            ==== JUEGO DE MEMORIA CON COLORES =====

    El objetivo de este programa es crear un juego usando el
    módulo GUI Tkinter de Python. El juego consiste en hallar
    cada par de colores similares entre 16 opciones posibles,
    hasta descubrir todo el tablero con cada par de color (para
    un total de 8 aciertos). Se lleva igualmente el conteo de
    intentos y de acuerdo a los intentos totales se muestra un
    mensaje de resultado distinto al usuario en una ventana 
    emergente y se pregunta si desea volver a jugar o no.

    Se hace uso de herramientas GUI como ventanas (principal y
    emergente), botones, labels y frames. También se hace uso 
    de módulos para manejo de funciones parciales, de lambdas,
    de timers de tipo threading (hilos) y de random.shuffle 
    (para establecer los colores a descubrir del tablero al azar).

    Autor: Mao Moreno
    Fecha: 01/06/2021
    ============================================================= '''

#============ Llamado a módulos usados ================
from tkinter import Tk, Toplevel, Frame, Button, Label, StringVar
from random import shuffle
from functools import partial
from threading import Timer
from sys import exit as terminar
#============ Constantes ================
colores = ["red", "blue", "yellow", "green", "orange", "purple", "cyan", "black"] * 2
egg = "Juego programado por: Fabián Mauricio Moreno Camargo - 2021"
ancho_tablero, alto_tablero = 680, 700
#============ Ventana principal (tablero) ================
tablero = Tk()
tablero.state(newstate = "withdraw") # tablero no se muestra (queda invisible)
x = (tablero.winfo_screenwidth() - ancho_tablero) // 2 # Calcula posicion central en x con respecto a la pantalla
y = (tablero.winfo_screenheight() - alto_tablero) // 2 # Calcula posicion central en y con respecto a la pantalla
tablero.geometry("{}x{}+{}+{}".format(ancho_tablero, alto_tablero, x, y)) # formato "WxH+x+y"
tablero.title("ColorsMemGame (4 x 4)")
#tablero.iconbitmap('colors.ico') # Ruta relativa donde se encuentra el ícono (.ico) - No sirve al compilar
tablero.resizable(width=False, height=False) # tablero.resizable(0, 0) - Bloquea el tamaño del tablero
tablero.state(newstate = "normal") # Abre/hace visible tablero
#============ Frame (para botones) ================
frame = Frame(tablero)
frame.pack()
#============ Botones ================
botones = [Button(frame, width = 20, height = 8, bg = "lightgray", cursor = "hand2") for i in range(16)]
for i in range(16):
    botones[i].grid(row = i // 4, column = i % 4)
#============ Labels (status del juego) ================
ints = Label(tablero, font = ("Segoe UI", 14, "bold"))
ints.place(relx = .15, rely = .95)
acrt = Label(tablero, font = ("Segoe UI", 14, "bold"))
acrt.place(relx = .65, rely = .95)
str_egg = Label(tablero, font = ("Segoe Print", 13, "bold"), text = egg)
#============ Strings variables ================
intentos_str = StringVar()
aciertos_str = StringVar()
#============ Funcionalidades ================
def iniciar_juego():
    global intentos, aciertos, seleccion
    seleccion = [] # Variable que guarda el par de botones pulsados que deben ser verificados
    intentos = aciertos = 0
    intentos_str.set(f"Intentos = {intentos}")
    aciertos_str.set(f"Aciertos = {aciertos}")
    ints.config(textvariable = intentos_str)
    acrt.config(textvariable = aciertos_str)
    restaurar_botones(list(range(16)))
    comandos_botones()
    shuffle(colores) # Reordena la lista de colores al azar

def evaluar():
    # Evalúa si hay o no una pareja, y si ya se completó el juego
    global intentos, aciertos
    intentos += 1
    intentos_str.set(f"Intentos = {intentos}")
    if colores[seleccion[0]] != colores[seleccion[1]]: # Si no hay pareja
        t = Timer(.5, partial(restaurar_botones, seleccion)) # Crea un timer usando hilos - threading (pues time.sleep no sirve)
        t.start()
    else:
        aciertos += 1
        aciertos_str.set(f"Aciertos = {aciertos}")
        if aciertos == 8: # Si ya se completó el juego (8 aciertos):
            mensaje_final()

def elegir_boton(pos: int):
    # Cuando se pulsa un botón:
    global seleccion
    botones[pos].config(state = "disabled", bg = colores[pos], cursor = "X_cursor") # Inhabilita y cambia color de botón elegido
    seleccion.append(pos) # Añade la posición relativa correspondiente del botón a la lista selección
    if len(seleccion) == 2:  # Verifica si ya hay 2 elementos (pares de botones) en la lista selección
        evaluar()
        seleccion = [] # Borra la lista

def restaurar_botones(opcion:list):
    # Vuelve los botones especificados en la lista opción a su estado normal
    for sel in opcion:
        botones[sel].config(state = "normal", bg = "lightgray", cursor = "hand2")

def comandos_botones():
    # Asigna el respectivo comando a cada botón
    for i in range(16):
        botones[i].config(command = partial(elegir_boton, i))

def mensaje_final(): 
    # Crea y abre una ventana emergente cuando el juego acaba, mostrando un 
    # mensaje y preguntando si se quiere volver a comenzar o salir del juego
    global ok, salir
    ancho_ventana, alto_ventana = 320, 200
    mensajes = ["¡Eres todo un genio!", 
                "¡Excelente!",
                "¡Muy bien!",
                "¡Nada mal!",
                "¡Puedes mejorar!",
                "¡Te falta práctica!",
                "¡Tienes memoria de pollo!"]
    mensaje = "\n" + mensajes[(intentos - 1) // 5 - 1] + f"\nLo lograste en {intentos} intentos"
    #============ Creación y apertura ventana emergente ================
    ventana = Toplevel(tablero) # Crea ventana (dependiente de tablero)
    ventana.withdraw() # Mantiene ventana invisible
    ventana.attributes("-disabled") #ventana.overrideredirect(1) - Bloquea ventana (no se puede cambiar tamaño, minimizar o cerrar)
    x = tablero.winfo_x() + (ancho_tablero - ancho_ventana)// 2  # Calcula posición central en x con respecto a tablero
    y = tablero.winfo_y() + (alto_tablero - alto_ventana)// 2  # Calcula posición central en y con respecto a tablero
    ventana.geometry("{}x{}+{}+{}".format(ancho_ventana, alto_ventana, x, y)) # formato "WxH+x+y"
    ventana.title("Juego terminado")
    #ventana.iconbitmap('colors.ico') #No sirve al compilar
    ventana.deiconify() # Abre/restaura/vuelve visible ventana
    ventana.focus_set() # Mantiene el foco en la ventana
    ventana.grab_set_global() # Impide que la ventana del tablero sea movida
    #============ Labels ventana (mensajes) ================
    Label(ventana, font = ("Segoe UI", 15, "bold italic"), text = mensaje).pack(anchor = "center")
    Label(ventana, font = ("Segoe UI", 13), text = "\n¿Quieres volver a intentar?\n").pack(anchor = "center")
    #============ Botones ventana (OK y Salir) ================
    fuente = ("Segoe UI", 12, "bold")
    comandos = lambda:(ventana.destroy(), iniciar_juego()) # Comandos para OK (usando lambdas): Destruye la ventana y re-inicia el juego
    ok = Button(ventana, width = 7, font = fuente, text = "¡Vale!",  bg = "lightgray", command = comandos)
    ok.place(relx = .15, rely = .75) 
    salir = Button(ventana, width = 10, font = fuente, text = "Después...",  bg = "lightgray", command = terminar)
    salir.place(relx = .50, rely = .75)
    #============ Otras instrucciones ================
    reset_clicks()
    ventana.bind("<Button-3>", easter_egg) # Huevo de pascua

def reset_clicks():
    global clicks
    clicks = 0

def easter_egg(event):
    #============ ( ͡° ͜ʖ ͡°) ============
    global clicks
    clicks += 1
    if clicks == intentos:
        str_egg.pack(anchor = "s")
        ok.config(state = "disabled")
        salir.config(state = "disabled")
        # Comandos para el timer, usando lambdas:
        comandos = lambda:(str_egg.pack_forget(), ok.config(state = "normal"), salir.config(state = "normal"), reset_clicks())
        t = Timer(3, comandos) # Crea un timer usando hilos - threading (pues time.sleep no sirve)
        t.start()

#============ mainloop ================
iniciar_juego()
tablero.mainloop()
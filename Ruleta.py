import tkinter as tk
from tkinter import messagebox  # Importación correcta de messagebox
import random
import math

# Configuración básica de la ruleta
numeros = list(range(37))  # Números del 0 al 36
colores = {  # Colores de cada número en la ruleta europea
    0: "green",
    **{num: "red" if num in (
        1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36) else "black" #Los colores hay que escribirlos en inglés (valen red, black, green)
       for num in range(1, 37)}
}
tabla_pagos = {"número": 36, "color": 2, "paridad": 2, "rango":3}

# Función para girar la ruleta
def girar_ruleta():
    numero_ganador = random.choice(numeros)
    color_ganador = colores[numero_ganador]
    return numero_ganador, color_ganador

# Función para calcular el resultado y el pago
def calcular_resultado(apuesta, tipo_apuesta, numero_ganador, color_ganador):
    ganancia = 0
    exito = False
    if tipo_apuesta == "número":
        if apuesta == numero_ganador:
            ganancia = tabla_pagos[tipo_apuesta] * apuesta_inicial
            exito = True
    elif tipo_apuesta == "color":
        if apuesta == color_ganador:
            ganancia = tabla_pagos[tipo_apuesta] * apuesta_inicial
            exito = True
    elif tipo_apuesta == "paridad":
        if (apuesta == "par" and numero_ganador % 2 == 0) or (apuesta == "impar" and numero_ganador % 2 != 0):
            ganancia = tabla_pagos[tipo_apuesta] * apuesta_inicial
            exito = True
    elif tipo_apuesta == "rango":
        if (apuesta == "1-12" and 1 <= numero_ganador <= 12) or (apuesta == "13-24" and 13 <= numero_ganador <= 24) or (apuesta == "25-36" and 25 <= numero_ganador <= 36):
            ganancia = tabla_pagos[tipo_apuesta] * apuesta_inicial
            exito = True
    return ganancia, exito

# Interfaz gráfica con Tkinter
class RuletaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruleta de Apuestas")
        self.apuesta_inicial = 0
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="Tipo de Apuesta:").grid(row=0, column=0)
        self.tipo_apuesta = tk.StringVar(value="número")
        tk.OptionMenu(self.root, self.tipo_apuesta, "número", "color", "paridad", "rango").grid(row=0, column=1)

        tk.Label(self.root, text="Apuesta:").grid(row=1, column=0)
        self.entry_apuesta = tk.Entry(self.root)
        self.entry_apuesta.grid(row=1, column=1)

        tk.Label(self.root, text="Cantidad a Apostar:").grid(row=2, column=0)
        self.entry_cantidad = tk.Entry(self.root)
        self.entry_cantidad.grid(row=2, column=1)

        self.resultado_label = tk.Label(self.root, text="Resultado: ")
        self.resultado_label.grid(row=3, column=0, columnspan=2)

        tk.Button(self.root, text="Girar Ruleta", command=self.jugar).grid(row=4, column=0, columnspan=2)

        # Canvas para la ruleta
        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.grid(row=5, column=0, columnspan=2)
        self.dibujar_ruleta()

    def dibujar_ruleta(self):
        self.canvas.create_oval(20, 20, 180, 180, fill="green")
        for i, num in enumerate(numeros):
            angle = i * (360 / 37)
            x = 100 + 70 * math.cos(math.radians(angle))
            y = 100 + 70 * math.sin(math.radians(angle))
            color = colores[num]
            self.canvas.create_text(x, y, text=str(num), fill=color)

    def jugar(self):
        global apuesta_inicial
        apuesta_inicial = int(self.entry_cantidad.get())
        tipo_apuesta = self.tipo_apuesta.get()
        apuesta = self.entry_apuesta.get()

        if tipo_apuesta == "número":
            apuesta = int(apuesta)
        numero_ganador, color_ganador = girar_ruleta()

        ganancia, exito = calcular_resultado(apuesta, tipo_apuesta, numero_ganador, color_ganador)
        self.mostrar_resultado(numero_ganador, color_ganador, ganancia, exito)

    def mostrar_resultado(self, numero_ganador, color_ganador, ganancia, exito):
        self.resultado_label.config(text=f"Resultado: {numero_ganador} ({color_ganador})")
        if exito:
            messagebox.showinfo("Ganaste", f"¡Felicidades! Ganaste {ganancia} euros.")
        else:
            messagebox.showinfo("Perdiste", "Perdiste tu apuesta.")

# Ejecutar la aplicación
root = tk.Tk()
app = RuletaApp(root)
root.mainloop()

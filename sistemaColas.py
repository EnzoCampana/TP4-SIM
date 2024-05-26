"""
N LINEAS PARA VER - EJEMPLO 5000
NUMERO DE LINEA A PARTIR DESDE DONDE VER - POR EJEMPLO LINEA 5 (MUESTRA SOLO 300 DE ELLAS, HASTA LA 305)
CABECERA VECTOR DE ESTADO (PRIMERA FILA)
ULTIMA FILA DEL VECTOR DE ESTADO

Objetos

Clientes -> Pacientes
estados: siendo atendido, esperando

Servidores -> dependen del area
estados: atendiendo, libre

Eventos

llegada_paciente ( exponencial PERO SU DISTRIBUCION DEPENDE DEL AREA)
fin_atencion_paciente ( SU DISTRIBUCION DEPENDE DEL AREA)

"""

import random
import math
import tkinter as tk
from tkinter import ttk

class Paciente:
    def __init__(self, id, hora_llegada, area, estado):
        self.id = id
        self.hora_llegada = hora_llegada
        self.hora_salida = None
        self.area = area
        self.estado = estado

class Servidor:
    def __init__(self, id, tasa_servicio):
        self.id = id
        self.tasa_servicio = tasa_servicio
        self.estado = "L"  # Libre
        self.cola = []

def llegada_paciente(reloj, tasa, area):
    tiempo_entre_llegadas = generar_tiempo_exponencial(tasa)
    prox_llegada = reloj + tiempo_entre_llegadas
    paciente = Paciente(len(pacientes), prox_llegada, area, "Esperando")
    return prox_llegada, paciente

def fin_atencion_paciente(reloj, tasa):
    tiempo_atencion = generar_tiempo_exponencial(tasa)
    fin_atencion = reloj + tiempo_atencion
    return fin_atencion

def generar_tiempo_exponencial(tasa):
    return -math.log(1 - random.random()) / tasa

def simular_farmacia(N, tasa_llegada, tasa_servicio):
    reloj = 0
    cantidad_farmaceuticos = 2
    farmaceuticos = [Servidor(i, tasa_servicio) for i in range(cantidad_farmaceuticos)]
    global pacientes
    pacientes = []

    prox_llegada, paciente = llegada_paciente(reloj, tasa_llegada, "Farmacia")
    pacientes.append(paciente)

    # Definir la lista de eventos
    eventos = [(prox_llegada, "llegada", paciente)]
    
    while len(pacientes) < N:
        eventos.sort(key=lambda x: x[0])
        reloj, tipo_evento, entidad = eventos.pop(0)
        
        if tipo_evento == "llegada":
            paciente = entidad
            pacientes.append(paciente)
            asignar_a_farmaceutico(paciente, farmaceuticos, reloj, eventos)

            prox_llegada, nuevo_paciente = llegada_paciente(reloj, tasa_llegada, "Farmacia")
            eventos.append((prox_llegada, "llegada", nuevo_paciente))
        
        elif tipo_evento == "fin_atencion":
            farmaceutico = entidad
            if farmaceutico.cola:
                paciente_atendido = farmaceutico.cola.pop(0)
                paciente_atendido.estado = "Atendido"
                paciente_atendido.hora_salida = reloj

                if farmaceutico.cola:
                    prox_fin_atencion = fin_atencion_paciente(reloj, farmaceutico.tasa_servicio)
                    eventos.append((prox_fin_atencion, "fin_atencion", farmaceutico))
                else:
                    farmaceutico.estado = "L"

def asignar_a_farmaceutico(paciente, farmaceuticos, reloj, eventos):
    for farmaceutico in farmaceuticos:
        if farmaceutico.estado == "L":
            farmaceutico.cola.append(paciente)
            farmaceutico.estado = "Ocupado"
            paciente.estado = "Siendo Atendido"
            prox_fin_atencion = fin_atencion_paciente(reloj, farmaceutico.tasa_servicio)
            eventos.append((prox_fin_atencion, "fin_atencion", farmaceutico))
            return

    menor_cola = min(farmaceuticos, key=lambda f: len(f.cola))
    menor_cola.cola.append(paciente)

def mostrar_resultados(pacientes):
    root = tk.Tk()
    root.title("Simulación del Centro de Salud")

    tree = ttk.Treeview(root)
    tree["columns"] = ("Evento", "Reloj", "Hora de Salida", "Área", "Estado")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Evento", anchor=tk.CENTER, width=50)
    tree.column("Reloj", anchor=tk.CENTER, width=150)
   
    tree.heading("#0", text="", anchor=tk.CENTER)
    tree.heading("Evento", text="Evento", anchor=tk.CENTER)
    tree.heading("Reloj", text="Reloj", anchor=tk.CENTER)
   

    for paciente in pacientes:
        tree.insert("", tk.END, values=(paciente.id, round(paciente.hora_llegada, 2)))

    tree.pack()
    root.mainloop()

# Parámetros de la simulación
N = 5000  # Número de líneas para ver
tasa_llegada = 25  # Tasa de llegada de pacientes
tasa_servicio = 15  # Tasa de servicio de los farmacéuticos

# Ejecutar simulación
simular_farmacia(N, tasa_llegada, tasa_servicio)

# Mostrar resultados en una tabla de Tkinter
mostrar_resultados(pacientes)

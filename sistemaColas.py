import random
import math
import pyQt5

class Area:
    def __init__(self, nombre, cantidad_especialistas, especialistas):
        self.nombre = nombre
        self.cantidad_especialistas = cantidad_especialistas
        self.especialistas = especialistas

class Especialista:
    def __init__(self, tasa_servicio):
        self.tasa_servicio = tasa_servicio
        self.estado = "L"  # Libre # Atendiendo
        self.cola = []

class Paciente:
    def __init__(self, id, hora_llegada,estado, area, puesto):
        self.id = id
        self.hora_llegada = hora_llegada
        self.hora_salida = None
        self.estado = estado #Esperando Atencion #Siendo Atendido 
        self.area = area
        self.puesto = puesto
  
def buscar_tasa_llegada_por_area(area):
    tasas_por_area = {
        "consulta": 30,
        "odontologia": 12,
        "pediatria": 10,
        "laboratorio": 20,
        "farmacia": 25
    }
    return tasas_por_area.get(area, "Área no válida")

def buscar_tasa_atencion_por_area(area):
    tasas_por_area = {
        "consulta": 6,
        "odontologia": 4,
        "pediatria": 5,
        "laboratorio": 8,
        "farmacia": 15
    }
    return tasas_por_area.get(area, "Área no válida")
        
def generar_tiempo_exponencial(tasa):
    lambd = tasa / 60
    return -1/lambd*math.log(1-random.random())

def llegada_paciente(reloj, area):
    tasa = buscar_tasa_llegada_por_area(area)
    tiempo_entre_llegadas = generar_tiempo_exponencial(tasa)
    prox_llegada = reloj + tiempo_entre_llegadas
    paciente = Paciente(len(pacientes), prox_llegada, area, "EA")
    return prox_llegada, paciente

def fin_atencion_paciente(reloj, area):
    tasa = buscar_tasa_llegada_por_area(area)
    tiempo_atencion = generar_tiempo_exponencial(tasa)
    fin_atencion = reloj + tiempo_atencion
    return tiempo_atencion, fin_atencion

def simular_centro_salud(N, tasa_servicio):
    reloj = 0
    global pacientes
    pacientes = []

    cantidad_farmaceuticos = 2
    farmaceuticos = [Especialista(i, tasa_servicio) for i in range(cantidad_farmaceuticos)]

    prox_llegada, paciente = llegada_paciente(reloj, "farmacia")
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

            prox_llegada, nuevo_paciente = llegada_paciente(reloj, "farmacia")
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
        if farmaceutico.estado == "Libre":
            farmaceutico.cola.append(paciente)
            farmaceutico.estado = "Atendiendo"
            paciente.estado = "SA"
            prox_fin_atencion = fin_atencion_paciente(reloj, farmaceutico.tasa_servicio)
            eventos.append((prox_fin_atencion, "fin_atencion", farmaceutico))
            return

    menor_cola = min(farmaceuticos, key=lambda f: len(f.cola))
    menor_cola.cola.append(paciente)

def mostrar_resultados(pacientes):
    pass
    
# Parámetros de la simulación
N = 10  # Número de líneas a simular
tasa_llegada = 25  # Tasa de llegada de pacientes
tasa_servicio = 15  # Tasa de servicio de los farmacéuticos

# Ejecutar simulación
simular_farmacia(N, tasa_llegada, tasa_servicio)

# Mostrar resultados en una tabla de Tkinter
mostrar_resultados(pacientes)

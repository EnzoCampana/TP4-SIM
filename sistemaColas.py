import random
import math
import pyQt5

class Area:
    def __init__(self, nombre, numero_especialistas, tasa):
        self.nombre = nombre
        self.numero_especialistas = numero_especialistas
        self.tasa = tasa
        self.especialistas = []

class Especialista:
    def __init__(self, id, estado):
        self.id = id
        self.estado = estado  # Libre # Atendiendo
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

def simular_centro_salud(N):
    reloj = 0
    global pacientes
    pacientes = []

    areas_info = [
            ("consulta", 5),
            ("odontologia", 3),
            ("pediatria", 2),
            ("laboratorio", 4),
            ("farmacia", 2)
        ]
        
    areas = []
    for area_nombre, numero_especialistas in areas_info:
            tasa = buscar_tasa_atencion_por_area(area_nombre)
            area = Area(area_nombre, numero_especialistas, tasa)
            
            for i in range(numero_especialistas):
                especialista = Especialista(id=i)
                area.especialistas.append(especialista)

            areas.append(area)


    eventos = []
# Inicializar eventos de llegada para cada área
    for area in areas:
        prox_llegada, paciente = llegada_paciente(reloj, area.nombre)
        pacientes.append(paciente)
        eventos.append((prox_llegada, "llegada", paciente))

    # Definir la lista de eventos
    
    while len(pacientes) < N:
        eventos.sort(key=lambda x: x[0])
        reloj, tipo_evento, entidad = eventos.pop(0)

        if tipo_evento == "llegada":
            paciente = entidad
            pacientes.append(paciente)
            for area in areas:
                if area.nombre == paciente.area:
                    asignar_a_especialista(paciente, area.especialistas, reloj, eventos)
            prox_llegada, nuevo_paciente = llegada_paciente(reloj, paciente.area)
            eventos.append((prox_llegada, "llegada", nuevo_paciente))

        elif tipo_evento == "fin_atencion":
            especialista = entidad
            if especialista.cola:
                paciente_atendido = especialista.cola.pop(0)
                paciente_atendido.estado = "Atendido"
                paciente_atendido.hora_salida = reloj

                if especialista.cola:
                    prox_fin_atencion = fin_atencion_paciente(reloj, especialista.tasa_servicio)
                    eventos.append((prox_fin_atencion, "fin_atencion", especialista))
                else:
                    especialista.estado = "L"

def asignar_a_especialista(paciente, especialistas, reloj, eventos):
    for especialista in especialistas:
        if especialista.estado == "L":
            especialista.cola.append(paciente)
            especialista.estado = "Atendiendo"
            paciente.estado = "SA"
            prox_fin_atencion = fin_atencion_paciente(reloj, especialista.tasa_servicio)
            eventos.append((prox_fin_atencion, "fin_atencion", especialista))
            return

    menor_cola = min(especialistas, key=lambda e: len(e.cola))
    menor_cola.cola.append(paciente)

# Parámetros de la simulación

N = 10  # Número de líneas a simular

# Ejecutar simulación
simular_centro_salud(N)

import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, \
    QPushButton, QScrollArea
from PyQt5.QtGui import QColor
import sys


class Area:
    def __init__(self, nombre, cantidad_especialistas, media_llegada, media_atencion):
        self.nombre = nombre
        self.cantidad_especialistas = cantidad_especialistas
        self.cola_area = []
        self.media_llegada = media_llegada
        self.media_atencion = media_atencion

        self.medicos = [Medico(i) for i in range(cantidad_especialistas)]

        self.pacientes_atendidos = []

    def agregar_paciente_atendido(self, paciente):
        self.pacientes_atendidos.append(paciente)

    def quitar_paciente_atendido(self, paciente):
        self.pacientes_atendidos.remove(paciente)


class Medico:
    def __init__(self, id):
        self.id = id
        self.estado = "libre"  # "libre" o "atendiendo"


class Paciente:
    def __init__(self, tiempo_ingreso):
        self.estado = "esperando_atencion"  # "esperando_atencion" o "siendo_atendido"
        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None
        # es necesario para liberar a ese medico cuando termine la atencion
        self.medico_asignado = None


def generar_tiempo_exponencial(media):
    return -media * math.log(1 - random.random())


def generar_tiempo_entre_llegadas(media):
    tiempo_entre_llegadas = generar_tiempo_exponencial(media)
    return tiempo_entre_llegadas


def generar_tiempo_atencion(media):
    tiempo_atencion = generar_tiempo_exponencial(media)
    return tiempo_atencion


class SimulacionCentroSalud:
    def __init__(self):
        self.reloj = 0
        self.tiempo_total_simulacion = 60
        self.cantidad_eventos_a_simular = 300
        self.eventos = []
        # crear las areas
        self.areas = []
        self.nombre_areas = ["consulta", "odontologia", "pediatria", "laboratorio", "farmacia"]
        self.especialistas_por_area = [5, 3, 2, 4, 2]
        self.media_llegadas_area = [30, 12, 10, 20, 25]
        self.media_atencion_area = [6, 4, 5, 8, 15]

        for i in range(len(self.nombre_areas)):
            self.areas.append(Area(self.nombre_areas[i],
                                   self.especialistas_por_area[i],
                                   self.media_llegadas_area[i],
                                   self.media_atencion_area[i]))

        # estos datos son para calcular los estadisticos q pide
        self.pacientes_atendidos = 0
        self.tiempo_permanencia_total = 0
        self.pacientes_atendido_consulta = 0
        self.pacientes_atendidos_odontolo = 0
        self.pacientes_atendidos_pediatr = 0
        self.pacientes_atendidos_laborator = 0
        self.pacientes_atendidos_farm = 0
        self.tiempoEsperaPromedioFarm = 0
        self.tiempoEsperaPromedioConsulta = 0
        self.tiempoEsperaPromedioOdonto = 0
        self.tiempoEsperaPromedioLabora = 0
        self.tiempoEsperaPromedioPedia = 0
        self.tiempo_permanencia_totalCons = 0
        self.tiempo_permanencia_totalOdon = 0
        self.tiempo_permanencia_totalPed = 0
        self.tiempo_permanencia_totalLab = 0
        self.tiempo_permanencia_totalFarm = 0
        self.tabla_resultados = []  # evento, reloj,
        self.diccionario = {
            "Evento": "Inicializacion",
            "Reloj": "0",
            "llegada paciente consulta": {
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente odontologia": {
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente pediatria": {
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente laboratorio": {
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente farmacia": {
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "Fin atencion consulta": {
                "Tiempo atencion": "0",
                "Fin atencion": "0"
            },
            "Fin atencion odontologia": {
                "Tiempo atencion": "0",
                "Fin atencion": "0"
            },
            "Fin atencion pediatria": {
                "Tiempo atencion": "0",
                "Fin atencion": "0"
            },
            "Fin atencion laboratorio": {
                "Tiempo atencion": "0",
                "Fin atencion": "0"
            },
            "Fin atencion farmacia": {
                "Tiempo atencion": "0",
                "Fin atencion": "0"
            },
            "Tiempo de espera promedio": {
                "Consulta general": "0",
                "Odontologia": "0",
                "Pediatria": "0",
                "Laboratorio": "0",
                "Farmacia": "0"
            },
            "Cola de consultas generales": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Medico 4": "Libre",
                "Medico 5": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de odontologia": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de pediatria": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de laboratorio": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Medico 4": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de farmacia": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            }
        }

    def inicializar(self):
        primeras_llegadas = []  #0consulta 1odont 2ped 3lab 4farm
        for area in self.areas:
            tiempo_primera_llegada = generar_tiempo_entre_llegadas(area.media_llegada)
            self.eventos.append((f"llegada_paciente_{area.nombre}", tiempo_primera_llegada))
            primeras_llegadas.append(tiempo_primera_llegada)

        self.diccionario["Evento"] = "inicializacion"
        self.diccionario["Reloj"] = self.reloj
        self.diccionario["llegada paciente consulta"]["Tiempo entre llegadas"] = primeras_llegadas[0]
        self.diccionario["llegada paciente odontologia"]["Tiempo entre llegadas"] = primeras_llegadas[1]
        self.diccionario["llegada paciente pediatria"]["Tiempo entre llegadas"] = primeras_llegadas[2]
        self.diccionario["llegada paciente laboratorio"]["Tiempo entre llegadas"] = primeras_llegadas[3]
        self.diccionario["llegada paciente farmacia"]["Tiempo entre llegadas"] = primeras_llegadas[4]
        self.diccionario["llegada paciente consulta"]["Proxima llegada"] = primeras_llegadas[0]
        self.diccionario["llegada paciente odontologia"]["Proxima llegada"] = primeras_llegadas[1]
        self.diccionario["llegada paciente pediatria"]["Proxima llegada"] = primeras_llegadas[2]
        self.diccionario["llegada paciente laboratorio"]["Proxima llegada"] = primeras_llegadas[3]
        self.diccionario["llegada paciente farmacia"]["Proxima llegada"] = primeras_llegadas[4]
        lista = self.diccionario_vector()
        self.tabla_resultados.append(lista)
        print(self.diccionario)

    def escribir_fila_tabla_resultados(self, area, evento, tiempo_entre_llegadas, proxima_llegada, tiempo_atencion,
                                       fin_atencion,
                                       pacientes_atendido_consulta, pacientes_atendidos_odontolo,
                                       pacientes_atendidos_pediatr,
                                       pacientes_atendidos_laborator, pacientes_atendidos_farm):
        evento_map = {
            "consulta": ("llegada_paciente_consulta", "Fin atencion consulta"),
            "odontologia": ("llegada_paciente_odontologia", "Fin atencion odontologia"),
            "pediatria": ("llegada_paciente_pediatria", "Fin atencion pediatria"),
            "laboratorio": ("llegada_paciente_laboratorio", "Fin atencion laboratorio"),
            "farmacia": ("llegada_paciente_farmacia", "Fin atencion farmacia")
        }

        if area not in evento_map:
            raise ValueError("Área no reconocida")

        llegada_evento, fin_atencion_evento = evento_map[area]

        # Redondear a 4 decimales
        if tiempo_entre_llegadas is not None:
            tiempo_entre_llegadas = round(tiempo_entre_llegadas, 4)
        if proxima_llegada is not None:
            proxima_llegada = round(proxima_llegada, 4)

        if evento == "llegada":
            self.diccionario[f"llegada paciente {area}"]["Tiempo entre llegadas"] = tiempo_entre_llegadas
            self.diccionario[f"llegada paciente {area}"]["Proxima llegada"] = proxima_llegada

        elif evento == "fin_atencion":
            self.diccionario[f"Fin atencion {area}"]["Tiempo atencion"] = tiempo_atencion
            self.diccionario[f"Fin atencion {area}"]["Fin atencion"] = fin_atencion

        self.diccionario["Evento"] = llegada_evento if evento == "llegada" else fin_atencion_evento
        self.diccionario["Reloj"] = self.reloj
        self.diccionario["pacientes_atendido_consulta"] = pacientes_atendido_consulta
        self.diccionario["pacientes_atendidos_odontolo"] = pacientes_atendidos_odontolo
        self.diccionario["pacientes_atendidos_pediatr"] = pacientes_atendidos_pediatr
        self.diccionario["pacientes_atendidos_laborator"] = pacientes_atendidos_laborator
        self.diccionario["pacientes_atendidos_farm"] = pacientes_atendidos_farm
        lista = self.diccionario_vector()
        self.tabla_resultados.append(lista)
        print(lista)

    def simular(self):
        # aca la condicion de simulacion va a ser un parametro N que va a venir de la interfaz y la cantidad de eventos len(tabla_resultaodos)
        while len(self.tabla_resultados) < self.cantidad_eventos_a_simular:
            # Ordenar eventos por tiempo
            self.eventos.sort(key=lambda evento: evento[1])
            if len(self.eventos) > 0:
                evento_actual = self.eventos.pop(0)
                self.reloj = evento_actual[1]
                tipo_evento = evento_actual[0]

                if tipo_evento == "llegada_paciente_consulta":
                    self.procesar_llegada_paciente("consulta")


                elif tipo_evento == "fin_atencion_paciente_consulta":
                    self.procesar_fin_atencion_paciente("consulta")

                elif tipo_evento == "llegada_paciente_odontologia":
                    self.procesar_llegada_paciente("odontologia")

                elif tipo_evento == "fin_atencion_paciente_odontologia":
                    self.procesar_fin_atencion_paciente("odontologia")


                elif tipo_evento == "llegada_paciente_pediatria":
                    self.procesar_llegada_paciente("pediatria")
                    print(self.diccionario)
                elif tipo_evento == "fin_atencion_paciente_pediatria":
                    self.procesar_fin_atencion_paciente("pediatria")
                    print(self.diccionario)

                elif tipo_evento == "llegada_paciente_laboratorio":
                    self.procesar_llegada_paciente("laboratorio")

                elif tipo_evento == "fin_atencion_paciente_laboratorio":
                    self.procesar_fin_atencion_paciente("laboratorio")


                elif tipo_evento == "llegada_paciente_farmacia":
                    self.procesar_llegada_paciente("farmacia")

                elif tipo_evento == "fin_atencion_paciente_farmacia":
                    self.procesar_fin_atencion_paciente("farmacia")

    def diccionario_vector(self, d=None):
        if d is None:
            d = self.diccionario

        vector = []
        for key, value in d.items():
            if isinstance(value, dict):
                vector.extend(self.diccionario_vector(value))
            else:
                vector.append(value)
        return vector

    def procesar_llegada_paciente(self, nombre_area):
        area_atencion = next((a for a in self.areas if nombre_area == a.nombre), None)
        if area_atencion is None:
            raise ValueError(f"El área {nombre_area} no existe")

        nuevo_paciente = Paciente(self.reloj)
        tiempo_entre_llegadas = generar_tiempo_entre_llegadas(area_atencion.media_llegada)
        proxima_llegada = self.reloj + tiempo_entre_llegadas
        llave = self.buscar_key(area_atencion.nombre, "llegada")
        self.diccionario[llave]["Tiempo entre llegadas"] = tiempo_entre_llegadas
        self.diccionario[llave]["Proxima llegada"] = proxima_llegada
        self.eventos.append((f"llegada_paciente_{area_atencion.nombre}", proxima_llegada))

        atendido = False
        for medico in area_atencion.medicos:
            if medico.estado == "libre":
                nuevo_paciente.estado = "siendo_atendido"
                nuevo_paciente.tiempo_inicio_atencion = self.reloj
                nuevo_paciente.medico_asignado = medico
                tiempo_atencion = generar_tiempo_atencion(area_atencion.media_atencion)
                fin_atencion = self.reloj + tiempo_atencion
                llave = self.buscar_key(area_atencion.nombre, "Fin")
                self.diccionario[llave]["Fin atencion"] = fin_atencion
                self.diccionario[llave]["Tiempo atencion"] = tiempo_atencion
                self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))
                medico.estado = "atendiendo"
                llave = self.buscar_key(area_atencion.nombre, "Cola de")
                medico_key = "Medico " + str(1 + medico.id)
                self.diccionario[llave][medico_key] = "atendiendo"
                area_atencion.agregar_paciente_atendido(nuevo_paciente)
                atendido = True
                break

        if not atendido:
            llave = self.buscar_key(area_atencion.nombre, "Cola de")
            cola = int(self.diccionario[llave]["Cola"])
            cola += 1
            self.diccionario[llave]["Cola"] = str(cola)
            area_atencion.cola_area.append(nuevo_paciente)

        self.escribir_fila_tabla_resultados(area_atencion.nombre, "llegada", tiempo_entre_llegadas, proxima_llegada,
                                            tiempo_atencion if atendido else None, fin_atencion if atendido else None,
                                            self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo,
                                            self.pacientes_atendidos_pediatr,
                                            self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm)

    def buscar_key(self, nombre_area, evento):
        claves_encontradas = [clave for clave in self.diccionario.keys() if
                              nombre_area in clave and clave.startswith(evento)]
        if claves_encontradas:
            return claves_encontradas[0]
        else:
            raise KeyError(f"No se encontró la clave para {nombre_area} con evento {evento}")

    def procesar_fin_atencion_paciente(self, nombre_area):
        area_atencion = next((a for a in self.areas if nombre_area == a.nombre), None)
        if area_atencion is None:
            return

        paciente_atendido = next((p for p in area_atencion.pacientes_atendidos if p.estado == "siendo_atendido"), None)
        if paciente_atendido is None:
            return

        medico = paciente_atendido.medico_asignado
        if medico is not None:
            medico.estado = "libre"
            ####################################################################
            llave = self.buscar_key(area_atencion.nombre, "Cola de")
            medico_key = "Medico " + str(1 + medico.id)
            self.diccionario[llave][medico_key] = "libre"

        area_atencion.quitar_paciente_atendido(paciente_atendido)

        if nombre_area == "consulta":
            self.pacientes_atendido_consulta += 1
            self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Consulta general")
        elif nombre_area == "odontologia":
            self.pacientes_atendidos_odontolo += 1
            self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Odontologia")
        elif nombre_area == "pediatria":
            self.pacientes_atendidos_pediatr += 1
            self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Pediatria")
        elif nombre_area == "laboratorio":
            self.pacientes_atendidos_laborator += 1
            self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Laboratorio")
        elif nombre_area == "farmacia":
            self.pacientes_atendidos_farm += 1
            self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Farmacia")

        if area_atencion.cola_area:
            siguiente_paciente = area_atencion.cola_area.pop(0)
            llave = self.buscar_key(area_atencion.nombre, "Cola de")
            cola = int(self.diccionario[llave]["Cola"])
            cola -= 1
            self.diccionario[llave]["Cola"] = str(cola)
            siguiente_paciente.estado = "siendo_atendido"
            siguiente_paciente.tiempo_inicio_atencion = self.reloj
            siguiente_paciente.medico_asignado = medico
            tiempo_atencion = generar_tiempo_atencion(area_atencion.media_atencion)
            fin_atencion = self.reloj + tiempo_atencion
            llave = self.buscar_key(area_atencion.nombre, "Fin atencion")
            self.diccionario[llave]["Tiempo atencion"] = tiempo_atencion
            self.diccionario[llave]["Fin atencion"] = fin_atencion
            self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))
            llave = self.buscar_key(area_atencion.nombre, "Cola de")
            medico.estado = "atendiendo"
            medico_key = "Medico " + str(1 + medico.id)
            self.diccionario[llave][medico_key] = "atendiendo"

            self.escribir_fila_tabla_resultados(area_atencion.nombre, "fin_atencion", None, None, tiempo_atencion,
                                                fin_atencion,
                                                self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo,
                                                self.pacientes_atendidos_pediatr,
                                                self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm)
        else:
            self.escribir_fila_tabla_resultados(area_atencion.nombre, "fin_atencion", None, None, None, None,
                                                self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo,
                                                self.pacientes_atendidos_pediatr,
                                                self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm)

    def actualizar_tiempo_promedio(self, area_atencion, paciente_atendido, area_nombre):
        paciente_atendido.tiempo_salida = self.reloj
        self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

        if area_nombre == "Consulta general":
            self.tiempo_permanencia_totalCons += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            self.tiempoEsperaPromedioConsulta += self.tiempo_permanencia_totalCons / self.pacientes_atendido_consulta
        elif area_nombre == "Odontologia":
            self.tiempo_permanencia_totalOdon += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            self.tiempoEsperaPromedioOdonto += self.tiempo_permanencia_totalOdon / self.pacientes_atendidos_odontolo
        elif area_nombre == "Pediatria":
            self.tiempo_permanencia_totalPed += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            self.tiempoEsperaPromedioPedia += self.tiempo_permanencia_totalPed / self.pacientes_atendidos_pediatr
        elif area_nombre == "Laboratorio":
            self.tiempo_permanencia_totalLab += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            self.tiempoEsperaPromedioLabora += self.tiempo_permanencia_totalLab / self.pacientes_atendidos_laborator
        elif area_nombre == "Farmacia":
            self.tiempo_permanencia_totalFarm += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            self.tiempoEsperaPromedioFarm += self.tiempo_permanencia_totalFarm / self.pacientes_atendidos_farm

    def calcular_t_espera(self):
        if self.pacientes_atendidos > 0:
            tiempo_espera_promedio = self.tiempo_permanencia_total / self.pacientes_atendidos
        else:
            tiempo_espera_promedio = 0

        if self.pacientes_atendido_consulta > 0:
            tiempo_espera_promedioConsulta = self.tiempo_permanencia_totalCons / self.pacientes_atendido_consulta
        else:
            tiempo_espera_promedioConsulta = 0

        if self.pacientes_atendidos_odontolo > 0:
            tiempo_espera_promedioOdontolo = self.tiempo_permanencia_totalOdon / self.pacientes_atendidos_odontolo
        else:
            tiempo_espera_promedioOdontolo = 0

        if self.pacientes_atendidos_pediatr > 0:
            tiempo_espera_promedioPediatr = self.tiempo_permanencia_totalPed / self.pacientes_atendidos_pediatr
        else:
            tiempo_espera_promedioPediatr = 0

        if self.pacientes_atendidos_laborator > 0:
            tiempo_espera_promedioLaborat = self.tiempo_permanencia_totalLab / self.pacientes_atendidos_laborator
        else:
            tiempo_espera_promedioLaborat = 0

        if self.pacientes_atendidos_farm > 0:
            tiempo_espera_promedioFarmaci = self.tiempo_permanencia_totalFarm / self.pacientes_atendidos_farm
        else:
            tiempo_espera_promedioFarmaci = 0

        return self.pacientes_atendidos, tiempo_espera_promedio, tiempo_espera_promedioConsulta, tiempo_espera_promedioOdontolo, tiempo_espera_promedioPediatr, tiempo_espera_promedioLaborat, tiempo_espera_promedioFarmaci


class VentanaSimulacion(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Simulación Centro de Salud')
        self.setGeometry(100, 100, 1200, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.boton_simular = QPushButton('Iniciar Simulación')
        self.boton_simular.clicked.connect(self.iniciar_simulacion)
        self.layout.addWidget(self.boton_simular)

        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.tabla_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

    def iniciar_simulacion(self):
        simulacion = SimulacionCentroSalud()
        simulacion.inicializar()
        simulacion.simular()

        self.mostrar_resultados(simulacion.tabla_resultados)
        self.mostrar_tiempo_espera(simulacion.calcular_t_espera())

    def mostrar_resultados(self, tabla_resultados):
        tabla_widget = QTableWidget()
        self.tabla_layout.addWidget(tabla_widget)
        self.llenar_tabla(tabla_widget, tabla_resultados)


    def llenar_tabla(self, tabla, tabla_resultados):
        # Fijar la cantidad de filas en la tabla
        tabla.setRowCount(len(tabla_resultados))

        # Definir los encabezados de las columnas
        encabezado_tabla = [
            'Evento', 'Reloj',
            'llegada paciente consulta.Tiempo entre llegadas', 'llegada paciente consulta.Proxima llegada',
            'llegada paciente Odontologia.Tiempo entre llegadas', 'llegada paciente Odontologia.Proxima llegada',
            'llegada paciente Pediatria.Tiempo entre llegadas', 'llegada paciente Pediatria.Proxima llegada',
            'llegada paciente Laboratorio.Tiempo entre llegadas', 'llegada paciente Laboratorio.Proxima llegada',
            'llegada paciente Farmacia.Tiempo entre llegadas', 'llegada paciente Farmacia.Proxima llegada',
            'fin atencion consulta.Tiempo atencion', 'fin atencion consulta.Fin atencion',
            'fin atencion odontologia.Tiempo atencion', 'fin atencion odontologia.Fin atencion',
            'fin atencion Pediatria.Tiempo atencion', 'fin atencion Pediatria.Fin atencion',
            'fin atencion laboratorio.Tiempo atencion', 'fin atencion laboratorio.Fin atencion',
            'fin atencion farmacia.Tiempo atencion', 'fin atencion farmacia.Fin atencion',
            'Tiempo de espera Promedio.Consulta general', 'Tiempo de espera Promedio.Odontologia',
            'Tiempo de espera Promedio.Pediatria', 'Tiempo de espera Promedio.Laboratorio',
            'Tiempo de espera Promedio.Farmacia', 'Cola de consultas generales.Medico 1',
            'Cola de consultas generales.Medico 2', 'Cola de consultas generales.Medico 3',
            'Cola de consultas generales.Medico 4', 'Cola de consultas generales.Medico 5',
            'Cola de consultas generales.Cola', 'Cola de consultas generales.Contador',
            'Cola de consultas generales.Tiempo de permanencia', 'Cola de Odontologia.Medico 1',
            'Cola de Odontologia.Medico 2', 'Cola de Odontologia.Medico 3', 'Cola de Odontologia.Cola',
            'Cola de Odontologia.Contador', 'Cola de Odontologia.Tiempo de permanencia',
            'Cola de Pediatria.Medico 1', 'Cola de Pediatria.Medico 2', 'Cola de Pediatria.Cola',
            'Cola de Pediatria.Contador', 'Cola de Pediatria.Tiempo de permanencia', 'Cola de Laboratorio.Medico 1',
            'Cola de Laboratorio.Medico 2', 'Cola de Laboratorio.Medico 3', 'Cola de Laboratorio.Medico 4',
            'Cola de Laboratorio.Cola', 'Cola de Laboratorio.Contador', 'Cola de Laboratorio.Tiempo de permanencia',
            'Cola de Farmacia.Medico 1', 'Cola de Farmacia.Medico 2', 'Cola de Farmacia.Cola',
            'Cola de Farmacia.Contador', 'Cola de Farmacia.Tiempo de permanencia', 'pacientes_atendido_consulta',
            "pacientes_atendidos_odontolo", "pacientes_atendidos_pediatr", "pacientes_atendidos_laborator",
            "pacientes_atendidos_farm"
        ]

        # Fijar la cantidad de columnas y sus encabezados
        tabla.setColumnCount(len(encabezado_tabla))
        tabla.setHorizontalHeaderLabels(encabezado_tabla)

        # Llenar la tabla con los datos de tabla_resultados
        for i, resultado in enumerate(tabla_resultados):
            # Obtener el valor de la columna "Reloj" de la siguiente fila
            reloj_valor_siguiente_fila = tabla_resultados[i + 1][1] if i + 1 < len(tabla_resultados) else None
            for j, valor in enumerate(resultado):
                if valor is not None:
                    item = QTableWidgetItem(f"{valor:.2f}" if isinstance(valor, (int, float)) else str(valor))
                else:
                    item = QTableWidgetItem("")

                # Resaltar la celda si su valor coincide con el valor de la columna "Reloj" de la siguiente fila
                if valor == reloj_valor_siguiente_fila:
                    item.setBackground(QColor(255, 255, 0))  # Amarillo

                tabla.setItem(i, j, item)

    def mostrar_tiempo_espera(self, resultados_finales):
        pacientes_atendidos, tiempo_espera_promedio, tiempo_espera_promedioConsulta, tiempo_espera_promedioOdontolo, tiempo_espera_promedioPediatr, tiempo_espera_promedioLaborat, tiempo_espera_promedioFarmaci = resultados_finales

        texto_resultados_general = f"Pacientes atendidos: {pacientes_atendidos}\nTiempo de espera promedio general: {tiempo_espera_promedio:.2f} minutos"
        texto_resultados_especialidad = f"\nTiempo de espera promedio por especialidad:\n"
        texto_resultados_especialidad += f"Consulta: {tiempo_espera_promedioConsulta:.2f} minutos\n"
        texto_resultados_especialidad += f"Odontología: {tiempo_espera_promedioOdontolo:.2f} minutos\n"
        texto_resultados_especialidad += f"Pediatria: {tiempo_espera_promedioPediatr:.2f} minutos\n"
        texto_resultados_especialidad += f"Laboratorio: {tiempo_espera_promedioLaborat:.2f} minutos\n"
        texto_resultados_especialidad += f"Farmacia: {tiempo_espera_promedioFarmaci:.2f} minutos"

        etiqueta_resultados_general = QLabel(texto_resultados_general)
        etiqueta_resultados_especialidad = QLabel(texto_resultados_especialidad)

        self.tabla_layout.addWidget(etiqueta_resultados_general)
        self.tabla_layout.addWidget(etiqueta_resultados_especialidad)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaSimulacion()
    ventana.show()
    sys.exit(app.exec_())

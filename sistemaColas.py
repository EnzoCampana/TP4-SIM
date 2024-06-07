import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QScrollArea

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
    def inicializar(self):
        primeras_llegadas = [] #0consulta 1odont 2ped 3lab 4farm
        for area in self.areas:
            tiempo_primera_llegada = generar_tiempo_entre_llegadas(area.media_llegada)
            self.eventos.append((f"llegada_paciente_{area.nombre}", tiempo_primera_llegada))
            primeras_llegadas.append(tiempo_primera_llegada)
        self.tabla_resultados.append(("inicializacion", self.reloj, primeras_llegadas[0], primeras_llegadas[0], None, None,
                                      primeras_llegadas[1], primeras_llegadas[1], None, None,  
                                      primeras_llegadas[2], primeras_llegadas[2], None, None, 
                                      primeras_llegadas[3], primeras_llegadas[3], None, None, 
                                      primeras_llegadas[4], primeras_llegadas[4], None, None, 
                                       None, None))
        
    def escribir_fila_tabla_resultados(self, area, evento, tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                   pacientes_atendido_consulta, pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                   pacientes_atendidos_laborator, pacientes_atendidos_farm):
        if area == "consulta":
            if evento == "llegada":
                self.tabla_resultados.append((f"llegada_paciente_{area}", self.reloj, tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion,
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta, 
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
            elif evento == "fin_atencion":
                self.tabla_resultados.append((f"fin_atencion_paciente_{area}", self.reloj, None, None, tiempo_atencion, fin_atencion, 
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
        elif area == "odontologia":
            if evento == "llegada":
                self.tabla_resultados.append((f"llegada_paciente_{area}", self.reloj, None, None, None, None, 
                                            tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
            elif evento == "fin_atencion":
                self.tabla_resultados.append((f"fin_atencion_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, tiempo_atencion, fin_atencion,
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
        elif area == "pediatria":
            if evento == "llegada":
                self.tabla_resultados.append((f"llegada_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
            elif evento == "fin_atencion":
                self.tabla_resultados.append((f"fin_atencion_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            None, None,  tiempo_atencion, fin_atencion,  
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
        elif area == "laboratorio":
            if evento == "llegada":
                self.tabla_resultados.append((f"llegada_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                            None, None, None, None, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
            elif evento == "fin_atencion":
                self.tabla_resultados.append((f"fin_atencion_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            None, None,  tiempo_atencion, fin_atencion, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
        elif area == "farmacia":
            if evento == "llegada":
                self.tabla_resultados.append((f"llegada_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            None, None, None, None, 
                                            tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))
            elif evento == "fin_atencion":
                self.tabla_resultados.append((f"fin_atencion_paciente_{area}", self.reloj, None, None, None, None,
                                            None, None, None, None,  
                                            None, None, None, None, 
                                            None, None,  tiempo_atencion, fin_atencion, 
                                            None, None, pacientes_atendido_consulta,
                                            pacientes_atendidos_odontolo, pacientes_atendidos_pediatr,
                                            pacientes_atendidos_laborator, pacientes_atendidos_farm))

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
                elif tipo_evento == "fin_atencion_paciente_pediatria":
                    self.procesar_fin_atencion_paciente("pediatria")

                elif tipo_evento == "llegada_paciente_laboratorio":
                    self.procesar_llegada_paciente("laboratorio")
                elif tipo_evento == "fin_atencion_paciente_laboratorio":
                    self.procesar_fin_atencion_paciente("laboratorio")

                elif tipo_evento == "llegada_paciente_farmacia":
                    self.procesar_llegada_paciente("farmacia")
                elif tipo_evento == "fin_atencion_paciente_farmacia":
                    self.procesar_fin_atencion_paciente("farmacia")

    def procesar_llegada_paciente(self, nombre_area):
        # busco el area
        for a in self.areas:
            if nombre_area == a.nombre:
                 area_atencion = a

        # Se crea el nuevo cliente
        nuevo_paciente = Paciente(self.reloj)

        # Programo la próxima llegada de paciente
        tiempo_entre_llegadas = generar_tiempo_entre_llegadas(area_atencion.media_llegada)
        proxima_llegada = self.reloj + tiempo_entre_llegadas
        self.eventos.append((f"llegada_paciente_{area_atencion.nombre}", proxima_llegada))

        atendido = False

        #recorro los medicos del area
        for medico in area_atencion.medicos:

            if medico.estado == "libre":
                # Si el medico está libre, atiende al paciente (calcula tiempo atencion)
                nuevo_paciente.estado = "siendo_atendido"
                nuevo_paciente.tiempo_inicio_atencion = self.reloj
                nuevo_paciente.medico_asignado = medico
                tiempo_atencion = generar_tiempo_atencion(area_atencion.media_atencion)
                fin_atencion = self.reloj + tiempo_atencion
                self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))
                medico.estado = "atendiendo"
                area_atencion.agregar_paciente_atendido(nuevo_paciente)
                atendido = True
                break

        if not atendido:
                # Si no se pudo atender al paciente porque todos los medicos del area estaban ocupados, lo mete en la cola y no calcula tiempo de atencion ni nada
                area_atencion.cola_area.append(nuevo_paciente)
                tiempo_atencion = None
                fin_atencion = None
        self.escribir_fila_tabla_resultados(area_atencion.nombre, "llegada", tiempo_entre_llegadas, proxima_llegada, tiempo_atencion, fin_atencion, 
                                   self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo, self.pacientes_atendidos_pediatr,
                                   self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm)


    def procesar_fin_atencion_paciente(self, nombre_area):
        # busco el area
        for a in self.areas:
            if nombre_area == a.nombre:
                 area_atencion = a

         # Encontrar el paciente que acaba de terminar su atención
        paciente_atendido = next((p for p in area_atencion.pacientes_atendidos if p.estado == "siendo_atendido"), None)
        if paciente_atendido is None:
            return
        
        # Liberar al médico que atendió al paciente
        medico = paciente_atendido.medico_asignado
        if medico is not None:
            medico.estado = "libre"
            #paciente_atendido.estado = "atendido"

        area_atencion.quitar_paciente_atendido(paciente_atendido)

        # actualizar las estadísticas
        if nombre_area == "consulta":
            'El self.pacientes atendidos creo no iria en esta parte pero no se si lo usas en otro lado asi que lo deje !'
            self.pacientes_atendidos += 1
            self.pacientes_atendido_consulta += 1
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempo_permanencia_totalCons += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            
            self.tiempoEsperaPromedioConsulta +=  self.tiempo_permanencia_total / self.pacientes_atendido_consulta
        elif nombre_area == "odontologia":
            self.pacientes_atendidos += 1
            self.pacientes_atendidos_odontolo += 1
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempo_permanencia_totalOdon += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
            
            self.tiempoEsperaPromedioOdonto +=  self.tiempo_permanencia_total / self.pacientes_atendidos_odontolo
        elif nombre_area == "pediatria":
            self.pacientes_atendidos += 1
            self.pacientes_atendidos_pediatr += 1
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempo_permanencia_totalPed += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
           
            self.tiempoEsperaPromedioPedia +=  self.tiempo_permanencia_total / self.pacientes_atendidos_pediatr

        elif nombre_area == "laboratorio":
            self.pacientes_atendidos += 1
            self.pacientes_atendidos_laborator += 1
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)
           
            self.tiempo_permanencia_totalLab += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempoEsperaPromedioLabora +=  self.tiempo_permanencia_total / self.pacientes_atendidos_laborator
        else:
            self.pacientes_atendidos += 1
            self.pacientes_atendidos_farm += 1
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempo_permanencia_totalFarm += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

            self.tiempoEsperaPromedioFarm +=  self.tiempo_permanencia_total / self.pacientes_atendidos_farm

        if len(area_atencion.cola_area) > 0:
            # Atender al siguiente cliente en la cola
            
            siguiente_paciente = area_atencion.cola_area.pop(0)
            siguiente_paciente.estado = "siendo_atendido"
            siguiente_paciente.tiempo_inicio_atencion = self.reloj
            siguiente_paciente.medico_asignado = medico
            tiempo_atencion = generar_tiempo_atencion(area_atencion.media_atencion)
            fin_atencion = self.reloj + tiempo_atencion
            self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))
            medico.estado = "atendiendo"
            self.escribir_fila_tabla_resultados(area_atencion.nombre, "llegada", None, None, tiempo_atencion, fin_atencion, 
                                   self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo, self.pacientes_atendidos_pediatr,
                                   self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm)
            
        else:
            self.escribir_fila_tabla_resultados(area_atencion.nombre, "fin_atencion", None, None, None, None,
                                   self.pacientes_atendido_consulta, self.pacientes_atendidos_odontolo, self.pacientes_atendidos_pediatr,
                                   self.pacientes_atendidos_laborator, self.pacientes_atendidos_farm) 
            
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

        return self.pacientes_atendidos, tiempo_espera_promedio, tiempo_espera_promedioConsulta, tiempo_espera_promedioOdontolo,tiempo_espera_promedioPediatr,tiempo_espera_promedioLaborat,tiempo_espera_promedioFarmaci
    
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

        # despues vemos bien lo que necesitamos calcular y mostrar
        self.mostrar_tiempo_espera(simulacion.calcular_t_espera())

    def mostrar_resultados(self, tabla_resultados):
        tabla_widget = QTableWidget()
        self.tabla_layout.addWidget(tabla_widget)
        self.llenar_tabla(tabla_widget, tabla_resultados)

    def llenar_tabla(self, tabla, tabla_resultados):
        # Fijar la cantidad de filas en la tabla
        tabla.setRowCount(len(tabla_resultados))
        
        # Definir los encabezados de las columnas, incluyendo las nuevas columnas
        encabezado_tabla = [
            'Evento', 'Reloj', 'Tiempo entre Llegadas', 'Próxima Llegada Consulta', 'Tiempo de Atención', 'Fin de Atención Consulta',
            'Tiempo entre Llegadas', 'Próxima Llegada Odontologia', 'Tiempo de Atención', 'Fin de Atención Odont.',
            'Tiempo entre Llegadas', 'Próxima Llegada Pediatria', 'Tiempo de Atención', 'Fin de Atención Ped.',
            'Tiempo entre Llegadas', 'Próxima Llegada Laboratorio', 'Tiempo de Atención', 'Fin de Atención Lab.',
            'Tiempo entre Llegadas', 'Próxima Llegada Farmacia', 'Tiempo de Atención', 'Fin de Atención Farmacia', 
            'Toma Servicio', 'Tiempo de Atencion SS', 'Fin de Atencion SS', 'ACOMULADORES - Tiempo de espera promedio',
            'Cont. Atend Consulta', 'Cont. Atend Odonto', 'Cont. Atend Pediatri', 'Cont. Atend Laboratorio', 'Cont. Atend Farmacia'
        ]
        
        # Fijar la cantidad de columnas y sus encabezados
        tabla.setColumnCount(len(encabezado_tabla))
        tabla.setHorizontalHeaderLabels(encabezado_tabla)

        # Inicializar los contadores
        cont_consulta = 0
        cont_odonto = 0
        cont_pediatria = 0
        cont_laboratorio = 0
        cont_farmacia = 0

        # Llenar la tabla con los datos de tabla_resultados
        for i, resultado in enumerate(tabla_resultados):
            for j, valor in enumerate(resultado):
                # Crear un elemento de tabla con el valor correspondiente
                if valor is not None:
                    # Formatear números a dos decimales si son int o float
                    item = QTableWidgetItem(f"{valor:.2f}" if isinstance(valor, (int, float)) else str(valor))
                else:
                    # Dejar la celda vacía si el valor es None
                    item = QTableWidgetItem("")
                
                # Añadir el elemento a la celda correspondiente
                tabla.setItem(i, j, item)
            
            # Actualizar los contadores de acuerdo al evento de "fin de atención"
            if resultado[5] is not None:  # Fin de Atención Consulta
                cont_consulta += 1
            if resultado[9] is not None:  # Fin de Atención Odontología
                cont_odonto += 1
            if resultado[13] is not None:  # Fin de Atención Pediatría
                cont_pediatria += 1
            if resultado[17] is not None:  # Fin de Atención Laboratorio
                cont_laboratorio += 1
            if resultado[21] is not None:  # Fin de Atención Farmacia
                cont_farmacia += 1
            
            # Añadir los contadores a las celdas correspondientes al final de cada fila
            tabla.setItem(i, len(encabezado_tabla) - 5, QTableWidgetItem(str(cont_consulta)))
            tabla.setItem(i, len(encabezado_tabla) - 4, QTableWidgetItem(str(cont_odonto)))
            tabla.setItem(i, len(encabezado_tabla) - 3, QTableWidgetItem(str(cont_pediatria)))
            tabla.setItem(i, len(encabezado_tabla) - 2, QTableWidgetItem(str(cont_laboratorio)))
            tabla.setItem(i, len(encabezado_tabla) - 1, QTableWidgetItem(str(cont_farmacia)))


    def mostrar_tiempo_espera(self, resultados_finales):
        pacientes_atendidos, tiempo_espera_promedio, tiempo_espera_promedioConsulta, tiempo_espera_promedioOdontolo, tiempo_espera_promedioPediatr, tiempo_espera_promedioLaborat, tiempo_espera_promedioFarmaci = resultados_finales
        
        # Texto para mostrar los resultados generales
        texto_resultados_general = f"Pacientes atendidos: {pacientes_atendidos}\nTiempo de espera promedio general: {tiempo_espera_promedio:.2f} minutos"
        
        # Texto para mostrar los resultados específicos por especialidad
        texto_resultados_especialidad = f"\nTiempo de espera promedio por especialidad:\n"
        texto_resultados_especialidad += f"Consulta: {tiempo_espera_promedioConsulta:.2f} minutos\n"
        texto_resultados_especialidad += f"Odontología: {tiempo_espera_promedioOdontolo:.2f} minutos\n"
        texto_resultados_especialidad += f"Pediatria: {tiempo_espera_promedioPediatr:.2f} minutos\n"
        texto_resultados_especialidad += f"Laboratorio: {tiempo_espera_promedioLaborat:.2f} minutos\n"
        texto_resultados_especialidad += f"Farmacia: {tiempo_espera_promedioFarmaci:.2f} minutos"
        
        # Crear QLabel para mostrar los resultados generales
        etiqueta_resultados_general = QLabel(texto_resultados_general)
        
        # Crear QLabel para mostrar los resultados específicos por especialidad
        etiqueta_resultados_especialidad = QLabel(texto_resultados_especialidad)
        
        # Agregar las etiquetas a la tabla_layout
        self.tabla_layout.addWidget(etiqueta_resultados_general)
        self.tabla_layout.addWidget(etiqueta_resultados_especialidad)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaSimulacion()
    ventana.show()
    sys.exit(app.exec_())

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
        
        self.pacientes_atendidos = 0

class Medico:
    def __init__(self):
        self.estado = "libre"  # "libre" o "atendiendo"

class Paciente:
    def __init__(self, tiempo_ingreso):
        self.estado = "esperando_atencion"  # "esperando_atencion" o "siendo_atendido"
        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None

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

        self.media_llegadas = 8
        self.eventos = []
        # crear las areas

        # crear medicos por cada area
        self.medico = Medico()
        # estos datos son para calcular los estadisticos q pide
        self.pacientes_atendidos = 0
        self.tiempo_permanencia_total = 0
        
        self.tabla_resultados = []  # evento, reloj, 

    def inicializar(self):
        tiempo_primera_llegada = generar_tiempo_entre_llegadas(self.media_llegadas)
        #aca hago un append de todos las llegadas de las areas
        
        self.eventos.append(("llegada_cliente", tiempo_primera_llegada))
        self.tabla_resultados.append(("inicializacion", self.reloj, tiempo_primera_llegada, tiempo_primera_llegada ,self.medico.estado, len(self.medico.cola), None, None ))

    def simular(self):
        while self.reloj < self.tiempo_total_simulacion:
            # Ordenar eventos por tiempo
            self.eventos.sort(key=lambda evento: evento[1])
            if len(self.eventos) > 0:
                evento_actual = self.eventos.pop(0)
                self.reloj = evento_actual[1]
                tipo_evento = evento_actual[0]

                if tipo_evento == "llegada_paciente_consulta":
                    self.procesar_llegada_paciente()
                elif tipo_evento == "fin_atencion_paciente_consulta":
                    self.procesar_fin_atencion_paciente()

                elif tipo_evento == "llegada_paciente_odontologia":
                    self.procesar_llegada_paciente()
                elif tipo_evento == "fin_atencion_paciente_odontologia":
                    self.procesar_fin_atencion_paciente()

                elif tipo_evento == "llegada_paciente_pediatria":
                    self.procesar_llegada_paciente()
                elif tipo_evento == "fin_atencion_paciente_pediatria":
                    self.procesar_fin_atencion_paciente()

                elif tipo_evento == "llegada_paciente_laboratorio":
                    self.procesar_llegada_paciente()
                elif tipo_evento == "fin_atencion_paciente_laboratorio":
                    self.procesar_fin_atencion_paciente()

                elif tipo_evento == "llegada_paciente_farmacia":
                    self.procesar_llegada_paciente()
                elif tipo_evento == "fin_atencion_paciente_farmacia":
                    self.procesar_fin_atencion_paciente()

    def procesar_llegada_paciente(self):
        # Se crea el nuevo cliente
        nuevo_paciente = Paciente(self.reloj)

        if self.medico.estado == "libre":
            # Si la medico está libre, atiende al cliente (calcula tiempo atencion)
            paciente_atendido = nuevo_paciente
            paciente_atendido.estado = "siendo_atendido"
            paciente_atendido.tiempo_inicio_atencion = self.reloj
            tiempo_atencion = generar_tiempo_atencion()
            fin_atencion = self.reloj + tiempo_atencion
            self.eventos.append(("fin_atencion_cliente", fin_atencion))
            self.medico.estado = "atendiendo"

            # para anotar en la tabla de resultados y los eventos, hacer una busqueda segun el tipo para manejar bien los eventos
            self.tabla_resultados.append(("llegada_cliente", self.reloj, None, None,self.medico.estado, len(self.medico.cola), tiempo_atencion, fin_atencion))

        elif self.medico.estado == "atendiendo":
            # Si está atendiendo a alguien, lo mete en la cola y no calcula tiempo de atencion ni nada
            self.medico.cola.append(nuevo_paciente)
            self.tabla_resultados.append(("llegada_cliente", self.reloj, None, None,self.medico.estado, len(self.medico.cola), None, None))

        # Programo la próxima llegada de cliente
        tiempo_entre_llegadas = generar_tiempo_entre_llegadas(self.media_llegadas)
        proxima_llegada = self.reloj + tiempo_entre_llegadas
        self.eventos.append(("llegada_cliente", proxima_llegada))

        # aca se actualiza o sobreescribe la entrada que se agrego recien en los if de arriba, para agregar la proxima llegada
        ultimo_resultado = self.tabla_resultados[-1]
        self.tabla_resultados[-1] = (ultimo_resultado[0], ultimo_resultado[1], tiempo_entre_llegadas, proxima_llegada,self.medico.estado, len(self.medico.cola), ultimo_resultado[6], ultimo_resultado[7])

    def procesar_fin_atencion_paciente(self):
        # Procesar la finalización de atención de un cliente
        self.pacientes_atendidos += 1
        paciente_atendido = self.medico.cola[0] if self.medico.cola else None
        if paciente_atendido:
            paciente_atendido.tiempo_salida = self.reloj
            self.tiempo_permanencia_total += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso)

        if len(self.medico.cola) > 0:
            # Atender al siguiente cliente en la cola
            
            siguiente_paciente = self.medico.cola.pop(0)
            siguiente_paciente.estado = "siendo_atendido"
            siguiente_paciente.tiempo_inicio_atencion = self.reloj
            tiempo_atencion = generar_tiempo_atencion()
            fin_atencion = self.reloj + tiempo_atencion
            self.eventos.append(("fin_atencion_cliente", fin_atencion))

            self.tabla_resultados.append(("fin_atencion_cliente", self.reloj, None, None,self.medico.estado, len(self.medico.cola), tiempo_atencion, fin_atencion))

            
        else:
            self.medico.estado = "libre"
            self.tabla_resultados.append(("fin_atencion_cliente", self.reloj, None, None,self.medico.estado, len(self.medico.cola), None, None))
            

    def calcular_t_espera(self):
        if self.pacientes_atendidos > 0:
            tiempo_espera_promedio = self.tiempo_permanencia_total / self.pacientes_atendidos
        else:
            tiempo_espera_promedio = 0
        return self.pacientes_atendidos, tiempo_espera_promedio
    
class VentanaSimulacion(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Simulación de Peluquería')
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
        tabla.setRowCount(len(tabla_resultados))
        tabla.setColumnCount(8)
        tabla.setHorizontalHeaderLabels(['Evento', 'Reloj', 'Tiempo entre Llegadas', 'Próxima Llegada',  'Estado Peluquera', 'Personas en Cola', 'Tiempo de Atención', 'Fin de Atención'])

        for i, resultado in enumerate(tabla_resultados):
            tabla.setItem(i, 0, QTableWidgetItem(resultado[0]))
            tabla.setItem(i, 1, QTableWidgetItem(f"{resultado[1]:.2f}" if resultado[1] is not None else ""))
            tabla.setItem(i, 2, QTableWidgetItem(f"{resultado[2]:.2f}" if resultado[2] is not None else ""))
            tabla.setItem(i, 3, QTableWidgetItem(f"{resultado[3]:.2f}" if resultado[3] is not None else ""))
            tabla.setItem(i, 4, QTableWidgetItem(resultado[4]))
            tabla.setItem(i, 5, QTableWidgetItem(str(resultado[5])))
            tabla.setItem(i, 6, QTableWidgetItem(f"{resultado[6]:.2f}" if resultado[6] is not None else ""))
            tabla.setItem(i, 7, QTableWidgetItem(f"{resultado[7]:.2f}" if resultado[7] is not None else ""))
            

    def mostrar_tiempo_espera(self, resultados_finales):
        pacientes_atendidos, tiempo_espera_promedio = resultados_finales
        texto_resultados = f"Pacientes atendidos: {pacientes_atendidos}\nTiempo de espera promedio: {tiempo_espera_promedio:.2f} minutos"
        
        # Crear un QLabel para mostrar los resultados
        etiqueta_resultados = QLabel(texto_resultados)
        self.tabla_layout.addWidget(etiqueta_resultados)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaSimulacion()
    ventana.show()
    sys.exit(app.exec_())

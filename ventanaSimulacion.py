from simulacionCentroSalud import SimulacionCentroSalud
from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QScrollArea
from PyQt5.QtGui import QColor, QFont, QBrush


class VentanaSimulacion(QWidget):
    def __init__(self, lineas, mostrar_desde, lambda1, lambda2, lambda3, lambda4, lambda5,
                 lambda6, lambda7, lambda8, lambda9, lambda10):
        super().__init__()
        self.setWindowTitle('Simulación Centro de Salud')
        self.setGeometry(100, 100, 1200, 600)
        self.lineas = lineas
        self.mostrar_desde = mostrar_desde
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.lambda4 = lambda4
        self.lambda5 = lambda5
        self.lambda6 = lambda6
        self.lambda7 = lambda7
        self.lambda8 = lambda8
        self.lambda9 = lambda9
        self.lambda10 = lambda10

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
        simulacion = SimulacionCentroSalud(self.lineas, self.mostrar_desde, self.lambda1, self.lambda2, self.lambda3,
                                           self.lambda4, self.lambda5, self.lambda6, self.lambda7, self.lambda8,
                                           self.lambda9, self.lambda10)
        simulacion.inicializar()
        simulacion.simular()

        self.mostrar_resultados(simulacion.tablaResultados)
        self.mostrar_tiempo_espera(simulacion.calcularEstadisticas())

    def mostrar_resultados(self, tablaResultados):
        tabla_widget = QTableWidget()
        self.tabla_layout.addWidget(tabla_widget)
        self.llenar_tabla(tabla_widget, tablaResultados)

    def llenar_tabla(self, tabla, tablaResultados):
        # Fijar la cantidad de filas en la tabla
        tabla.setRowCount(len(tablaResultados))

        # Definir los encabezados de las columnas
        encabezado_tabla = [
            'Evento', 'Reloj',
            'RND', 'llegada paciente consulta.Tiempo entre llegadas', 'llegada paciente consulta.Proxima llegada',
            'RND','llegada paciente Odontologia.Tiempo entre llegadas', 'llegada paciente Odontologia.Proxima llegada',
            'RND','llegada paciente Pediatria.Tiempo entre llegadas', 'llegada paciente Pediatria.Proxima llegada',
            'RND','llegada paciente Laboratorio.Tiempo entre llegadas', 'llegada paciente Laboratorio.Proxima llegada',
            'RND','llegada paciente Farmacia.Tiempo entre llegadas', 'llegada paciente Farmacia.Proxima llegada',
            'RND','fin atencion consulta.Tiempo atencion', 'fin atencion consulta.Fin atencion', '1', '2', '3', '4', '5' ,
            'RND','fin atencion odontologia.Tiempo atencion', 'fin atencion odontologia.Fin atencion','1', '2', '3',
            'RND','fin atencion Pediatria.Tiempo atencion', 'fin atencion Pediatria.Fin atencion','1', '2',
            'RND','fin atencion laboratorio.Tiempo atencion', 'fin atencion laboratorio.Fin atencion','1', '2', '3', '4',
            'RND','fin atencion farmacia.Tiempo atencion', 'fin atencion farmacia.Fin atencion','1', '2',
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
            'Cola de Farmacia.Contador', 'Cola de Farmacia.Tiempo de permanencia', 'RND Servicio', 'Toma SS Nutri', 'RND', 'fin atencion nutricion.Tiempo de Atencion Nutri','fin atencion nutricion.Fin de atencion Nutri','1','Estado Medico 1 Nutri', 'Cola Nutri']

        # Fijar la cantidad de columnas y sus encabezados
        tabla.setColumnCount(len(encabezado_tabla))
        tabla.setHorizontalHeaderLabels(encabezado_tabla)
        
        header = tabla.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0; /* Color gris claro */
                font-weight: bold;
                border: none; /* Eliminar bordes */
                padding: 6px; /* Añadir un poco de espacio interno */
            }
        """)
        # Ajustar las columnas al contenido
        tabla.resizeColumnsToContents()

        # Aplicar estilo a los encabezados



        # Llenar la tabla con los datos de tablaResultados
        for i, resultado in enumerate(tablaResultados):
            for j, valor in enumerate(resultado):
                if valor is not None:
                    item = QTableWidgetItem(f"{valor:.2f}" if isinstance(valor, (int, float)) else str(valor))
                else:
                    item = QTableWidgetItem("")
                tabla.setItem(i, j, item)

    def mostrar_tiempo_espera(self, resultados_finales):
        pacientesAtendidos, tiempoEsperaPromedioTotal, tiempoEsperaPromedioConsulta, tiempoEsperaPromedioOdontologia, tiempoEsperaPromedioPediatria, tiempoEsperaPromedioLaboratorio, tiempoEsperaPromedioFarmacia, tiempoPermanenciaTotal , porcentajeConsulta, porcentajeOdontologia, porcentajePediatria, porcentajeLaboratorio, porcentajeFarmacia, pacientesAtendidosConsulta, pacientesAtendidosOdontologia, pacientesAtendidosPediatria, pacientesAtendidosFarmacia, pacientesAtendidosLaboratorio, tiempoPermanenciaTotalConsulta, tiempoPermanenciaTotalFarmacia, tiempoPermanenciaTotalLaboratorio, tiempoPermanenciaTotalOdontologia, tiempoPermanenciaTotalOdontologia = resultados_finales

        texto_resultados_general = f"Pacientes atendidos: {pacientesAtendidos}\nTiempo de espera promedio general: {tiempoEsperaPromedioTotal:.2f} minutos"
        
        texto_resultados_especialidad = f"\nTiempo de espera promedio por especialidad:\n"
        texto_resultados_especialidad += f"Consulta: {tiempoEsperaPromedioConsulta:.2f} minutos. Porcentaje de ocupacion: {round(porcentajeConsulta,2)}%\n"
        texto_resultados_especialidad += f"Odontología: {tiempoEsperaPromedioOdontologia:.2f} minutos. Porcentaje de ocupacion : {round(porcentajeOdontologia,2)}%\n"
        texto_resultados_especialidad += f"Pediatria: {tiempoEsperaPromedioPediatria:.2f} minutos. Porcentaje de ocupacion: {round(porcentajePediatria,2)}%\n"
        texto_resultados_especialidad += f"Laboratorio: {tiempoEsperaPromedioLaboratorio:.2f} minutos. Porcentaje de ocupacion: {round(porcentajeLaboratorio,2)}%\n"
        texto_resultados_especialidad += f"Farmacia: {tiempoEsperaPromedioFarmacia:.2f} minutos. Porcentaje de ocupacion: {round(porcentajeFarmacia,2)}%\n"

        
        pacientesporarea = f"Pacientes atendidos en Consulta: {pacientesAtendidosConsulta}\n"
        pacientesporarea += f"Pacientes atendidos en Odontologia: {pacientesAtendidosOdontologia}\n"
        pacientesporarea += f"Pacientes atendidos en Pediatria: {pacientesAtendidosPediatria}\n"
        pacientesporarea += f"Pacientes atendidos en Laboratorio: {pacientesAtendidosLaboratorio}\n"
        pacientesporarea += f"Pacientes atendidos en Farmacia: {pacientesAtendidosFarmacia}\n"

        tiemposPermanencia = f"Tiempo de permanencia promedio total: {tiempoPermanenciaTotal:.2f} minutos\n"
        tiemposPermanencia += f"Tiempo de permanencia promedio en Consulta: {tiempoPermanenciaTotalConsulta:.2f} minutos\n"
        tiemposPermanencia += f"Tiempo de permanencia promedio en Farmacia: {tiempoPermanenciaTotalFarmacia:.2f} minutos\n"
        tiemposPermanencia += f"Tiempo de permanencia promedio en Laboratorio: {tiempoPermanenciaTotalLaboratorio:.2f} minutos\n"
        tiemposPermanencia += f"Tiempo de permanencia promedio en Odontologia: {tiempoPermanenciaTotalOdontologia:.2f} minutos\n"

        etiqueta_resultados_general = QLabel(texto_resultados_general)
        etiqueta_resultados_especialidad = QLabel(texto_resultados_especialidad)
        etiquetaPacientesPorArea = QLabel(pacientesporarea)
        etiquetaTiemposPermanencia = QLabel(tiemposPermanencia)

        self.tabla_layout.addWidget(etiqueta_resultados_general)
        self.tabla_layout.addWidget(etiqueta_resultados_especialidad)
        self.tabla_layout.addWidget(etiquetaPacientesPorArea)
        self.tabla_layout.addWidget(etiquetaTiemposPermanencia)
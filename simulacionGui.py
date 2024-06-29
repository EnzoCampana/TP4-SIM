from simulacionCentroSalud import SimulacionCentroSalud
from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QScrollArea, QHBoxLayout, QGroupBox, QGridLayout, QLineEdit, QMessageBox

from ventanaSimulacion  import VentanaSimulacion


class simulacionGui(QWidget):

    def __init__(self):
        super().__init__()

        #Se establecen las características de la ventana
        self.title = 'Simulacion - Centro de Salud'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 600

        self.inicializarGui()
    
    def inicializarGui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.distr_vertical = QVBoxLayout()

        lblCantidadLineas = QLabel('Cantidad de líneas a simular:')
        self.distr_vertical.addWidget(lblCantidadLineas)
        self.txtCantidadLineas = QLineEdit()
        self.txtCantidadLineas.setText('300') # Valor predeterminado
        self.distr_vertical.addWidget(self.txtCantidadLineas)

        self.lblMostrarDesde = QLabel('Mostrar desde la línea:')
        self.distr_vertical.addWidget(self.lblMostrarDesde)
        self.txtMostrarDesde = QLineEdit()
        self.txtMostrarDesde.setText('1')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtMostrarDesde)

        self.lblLlegadaConsultaGeneral = QLabel('Llegada consulta general por hora:')
        self.distr_vertical.addWidget(self.lblLlegadaConsultaGeneral)
        self.txtLlegadaConsultaGeneral = QLineEdit()
        self.txtLlegadaConsultaGeneral.setText('30')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtLlegadaConsultaGeneral)

        self.lblLlegadaOdontologia = QLabel('Llegada odontología por hora:')
        self.distr_vertical.addWidget(self.lblLlegadaOdontologia)
        self.txtLlegadaOdontologia = QLineEdit()
        self.txtLlegadaOdontologia.setText('12')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtLlegadaOdontologia)

        self.lblLlegadaPediatria = QLabel('Llegada pediatría por hora:')
        self.distr_vertical.addWidget(self.lblLlegadaPediatria)
        self.txtLlegadaPediatria = QLineEdit()
        self.txtLlegadaPediatria.setText('10')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtLlegadaPediatria)

        self.lblLlegadaLaboratorio = QLabel('Llegada laboratorio por hora:')
        self.distr_vertical.addWidget(self.lblLlegadaLaboratorio)
        self.txtLlegadaLaboratorio = QLineEdit()
        self.txtLlegadaLaboratorio.setText('20')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtLlegadaLaboratorio)

        self.lblLlegadaFarmacia = QLabel('Llegada farmacia por hora:')
        self.distr_vertical.addWidget(self.lblLlegadaFarmacia)
        self.txtLlegadaFarmacia = QLineEdit()
        self.txtLlegadaFarmacia.setText('25')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtLlegadaFarmacia)

        self.lblFinAtencionConsultaGeneral = QLabel('Fin atención consulta general por hora:')
        self.distr_vertical.addWidget(self.lblFinAtencionConsultaGeneral)
        self.txtFinAtencionConsultaGeneral = QLineEdit()
        self.txtFinAtencionConsultaGeneral.setText('6')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtFinAtencionConsultaGeneral)

        self.lblFinAtencionOdontologia = QLabel('Fin atención odontología por hora:')
        self.distr_vertical.addWidget(self.lblFinAtencionOdontologia)
        self.txtFinAtencionOdontologia = QLineEdit()
        self.txtFinAtencionOdontologia.setText('4')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtFinAtencionOdontologia)

        self.lblFinAtencionPediatria = QLabel('Fin atención pediatría por hora:')
        self.distr_vertical.addWidget(self.lblFinAtencionPediatria)
        self.txtFinAtencionPediatria = QLineEdit()
        self.txtFinAtencionPediatria.setText('5')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtFinAtencionPediatria)

        self.lblFinAtencionLaboratorio = QLabel('Fin atención laboratorio por hora:')
        self.distr_vertical.addWidget(self.lblFinAtencionLaboratorio)
        self.txtFinAtencionLaboratorio = QLineEdit()
        self.txtFinAtencionLaboratorio.setText('8')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtFinAtencionLaboratorio)

        self.lblFinAtencionFarmacia = QLabel('Fin atención farmacia por hora:')
        self.distr_vertical.addWidget(self.lblFinAtencionFarmacia)
        self.txtFinAtencionFarmacia = QLineEdit()
        self.txtFinAtencionFarmacia.setText('15')  # Valor predeterminado
        self.distr_vertical.addWidget(self.txtFinAtencionFarmacia)

        self.boton_iniciar = QPushButton('Iniciar Simulación')
        self.boton_iniciar.clicked.connect(self.iniciar_simulacion)
        self.distr_vertical.addWidget(self.boton_iniciar)

        # esto es lo ultimo q pasa, se muestra
        self.setLayout(self.distr_vertical)
        self.show()


    def iniciar_simulacion(self):
        try:
            cantidad_lineas = int(self.txtCantidadLineas.text())
            mostrar_desde = int(self.txtMostrarDesde.text())
            llegada_consulta_general = float(self.txtLlegadaConsultaGeneral.text())
            llegada_odontologia = float(self.txtLlegadaOdontologia.text())
            llegada_pediatria = float(self.txtLlegadaPediatria.text())
            llegada_laboratorio = float(self.txtLlegadaLaboratorio.text())
            llegada_farmacia = float(self.txtLlegadaFarmacia.text())
            fin_atencion_consulta_general = float(self.txtFinAtencionConsultaGeneral.text())
            fin_atencion_odontologia = float(self.txtFinAtencionOdontologia.text())
            fin_atencion_pediatria = float(self.txtFinAtencionPediatria.text())
            fin_atencion_laboratorio = float(self.txtFinAtencionLaboratorio.text())
            fin_atencion_farmacia = float(self.txtFinAtencionFarmacia.text())

            if mostrar_desde < 0 or mostrar_desde >= cantidad_lineas:
                QMessageBox.critical(self, "Error",
                                     "La línea de inicio debe estar dentro del rango del total de líneas.")
                return

            self.hide()
            self.ventana_simulacion = VentanaSimulacion(cantidad_lineas, mostrar_desde, llegada_consulta_general, llegada_odontologia,
                llegada_pediatria, llegada_laboratorio, llegada_farmacia, fin_atencion_consulta_general, fin_atencion_odontologia, fin_atencion_pediatria, fin_atencion_laboratorio, fin_atencion_farmacia)

            self.ventana_simulacion.show()

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores válidos.")


        
        
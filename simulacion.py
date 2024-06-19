import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, \
    QPushButton, QScrollArea, QMessageBox, QLineEdit
from PyQt5.QtWidgets import QApplication
import sys

import ventanaSimulacion


class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Configuración de la Simulación')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('Cantidad de líneas a simular:'))
        self.lineas_entry = QLineEdit()
        self.lineas_entry.setText('1000')
        self.layout.addWidget(self.lineas_entry)

        self.layout.addWidget(QLabel('Mostrar desde la línea:'))
        self.mostrar_desde_entry = QLineEdit()
        self.mostrar_desde_entry.setText('12')  # Valor predeterminado
        self.layout.addWidget(self.mostrar_desde_entry)

        self.layout.addWidget(QLabel('Llegada consulta general por hora:'))
        self.lambdaentry1 = QLineEdit()
        self.lambdaentry1.setText('30')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry1)

        self.layout.addWidget(QLabel('Llegada odontología por hora:'))
        self.lambdaentry2 = QLineEdit()
        self.lambdaentry2.setText('12')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry2)

        self.layout.addWidget(QLabel('Llegada pediatría por hora:'))
        self.lambdaentry3 = QLineEdit()
        self.lambdaentry3.setText('10')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry3)

        self.layout.addWidget(QLabel('Llegada laboratorio por hora:'))
        self.lambdaentry4 = QLineEdit()
        self.lambdaentry4.setText('20')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry4)

        self.layout.addWidget(QLabel('Llegada farmacia por hora:'))
        self.lambdaentry5 = QLineEdit()
        self.lambdaentry5.setText('25')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry5)

        self.layout.addWidget(QLabel('Fin atención consulta general por hora:'))
        self.lambdaentry6 = QLineEdit()
        self.lambdaentry6.setText('6')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry6)

        self.layout.addWidget(QLabel('Fin atención odontología por hora:'))
        self.lambdaentry7 = QLineEdit()
        self.lambdaentry7.setText('4')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry7)

        self.layout.addWidget(QLabel('Fin atención pediatría por hora:'))
        self.lambdaentry8 = QLineEdit()
        self.lambdaentry8.setText('5')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry8)

        self.layout.addWidget(QLabel('Fin atención laboratorio por hora:'))
        self.lambdaentry9 = QLineEdit()
        self.lambdaentry9.setText('8')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry9)

        self.layout.addWidget(QLabel('Fin atención farmacia por hora:'))
        self.lambdaentry10 = QLineEdit()
        self.lambdaentry10.setText('15')  # Valor predeterminado
        self.layout.addWidget(self.lambdaentry10)

        self.boton_iniciar = QPushButton('Iniciar Simulación')
        self.boton_iniciar.clicked.connect(self.iniciar_simulacion)
        self.layout.addWidget(self.boton_iniciar)

    def iniciar_simulacion(self):
        try:
            lineas = int(self.lineas_entry.text())
            mostrar_desde = int(self.mostrar_desde_entry.text())
            lambda1 = float(self.lambdaentry1.text())
            lambda2 = float(self.lambdaentry2.text())
            lambda3 = float(self.lambdaentry3.text())
            lambda4 = float(self.lambdaentry4.text())
            lambda5 = float(self.lambdaentry5.text())
            lambda6 = float(self.lambdaentry6.text())
            lambda7 = float(self.lambdaentry7.text())
            lambda8 = float(self.lambdaentry8.text())
            lambda9 = float(self.lambdaentry9.text())
            lambda10 = float(self.lambdaentry10.text())

            if mostrar_desde < 0 or mostrar_desde >= lineas:
                QMessageBox.critical(self, "Error",
                                     "La línea de inicio debe estar dentro del rango del total de líneas.")
                return

            self.hide()
            self.ventana_simulacion = ventanaSimulacion.VentanaSimulacion(lineas, mostrar_desde, lambda1, lambda2, lambda3, lambda4,
                                                        lambda5,
                                                        lambda6, lambda7, lambda8, lambda9, lambda10)
            self.ventana_simulacion.show()

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores válidos.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicial()
    ventana.show()
    sys.exit(app.exec_())

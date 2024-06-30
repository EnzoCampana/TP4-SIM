import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

# Funcion que establece a que hora se realiza el corte
def relojCorte(t): 

    """
    Minutos       P ()         P () Ac 
    4t minutos    0,20         0,20
    6t minutos    0,60         0,80
    8t minutos    0,20         1,00
    
    """

    rnd = round(random.random(),4)
    if rnd < 0.20:
        return 4*t
    elif rnd < 0.80:
        return 6*t
    else:
        return 8*t

class RungeKuttaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Runge-Kutta Method")
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['t','C' ,'k1', 'k2', 'k3', 'k4', 't(i+1)', 'C(i+1)'])

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.rungeKutta(1000) # Aca poner el t correspondiente

    def inicializar(self, values):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            for i, value in enumerate(values):
                self.table.setItem(rowPosition, i, QTableWidgetItem(str(value)))

    def rungeKutta(self, t):
        h = 0.01
        to = 0
        Co = t
        tiempoEnfriamento = 0

        self.inicializar(['', '', '', '', '', '', to, Co])

        while Co >= 0:
            k1 = (0.025 * to) - (0.5 * Co) - 12.85
            k2 = (0.025 * (to + (h / 2))) - (0.5 * (Co + (h / 2) * k1)) - 12.85
            k3 = (0.025 * (to + (h / 2))) - (0.5 * (Co + (h / 2) * k2)) - 12.85
            k4 = (0.025 * (to + h)) - (0.5 * (Co + h * k3)) - 12.85

            to = to + h
            Co = Co + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

            k1 = round(k1, 4)
            k2 = round(k2, 4)
            k3 = round(k3, 4)
            k4 = round(k4, 4)

            to = round(to, 4)
            Co = round(Co, 4)
            vector = [to, Co, k1, k2, k3, k4, round(to + h,4), round(Co + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4),4)] 
            self.llenarTabla(vector)
        
        tiempoEnfriamento = ((to * 30) / 60)
        return tiempoEnfriamento

    def llenarTabla(self, vector):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

        for i, value in enumerate(vector):
            self.table.setItem(rowPosition, i, QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RungeKuttaApp()
    ex.show()
    sys.exit(app.exec_())
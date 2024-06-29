import random

class Paciente:
    def __init__(self, tiempo_ingreso):
        
        self.tiempo_ingreso = tiempo_ingreso
        #esto le genera un id unico
        #self.id = 
        self.estado = "EA"  # "esperando_atencion" o "siendo_atendido" # destruido
        # estados EA - SA_[LETRA AREA](N) <- N es el numero de servidor
        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None

        #self.tiempo_restante = None <- esto veo si lo voy a necesitar para cuand ose corte la loz

        # es necesario para liberar a ese medico cuando termine la atencion
        self.medico_asignado = None

    def getEstado(self):
        return self.estado
    
    def setEstadoSiendoAtendido(self, nombre_area, num_servidor):
        self.estado = f"SA_{nombre_area}({num_servidor})"

    def asignarMedico(self, medico):
        self.medico_asignado = medico
    
    def getMedicoDePaciente(self):
        return self.medico_asignado


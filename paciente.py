class Paciente:
    def __init__(self, tiempo_ingreso):
        
        self.tiempo_ingreso = tiempo_ingreso

        self.estado = "esperando_atencion"  # "esperando_atencion" o "siendo_atendido"
        self.tiempo_ingreso = tiempo_ingreso
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None

        # es necesario para liberar a ese medico cuando termine la atencion
        self.medico_asignado = None

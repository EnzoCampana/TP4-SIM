from medico import Medico


class Area:
    def __init__(self, nombre, cantidad_especialistas, media_llegada, media_atencion):

        self.nombre = nombre
        self.cantidad_especialistas = cantidad_especialistas
        self.media_llegada = media_llegada
        self.media_atencion = media_atencion
        
        self.cola_area = []

        self.medicos = [Medico(i) for i in range(cantidad_especialistas)]
        self.primer_inicio_atencion = None
        self.pacientesAtendidos = []

        self.pacientesTotal = []

    def getNombre(self):
        return self.nombre

    def agregar_paciente_atendido(self, paciente):
        self.pacientesAtendidos.append(paciente)

    def quitar_paciente_atendido(self, paciente):
        self.pacientesAtendidos.remove(paciente)

    def agregar_paciente_entrante(self, paciente):
        self.pacientesTotal.append(paciente)
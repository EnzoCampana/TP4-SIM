import medico


class Area:
    def __init__(self, nombre, cantidad_especialistas, media_llegada, media_atencion):

        self.nombre = nombre
        self.cantidad_especialistas = cantidad_especialistas
        self.media_llegada = media_llegada
        self.media_atencion = media_atencion
        
        self.cola_area = []

        self.medicos = [medico.Medico(i) for i in range(cantidad_especialistas)]
        self.primer_inicio_atencion = None
        self.pacientesAtendidos = []

    def agregar_paciente_atendido(self, paciente):
        self.pacientesAtendidos.append(paciente)

    def quitar_paciente_atendido(self, paciente):
        self.pacientesAtendidos.remove(paciente)

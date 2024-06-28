from area import Area
from paciente import Paciente
import random
import math
import json

def generar_tiempo_exponencial(lambdaValor):
    media = 1 / (lambdaValor / 60)
    rnd = random.random()
    return (-media * math.log(1 - rnd)), rnd

def generar_tiempo_entre_llegadas(lambdaValor):
    tiempo_entre_llegadas, rnd = generar_tiempo_exponencial(lambdaValor)
    return tiempo_entre_llegadas, rnd

def generar_tiempo_atencion(lambdaValor):
    tiempo_atencion, rnd = generar_tiempo_exponencial(lambdaValor)
    return tiempo_atencion, rnd

class SimulacionCentroSalud:
    def __init__(self, lineas, mostrar_desde, lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7, lambda8,
                 lambda9, lambda10):

        self.reloj = 0
        self.eventos = []

        self.nro_evento_simulado = 0
        self.mostrar_desde = mostrar_desde
        self.lineas = lineas

        # Crear las areas
        self.areas = []
        self.nombre_areas = ["consulta", "odontologia", "pediatria", "laboratorio", "farmacia", "nutricion"]

        # ACA SE PEUDE CAMBIAR LA CANTIDAD DE FARMACEUTICOS PARA EL PUNTO 3 !!!!
        self.especialistas_por_area = [5, 3, 2, 4, 2, 1]
        self.lambda_llegadas_area = [lambda1, lambda2, lambda3, lambda4, lambda5, 1]
        self.lambda_atencion_area = [lambda6, lambda7, lambda8, lambda9, lambda10, 2]

        for i in range(len(self.nombre_areas)):
            self.areas.append(Area(self.nombre_areas[i],
                                   self.especialistas_por_area[i],
                                   self.lambda_llegadas_area[i],
                                   self.lambda_atencion_area[i]))

        # Tiempo de espera promedio y porcentaje de ocupacion. Necesitamos acumular/sumar el tiempo de espera promedio.
        # Necesito para cada paciente que inicia atencion, tiempo inicio atencion - tiempo ingreso / cant pacientes area

        self.tiempoEsperaPromedioAcFarmacia = 0
        self.tiempoEsperaPromedioAcConsulta = 0
        self.tiempoEsperaPromedioAcOdontologia = 0
        self.tiempoEsperaPromedioAcLaboratorio = 0
        self.tiempoEsperaPromedioAcPediatria = 0

        # Tiempo de espera promedio general. 
        # Necesitamos sumar todos los tiempos de espera promedio de cada area / cantidad de pacientes

        self.tiempoEsperaPromedioGeneral = 0

        # Cantidad de pacientes atendidos.
        # Necesitamos acumular +1 al contador cada vez que se finaliza la atencion

        self.pacientes_atendidos = 0

        # Cantidad de pacientes por area. 
        # Necesitamos acumular +1 al contador cada vez que se finaliza la atencion en esa area

        self.pacientesAtendidosConsulta = 0
        self.pacientesAtendidosOdontologia = 0
        self.pacientesAtendidosPediatria = 0
        self.pacientesAtendidosLaboratorio = 0
        self.pacientesAtendidosFarmacia = 0

        # Porcentaje de ocupacion. Para calcular el tiempo ocupado. Acumular tiempo fin atencion - tiempo inicio atencion 
        # de cada paciente atendido de cada medico        
        # Necesitamos dividir el (tiempo ocupado / tiempo disponible (reloj) ) * 100

        self.tiempoOcupadoConsulta = 0
        self.tiempoOcupadoOdontologia = 0
        self.tiempoOcupadoPediatria = 0
        self.tiempoOcupadoLaboratorio = 0
        self.tiempoOcupadoFarmacia = 0
        
        self.tiempoPermanenciaTotal = 0
        self.tiempoPermanenciaTotalConsulta = 0
        self.tiempoPermanenciaTotalOdontologia = 0
        self.tiempoPermanenciaTotalPediatria = 0
        self.tiempoPermanenciaTotalLaboratorio = 0
        self.tiempoPermanenciaTotalFarmacia = 0

        self.tablaResultados = []  # Vector ESTADO
        
        self.diccionario = {

            "Evento": "Inicializacion",
            "Reloj": "0",
            "llegada paciente consulta": {
                "RND": "-",
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente odontologia": {
                "RND": "-",
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente pediatria": {
                "RND": "-",
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente laboratorio": {
                "RND": "-",
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"
            },
            "llegada paciente farmacia": {
                "RND": "-",
                "Tiempo entre llegadas": "0",
                "Proxima llegada": "0"

            },
            "Fin atencion consulta": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "1": "-", "2": "-", "3": "-", "4": "-", "5": "-"

            },
            "Fin atencion odontologia": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "1": "-", "2": "-", "3": "-"
            
            },
            "Fin atencion pediatria": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "Fin atencion": "-", 
                "1": "-", "2": "-",
                
            },
            "Fin atencion laboratorio": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "1": "-", "2": "-", "3": "-", "4": "-"
                
            },
            "Fin atencion farmacia": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "Fin atencion": "-", 
                "1": "-", "2": "-"
            },
            "Tiempo de espera promedio": {
                "Consulta general": "0",
                "Odontologia": "0",
                "Pediatria": "0",
                "Laboratorio": "0",
                "Farmacia": "0"
            },
            "Cola de consultas generales": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Medico 4": "Libre",
                "Medico 5": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de odontologia": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de pediatria": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de laboratorio": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Medico 3": "Libre",
                "Medico 4": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "Cola de farmacia": {
                "Medico 1": "Libre",
                "Medico 2": "Libre",
                "Cola": "0",
                "Contador": "0",
                "Tiempo de permanencia": "0"
            },
            "RND Servicio": "-",
            "Toma Servicio" : "-",
            "Fin atencion nutricion": {
                "RND": "-",
                "Tiempo atencion": "-",
                "Fin atencion": "-",
                "1": "-"
            },
             "Cola de nutricion": {
                "Medico 1": "Libre",
                "Cola": "0",
            }
        }

    def buscar_area(self, nombre_area):
        return next((area for area in self.areas if area.nombre == nombre_area), None)

    # Metodo que inicializa la simulacion. Calcula los tiempos de llegada de cada area. Actualiza el diccionario. 
    def inicializar(self):
        def actualizar_diccionario_llegadas(area, tiempo_llegada, rnd):
            key_llegada = f"llegada paciente {area.nombre}"
            if key_llegada not in self.diccionario:
                self.diccionario[key_llegada] = {}
            self.diccionario[key_llegada]["RND"] = rnd
            self.diccionario[key_llegada]["Tiempo entre llegadas"] = tiempo_llegada
            self.diccionario[key_llegada]["Proxima llegada"] = tiempo_llegada + self.reloj

        for area in self.areas:

            if area.nombre != "nutricion":

                tiempo_primera_llegada, rndLlegada = generar_tiempo_entre_llegadas(area.media_llegada)
                self.eventos.append((f"llegada_paciente_{area.nombre}", tiempo_primera_llegada))
                actualizar_diccionario_llegadas(area, tiempo_primera_llegada, rndLlegada)

        self.diccionario["Evento"] = "Inicializacion"
        self.diccionario["Reloj"] = self.reloj

        lista = self.diccionario_vector()
        self.tablaResultados.append(lista)
        print(self.tablaResultados)

        self.nro_evento_simulado += 1

    # Metodo que sigue la simulacion por la cantidad de lineas 
    def simular(self):
        

        for _ in range(self.lineas):
            # Ordenar eventos por tiempo
            self.eventos.sort(key=lambda evento: evento[1]) # Ordena los eventos segun el 2 parametro que es el tiempo llegada


            if len(self.eventos) > 0:
                evento_actual = self.eventos.pop(0) # Elimina y devuelve el primer elemento de la lista 
                self.nro_evento_simulado += 1
                self.reloj = evento_actual[1] # Agarra el tiempo para ponerlo como reloj
                tipo_evento = evento_actual[0] # Agarra el tipo de evento

                if tipo_evento.startswith("llegada_paciente_"):
                    area_nombre = tipo_evento.split("_")[-1]
                    self.procesarLlegadaPaciente(area_nombre)
                elif tipo_evento.startswith("fin_atencion_paciente_"):
                    area_nombre = tipo_evento.split("_")[-1]
                    self.procesarFinAtencionPaciente(area_nombre)
                
    def procesarLlegadaPaciente(self, nombre_area):

        global numero 
        area_atencion = None
        area_atencion = self.buscar_area(nombre_area) 

        if area_atencion is None:
            raise ValueError(f"El área {nombre_area} no existe")
        
        nuevo_paciente = Paciente(self.reloj)

        # Nutricion se maneja con el random, no con tiempo de llegadas
        if area_atencion.nombre != "nutricion":

            self.diccionario['RND Servicio'] = "-"
            self.diccionario['Toma Servicio'] = "-"

            tiempo_entre_llegadas, rndLlegada = generar_tiempo_entre_llegadas(area_atencion.media_llegada)
            proxima_llegada = self.reloj + tiempo_entre_llegadas
            llave = self.buscar_key(area_atencion.nombre, "llegada")

           

            self.diccionario[llave]["RND"] = rndLlegada
            self.diccionario[llave]["Tiempo entre llegadas"] = tiempo_entre_llegadas
            self.diccionario[llave]["Proxima llegada"] = proxima_llegada


            self.eventos.append((f"llegada_paciente_{area_atencion.nombre}", proxima_llegada))

        else:

            # Esto es para el area de nutricion, recordemos que se maneja con el random
            rndLlegada = None
            tiempo_entre_llegadas = 0
            proxima_llegada = 0

            self.diccionario['RND Servicio'] = "-"
            self.diccionario['Toma Servicio'] = "-"
            
        
        atendido = False

        for medico in area_atencion.medicos:
            if medico.estado == "libre":
                nuevo_paciente.estado = "siendo_atendido"
                nuevo_paciente.tiempo_inicio_atencion = self.reloj
                if area_atencion.nombre == 'consulta': 
                    self.tiempoEsperaPromedioAcConsulta+= (nuevo_paciente.tiempo_inicio_atencion - nuevo_paciente.tiempo_ingreso)
                elif area_atencion.nombre == 'odontologia':
                    self.tiempoEsperaPromedioAcOdontologia += (nuevo_paciente.tiempo_inicio_atencion - nuevo_paciente.tiempo_ingreso)
                elif area_atencion.nombre == 'pediatria':
                    self.tiempoEsperaPromedioAcPediatria += (nuevo_paciente.tiempo_inicio_atencion - nuevo_paciente.tiempo_ingreso)
                elif area_atencion.nombre == 'laboratorio':
                    self.tiempoEsperaPromedioAcLaboratorio += (nuevo_paciente.tiempo_inicio_atencion - nuevo_paciente.tiempo_ingreso)
                elif area_atencion.nombre == 'farmacia':
                    self.tiempoEsperaPromedioAcFarmacia += (nuevo_paciente.tiempo_inicio_atencion - nuevo_paciente.tiempo_ingreso)

                nuevo_paciente.medico_asignado = medico

                tiempo_atencion, rndAtencion = generar_tiempo_atencion(area_atencion.media_atencion)
                fin_atencion = self.reloj + tiempo_atencion
                nuevo_paciente.tiempo_aux = str(fin_atencion) #
                llave = self.buscar_key(area_atencion.nombre, "Fin")

                self.diccionario[llave]['RND'] = rndAtencion
                self.diccionario[llave]["Fin atencion"] = fin_atencion
                self.diccionario[llave]["Tiempo atencion"] = tiempo_atencion
                self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))

                numero = str(1 + medico.id) #
                self.diccionario[llave][numero] = fin_atencion #
                medico.estado = "Atendiendo"
                llave = self.buscar_key(area_atencion.nombre, "Cola de")
                medico_key = "Medico " + str(1 + medico.id)
                self.diccionario[llave][medico_key] = "Atendiendo"

                area_atencion.agregar_paciente_atendido(nuevo_paciente)
                atendido = True
                break

        # Si no lo puede atender nadie, lo manda a la cola 
        if not atendido:
            
            llave = self.buscar_key(area_atencion.nombre, "Cola de")
            cola = int(self.diccionario[llave]["Cola"])
            cola += 1
            self.diccionario[llave]["Cola"] = str(cola)
            area_atencion.cola_area.append(nuevo_paciente)

        asiste_servicio = False
        self.escribir_fila_tablaResultados(area_atencion.nombre, "llegada", rndLlegada, tiempo_entre_llegadas, proxima_llegada, rndAtencion if atendido else None,
                                            tiempo_atencion if atendido else None, fin_atencion if atendido else None,
                                            self.pacientesAtendidosConsulta, self.pacientesAtendidosOdontologia,
                                            self.pacientesAtendidosPediatria,
                                            self.pacientesAtendidosLaboratorio, self.pacientesAtendidosFarmacia,
                                            self.mostrar_desde, self.nro_evento_simulado, self.lineas, asiste_servicio)
        
        self.limpiar_rnd_otras_areas(area_atencion.nombre) # Limpiamos

    def procesarFinAtencionPaciente(self, nombre_area):
            area_atencion = self.buscar_area(nombre_area)
            paciente_atendido = None
            if area_atencion is None:
                raise ValueError(f"El área {nombre_area} no existe")

            for p in area_atencion.pacientesAtendidos:
                if p.estado == "siendo_atendido" and p.tiempo_aux == str(self.reloj):
                    paciente_atendido = p
                    break

            if paciente_atendido is None:
                return
            
            self.pacientes_atendidos += 1
            paciente_atendido.estado = "D"

            medico = paciente_atendido.medico_asignado

            if medico is not None:
                medico.estado = "libre"
                llave = self.buscar_key(area_atencion.nombre, "Cola de")
                medico_key = "Medico " + str(1 + medico.id)
                self.diccionario[llave][medico_key] = "libre"
                llave = self.buscar_key(area_atencion.nombre, "Fin")
                numero = str(1 + medico.id)
                self.diccionario[llave][numero] = "-"

            paciente_atendido.estado = "D"
            area_atencion.quitar_paciente_atendido(paciente_atendido)

            self.calcularTiempoOcupado( area_atencion, paciente_atendido)
            # Agrego 1 al contador del area, actualizo los tiempos promedios de PERMANENCIA. Escribo en el diccionario
            if nombre_area == "consulta":

                self.tiempoEsperaPromedioAcConsulta += (
                    paciente_atendido.tiempo_inicio_atencion - paciente_atendido.tiempo_ingreso)
                
                self.pacientesAtendidosConsulta += 1
                self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Consulta general")
                self.diccionario["Cola de consultas generales"][
                    "Tiempo de permanencia"]=self.tiempoPermanenciaTotalConsulta
                self.diccionario["Tiempo de espera promedio"]["Consulta general"] = self.tiempoEsperaPromedioAcConsulta / self.pacientesAtendidosConsulta
            elif nombre_area == "odontologia":

                self.tiempoEsperaPromedioAcOdontologia += (
                    paciente_atendido.tiempo_inicio_atencion - paciente_atendido.tiempo_ingreso)
                self.pacientesAtendidosOdontologia += 1
                self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Odontologia")
                self.diccionario["Cola de odontologia"]["Tiempo de permanencia"] = self.tiempoPermanenciaTotalOdontologia
                self.diccionario["Tiempo de espera promedio"]["Odontologia"] = self.tiempoEsperaPromedioAcOdontologia / self.pacientesAtendidosOdontologia

            elif nombre_area == "pediatria":
                self.tiempoEsperaPromedioAcPediatria += (
                    paciente_atendido.tiempo_inicio_atencion - paciente_atendido.tiempo_ingreso)
                self.pacientesAtendidosPediatria += 1
                self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Pediatria")
                self.diccionario["Cola de pediatria"]["Tiempo de permanencia"] = self.tiempoPermanenciaTotalPediatria
                self.diccionario["Tiempo de espera promedio"]["Pediatria"] = self.tiempoEsperaPromedioAcPediatria / self.pacientesAtendidosPediatria
            elif nombre_area == "laboratorio":
                self.tiempoEsperaPromedioAcLaboratorio += (
                    paciente_atendido.tiempo_inicio_atencion - paciente_atendido.tiempo_ingreso)
                self.pacientesAtendidosLaboratorio += 1
                self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Laboratorio")
                self.diccionario["Cola de laboratorio"]["Tiempo de permanencia"] = self.tiempoPermanenciaTotalFarmacia
                self.diccionario["Tiempo de espera promedio"]["Laboratorio"] = self.tiempoEsperaPromedioAcLaboratorio / self.pacientesAtendidosLaboratorio


            elif nombre_area == "farmacia":
                self.tiempoEsperaPromedioAcFarmacia += (paciente_atendido.tiempo_inicio_atencion - paciente_atendido.tiempo_ingreso)
                self.pacientesAtendidosFarmacia += 1
                self.actualizar_tiempo_promedio(area_atencion, paciente_atendido, "Farmacia")
                self.diccionario["Cola de farmacia"]["Tiempo de permanencia"] = self.tiempoPermanenciaTotalFarmacia
                self.diccionario["Tiempo de espera promedio"]["Farmacia"] = self.tiempoEsperaPromedioAcFarmacia / self.pacientesAtendidosFarmacia

            # Simulamos si va al nuevo servicio o no
            asiste_servicio = None
            if area_atencion.nombre != "nutricion":
                rnd = random.random()
                self.diccionario["RND Servicio"] = rnd
                if rnd <= 0.2:
                    asiste_servicio = True
                    # se genera una llegada para el mismo instante de tiempo
                    self.eventos.append(("llegada_paciente_nutricion", self.reloj))
                    self.diccionario['Toma Servicio'] = 'Si'
                else:
                    asiste_servicio = False
                    self.diccionario['Toma Servicio'] = "No"
                

            if area_atencion.cola_area:
                siguiente_paciente = area_atencion.cola_area.pop(0)
                llave = self.buscar_key(area_atencion.nombre, "Cola de")
                cola = int(self.diccionario[llave]["Cola"]) - 1
                self.diccionario[llave]["Cola"] = str(cola)
                # aca podriamos ver si lo podemos cambiar a SA - numero de servidor - area
                siguiente_paciente.estado = "siendo_atendido"
                siguiente_paciente.tiempo_inicio_atencion = self.reloj
                siguiente_paciente.medico_asignado = medico
                tiempo_atencion, rndAtencion = generar_tiempo_atencion(area_atencion.media_atencion)

                fin_atencion = self.reloj + tiempo_atencion

                llave = self.buscar_key(area_atencion.nombre, "Fin atencion")
                self.diccionario[llave]["RND"] = rndAtencion
                self.diccionario[llave]["Tiempo atencion"] = tiempo_atencion
                self.diccionario[llave]["Fin atencion"] = fin_atencion
                siguiente_paciente.tiempo_aux = str(fin_atencion)
                numero = str(1 + medico.id)
                self.diccionario[llave][numero] = fin_atencion
                self.eventos.append((f"fin_atencion_paciente_{area_atencion.nombre}", fin_atencion))
                llave = self.buscar_key(area_atencion.nombre, "Cola de")
                medico.estado = "Atendiendo"
                medico_key = "Medico " + str(1 + medico.id)
                area_atencion.pacientesAtendidos.append(siguiente_paciente)
                self.diccionario[llave][medico_key] = "Atendiendo"

                self.escribir_fila_tablaResultados(area_atencion.nombre, "fin_atencion", None, None, None, rndAtencion, tiempo_atencion,
                                                    fin_atencion,
                                                    self.pacientesAtendidosConsulta, self.pacientesAtendidosOdontologia,
                                                    self.pacientesAtendidosPediatria,
                                                    self.pacientesAtendidosLaboratorio, self.pacientesAtendidosFarmacia,
                                                    self.mostrar_desde, self.nro_evento_simulado, self.lineas, asiste_servicio)
            else:
                self.escribir_fila_tablaResultados(area_atencion.nombre, "fin_atencion",None, None, None, None, None, None,
                                                    self.pacientesAtendidosConsulta, self.pacientesAtendidosOdontologia,
                                                    self.pacientesAtendidosPediatria,
                                                    self.pacientesAtendidosLaboratorio, self.pacientesAtendidosFarmacia,
                                                    self.mostrar_desde, self.nro_evento_simulado, self.lineas, asiste_servicio)

    def actualizar_tiempo_promedio(self, area_atencion, paciente_atendido, area_nombre):
            paciente_atendido.tiempo_salida = self.reloj

            if area_nombre == "Consulta general":
                
                self.tiempoPermanenciaTotalConsulta += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso) / self.pacientes_atendidos
                
            elif area_nombre == "Odontologia":
                self.tiempoPermanenciaTotalOdontologia += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso) / self.pacientes_atendidos
                
            elif area_nombre == "Pediatria":
                self.tiempoPermanenciaTotalPediatria += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso) / self.pacientes_atendidos
                
            elif area_nombre == "Laboratorio":
                self.tiempoPermanenciaTotalLaboratorio += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso) / self.pacientes_atendidos
                
            elif area_nombre == "Farmacia":
                self.tiempoPermanenciaTotalFarmacia += (paciente_atendido.tiempo_salida - paciente_atendido.tiempo_ingreso) / self.pacientes_atendidos

    def calcularTiempoOcupado(self, area, pacienteAtendido): 
                    # Verificar si hay al menos un médico atendiendo
            hay_medico_atendiendo = any(medico.estado == "Atendiendo" for medico in area.medicos)

            # Acumular tiempo ocupado solo si hay al menos un médico atendiendo
            if hay_medico_atendiendo:
                if area.primer_inicio_atencion is None:
                    area.primer_inicio_atencion = pacienteAtendido.tiempo_inicio_atencion

                if area.nombre == "consulta":
                    self.tiempoOcupadoConsulta = (self.reloj - area.primer_inicio_atencion)
                elif area.nombre == "odontologia":
                    self.tiempoOcupadoOdontologia = (self.reloj - area.primer_inicio_atencion)
                elif area.nombre == "pediatria":
                    self.tiempoOcupadoPediatria = (self.reloj - area.primer_inicio_atencion)
                elif area.nombre == "laboratorio":
                    self.tiempoOcupadoLaboratorio = (self.reloj - area.primer_inicio_atencion)
                elif area.nombre == "farmacia":
                    self.tiempoOcupadoFarmacia = (self.reloj - area.primer_inicio_atencion)

            # Reiniciar el registro del primer inicio de atención si todos los médicos están libres
            if all(medico.estado == "libre" for medico in area.medicos):
                area.primer_inicio_atencion = None

    def calcularEstadisticas(self):

        if self.pacientes_atendidos > 0:
            self.tiempoPermanenciaTotal = self.tiempoPermanenciaTotalConsulta + self.tiempoPermanenciaTotalOdontologia + self.tiempoPermanenciaTotalPediatria + self.tiempoPermanenciaTotalLaboratorio + self.tiempoPermanenciaTotalFarmacia
            tiempoPermanenciaTotal = self.tiempoPermanenciaTotal
            self.tiempoEsperaPromedioGeneral = self.tiempoEsperaPromedioAcConsulta + self.tiempoEsperaPromedioAcOdontologia + self.tiempoEsperaPromedioAcPediatria + self.tiempoEsperaPromedioAcLaboratorio + self.tiempoEsperaPromedioAcFarmacia
            tiempoEsperaPromedioTotal = self.tiempoEsperaPromedioGeneral / self.pacientes_atendidos
        else:
            tiempoEsperaPromedioTotal = 0
            tiempoPermanenciaTotal = 0

        if self.pacientesAtendidosConsulta > 0:

            tiempoEsperaPromedioConsulta = self.tiempoEsperaPromedioAcConsulta / self.pacientesAtendidosConsulta
            porcentajeConsulta = (self.tiempoOcupadoConsulta / self.reloj) * 100
            
        else:
            tiempoEsperaPromedioConsulta = 0
            porcentajeConsulta = 0

        if self.pacientesAtendidosOdontologia > 0:
            tiempoEsperaPromedioOdontologia = self.tiempoEsperaPromedioAcOdontologia / self.pacientesAtendidosOdontologia
            porcentajeOdontologia = (self.tiempoOcupadoOdontologia / self.reloj) * 100
        else:
            tiempoEsperaPromedioOdontologia = 0
            porcentajeOdontologia = 0

        if self.pacientesAtendidosPediatria > 0:
            tiempoEsperaPromedioPediatria = self.tiempoEsperaPromedioAcPediatria / self.pacientesAtendidosPediatria
            porcentajePediatria = (self.tiempoOcupadoPediatria / self.reloj) * 100
            #print(self.reloj)
        else:
            tiempoEsperaPromedioPediatria = 0
            porcentajePediatria = 0

        if self.pacientesAtendidosLaboratorio > 0:
            tiempoEsperaPromedioLaboratorio = self.tiempoEsperaPromedioAcLaboratorio / self.pacientesAtendidosLaboratorio
            porcentajeLaboratorio = (self.tiempoOcupadoLaboratorio / self.reloj) * 100
            #print(self.tiempoOcupadoLaboratorio)
            #print(self.reloj)
        else:
            tiempoEsperaPromedioLaboratorio = 0
            porcentajeLaboratorio = 0

        if self.pacientesAtendidosFarmacia > 0:
            tiempoEsperaPromedioFarmacia = self.tiempoEsperaPromedioAcFarmacia / self.pacientesAtendidosFarmacia
            porcentajeFarmacia = (self.tiempoOcupadoFarmacia / self.reloj) * 100
        else:
            tiempoEsperaPromedioFarmacia = 0
            porcentajeFarmacia = 0

        return (self.pacientes_atendidos, tiempoEsperaPromedioTotal, tiempoEsperaPromedioConsulta, 
                tiempoEsperaPromedioOdontologia, tiempoEsperaPromedioPediatria, tiempoEsperaPromedioLaboratorio, 
                tiempoEsperaPromedioFarmacia, tiempoPermanenciaTotal, porcentajeConsulta, porcentajeOdontologia, porcentajePediatria,
                porcentajeLaboratorio, porcentajeFarmacia, self.pacientesAtendidosConsulta, 
                self.pacientesAtendidosOdontologia, self.pacientesAtendidosPediatria, 
                self.pacientesAtendidosFarmacia, self.pacientesAtendidosLaboratorio, 
                self.tiempoPermanenciaTotalConsulta, self.tiempoPermanenciaTotalFarmacia, 
                self.tiempoPermanenciaTotalLaboratorio, self.tiempoPermanenciaTotalOdontologia, self.tiempoPermanenciaTotalOdontologia)

        
    def procesarObjetosTemporales(self):
        estados_pacientes = []
        for area in self.areas:
            for paciente in area.pacientesAtendidos:
                estados_pacientes.append(paciente.estado)

    # -------------------------- Metodos extra ------------------------------------------

    
    # Metodo para transformar el diccionario en un vector 

    def diccionario_vector(self, d=None):
        if d is None:
            d = self.diccionario

        vector = []
        for key, value in d.items():
            if isinstance(value, dict):
                vector.extend(self.diccionario_vector(value))
            else:
                vector.append(value)
        return vector
    
    # Metodo para buscar keys
    def buscar_key(self, nombre_area, evento):
        claves_encontradas = [clave for clave in self.diccionario.keys() if
                                nombre_area in clave and clave.startswith(evento)]
        if claves_encontradas:
            return claves_encontradas[0]
        else:
            raise KeyError(f"No se encontró la clave para {nombre_area} con evento {evento}")
        
    def limpiar_rnd_otras_areas(self,nombre_area):
        for area in self.areas:
            if area.nombre != "nutricion":
                self.diccionario[self.buscar_key(area.nombre, "llegada")]["RND"] = "-"
                self.diccionario[self.buscar_key(area.nombre, "llegada")]["Tiempo entre llegadas"] = "-"


    def escribir_fila_tablaResultados(self, area, evento, rndLlegada, rndAtencion, tiempo_entre_llegadas, proxima_llegada, tiempo_atencion,
                                        fin_atencion,
                                        pacientesAtendidosConsulta, pacientesAtendidosOdontologia,
                                        pacientesAtendidosPediatria,
                                        pacientesAtendidosLaboratorio, pacientesAtendidosFarmacia, mostrar_desde,
                                        nro_evento_simulado, lineas, asiste_servicio):
            
            evento_map = {
                "consulta": ("llegada_paciente_consulta", "Fin atencion consulta"),
                "odontologia": ("llegada_paciente_odontologia", "Fin atencion odontologia"),
                "pediatria": ("llegada_paciente_pediatria", "Fin atencion pediatria"),
                "laboratorio": ("llegada_paciente_laboratorio", "Fin atencion laboratorio"),
                "farmacia": ("llegada_paciente_farmacia", "Fin atencion farmacia"),
                "nutricion": ("llegada_paciente_nutricion", "Fin atencion nutricion"), 
            }


            if area not in evento_map:
                raise ValueError("Área no reconocida")

            llegada_evento, fin_atencion_evento = evento_map[area]
            # Redondear a 4 decimales
            if tiempo_entre_llegadas is not None:
                tiempo_entre_llegadas = round(tiempo_entre_llegadas, 4)
            if proxima_llegada is not None:
                proxima_llegada = round(proxima_llegada, 4)

            if evento == "llegada":
                if area == "nutricion":
                    pass
                else: 
                    self.diccionario[f"Fin atencion {area}"]["RND"] = rndAtencion
                    self.diccionario[f"Fin atencion {area}"]["Tiempo atencion"] = tiempo_atencion
                    self.diccionario[f"Fin atencion {area}"]["Fin atencion"] = fin_atencion
                    for areas in self.nombre_areas:
                        if areas != area:
                            self.diccionario[f"Fin atencion {areas}"]["RND"] = "-"
                            self.diccionario[f"Fin atencion {areas}"]["Tiempo atencion"] = "-"
                            self.diccionario[f"Fin atencion {areas}"]["Fin atencion"] = "-"

                
            elif evento == "fin_atencion":
                if area == "nutricion":
                    if tiempo_atencion is not None:
                        self.diccionario[f"Fin atencion {area}"]["RND"] = rndAtencion
                        self.diccionario[f"Fin atencion {area}"]["Tiempo atencion"] = tiempo_atencion
                        self.diccionario[f"Fin atencion {area}"]["Fin atencion"] = fin_atencion
                else:

                    for areas in self.nombre_areas:
                        if areas != area:
                            
                            self.diccionario[f"Fin atencion {areas}"]["RND"] = "-"
                            self.diccionario[f"Fin atencion {areas}"]["Tiempo atencion"] = "-"
                            self.diccionario[f"Fin atencion {areas}"]["Fin atencion"] = "-"


            self.diccionario["Evento"] = llegada_evento if evento == "llegada" else fin_atencion_evento
            self.diccionario["Reloj"] = self.reloj

            self.diccionario["Cola de consultas generales"]["Contador"] = pacientesAtendidosConsulta
            self.diccionario["Cola de odontologia"]["Contador"] = pacientesAtendidosOdontologia
            self.diccionario["Cola de pediatria"]["Contador"] = pacientesAtendidosPediatria
            self.diccionario["Cola de laboratorio"]["Contador"] = pacientesAtendidosLaboratorio
            self.diccionario["Cola de farmacia"]["Contador"] = pacientesAtendidosFarmacia

            

            
            if (mostrar_desde <= nro_evento_simulado <= mostrar_desde + 299) or nro_evento_simulado == lineas:
                lista = self.diccionario_vector()
                if nro_evento_simulado == 50:
                    print()
                self.tablaResultados.append(lista)
            
            
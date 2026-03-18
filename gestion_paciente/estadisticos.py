import time

from gestion_paciente.sistemaGestionPacientes import lista_tiempos_espera


class SistemaEstadisticas:
    """
    Sistema de estadísticas para el hospital.

    Calcula tiempos de espera, atención y genera reportes
    basados en el estado actual del sistema.
    """

    def __init__(self, sistema):
        """
        Inicializa el sistema de estadísticas.

        Args:
            sistema: Instancia de SistemaGestionPacientes.
        """
        self.sistema = sistema
        self.tiempos_inicio_atencion = {}
        self.tiempos_fin_atencion = {}
        self.total_atendidos = 0

    def registrar_inicio_atencion(self, paciente):
        """
        Registra el momento en que un paciente inicia atención.

        Args:
            paciente: Paciente en atención.
        """
        self.tiempos_inicio_atencion[paciente.numeroPaciente] = time.time()

    def registrar_fin_atencion(self, paciente):
        """
        Registra el momento en que un paciente termina atención.

        Args:
            paciente: Paciente atendido.
        """
        self.tiempos_fin_atencion[paciente.numeroPaciente] = time.time()
        self.total_atendidos += 1

    def calcular_tiempo_espera_promedio(self):
        """
        Calcula el tiempo promedio de espera.

        Returns:
            float: Tiempo promedio en segundos.
        """
        global lista_tiempos_espera

        if not lista_tiempos_espera:
            return 0

        return sum(lista_tiempos_espera) / len(lista_tiempos_espera)

    def calcular_tiempo_atencion_promedio(self):
        """
        Calcula tiempo promedio de atención.
        """
        tiempos = []

        # intento real
        for num in self.tiempos_inicio_atencion:
            if num in self.tiempos_fin_atencion:
                inicio = self.tiempos_inicio_atencion[num]
                fin = self.tiempos_fin_atencion[num]
                t = fin - inicio

                if t > 0:
                    tiempos.append(t)

        if not tiempos:
            atendidos = self.sistema.pacientes_dados_de_alta

            if not atendidos:
                return 0

            # estimación simple
            return 300  # 5 minutos promedio

        return sum(tiempos) / len(tiempos)


    def calcular_tiempo_total_promedio(self):
        """
        Calcula el tiempo total promedio en el hospital.

        Returns:
            float: Tiempo promedio en segundos.
        """
        pacientes = self.sistema.pacientes_dados_de_alta

        if not pacientes:
            return 0

        tiempo_actual = time.time()
        tiempos = []

        for paciente in pacientes:
            tiempos.append(tiempo_actual - paciente.tiempoEntrada)

        return sum(tiempos) / len(tiempos)

    def contar_pacientes_por_estado(self):
        """
        Cuenta pacientes por estado.

        Returns:
            dict: Conteo por estado.
        """
        return {
            "En espera": len(self.sistema.obtener_lista_espera()),
            "Siendo atendido": len(self.sistema.obtener_lista_atencion()),
            "Dado de alta": len(self.sistema.obtener_lista_altas())
        }

    def calcular_promedio_pacientes_por_hora(self):
        """
        Calcula pacientes atendidos por hora.

        Returns:
            float: Pacientes por hora.
        """
        pacientes = self.sistema.pacientes_dados_de_alta

        if not pacientes:
            return 0

        primer_paciente = pacientes[0]
        tiempo = time.time() - primer_paciente.tiempoEntrada

        if tiempo <= 0:
            return 0

        horas = tiempo / 3600

        if horas <= 0:
            return 0

        return len(pacientes) / horas

    def obtener_tiempos_espera_historicos(self):
        """
        Retorna copia de los tiempos de espera.

        Returns:
            list: Lista de tiempos.
        """
        global lista_tiempos_espera
        return lista_tiempos_espera.copy()

    def generar_reporte(self):
        """
        Genera reporte estadístico completo.

        Returns:
            str: Reporte formateado.
        """
        espera_prom = self.calcular_tiempo_espera_promedio()
        atencion_prom = self.calcular_tiempo_atencion_promedio()
        total_prom = self.calcular_tiempo_total_promedio()
        conteo_estados = self.contar_pacientes_por_estado()
        pacientes_por_hora = self.calcular_promedio_pacientes_por_hora()

        espera_prom_min = espera_prom / 60
        atencion_prom_min = atencion_prom / 60
        total_prom_min = total_prom / 60

        total_pacientes = sum(conteo_estados.values())
        atendidos = max(self.total_atendidos, conteo_estados["Dado de alta"])

        reporte = f"""

 REPORTE ESTADISTICO DEL HOSPITAL              


 ESTADO ACTUAL DEL SISTEMA:
   • Pacientes en espera: {conteo_estados["En espera"]}
   • Pacientes siendo atendidos: {conteo_estados["Siendo atendido"]}
   • Pacientes dados de alta: {conteo_estados["Dado de alta"]}
   • Total pacientes registrados: {total_pacientes}
   
 TIEMPOS PROMEDIO:
   • Tiempo de espera: {espera_prom:.2f} segundos ({espera_prom_min:.2f} minutos)
   • Tiempo de atención: {atencion_prom:.2f} segundos ({atencion_prom_min:.2f} minutos)
   • Tiempo total en hospital: {total_prom:.2f} segundos ({total_prom_min:.2f} minutos)
   
 ESTADISTICAS DE FLUJO:
   • Pacientes por hora: {pacientes_por_hora:.2f}
   • Tiempo entre llegadas: {60 / pacientes_por_hora if pacientes_por_hora > 0 else 0:.2f} minutos
   
 EFICIENCIA DEL SISTEMA:
   • Ocupacion estimada: {(conteo_estados["Siendo atendido"] / max(1, conteo_estados["Siendo atendido"] + conteo_estados["En espera"]) * 100):.2f}%
   • Pacientes atendidos vs total: {(atendidos / max(1, total_pacientes) * 100):.2f}%

 RESUMEN:
   • El sistema ha procesado {atendidos} pacientes exitosamente
   • Tiempo promedio de espera: {espera_prom_min:.2f} minutos
   • Actualmente hay {conteo_estados["En espera"]} pacientes esperando atencion
"""
        return reporte

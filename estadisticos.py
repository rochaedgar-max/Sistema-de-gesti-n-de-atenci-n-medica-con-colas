import time
from collections import deque

from sistema_gestion import lista_tiempos_espera

class SistemaEstadisticas:
    """
    Sistema de estadisticas para el hospital.
    Calcula tiempos de espera, genera reportes y analiza eficiencia.
    Trabaja con las clases Paciente y SistemaGestionPacientes existentes.
    """
    
    def __init__(self, sistema):
        """
        Inicializa el sistema de estadisticas.
        
        Args:
            sistema (SistemaGestionPacientes): Instancia del sistema de gestion existente
        """
        self.sistema = sistema
        # Diccionario para almacenar tiempos de inicio de atencion
        self.tiempos_inicio_atencion = {}
        
    def registrar_inicio_atencion(self, paciente):
        """
        Registra el momento en que un paciente comienza a ser atendido.
        
        Args:
            paciente (Paciente): Paciente que inicia atencion
        """
        self.tiempos_inicio_atencion[paciente.numeroPaciente] = time.time()
    
    def calcular_tiempo_espera_promedio(self):
        """
        Calcula el tiempo promedio que los pacientes esperan para ser atendidos.
        Usa la lista global de tiempos de espera de la primera rama.
        
        Returns:
            float: Tiempo promedio en segundos, 0 si no hay datos.
        """
        global lista_tiempos_espera
        
        if not lista_tiempos_espera:
            return 0
            
        return sum(lista_tiempos_espera) / len(lista_tiempos_espera)
    
    def calcular_tiempo_atencion_promedio(self):
        """
        Calcula el tiempo promedio de atencion medica.
        Estima el tiempo basado en las diferencias entre altas.
        
        Returns:
            float: Tiempo promedio en segundos, 0 si no hay datos.
        """
        if len(self.sistema.pacientes_dados_de_alta) < 2:
            return 0
            
        # Estimacion basada en el orden de las altas
        tiempos_atencion = []
        for i in range(1, len(self.sistema.pacientes_dados_de_alta)):
            paciente_actual = self.sistema.pacientes_dados_de_alta[i]
            paciente_anterior = self.sistema.pacientes_dados_de_alta[i-1]
            
            # Estimamos que la atencion del actual comenzo cuando termino el anterior
            if paciente_actual.numeroPaciente in self.tiempos_inicio_atencion:
                fin_estimado = paciente_actual.tiempoEntrada + 300  # 5 min estimado
                tiempo_atencion = fin_estimado - self.tiempos_inicio_atencion[paciente_actual.numeroPaciente]
                if tiempo_atencion > 0:
                    tiempos_atencion.append(tiempo_atencion)
        
        if not tiempos_atencion:
            return 300  # Retorna 5 minutos como valor por defecto
        
        return sum(tiempos_atencion) / len(tiempos_atencion)
    
    def calcular_tiempo_total_promedio(self):
        """
        Calcula el tiempo total promedio desde ingreso hasta alta.
        
        Returns:
            float: Tiempo promedio en segundos, 0 si no hay datos.
        """
        pacientes_atendidos = self.sistema.pacientes_dados_de_alta
        
        if not pacientes_atendidos:
            return 0
            
        tiempo_actual = time.time()
        tiempos_totales = []
        
        for paciente in pacientes_atendidos:
            # Estimamos el tiempo total hasta ahora
            tiempo_total = tiempo_actual - paciente.tiempoEntrada
            tiempos_totales.append(tiempo_total)
        
        return sum(tiempos_totales) / len(tiempos_totales)
    
    def contar_pacientes_por_estado(self):
        """
        Cuenta cuantos pacientes hay en cada estado.
        
        Returns:
            dict: Diccionario con conteos por estado.
        """
        conteo = {
            "En espera": len(self.sistema.obtener_lista_espera()),
            "Siendo atendido": len(self.sistema.obtener_lista_atencion()),
            "Dado de alta": len(self.sistema.obtener_lista_altas())
        }
        return conteo
    
    def calcular_promedio_pacientes_por_hora(self):
        """
        Calcula el promedio de pacientes atendidos por hora.
        
        Returns:
            float: Pacientes por hora.
        """
        if not self.sistema.pacientes_dados_de_alta:
            return 0
            
        primer_paciente = self.sistema.pacientes_dados_de_alta[0]
        tiempo_transcurrido = time.time() - primer_paciente.tiempoEntrada
        
        if tiempo_transcurrido <= 0:
            return 0
            
        horas = tiempo_transcurrido / 3600
        return len(self.sistema.pacientes_dados_de_alta) / horas if horas > 0 else 0
    
    def obtener_tiempos_espera_historicos(self):
        """
        Retorna la lista completa de tiempos de espera.
        
        Returns:
            list: Lista de tiempos de espera en segundos.
        """
        global lista_tiempos_espera
        return lista_tiempos_espera.copy()
    
    def generar_reporte(self):
        """
        Genera un reporte completo de estadisticas del hospital.
        
        Returns:
            str: Reporte formateado.
        """
        espera_prom = self.calcular_tiempo_espera_promedio()
        atencion_prom = self.calcular_tiempo_atencion_promedio()
        total_prom = self.calcular_tiempo_total_promedio()
        conteo_estados = self.contar_pacientes_por_estado()
        pacientes_por_hora = self.calcular_promedio_pacientes_por_hora()
        
        # Convertir tiempos a minutos para mejor legibilidad
        espera_prom_min = espera_prom / 60
        atencion_prom_min = atencion_prom / 60
        total_prom_min = total_prom / 60
        
        reporte = f"""

 REPORTE ESTADISTICO DEL HOSPITAL              


 ESTADO ACTUAL DEL SISTEMA:
   • Pacientes en espera: {conteo_estados["En espera"]}
   • Pacientes siendo atendidos: {conteo_estados["Siendo atendido"]}
   • Pacientes dados de alta: {conteo_estados["Dado de alta"]}
   • Total pacientes registrados: {sum(conteo_estados.values())}
   
 TIEMPOS PROMEDIO:
   • Tiempo de espera: {espera_prom:.2f} segundos ({espera_prom_min:.2f} minutos)
   • Tiempo de atención: {atencion_prom:.2f} segundos ({atencion_prom_min:.2f} minutos)
   • Tiempo total en hospital: {total_prom:.2f} segundos ({total_prom_min:.2f} minutos)
   
 ESTADISTICAS DE FLUJO:
   • Pacientes por hora: {pacientes_por_hora:.2f}
   • Tiempo entre llegadas: {60/pacientes_por_hora if pacientes_por_hora > 0 else 0:.2f} minutos
   
 EFICIENCIA DEL SISTEMA:
   • Ocupacion estimada: {(conteo_estados["Siendo atendido"] / max(1, conteo_estados["Siendo atendido"] + conteo_estados["En espera"]) * 100):.2f}%
   • Pacientes atendidos vs total: {(conteo_estados["Dado de alta"] / max(1, sum(conteo_estados.values())) * 100):.2f}%

 RESUMEN:
   • El sistema ha procesado {conteo_estados["Dado de alta"]} pacientes exitosamente
   • Tiempo promedio de espera: {espera_prom_min:.2f} minutos
   • Actualmente hay {conteo_estados["En espera"]} pacientes esperando atencion
"""
        return reporte
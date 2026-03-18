class Historico:
    """
    Guarda el historial de pacientes atendidos.
    """

    def __init__(self):
        self.historial = []

    def registrar(self, paciente):
        """
        Registra un paciente en el historial.
        """
        self.historial.append(paciente)

    def obtener_historial(self):
        return self.historial

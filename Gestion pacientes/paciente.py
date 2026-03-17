from collections import deque
import time


class Paciente:
    """
    Representa a un paciente que sera agregado al sistema de atención de pacientes.

    Atributos:
        - numeroPaciente (int): Indentificador único.
        - nombrePaciente (str): Nombre completo.
        - condicionMedica (str): Descripción del padecimiento.
        - tiempoEntrada (float): Marca de tiempo (Unix timestamp) del registro.
        - estado (str): Estado actual ("En espera", "Siendo atendido", "Dado de alta").
    """

    def __init__(self, numeroPaciente, nombrePaciente, condicionMedica) -> None:
        """
        Inicializador de la clase Paciente.

        Args:
            - numeroPaciente (int): ID asignado por el sistema.
            - nombrePaciente (str): Nombre del paciente.
            - condicionMedica (str): Condición médica inicial.
        """

        self.numeroPaciente = numeroPaciente
        self.nombrePaciente = nombrePaciente
        self.condicionMedica = condicionMedica
        self.tiempoEntrada = time.time()
        self.estado = "En espera"

    def obtener_ficha(self) -> str:
        """
        Permite ver los datos del paciente dentro de las listas.
        """

        return (f"Paciente #{self.numeroPaciente}\n"
                f"Nombre: {self.nombrePaciente}\n"
                f"Condición: {self.condicionMedica}\n"
                f"Estado: {self.estado}\n")

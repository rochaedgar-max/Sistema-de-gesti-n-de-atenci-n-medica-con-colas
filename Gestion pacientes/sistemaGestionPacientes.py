from paciente import Paciente
from collections import deque


class SistemaGestionPacientes:
    """
    Gestiona el flujo de pacientes desde su ingreso hasta su alta.

    Atributos:
        - cola_pacientes (deque): Cola de objetos Paciente en espera.
        - pacientes_atendidos (List): Pacientes en consulta.
        - pacientes_dados_de_alta (List): Historial de pacientes dados de alta.
        - contador_pacientes (int): ID automático para los pacientes.
    """

    def __init__(self) -> None:
        """
        Inicializador de la clase SistemaGestionPacientes.
        """

        self.cola_pacientes = deque()
        self.pacientes_atendidos = []
        self.pacientes_dados_de_alta = []
        self.contador_pacientes = 1

    def Agregar_paciente(self, nombre, condicion) -> Paciente:
        """
        Crea un paciente y lo coloca al final de la cola de espera.

        Args:
            nombre (str): Nombre del paciente.
            condicion (str): Condición médica.

        Returns:
            Paciente: El objeto paciente recien creado.

        Raises:
            ValueError: Si el nombre o la condición están vacíos.
        """

        if not nombre or not condicion:
            raise ValueError("El nombre y la condición son obligatorios.")

        nuevo_paciente = Paciente(self.contador_pacientes, nombre, condicion)
        self.cola_pacientes.append(nuevo_paciente)
        self.contador_pacientes += 1
        return nuevo_paciente

    def Atender_paciente(self) -> Paciente:
        """
        Cambia el estado del objeto paciente y lo coloca en una nueva lista.

        Returns:
            None: La lista se encuentra vacía.
            Paciente: Objeto paciente.
        """

        if not self.cola_pacientes:
            return None

        paciente = self.cola_pacientes.popleft()
        paciente.estado = "Siendo atendido"
        self.pacientes_atendidos.append(paciente)
        return paciente

    def Dar_de_alta(self, numeroIngresado) -> str | Paciente | None:
        """
        Finaliza la atención de un paciente.

        Args:
            numeroIngresado (int): ID del paciente para dar de alta.

        Returns:
            Paciente: Si el paciente fue encontrado y dado de alta.
            str: "repetido" si ya estaba dado de alta o "no_encontrado" si no existe.
        """

        for p in self.pacientes_dados_de_alta:
            if p.numeroPaciente == numeroIngresado:
                return "repetido"

        for i, paciente in enumerate(self.pacientes_atendidos):
            if paciente.numeroPaciente == numeroIngresado:
                paciente.estado = "Dado de alta"
                self.pacientes_dados_de_alta.append(paciente)
                self.pacientes_atendidos.pop(i)
                return paciente

        return "no_encontrado"

    def obtener_lista_espera(self) -> list[Paciente]:
        """
        Retorna la lista de los pacientes que se encuentran en espera de ser atendidos.
        """
        return list(self.cola_pacientes)

    def obtener_lista_atencion(self) -> list[Paciente]:
        """
        Retorna la lista de los pacientes que están siendo atendidos.
        """
        return self.pacientes_atendidos

    def obtener_lista_altas(self) -> list[Paciente]:
        """
        Retorna la lista de los pacientes que ya fueron dados de alta.
        """
        return self.pacientes_dados_de_alta

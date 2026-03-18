from paciente import Paciente
from collections import deque
import time


# Lista global que almacena los tiempos de espera (float) para el cálculo de estadísticas.
lista_tiempos_espera = []


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
            str: Manda un error en caso de que alguno de los datos ingresados es incorrecto o
            es un espacio en blanco.
        """

        nombre = str(nombre).strip()
        condicion = str(condicion).strip()

        if not nombre or not condicion:
            return "[Error]: El nombre y la condición son obligatorios.\n"

        if not isinstance(nombre, str) or not isinstance(condicion, str):
            return " [Error]: El nombre o la condición no pueden ser valores enteros.\n"

        if not nombre.replace(" ", "").isalpha():
            return " [Error]: El nombre no debe contener números ni simbolos.\n"

        if not condicion.replace(" ", "").isalpha():
            return " [Error]: La condición no debe contener números ni simbolos.\n"

        nuevo_paciente = Paciente(self.contador_pacientes, nombre, condicion)
        self.cola_pacientes.append(nuevo_paciente)
        self.contador_pacientes += 1

        return nuevo_paciente

    def Atender_paciente(self) -> str | Paciente:
        """
        Cambia el estado del objeto paciente y lo coloca en una nueva lista.

        Returns:
            str: Manda un aviso si la lista se encuentra vacía.
            Paciente: Objeto paciente.
        """

        if not self.cola_pacientes:
            return " [Aviso]: No hay pacientes en espera.\n"

        paciente = self.cola_pacientes.popleft()
        paciente.estado = "Siendo atendido"
        tiempo_espera = time.time() - paciente.tiempoEntrada
        lista_tiempos_espera.append(tiempo_espera)
        self.pacientes_atendidos.append(paciente)
        return paciente

    def Dar_de_alta(self, numeroIngresado=None) -> str | Paciente:
        """
        Finaliza la atención de un paciente.

        Args:
            numeroIngresado (int): ID del paciente para dar de alta.

        Returns:
            Paciente: Si el paciente fue encontrado y dado de alta.
            str: Manda un aviso para indicar si el paciente ya fue dado de alta o si no fue encontrado.
        """

        if numeroIngresado is None:
            return " [Error]: Debes ingresar el número de ID del paciente para darlo de alta.\n"

        if not isinstance(numeroIngresado, int):
            return " [Error]: El ID debe ser un número entero.\n"

        for p in self.pacientes_dados_de_alta:
            if p.numeroPaciente == numeroIngresado:
                return f" [Aviso]: El paciente #{numeroIngresado} ya fue dado de alta.\n"

        for i, paciente in enumerate(self.pacientes_atendidos):
            if paciente.numeroPaciente == numeroIngresado:
                paciente.estado = "Dado de alta"
                self.pacientes_dados_de_alta.append(paciente)
                self.pacientes_atendidos.pop(i)
                return paciente

        return " [Aviso]: El número de paciente ingresado no fue encontrado.\n"

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

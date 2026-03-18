from collections import deque


class PrioridadMedica:
    """
    Gestiona el orden de atención por prioridad médica.
    """

    def ordenar_por_prioridad(self, cola):
        """
        Ordena una cola de pacientes por prioridad (1 = mayor prioridad).

        Args:
            cola (deque): Cola de pacientes.

        Returns:
            deque: Cola ordenada.
        """
        return deque(sorted(cola, key=lambda p: getattr(p, "prioridad", 3)))

import unittest
import os

from gestion_paciente.sistemaGestionPacientes import SistemaGestionPacientes
from gestion_paciente.prioridad_medica import PrioridadMedica
from gestion_paciente.reservas import Reservas
from gestion_paciente.persistencia import Persistencia
from gestion_paciente.estadisticos import SistemaEstadisticas


class TestSistemaHospitalario(unittest.TestCase):
    """
    Pruebas unitarias del sistema hospitalario.
    """

    def setUp(self):
        """
        Inicializa instancias antes de cada prueba.
        """
        self.sistema = SistemaGestionPacientes()
        self.prioridad = PrioridadMedica()
        self.reservas = Reservas()
        self.persistencia = Persistencia()
        self.estadisticas = SistemaEstadisticas(self.sistema)

    def test_registro_paciente_valido(self):
        """
        Verifica que un paciente válido se registre correctamente.
        """
        paciente = self.sistema.Agregar_paciente("Juan Perez", "Dolor")

        self.assertFalse(isinstance(paciente, str))
        self.assertEqual(len(self.sistema.cola_pacientes), 1)

    def test_registro_paciente_invalido(self):
        """
        Verifica que datos inválidos no se registren.
        """
        paciente = self.sistema.Agregar_paciente("", "")

        self.assertTrue(isinstance(paciente, str))

    def test_atender_paciente(self):
        """
        Verifica que un paciente pueda ser atendido.
        """
        self.sistema.Agregar_paciente("Ana", "Fiebre")

        paciente = self.sistema.Atender_paciente()

        self.assertFalse(isinstance(paciente, str))
        self.assertEqual(len(self.sistema.cola_pacientes), 0)

    def test_prioridad(self):
        """
        Verifica que los pacientes se ordenen por prioridad.
        """
        p1 = self.sistema.Agregar_paciente("A", "Normal")
        p2 = self.sistema.Agregar_paciente("B", "Grave")

        p1.prioridad = 3
        p2.prioridad = 1

        ordenados = self.prioridad.ordenar_por_prioridad(
            self.sistema.cola_pacientes
        )

        self.assertEqual(ordenados[0].nombrePaciente, "B")

    def test_reserva(self):
        """
        Verifica que una reserva se genere correctamente.
        """
        mensaje = self.reservas.reservar(
            "Luis", "Chequeo", "2026-03-20", "General"
        )

        self.assertTrue(isinstance(mensaje, str))

    def test_persistencia_guardar_cargar(self):
        """
        Verifica guardado y carga de datos.
        """
        self.sistema.Agregar_paciente("Mario", "Dolor")

        self.persistencia.guardar(self.sistema)

        nuevo_sistema = SistemaGestionPacientes()
        self.persistencia.cargar(nuevo_sistema)

        self.assertGreater(len(nuevo_sistema.cola_pacientes), 0)

        if os.path.exists("datos.json"):
            os.remove("datos.json")

    def test_estadisticas_basicas(self):
        """
        Verifica que estadísticas no fallen.
        """
        self.sistema.Agregar_paciente("Pedro", "Fiebre")
        paciente = self.sistema.Atender_paciente()

        if not isinstance(paciente, str):
            self.estadisticas.registrar_inicio_atencion(paciente)
            self.estadisticas.registrar_fin_atencion(paciente)

        reporte = self.estadisticas.generar_reporte()

        self.assertTrue(isinstance(reporte, str))
        self.assertIn("REPORTE", reporte.upper())

    def test_sistema_vacio(self):
        """
        Verifica comportamiento con sistema vacío.
        """
        paciente = self.sistema.Atender_paciente()

        self.assertTrue(isinstance(paciente, str))


if __name__ == "__main__":
    unittest.main()

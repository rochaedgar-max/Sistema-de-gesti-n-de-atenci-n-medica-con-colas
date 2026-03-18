import json


class Persistencia:
    """
    Maneja guardado y carga del sistema en formato JSON.
    """

    def guardar(self, sistema, archivo="datos.json"):
        """
        Guarda el estado actual del sistema.

        Args:
            sistema: SistemaGestionPacientes.
            archivo (str): Ruta del archivo.
        """
        data = {
            "espera": [p.__dict__ for p in sistema.obtener_lista_espera()],
            "atencion": [p.__dict__ for p in sistema.obtener_lista_atencion()],
            "alta": [p.__dict__ for p in sistema.obtener_lista_altas()]
        }

        with open(archivo, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, sistema, archivo="datos.json"):
        """
        Carga datos en el sistema existente sin reemplazarlo.

        Args:
            sistema: SistemaGestionPacientes.
            archivo (str): Ruta del archivo.
        """
        try:
            with open(archivo, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return False

        sistema.cola_pacientes.clear()
        sistema.pacientes_atendidos.clear()
        sistema.pacientes_dados_de_alta.clear()

        for p in data["espera"]:
            sistema.cola_pacientes.append(self._crear_paciente(p))

        for p in data["atencion"]:
            sistema.pacientes_atendidos.append(self._crear_paciente(p))

        for p in data["alta"]:
            sistema.pacientes_dados_de_alta.append(self._crear_paciente(p))

        return True

    def _crear_paciente(self, data):
        """
        Reconstruye objeto paciente desde diccionario.
        """
        class Dummy:
            pass

        p = Dummy()
        p.__dict__.update(data)
        return p

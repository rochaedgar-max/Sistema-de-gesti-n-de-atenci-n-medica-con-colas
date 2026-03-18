class Reservas:
    """
    Gestiona las citas médicas futuras.
    """

    def __init__(self):
        self.citas = []

    def validar_texto(self, texto):
        return texto.strip() and texto.replace(" ", "").isalpha()

    def reservar(self, nombre, condicion, fecha, departamento):
        """
        Registra una cita médica.

        Returns:
            str: Mensaje de resultado.
        """

        if not self.validar_texto(nombre) or not self.validar_texto(condicion):
            return "Error: Nombre o condición inválidos"

        if not fecha.strip():
            return "Error: Fecha inválida"

        cita = {
            "nombre": nombre,
            "condicion": condicion,
            "fecha": fecha,
            "departamento": departamento
        }

        self.citas.append(cita)
        return f"Cita registrada para {nombre}"

    def obtener_citas(self):
        return self.citas

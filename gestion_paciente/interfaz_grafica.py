import tkinter as tk
from tkinter import ttk

from gestion_paciente.sistemaGestionPacientes import SistemaGestionPacientes
from gestion_paciente.prioridad_medica import PrioridadMedica
from gestion_paciente.reservas import Reservas
from gestion_paciente.persistencia import Persistencia
from gestion_paciente.estadisticos import SistemaEstadisticas


class InterfazGrafica:
    """
    Interfaz gráfica del sistema hospitalario.
    """

    def __init__(self):
        """
        Inicializa la interfaz y módulos del sistema.
        """
        self.sistema = SistemaGestionPacientes()
        self.prioridad = PrioridadMedica()
        self.reservas = Reservas()
        self.persistencia = Persistencia()
        self.estadisticas = SistemaEstadisticas(self.sistema)

        self.root = tk.Tk()
        self.root.title("Sistema Hospitalario")
        self.root.geometry("350x350")
        self.root.resizable(False, False)

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Sistema Hospitalario",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Registrar Paciente",
            command=self.ventana_registro,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Atender Paciente",
            command=self.atender,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Reservar Cita",
            command=self.ventana_reserva,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Ver Reporte",
            command=self.mostrar_reporte,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Guardar",
            command=self.guardar,
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="Cargar",
            command=self.cargar,
        ).pack(fill="x", pady=5)

        self.label = tk.Label(frame, text="", fg="blue")
        self.label.pack(pady=10)

    def ejecutar(self):
        """
        Ejecuta la aplicación.
        """
        self.root.mainloop()

    def validar_texto(self, texto):
        """
        Valida texto con letras y espacios.

        Args:
            texto (str): Texto a validar.

        Returns:
            bool
        """
        return texto.strip() and texto.replace(" ", "").isalpha()

    def hacer_modal(self, ventana):
        """
        Configura ventana como modal.

        Args:
            ventana (Toplevel)
        """
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.focus()
        ventana.wait_window()

    def ventana_registro(self):
        """
        Ventana de registro de pacientes.
        """
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Paciente")
        ventana.geometry("300x300")
        ventana.resizable(False, False)

        frame = tk.Frame(ventana, padx=15, pady=15)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, sticky="w")
        nombre = tk.Entry(frame)
        nombre.grid(row=1, column=0, sticky="ew")

        tk.Label(frame, text="Condición").grid(row=2, column=0, sticky="w")
        condicion = tk.Entry(frame)
        condicion.grid(row=3, column=0, sticky="ew")

        tk.Label(frame, text="Prioridad").grid(row=4, column=0, sticky="w")
        prioridad = ttk.Combobox(
            frame,
            values=["1 - Emergencia", "2 - Grave", "3 - Normal"],
            state="readonly",
        )
        prioridad.current(2)
        prioridad.grid(row=5, column=0, sticky="ew")

        error = tk.Label(frame, text="", fg="red")
        error.grid(row=6, column=0)

        def guardar():
            n = nombre.get()
            c = condicion.get()

            if not self.validar_texto(n):
                error.config(text="Nombre inválido")
                return

            if not self.validar_texto(c):
                error.config(text="Condición inválida")
                return

            paciente = self.sistema.Agregar_paciente(n, c)

            if isinstance(paciente, str):
                error.config(text=paciente)
                return

            paciente.prioridad = int(prioridad.get()[0])

            self.label.config(
                text=f"Paciente {paciente.nombrePaciente} registrado"
            )
            ventana.destroy()

        ttk.Button(frame, text="Guardar", command=guardar).grid(
            row=7, column=0, pady=10, sticky="ew"
        )

        self.hacer_modal(ventana)

    def atender(self):
        """
        Atiende paciente con prioridad.
        """
        self.sistema.cola_pacientes = self.prioridad.ordenar_por_prioridad(
            self.sistema.cola_pacientes
        )

        paciente = self.sistema.Atender_paciente()

        if isinstance(paciente, str):
            self.label.config(text=paciente)
            return

        self.estadisticas.registrar_inicio_atencion(paciente)
        self.estadisticas.registrar_fin_atencion(paciente)

        self.label.config(text=f"Turno: {paciente.nombrePaciente}")

    def ventana_reserva(self):
        """
        Ventana de reservas.
        """
        ventana = tk.Toplevel(self.root)
        ventana.title("Reservar Cita")
        ventana.geometry("300x320")
        ventana.resizable(False, False)

        frame = tk.Frame(ventana, padx=15, pady=15)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, sticky="w")
        nombre = tk.Entry(frame)
        nombre.grid(row=1, column=0, sticky="ew")

        tk.Label(frame, text="Condición").grid(row=2, column=0, sticky="w")
        condicion = tk.Entry(frame)
        condicion.grid(row=3, column=0, sticky="ew")

        tk.Label(frame, text="Fecha").grid(row=4, column=0, sticky="w")
        fecha = tk.Entry(frame)
        fecha.grid(row=5, column=0, sticky="ew")

        tk.Label(frame, text="Departamento").grid(
            row=6, column=0, sticky="w"
        )
        depto = ttk.Combobox(
            frame,
            values=["General", "Urgencias", "Pediatria"],
            state="readonly",
        )
        depto.current(0)
        depto.grid(row=7, column=0, sticky="ew")

        error = tk.Label(frame, text="", fg="red")
        error.grid(row=8, column=0)

        def guardar():
            n = nombre.get()
            c = condicion.get()
            f = fecha.get()

            if not self.validar_texto(n):
                error.config(text="Nombre inválido")
                return

            if not self.validar_texto(c):
                error.config(text="Condición inválida")
                return

            if not f.strip():
                error.config(text="Fecha requerida")
                return

            mensaje = self.reservas.reservar(n, c, f, depto.get())
            self.label.config(text=mensaje)
            ventana.destroy()

        ttk.Button(frame, text="Reservar", command=guardar).grid(
            row=9, column=0, pady=10, sticky="ew"
        )

        self.hacer_modal(ventana)

    def mostrar_reporte(self):
        """
        Muestra reporte estadístico.
        """
        ventana = tk.Toplevel(self.root)
        ventana.title("Reporte")
        ventana.geometry("500x400")

        texto = tk.Text(ventana, wrap="word")
        texto.pack(expand=True, fill="both")

        reporte = self.estadisticas.generar_reporte()
        texto.insert(tk.END, reporte)
        texto.config(state="disabled")

        self.hacer_modal(ventana)

    def guardar(self):
        """
        Guarda datos en JSON.
        """
        self.persistencia.guardar(self.sistema)
        self.label.config(text="Datos guardados")

    def cargar(self):
        """
        Carga datos desde JSON.
        """
        ok = self.persistencia.cargar(self.sistema)

        if not ok:
            self.label.config(text="No hay datos")
            return

        self.label.config(text="Datos cargados correctamente")

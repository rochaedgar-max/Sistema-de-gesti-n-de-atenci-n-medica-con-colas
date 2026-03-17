# 🏥 Sistema de Gestión de Atención Médica con Colas

## 📌 Descripción
Este sistema es una solución diseñada para organizar y optimizar la atención de pacientes en una unidad médica, utilizando estructuras de datos tipo cola.  

Su propósito es garantizar una atención eficiente, ya sea respetando el orden de llegada (**FIFO**) o priorizando casos según su gravedad médica.

---

## ⚙️ Funcionalidades principales

### 👥 Gestión de pacientes
El sistema permite administrar el flujo de pacientes desde su llegada hasta su atención:

- **Registro de pacientes (enqueue):**  
  Cada paciente que llega es registrado en la sala de espera y agregado a una cola.

- **Atención de pacientes (dequeue):**  
  Los pacientes son llamados para atención médica:
  - Por orden de llegada (**FIFO**)
  - O según su **prioridad médica**

- **Consulta del siguiente paciente:**  
  Permite visualizar quién será el próximo paciente en ser atendido sin retirarlo de la cola.

---

### 🚑 Sistema de prioridades médicas
Para mejorar la atención en situaciones críticas:

- Se implementa una **cola de prioridad**, donde:
  - Pacientes con emergencias tienen mayor prioridad
  - Se manejan niveles como: **alta, media, baja**

- **Múltiples departamentos:**  
  El sistema puede gestionar diferentes áreas médicas (urgencias, consulta general, pediatría, etc.), cada una con su propia cola.

---

### 📊 Estadísticas y análisis
El sistema incluye herramientas para evaluar su desempeño:

- **Cálculo de tiempos de espera promedio:**  
  Permite medir cuánto tiempo esperan los pacientes antes de ser atendidos.

- **Reportes de eficiencia:**  
  Genera informes sobre:
  - Número de pacientes atendidos
  - Tiempo promedio de atención
  - Rendimiento por departamento

---

## 🚀 Posibles mejoras

### 🔔 Notificaciones
- Avisar a los pacientes cuando su turno está próximo  
- Implementación mediante pantallas, SMS o apps móviles  

### 📅 Reservas de citas
- Permitir agendar consultas para fechas futuras  
- Reducir la saturación en la sala de espera  

### 🖥️ Interfaz gráfica
- Desarrollar una interfaz visual amigable:
  - Panel para recepcionistas  
  - Pantalla de turnos para pacientes  
  - Dashboard para administradores  

### 🗂️ Histórico de atenciones
- Registrar todas las consultas:
  - Datos del paciente  
  - Tiempo de espera  
  - Tipo de atención o diagnóstico  
- Útil para análisis y toma de decisiones  

---

## 🎯 Objetivo del sistema
El sistema busca:

- Mejorar la organización en la atención médica  
- Reducir tiempos de espera  
- Priorizar casos urgentes  
- Facilitar la toma de decisiones mediante datos  

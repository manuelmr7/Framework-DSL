"""
PRUEBA DEL REPLICATOR

Objetivo: comprobar de principio a fin que una tarea creada con el factory method
(CreadorTareas) lee un mensaje de un Slot de entrada y deja una copia en cada
uno de los Slots de salida.

Pasos:
  1. Se crean tres Slots vacíos: una entrada y dos salidas.
  2. Se construye un Mensaje con un cuerpo XML sencillo (id 1) y se escribe
     en el Slot de entrada.
  3. Se pide a CreadorTareas una tarea de tipo REPLICATOR conectada a esos Slots.
     El main no escribe Replicator(...): el parámetro TipoTarea decide qué
     clase se instancia.
  4. Se ejecuta la tarea: lee el mensaje de la entrada (lo saca del Slot) y
     escribe una copia en cada salida.

Resultado esperado:
  - Cada Slot de salida contiene 1 mensaje  ->  imprime "1 1"
  - El Slot de entrada ha quedado vacío     ->  imprime "True"
"""

from lxml import etree
from Slots.Slot import Slot
from Slots.Mensaje import Mensaje
from Tareas.CreadorTareas import CreadorTareas
from Tareas.TipoTarea import TipoTarea

# 1. Slots: una entrada y dos salidas
entrada = Slot()
salida1 = Slot()
salida2 = Slot()

# 2. Mensaje de prueba en el Slot de entrada
cuerpo = etree.ElementTree(etree.fromstring("<pedido><linea>A</linea></pedido>"))
entrada.escribir_mensaje(Mensaje(cuerpo, 1))

# 3. Creación de la tarea mediante el factory method
rep = CreadorTareas.crear(TipoTarea.REPLICATOR, [entrada], [salida1, salida2])

# 4. Ejecución
rep.ejecutar()

# Comprobaciones
print(salida1.get_longitud_mensaje(), salida2.get_longitud_mensaje())  # 1 1
print(entrada.esta_vacio())                                            # True
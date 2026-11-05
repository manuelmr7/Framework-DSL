# Framework-DSL

Framework de integración secuencial en Python, basado en un DSL, para orquestar flujos de datos y canalizaciones paso a paso de forma declarativa. Proyecto de la asignatura Integración de la Información y Aplicaciones (ETSI Huelva).

## Arquitectura

El framework se organiza en cuatro bloques, según el diagrama de diseño (`docs/diagrama_framework_DSL.drawio`):

| Bloque | Descripción |
|---|---|
| **Slots** | Buffers FIFO que contienen mensajes. Conectan las tareas entre sí. |
| **Mensajes** | Cabecera (id, id de correlación, id de secuencia, longitud) y cuerpo XML. |
| **Tareas** | Unidades de procesamiento. Leen mensajes de los slots de entrada y escriben en los de salida. |
| **Puertos y conectores** | Comunican el framework con el exterior. Un conector conoce a varios puertos, y cada puerto a un slot. |

Las tareas solo conocen a los slots, nunca a los puertos ni a los conectores.

### Creación de tareas (Factory Method parametrizado)

Todas las tareas se crean desde una única clase y un único método, `CreadorTareas.crear()`. El parámetro `TipoTarea` decide qué clase se instancia, de modo que la aplicación nunca llama directamente a `Splitter(...)`, `Translator(...)`, etc.

```python
tarea = CreadorTareas.crear(TipoTarea.SPLITTER, [slot_entrada], [slot_salida], "//linea")
```

Los argumentos son: el tipo de tarea, la lista de slots de entrada, la lista de slots de salida y la configuración propia de cada tarea (xpath, ruta de un XSLT, etc.).

> `TipoTarea` indica **qué clase crear**. No debe confundirse con `Tipo` (`ROUTER`, `TRANSFORMER`, `MODIFIER`), que es la categoría de la tarea.

## Estructura del proyecto

```
Framework/
├── Conectores/
├── Puertos/        Puerto, PuertoIN, PuertoOUT, PuertoSOL
├── Slots/          Slot, Mensaje
├── Tareas/         Tarea, Tipo, TipoTarea, CreadorTareas y una clase por tarea
├── docs/           Diagrama de diseño
└── main.py         Ejemplo de uso
```

## Tareas

| Tarea | Función | Estado |
|---|---|---|
| Replicator | Copia cada mensaje a todas las salidas | Implementada |
| Merger | Reúne los mensajes de varias entradas en una salida | Pendiente |
| Splitter | Divide un mensaje en fragmentos mediante un xpath | Pendiente |
| Distribuidor | Envía cada mensaje a una salida según condiciones xpath | Pendiente |
| Translator | Transforma el cuerpo con una plantilla XSLT | Pendiente |
| Correlator | Agrupa mensajes relacionados por un xpath | Pendiente |
| CorrelationIdSetter | Asigna el id de correlación a mensajes relacionados | Pendiente |
| ContextEnricher | Completa un mensaje con datos de otro | Pendiente |
| Aggregator | Reconstruye un mensaje a partir de sus fragmentos | Pendiente |

## Requisitos e instalación

- Python 3.10 o superior
- [lxml](https://lxml.de/)

```bash
git clone https://github.com/manuelmr7/Framework-DSL.git
cd Framework-DSL
python -m venv .venv
.venv\Scripts\activate        # En Linux/macOS: source .venv/bin/activate
pip install lxml
```

## Ejemplo de uso

```python
from lxml import etree
from Slots.Slot import Slot
from Slots.Mensaje import Mensaje
from Tareas.CreadorTareas import CreadorTareas
from Tareas.TipoTarea import TipoTarea

entrada, salida1, salida2 = Slot(), Slot(), Slot()

cuerpo = etree.ElementTree(etree.fromstring("<pedido><linea>A</linea></pedido>"))
entrada.escribir_mensaje(Mensaje(cuerpo, 1))

replicator = CreadorTareas.crear(TipoTarea.REPLICATOR, [entrada], [salida1, salida2])
replicator.ejecutar()

print(salida1.get_longitud_mensaje(), salida2.get_longitud_mensaje())  # 1 1
```

## Añadir una nueva tarea

1. Crear `Tareas/NuevaTarea.py` con una clase que herede de `Tarea` e implemente `ejecutar()`.
2. Añadir el miembro correspondiente a `TipoTarea`.
3. Registrar la clase en el diccionario de `CreadorTareas`.

## Autor

Manuel Muñoz — Universidad de Huelva

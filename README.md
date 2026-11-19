# Framework-DSL

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![lxml](https://img.shields.io/badge/XML%20%2F%20XSLT-lxml-0EA5E9?style=for-the-badge)](https://lxml.de/)
[![Asignatura](https://img.shields.io/badge/ETSI%20Huelva-IIA-22C55E?style=for-the-badge)](#autores)

Framework de integración secuencial en Python, basado en un **Domain-Specific Language (DSL)** e inspirado en *Enterprise Integration Patterns* (EIP), para orquestar flujos de datos y canalizaciones XML paso a paso de forma declarativa.

Proyecto desarrollado para la asignatura **Integración de la Información y Aplicaciones** en la **Escuela Técnica Superior de Ingeniería (ETSI) — Universidad de Huelva**.

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Arquitectura](#arquitectura)
  - [Creación de tareas (Factory Method parametrizado)](#creación-de-tareas-factory-method-parametrizado)
- [Catálogo de tareas](#catálogo-de-tareas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos e instalación](#requisitos-e-instalación)
- [Uso rápido](#uso-rápido)
- [Extensibilidad: añadir una nueva tarea](#extensibilidad-añadir-una-nueva-tarea)
- [Autores](#autores)

---

## Descripción general

**Framework-DSL** desacopla la definición de las canalizaciones de integración de su ejecución subyacente mediante el paso de mensajes XML entre colas internas. Permite componer tareas de enrutamiento, transformación y modificación de manera modular sin acoplar los componentes de procesamiento a los canales externos de entrada o salida.

---

## Arquitectura

El framework se organiza en **cuatro bloques fundamentales**, siguiendo el diagrama de diseño disponible en `diagrama_framework_DSL_v3.drawio.png`[cite: 1]:

| Bloque | Responsabilidad |
|---|---|
| **Slots** | Buffers FIFO que almacenan mensajes en tránsito y conectan las tareas entre sí. |
| **Mensajes** | Unidad mínima de intercambio: cabecera (`id`, `id` de correlación, `id` de secuencia, longitud) y cuerpo XML. |
| **Tareas** | Unidades de procesamiento atómicas. Leen mensajes de sus slots de entrada y escriben resultados en los de salida. |
| **Puertos y conectores** | Capa de comunicación con el exterior. Un conector gestiona varios puertos, y cada puerto enlaza con un slot. |

> **Principio de desacoplamiento:** Las tareas conocen únicamente a sus **slots** de entrada y salida; nunca interactúan directamente con puertos ni conectores.

### Creación de tareas (Factory Method parametrizado)

Todas las tareas se instancian a través de una única clase y un único método estático: `CreadorTareas.crear()`. El parámetro `TipoTarea` determina qué subclase concreta se construye, evitando que la aplicación cliente acople su código a constructores específicos (`Splitter(...)`, `Translator(...)`, etc.).

```python
tarea = CreadorTareas.crear(
    TipoTarea.SPLITTER,
    [slot_entrada],
    [slot_salida],
    "//linea",
)
```

| Argumento | Descripción |
|---|---|
| `tipo_tarea` | Miembro del enumerado `TipoTarea` que identifica la tarea concreta a instanciar. |
| `entradas` | Lista de objetos `Slot` desde los que la tarea leerá mensajes. |
| `salidas` | Lista de objetos `Slot` en los que la tarea depositará los mensajes procesados. |
| `*config` | Parámetros específicos de la tarea (expresión XPath, ruta a plantilla XSLT, etc.). |

> **Nota de diseño:** `TipoTarea` indica **qué clase instanciar**. No debe confundirse con `Tipo` (`ROUTER`, `TRANSFORMER`, `MODIFIER`), que representa la categoría funcional de la tarea.

---

## Catálogo de tareas

| Tarea | Función | Estado |
|---|---|---|
| **Replicator** | Copia cada mensaje recibido hacia todas las salidas configuradas | ✅ Implementada |
| **Merger** | Reúne los mensajes procedentes de varias entradas en una única salida | ✅ Implementada |
| **Splitter** | Divide un mensaje XML en fragmentos mediante una expresión XPath | ✅ Implementada |
| **Translator** | Transforma el cuerpo XML aplicando una plantilla XSLT | ✅ Implementada |
| **ContextEnricher** | Enriquece el contenido de un mensaje combinándolo con datos de otro | ✅ Implementada |
| **Distribuidor** | Enruta cada mensaje a una salida específica según condiciones XPath | ✅ Implementada |
| **Correlator** | Agrupa mensajes relacionados a partir de un identificador XPath | ✅ Implementada |
| **CorrelationIdSetter** | Asigna el identificador de correlación a mensajes relacionados | ✅ Implementada |
| **Aggregator** | Reconstruye un mensaje completo a partir de sus fragmentos | ✅ Implementada |

---

## Estructura del proyecto

El código fuente principal del framework se encuentra dentro de `src/`[cite: 1]. Por cada caso de uso o problema de integración resuelto se crea una carpeta dedicada en la raíz del repositorio (como `Problema café/`)[cite: 1], acompañada de la documentación y diagramas de secuencia del proyecto[cite: 1]:

```text
Framework-DSL/
├── Problema café/                        # Caso de integración del problema del café (XML, XSLT y flujo)[cite: 1]
├── SECUENCIA IIA/                        # Diagramas y documentación de secuencias de la asignatura[cite: 1]
├── src/                                  # Núcleo del framework[cite: 1]
│   ├── Conectores/                       # Conectores para la comunicación con sistemas externos
│   ├── Puertos/                          # Puerto, PuertoIN, PuertoOUT, PuertoSOL
│   ├── Slots/                            # Slot (cola FIFO) y Mensaje (cabecera + cuerpo XML)
│   ├── Tareas/                           # Tarea, Tipo, TipoTarea, CreadorTareas y clases concretas
│   └── main.py                           # Script principal de ejemplo
├── .gitignore[cite: 1]
├── Diagrama de secuencia simple Splitter.rtf  # Documentación de secuencia de la tarea Splitter[cite: 1]
├── diagrama_framework_DSL_v3.drawio.png  # Diagrama de arquitectura del framework[cite: 1]
└── README.md                             # Documentación del proyecto[cite: 1]
```

> **Convención para nuevos casos de uso:** Para modelar un nuevo problema de integración, basta con crear una nueva carpeta en la raíz del repositorio (siguiendo el esquema de `Problema café/`)[cite: 1] e importar los componentes desde `src/`.

---

## Requisitos e instalación

- **Python** 3.10 o superior
- **[lxml](https://lxml.de/)** para el procesamiento XML, XPath y XSLT

```bash
# 1. Clonar el repositorio
git clone [https://github.com/manuelmr7/Framework-DSL.git](https://github.com/manuelmr7/Framework-DSL.git)
cd Framework-DSL

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Instalar dependencias
pip install lxml
```

---

## Uso rápido

El siguiente ejemplo instancia tres slots, introduce un mensaje XML en el slot de entrada y utiliza `CreadorTareas` para duplicarlo mediante un `Replicator`:

```python
from lxml import etree
from src.Slots.Slot import Slot
from src.Slots.Mensaje import Mensaje
from src.Tareas.CreadorTareas import CreadorTareas
from src.Tareas.TipoTarea import TipoTarea

# Definición de canales internos (slots)
entrada, salida1, salida2 = Slot(), Slot(), Slot()

# Construcción e inserción del mensaje XML
cuerpo = etree.ElementTree(etree.fromstring("<pedido><linea>A</linea></pedido>"))
entrada.escribir_mensaje(Mensaje(cuerpo, 1))

# Instanciación y ejecución de la tarea mediante el Factory Method
replicator = CreadorTareas.crear(TipoTarea.REPLICATOR, [entrada], [salida1, salida2])
replicator.ejecutar()

print(salida1.get_longitud_mensaje(), salida2.get_longitud_mensaje())  # Salida: 1 1
```

---

## Extensibilidad: añadir una nueva tarea

Para incorporar una nueva operación al catálogo del framework sin alterar el flujo existente:

1. **Implementar la clase:** Crear `src/Tareas/NuevaTarea.py` heredando de `Tarea` e implementando el método `ejecutar()`.
2. **Registrar el identificador:** Añadir el nuevo miembro en el enumerado `TipoTarea`.
3. **Actualizar la factoría:** Asociar el nuevo `TipoTarea` con su clase en el diccionario interno de `CreadorTareas`.

---

## Autores

- **Manuel Martín Rodrigo**
- **Iván González Díaz**
- **Carmen Gutiérrez Sánchez**
- **Nabila Maamou**

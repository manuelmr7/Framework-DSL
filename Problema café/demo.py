"""
demo.py — Problema Cafetería
Solución de integración para el sistema de comandas del café.

Flujo (según Solución Problema Integración.png):
  1. ConectorFichero (poll)  → lee cada comanda XML de xml/orderN.xml
  2. CorrelationIDSetter     → asigna id de correlación (order_id del XML)
  3. Splitter                → divide la comanda en un fragmento por bebida (//drink)
  4. Replicator              → duplica cada fragmento bebida a dos ramas
  5a. Filter bebidas frías   → deja pasar solo drink[type='cold']
  5b. Filter bebidas calientes → deja pasar solo drink[type='hot']
  6a. PuertoSOL Barman Frío  → simula entrega al barman de frías y recibe respuesta
  6b. PuertoSOL Barman Caliente → simula entrega al barman de calientes y recibe respuesta
  7. Merger                  → reúne todas las bebidas preparadas en un solo slot
  8. Reconstrucción XML      → ensambla el <cafe_order> completo con todas las bebidas
  9. Translator (XSLT)       → transforma a <entrega> para el camarero
 10. ConectorFichero (write) → escribe en entregas/orderN.xml
"""

import sys
import os
import copy
import glob

from lxml import etree

# Añadimos src/ al path para poder importar el framework
SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, SRC_PATH)

from Slots.Slot import Slot
from Slots.Mensaje import Mensaje
from Tareas.CreadorTareas import CreadorTareas
from Tareas.TipoTarea import TipoTarea
from Puertos.PuertoIN import PuertoIN
from Puertos.PuertoOUT import PuertoOUT
from Puertos.PuertoSOL import PuertoSOL
from Conectores.ConectorFichero import ConectorFichero

# ---------------------------------------------------------------------------
# Rutas relativas al propio demo.py
# ---------------------------------------------------------------------------
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
XML_DIR       = os.path.join(BASE_DIR, "xml")
ENTREGAS_DIR  = os.path.join(BASE_DIR, "entregas")
XSLT_PATH     = os.path.join(BASE_DIR, "entrega.xslt")

os.makedirs(ENTREGAS_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Simulación de Barman: recibe fragmentos de un slot y los devuelve
# al slot de respuesta con <estado>preparado</estado> añadido
# ---------------------------------------------------------------------------
def simular_barman(slot_peticiones, slot_respuestas, nombre):
    """
    Simula un barman externo que:
      - Lee las peticiones (bebidas) del slot de salida del PuertoSOL
      - Añade <estado>preparado</estado> a cada bebida
      - Escribe la respuesta en el slot de entrada del PuertoSOL
    """
    while not slot_peticiones.esta_vacio():
        peticion = slot_peticiones.leer_mensaje()
        drink_elem = peticion.get_cuerpo().getroot()
        # Añadir <estado> si no lo tiene ya
        if drink_elem.find("estado") is None:
            estado_elem = etree.SubElement(drink_elem, "estado")
            estado_elem.text = "preparado"
        respuesta = Mensaje(etree.ElementTree(drink_elem), Mensaje.siguiente_id())
        respuesta.copiar_cabecera_de(peticion)
        slot_respuestas.escribir_mensaje(respuesta)
        print(f"      [{nombre}] Preparando: {drink_elem.findtext('name')} ({drink_elem.findtext('type')})")


# ---------------------------------------------------------------------------
# Procesado de una sola comanda
# ---------------------------------------------------------------------------
def procesar_comanda(ruta_xml):
    order_id = os.path.basename(ruta_xml).replace("order", "").replace(".xml", "")
    print(f"\n{'='*60}")
    print(f"  Procesando comanda: {os.path.basename(ruta_xml)}")
    print(f"{'='*60}")

    # ── SLOTS ────────────────────────────────────────────────────────
    slot_entrada          = Slot()   # Conector → CorrelationIDSetter
    slot_tras_corrida     = Slot()   # CorrelationIDSetter → Splitter
    slot_bebidas          = Slot()   # Splitter → Replicator
    slot_replica_frias    = Slot()   # Replicator → Filter frías
    slot_replica_calientes= Slot()   # Replicator → Filter calientes
    slot_frias_out        = Slot()   # Filter frías → PuertoSOL barman frío (peticiones)
    slot_frias_in         = Slot()   # PuertoSOL barman frío → Merger (respuestas)
    slot_calientes_out    = Slot()   # Filter calientes → PuertoSOL barman caliente (peticiones)
    slot_calientes_in     = Slot()   # PuertoSOL barman caliente → Merger (respuestas)
    slot_merger_out       = Slot()   # Merger → reconstrucción
    slot_tras_reconstruir = Slot()   # reconstrucción → Translator
    slot_entrega          = Slot()   # Translator → ConectorFichero OUT

    # ── PASO 1: ConectorFichero (poll) lee la comanda ─────────────────
    print(f"\n[1] ConectorFichero: leyendo {os.path.basename(ruta_xml)}")
    conector_entrada = ConectorFichero(ruta_xml)
    puerto_in = PuertoIN(slot_entrada)
    conector_entrada.agregar_puerto(puerto_in)
    conector_entrada.ejecutar()

    # ── PASO 2: CorrelationIDSetter → asigna id de correlación ────────
    print(f"[2] CorrelationIDSetter: asignando id de correlación")
    cid_setter = CreadorTareas.crear(
        TipoTarea.CORRELATION_ID_SETTER,
        [slot_entrada],
        [slot_tras_corrida]
    )
    cid_setter.ejecutar()

    # ── PASO 3: Splitter → divide por bebidas ─────────────────────────
    print(f"[3] Splitter: dividiendo bebidas (//drink)")
    splitter = CreadorTareas.crear(
        TipoTarea.SPLITTER,
        [slot_tras_corrida],
        [slot_bebidas],
        "//drink"
    )
    splitter.ejecutar()
    n_bebidas = slot_bebidas.get_longitud_mensaje()
    print(f"    → {n_bebidas} bebida(s) en el slot intermedio")

    # ── PASO 4: Replicator → duplica cada fragmento bebida ────────────
    # El Replicator del framework lee UN mensaje y lo replica a N salidas,
    # así que lo ejecutamos una vez por cada bebida
    print(f"[4] Replicator: replicando cada bebida a dos ramas")
    replicator = CreadorTareas.crear(
        TipoTarea.REPLICATOR,
        [slot_bebidas],
        [slot_replica_frias, slot_replica_calientes]
    )
    for _ in range(n_bebidas):
        replicator.ejecutar()

    # ── PASO 5a: Filter bebidas frías ─────────────────────────────────
    print(f"[5a] Filter bebidas frías (type='cold')")
    filtro_frias = CreadorTareas.crear(
        TipoTarea.FILTER,
        [slot_replica_frias],
        [slot_frias_out],
        "//drink[type='cold']"
    )
    filtro_frias.ejecutar()

    # ── PASO 5b: Filter bebidas calientes ─────────────────────────────
    print(f"[5b] Filter bebidas calientes (type='hot')")
    filtro_calientes = CreadorTareas.crear(
        TipoTarea.FILTER,
        [slot_replica_calientes],
        [slot_calientes_out],
        "//drink[type='hot']"
    )
    filtro_calientes.ejecutar()

    n_frias      = slot_frias_out.get_longitud_mensaje()
    n_calientes  = slot_calientes_out.get_longitud_mensaje()
    print(f"    → {n_frias} bebida(s) fría(s) | {n_calientes} bebida(s) caliente(s)")

    # ── PASO 6a: PuertoSOL Barman Bebidas Frías ───────────────────────
    print(f"[6a] Barman Bebidas Frías:")
    puerto_sol_frias = PuertoSOL(slot_frias_in, slot_frias_out)
    simular_barman(slot_frias_out, slot_frias_in, "Barman Frío")

    # ── PASO 6b: PuertoSOL Barman Bebidas Calientes ───────────────────
    print(f"[6b] Barman Bebidas Calientes:")
    puerto_sol_calientes = PuertoSOL(slot_calientes_in, slot_calientes_out)
    simular_barman(slot_calientes_out, slot_calientes_in, "Barman Caliente")

    # ── PASO 7: Merger → reúne todas las bebidas preparadas ───────────
    print(f"[7] Merger: reuniendo bebidas preparadas")
    merger = CreadorTareas.crear(
        TipoTarea.MERGER,
        [slot_frias_in, slot_calientes_in],
        [slot_merger_out]
    )
    merger.ejecutar()
    print(f"    → {slot_merger_out.get_longitud_mensaje()} bebida(s) reunidas en slot de salida del Merger")

    # ── PASO 8: Reconstrucción del XML <cafe_order> completo ──────────
    # El Merger entrega fragmentos <drink> sueltos; reconstruimos el
    # documento <cafe_order> completo para que el XSLT pueda transformarlo
    print(f"[8] Reconstrucción XML: ensamblando <cafe_order> con todas las bebidas")
    raiz = etree.Element("cafe_order")
    order_id_elem = etree.SubElement(raiz, "order_id")
    order_id_elem.text = order_id
    drinks_elem = etree.SubElement(raiz, "drinks")

    while not slot_merger_out.esta_vacio():
        frag = slot_merger_out.leer_mensaje()
        drink_elem = frag.get_cuerpo().getroot()
        drinks_elem.append(copy.deepcopy(drink_elem))

    doc_completo = etree.ElementTree(raiz)
    msg_completo = Mensaje(doc_completo, Mensaje.siguiente_id())
    slot_tras_reconstruir.escribir_mensaje(msg_completo)

    # ── PASO 9: Translator (XSLT) → genera XML de entrega ────────────
    print(f"[9] Translator: aplicando XSLT para generar XML de entrega")
    translator = CreadorTareas.crear(
        TipoTarea.TRANSLATOR,
        [slot_tras_reconstruir],
        [slot_entrega],
        XSLT_PATH
    )
    translator.ejecutar()

    # ── PASO 10: ConectorFichero (write) → escribe entrega ────────────
    ruta_entrega = os.path.join(ENTREGAS_DIR, f"order{order_id}.xml")
    print(f"[10] ConectorFichero: escribiendo entrega en {os.path.relpath(ruta_entrega, BASE_DIR)}")
    conector_salida = ConectorFichero(ruta_entrega)
    puerto_out = PuertoOUT(slot_entrega)
    conector_salida.agregar_puerto(puerto_out)
    conector_salida.ejecutar()

    # Mostrar resultado
    with open(ruta_entrega, "r", encoding="utf-8") as f:
        contenido = f.read()
    print(f"\n    Entrega generada:\n")
    for linea in contenido.strip().split("\n"):
        print(f"      {linea}")


# ---------------------------------------------------------------------------
# Main: procesa todas las comandas en bucle
# ---------------------------------------------------------------------------
def main():
    print("\n" + "="*60)
    print("  SISTEMA DE COMANDAS — CAFETERÍA")
    print("  Integración EAI con Framework IIA")
    print("="*60)

    comandas = sorted(glob.glob(os.path.join(XML_DIR, "order*.xml")))
    if not comandas:
        print(f"\n[ERROR] No se encontraron comandas en: {XML_DIR}")
        return

    print(f"\nComandas encontradas: {len(comandas)}")
    for ruta in comandas:
        procesar_comanda(ruta)

    print(f"\n{'='*60}")
    print(f"  ¡Todas las comandas procesadas!")
    print(f"  Entregas escritas en: entregas/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

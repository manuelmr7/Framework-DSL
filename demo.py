"""
demo.py — Demostración completa del Framework de Integración (IIA)
Muestra el uso de la Factory (CreadorTareas), los Slots, Mensajes con XML (lxml),
las diferentes Tareas y los Puertos/Conectores.
"""

import sys
import os
from lxml import etree

# Aseguramos que la carpeta src/ esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Slots.Slot import Slot
from Slots.Mensaje import Mensaje
from Tareas.CreadorTareas import CreadorTareas
from Tareas.TipoTarea import TipoTarea
from Puertos.PuertoIN import PuertoIN
from Puertos.PuertoOUT import PuertoOUT
from Puertos.PuertoSOL import PuertoSOL
from Conectores.ConectorBDMock import ConectorBDMock


def imprimir_xml(doc, titulo=""):
    if titulo:
        print(f"  [{titulo}]")
    cadena = etree.tostring(doc, encoding="utf-8", pretty_print=True).decode()
    for linea in cadena.strip().split("\n"):
        print(f"    {linea}")


def main():
    print("=" * 70)
    print("    FRAMEWORK DE INTEGRACIÓN IIA — DEMOSTRACIÓN")
    print("=" * 70)

    # =========================================================================
    # ESCENARIO 1: Patrón Scatter-Gather (Splitter -> Aggregator)
    # =========================================================================
    print("\n" + "─" * 70)
    print("1. ESCENARIO SCATTER-GATHER: Splitter y Aggregator")
    print("─" * 70)

    slot_entrada = Slot()
    slot_fragmentos = Slot()
    slot_reconstruido = Slot()

    # Documento XML de entrada: un pedido con 3 líneas
    xml_pedido = """
    <pedido id="101">
        <linea id="1"><articulo>Café</articulo><cantidad>2</cantidad></linea>
        <linea id="2"><articulo>Leche</articulo><cantidad>1</cantidad></linea>
        <linea id="3"><articulo>Croissant</articulo><cantidad>3</cantidad></linea>
    </pedido>
    """
    doc_pedido = etree.ElementTree(etree.fromstring(xml_pedido.strip()))
    slot_entrada.escribir_mensaje(Mensaje(doc_pedido, id=101))
    print("\n[App] Pedido original colocado en Slot de entrada:")
    imprimir_xml(doc_pedido)

    # Creación del Splitter mediante la Factory
    splitter = CreadorTareas.crear(
        TipoTarea.SPLITTER,
        [slot_entrada],
        [slot_fragmentos],
        "//linea"   # Divide por cada <linea>
    )
    splitter.ejecutar()

    num_fragmentos = slot_fragmentos.get_longitud_mensaje()
    print(f"\n[Splitter] Ha dividido el pedido en {num_fragmentos} fragmentos en el slot intermedio.")

    # Creación del Aggregator mediante la Factory
    aggregator = CreadorTareas.crear(
        TipoTarea.AGGREGATOR,
        [slot_fragmentos],
        [slot_reconstruido],
        "pedido_reconstruido"   # Nombre de la etiqueta raíz al unir
    )
    aggregator.ejecutar()

    pedido_final = slot_reconstruido.leer_mensaje()
    if pedido_final:
        print(f"\n[Aggregator] ¡Pedido reconstruido exitosamente! (idCorr={pedido_final.get_id_correlacion()}):")
        imprimir_xml(pedido_final.get_cuerpo())

    # =========================================================================
    # ESCENARIO 2: Enrutamiento (Distributor) y Filtrado (Filter)
    # =========================================================================
    print("\n" + "─" * 70)
    print("2. ESCENARIO ENRUTAMIENTO Y FILTRADO: Distributor y Filter")
    print("─" * 70)

    s_pedidos = Slot()
    s_vip = Slot()
    s_estandar = Slot()

    # Dos pedidos: uno VIP y otro estándar
    msg_vip = Mensaje(etree.ElementTree(etree.fromstring('<pedido cliente="vip"><total>500</total></pedido>')), 1)
    msg_est = Mensaje(etree.ElementTree(etree.fromstring('<pedido cliente="normal"><total>20</total></pedido>')), 2)
    s_pedidos.escribir_mensaje(msg_vip)
    s_pedidos.escribir_mensaje(msg_est)

    # Distributor: enruta según XPath
    distribuidor = CreadorTareas.crear(
        TipoTarea.DISTRIBUIDOR,
        [s_pedidos],
        [s_vip, s_estandar],
        '//pedido[@cliente="vip"]',     # ruta 0 -> salida 0 (VIP)
        '//pedido[@cliente="normal"]'   # ruta 1 -> salida 1 (Estándar)
    )
    distribuidor.ejecutar()

    print(f"\n[Distributor] Mensajes en canal VIP: {s_vip.get_longitud_mensaje()}")
    print(f"[Distributor] Mensajes en canal Estándar: {s_estandar.get_longitud_mensaje()}")

    # Filter: solo deja pasar pedidos de más de 100€
    s_filtrados = Slot()
    filtro = CreadorTareas.crear(
        TipoTarea.FILTER,
        [s_vip],
        [s_filtrados],
        '//pedido[total > 100]'
    )
    filtro.ejecutar()
    print(f"[Filter] Pedidos VIP con total > 100€ aprobados: {s_filtrados.get_longitud_mensaje()}")

    # =========================================================================
    # ESCENARIO 3: Enriquecimiento de Contenido (ContextEnricher)
    # =========================================================================
    print("\n" + "─" * 70)
    print("3. ESCENARIO MODIFICADOR: ContextEnricher")
    print("─" * 70)

    s_principal = Slot()
    s_contexto = Slot()
    s_enriquecido = Slot()

    # Mensaje principal (datos básicos del cliente)
    msg_cliente = Mensaje(etree.ElementTree(etree.fromstring('<cliente id="42"><nombre>Laura</nombre></cliente>')), 1)
    # Mensaje de contexto (información crediticia externa)
    msg_credito = Mensaje(etree.ElementTree(etree.fromstring('<datos_credito><puntuacion>A+</puntuacion><limite>3000</limite></datos_credito>')), 2)

    s_principal.escribir_mensaje(msg_cliente)
    s_contexto.escribir_mensaje(msg_credito)

    enricher = CreadorTareas.crear(
        TipoTarea.CONTEXT_ENRICHER,
        [s_principal, s_contexto],
        [s_enriquecido]
    )
    enricher.ejecutar()

    resultado_enriquecido = s_enriquecido.leer_mensaje()
    print("\n[ContextEnricher] Mensaje resultante con datos fusionados:")
    imprimir_xml(resultado_enriquecido.get_cuerpo())

    # =========================================================================
    # ESCENARIO 4: Puertos y Conectores (PuertoSOL y ConectorBDMock)
    # =========================================================================
    print("\n" + "─" * 70)
    print("4. ESCENARIO PUERTOS Y CONECTORES: PuertoSOL + ConectorBDMock")
    print("─" * 70)

    slot_peticiones = Slot()
    slot_respuestas = Slot()

    # Puerto de Solicitud-Respuesta (PuertoSOL):
    # - slot_respuestas: donde el conector escribe las respuestas recibidas
    # - slot_peticiones: donde el framework deja las peticiones
    puerto_sol = PuertoSOL(slot_respuestas, slot_peticiones)

    # Conector de prueba (Mock) con una respuesta preparada
    doc_bd = etree.ElementTree(etree.fromstring('<stock_articulo><cafe>150</cafe><leche>40</leche></stock_articulo>'))
    respuesta_preparada = Mensaje(doc_bd, id=999)
    conector_bd = ConectorBDMock(respuestas=[respuesta_preparada])
    conector_bd.agregar_puerto(puerto_sol)

    # Lanzamos una consulta SQL envuelta en un Mensaje XML
    peticion_sql = Mensaje(etree.ElementTree(etree.fromstring('<consulta><sql>SELECT * FROM stock</sql></consulta>')), id=50)
    slot_peticiones.escribir_mensaje(peticion_sql)
    print("\n[App] Consulta enviada al slot de peticiones.")

    # Conector ejecuta su ciclo: lee petición de PuertoSOL y escribe respuesta en PuertoSOL
    conector_bd.ejecutar()
    print(f"[ConectorBDMock] Petición atendida. Total consultas registradas: {conector_bd.get_num_consultas()}")

    respuesta_recibida = slot_respuestas.leer_mensaje()
    print("\n[App] Respuesta leída del slot de respuestas:")
    imprimir_xml(respuesta_recibida.get_cuerpo())

    print("\n" + "=" * 70)
    print("  ¡DEMOSTRACIÓN COMPLETADA CON ÉXITO!")
    print("=" * 70)


if __name__ == "__main__":
    main()

<?xml version="1.0" encoding="UTF-8"?>
<!--
    entrega.xslt
    Transforma un <cafe_order> con sus <drink> preparados
    en un <entrega> con el resumen de bebidas listas para el camarero.

    Entrada esperada:
        <cafe_order>
            <order_id>N</order_id>
            <drinks>
                <drink><name>cafe</name><type>hot</type><estado>preparado</estado></drink>
                ...
            </drinks>
        </cafe_order>

    Salida:
        <entrega>
            <comanda>N</comanda>
            <bebidas_listas>
                <bebida tipo="hot">cafe</bebida>
                ...
            </bebidas_listas>
        </entrega>
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/cafe_order">
        <entrega>
            <comanda><xsl:value-of select="order_id"/></comanda>
            <bebidas_listas>
                <xsl:apply-templates select="drinks/drink"/>
            </bebidas_listas>
        </entrega>
    </xsl:template>

    <xsl:template match="drink">
        <bebida>
            <xsl:attribute name="tipo"><xsl:value-of select="type"/></xsl:attribute>
            <xsl:value-of select="name"/>
        </bebida>
    </xsl:template>

</xsl:stylesheet>

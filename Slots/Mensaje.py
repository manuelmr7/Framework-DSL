class Mensaje:
    """
    Unidad de información que circula por el framework.
    Tiene una cabecera (diccionario con id, id_correlacion, id_secuencia y longitud)
    y un cuerpo (documento XML de lxml).
    siguiente_id() genera ids únicos con un contador de clase.
    copiar_cabecera_de(origen) copia la cabecera de otro mensaje, salvo su id.
    """
    _contador = 0

    def __init__(self, cuerpo, id):
        self._cabecera = {
            "id": id,
            "id_correlacion": None,
            "id_secuencia": None,
            "longitud": None,
        }
        self._cuerpo = cuerpo  # un documento lxml

    def get_id(self):
        return self._cabecera["id"]

    def get_id_correlacion(self):
        return self._cabecera["id_correlacion"]

    def get_id_secuencia(self):
        return self._cabecera["id_secuencia"]

    def get_longitud(self):
        return self._cabecera["longitud"]

    def get_cuerpo(self):
        return self._cuerpo

    def set_id(self, id):
        self._cabecera["id"] = id

    def set_id_correlacion(self, id):
        self._cabecera["id_correlacion"] = id

    def set_id_secuencia(self, n):
        self._cabecera["id_secuencia"] = n

    def set_longitud(self, lenght):
        self._cabecera["longitud"] = lenght

    def set_cuerpo(self, cuerpo):
        self._cuerpo = cuerpo

    @staticmethod
    def siguiente_id():
        Mensaje._contador += 1
        return Mensaje._contador

    def copiar_cabecera_de(self, origen):
        # copia la cabecera de otro mensaje, salvo su id propio
        for clave, valor in origen._cabecera.items():
            if clave != "id":
                self._cabecera[clave] = valor

    def __repr__(self):
        return f"Mensaje(id={self.get_id()}, id_corr={self.get_id_correlacion()}, seq={self.get_id_secuencia()}/{self.get_longitud()})"

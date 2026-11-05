class Mensaje:
    def __init__(self, cuerpo,id):
        self._cabecera={
            "id":id,
            "id_correlacion": None,
            "id_secuencia": None,
            "longitud": None,
        }
        self._cuerpo=cuerpo #un documento lxml

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
        def set_id(self,id):
            self._cabecera["id"]=id
        def set_id_correlacion(self,id):
            self._cabecera["id_correlacion"]=id
        def set_id_secuencia(self,n):
            self._cabecera["id_secuencia"]=n
        def set_longitud(self,lenght):
            self._cabecera["longitud"]=lenght
        def set_cuerpo(self,cuerpo):
            self._cuerpo=cuerpo
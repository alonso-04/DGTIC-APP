from dominio.entidades.servicio import Servicio
from dominio.entidades.departamento import Departamento
from dominio.entidades.tipo_servicio import TipoServicio
from dominio.excepciones import ServicioValidacionError, DepartamentoValidacionError, TipoServicioValidacionError
from datetime import date


class ServicioControlador:
    def __init__(
        self,
        registrar_departamento,
        listar_departamentos,
        actualizar_info_departamento,
        eliminar_departamento,
        registrar_servicio,
        listar_servicios,
        actualizar_info_servicio,
        eliminar_servicio,
        registrar_tipo_servicio,
        listar_tipos_servicio,
        actualizar_info_tipo_servicio,
        eliminar_tipo_servicio
    ):
        self.registrar_departamento = registrar_departamento
        self.listar_departamentos = listar_departamentos
        self.actualizar_info_departamento = actualizar_info_departamento
        self.eliminar_departamento = eliminar_departamento
        
        self.registrar_servicio = registrar_servicio
        self.listar_servicios = listar_servicios
        self.actualizar_info_servicio = actualizar_info_servicio
        self.eliminar_servicio = eliminar_servicio
        
        self.registrar_tipo_servicio = registrar_tipo_servicio
        self.listar_tipos_servicio = listar_tipos_servicio
        self.actualizar_info_tipo_servicio = actualizar_info_tipo_servicio
        self.eliminar_tipo_servicio = eliminar_tipo_servicio
    
    
    # MÉTODOS PARA LOS SERVICIOS
    
    def registrar_servicio_controlador(self, nombre_departamento: str, fecha_servicio: date, falla_presenta: str, tipo_servicio_prestado: str, nombres_tecnicos: str, observaciones_adicionales: str):
        try:
            if (nombre_departamento):
                departamento_id = self.listar_departamentos.obtener_por_nombre(nombre_departamento).departamento_id
            else:
                departamento_id = None
            
            
            if (tipo_servicio_prestado):
                tipo_servicio_id = self.listar_tipos_servicio.obtener_por_tipo_servicio(tipo_servicio_prestado).tipo_servicio_id
            else:
                tipo_servicio_id = None
            
            
            if (falla_presenta):
                falla_presenta = falla_presenta.upper()
            
            if (nombres_tecnicos):
                nombres_tecnicos = nombres_tecnicos.upper()
            
            if (observaciones_adicionales):
                observaciones_adicionales = observaciones_adicionales.upper()
            
            nuevo_servicio = Servicio(
                departamento_id = departamento_id,
                fecha_servicio = fecha_servicio,
                falla_presenta = falla_presenta,
                tipo_servicio_id = tipo_servicio_id,
                nombres_tecnicos = nombres_tecnicos,
                observaciones_adicionales = observaciones_adicionales
            )
            
            self.registrar_servicio.ejecutar(nuevo_servicio)
        except ServicioValidacionError as error:
            raise error
        except DepartamentoValidacionError as error:
            raise error
        except TipoServicioValidacionError as error:
            raise error
    
    def filtrar_mensual_servicios_controlador(self, mes_anio: str):
        try:
            servicios = self.listar_servicios.obtener_por_mes_anio(mes_anio)
            
            lista_dict_servicios = []
            
            if not(servicios):
                return []
            
            for servicio in servicios:
                elemento = {
                    "servicio_id": servicio[0],
                    "departamento_id": servicio[1],
                    "tipo_servicio_id": servicio[2],
                    "nombre_departamento": servicio[3],
                    "mes_anio": servicio[4],
                    "fecha_servicio": servicio[5],
                    "falla_presenta": servicio[6],
                    "tipo_servicio_prestado": servicio[7],
                    "nombres_tecnicos": servicio[8],
                    "observaciones_adicionales": servicio[9]
                }
                
                lista_dict_servicios.append(elemento)
            
            return lista_dict_servicios
        except ServicioValidacionError as error:
            raise error
    
    def filtrar_servicios_controlador(self, fecha_servicio: date, nombre_departamento: str, tipo_servicio_prestado: str):
        try:
            servicios = self.listar_servicios.obtener_por_fecha_o_departamento_o_tipo_servicio(
                fecha_servicio = fecha_servicio,
                nombre_departamento = nombre_departamento,
                tipo_servicio_prestado = tipo_servicio_prestado
            )
            
            lista_dict_servicios = []
            
            if not(servicios):
                return []
            
            for servicio in servicios:
                elemento = {
                    "servicio_id": servicio[0],
                    "departamento_id": servicio[1],
                    "tipo_servicio_id": servicio[2],
                    "nombre_departamento": servicio[3],
                    "fecha_servicio": servicio[4],
                    "falla_presenta": servicio[5],
                    "tipo_servicio_prestado": servicio[6],
                    "nombres_tecnicos": servicio[7],
                    "observaciones_adicionales": servicio[8]
                }
                    
                lista_dict_servicios.append(elemento)
            
            return lista_dict_servicios
        except ServicioValidacionError as error:
            raise error
    
    def conteo_tipos_servicios_realizados_controlador(self, mes_anio: str):
        try:
            conteo_servicios_realizados = self.listar_servicios.obtener_conteo_tipos_servicios_realizados(mes_anio)
            lista_dict_conteo_servicios_realizados = []
            
            for conteo in conteo_servicios_realizados:
                elemento = {
                    "tipo_servicio_prestado": conteo[0],
                    "cantidad": conteo[1]
                }
                
                lista_dict_conteo_servicios_realizados.append(elemento)
            
            return lista_dict_conteo_servicios_realizados
        except ServicioValidacionError as error:
            raise error
    
    def conteo_servicios_realizados_x_departamento_controlador(self, mes_anio: str):
        try:
            conteo_servicios_realizaods_x_departamento = self.listar_servicios.obtener_conteo_servicios_x_departamento(mes_anio)
            lista_dict_servicios_realizados_x_departamento = []
            
            for conteo in conteo_servicios_realizaods_x_departamento:
                elemento = {
                    "nombre_departamento": conteo[0],
                    "tipo_servicio_prestado": conteo[1],
                    "cantidad": conteo[2]
                }
                
                lista_dict_servicios_realizados_x_departamento.append(elemento)
            
            return lista_dict_servicios_realizados_x_departamento
        except ServicioValidacionError as error:
            raise error
    
    def seleccionar_servicio_controlador(self, servicio_id: int):
        try:
            servicio = self.listar_servicios.obtener_por_id(servicio_id)
            nombre_departamento = self.listar_departamentos.obtener_por_id(servicio.departamento_id)
            tipo_servicio_prestado = self.listar_tipos_servicio.obtener_por_id(servicio.tipo_servicio_id)
            
            dict_servicio = {
                "servicio_id": servicio.servicio_id,
                "nombre_departamento": nombre_departamento,
                "fecha_servicio": servicio.fecha_servicio,
                "falla_presenta": servicio.falla_presenta,
                "tipo_servicio_prestado": tipo_servicio_prestado,
                "nombres_tecnicos": servicio.nombres_tecnicos,
                "observaciones_adicionales": servicio.observaciones_adicionales
            }
            
            return dict_servicio
        except ServicioControlador as error:
            raise error
    
    def actualizar_info_servicio_controlador(self, servicio_id: int, fecha_servicio: date, nombre_departamento: str, falla_presenta: str, tipo_servicio_prestado: str, nombres_tecnicos: str, observaciones_adicionales: str):
        try:
            if (nombre_departamento):
                departamento_id = self.listar_departamentos.obtener_por_nombre(nombre_departamento).departamento_id
            else:
                departamento_id = None
            
            if (tipo_servicio_prestado):
                tipo_servicio_id = self.listar_tipos_servicio.obtener_por_tipo_servicio(tipo_servicio_prestado).tipo_servicio_id
            else:
                tipo_servicio_id = None
            
            
            if (falla_presenta):
                falla_presenta = falla_presenta.upper()
            
            if (nombres_tecnicos):
                nombres_tecnicos = nombres_tecnicos.upper()
            
            nuevos_datos = {
                "departamento_id": departamento_id,
                "fecha_servicio": fecha_servicio,
                "falla_presenta": falla_presenta,
                "tipo_servicio_id": tipo_servicio_id,
                "nombres_tecnicos": nombres_tecnicos,
                "observaciones_adicionales": observaciones_adicionales
            }
            
            self.actualizar_info_servicio.ejecutar(servicio_id, nuevos_datos)
        except ServicioValidacionError as error:
            raise error
        except DepartamentoValidacionError as error:
            raise error
        except TipoServicioValidacionError as error:
            raise error
    
    def eliminar_servicio_controlador(self, servicio_id: int):
        try:
            self.eliminar_servicio.ejecutar(servicio_id)
        except Exception as error:
            raise error
    
    
    # MÉTODOS PARA LOS DEPARTAMENTOS
    
    def registrar_departamento_controlador(self, nombre_departamento: str):
        try:
            if (nombre_departamento):
                nombre_departamento = nombre_departamento.upper()
            
            nuevo_departamento = Departamento(
                nombre_departamento = nombre_departamento
            )
            
            self.registrar_departamento.ejecutar(nuevo_departamento)
        except DepartamentoValidacionError as error:
            raise error
    
    def filtrar_todos_departamentos_controlador(self):
        try:
            departamentos = self.listar_departamentos.obtener_todos()
            
            list_dict_departamentos = []
            
            for departamento in departamentos:
                elemento = {
                    "departamento_id": departamento.departamento_id,
                    "nombre_departamento": departamento.nombre_departamento
                }
                
                list_dict_departamentos.append(elemento)
            
            return list_dict_departamentos
        except Exception:
            pass
    
    def filtrar_por_nombre_departamento_controlador(self, nombre_departamento: str):
        try:
            
            if (nombre_departamento):
                departamento = self.listar_departamentos.obtener_por_nombre(nombre_departamento)
                
                dict_departamento = [{
                    "departamento_id": departamento.departamento_id,
                    "nombre_departamento": departamento.nombre_departamento
                }]
                
                return dict_departamento
            else:
                lista_departamentos = self.filtrar_todos_departamentos_controlador()
                return lista_departamentos
        except DepartamentoValidacionError as error:
            raise error
    
    def seleccionar_departamento_controlador(self, departamento_id: int):
        try:
            departamento = self.listar_departamentos.obtener_por_id(departamento_id)
            
            dict_departamento = {
                "departamento_id": departamento.departamento_id,
                "nombre_departamento": departamento.nombre_departamento
            }
            
            return dict_departamento
        except DepartamentoValidacionError as error:
            raise error
    
    def actualizar_info_departamento_controlador(self, departamento_id: int, nuevo_nombre_departamento: str):
        try:
            nuevos_datos = {
                "nombre_departamento": nuevo_nombre_departamento
            }
            
            self.actualizar_info_departamento.ejecutar(departamento_id, nuevos_datos)
        except DepartamentoValidacionError as error:
            raise error
    
    def eliminar_departamento_controlador(self, departamento_id: int):
        try:
            self.eliminar_departamento.ejecutar(departamento_id)
        except DepartamentoValidacionError as error:
            raise error
    
    
    # MÉTODOS PARA LOS TIPOS DE SERVICIO
    
    
    def registrar_tipo_servicio_controlador(self, tipo_servicio_prestado: str):
        try:
            if (tipo_servicio_prestado):
                tipo_servicio_prestado = tipo_servicio_prestado.upper()
            
            nuevo_tipo_servicio = TipoServicio(
                tipo_servicio_prestado = tipo_servicio_prestado
            )
            
            self.registrar_tipo_servicio.ejecutar(nuevo_tipo_servicio)
        except TipoServicioValidacionError as error:
            raise error
    
    def filtrar_todos_tipos_servicio_controlador(self):
        try:
            tipos_servicio = self.listar_tipos_servicio.obtener_todos()
            
            list_dict_tipos_servicio = []
            
            for tipo_servicio in tipos_servicio:
                elemento = {
                    "tipo_servicio_id": tipo_servicio.tipo_servicio_id,
                    "tipo_servicio_prestado": tipo_servicio.tipo_servicio_prestado
                }
                list_dict_tipos_servicio.append(elemento)
            
            return list_dict_tipos_servicio
        except Exception:
            pass
    
    def filtrar_por_nombre_tipo_servicio_controlador(self, tipo_servicio_prestado: str):
        try:
            if (tipo_servicio_prestado):
                tipo_servicio_prestado = self.listar_tipos_servicio.obtener_por_tipo_servicio(tipo_servicio_prestado)
                
                dict_tipo_servicio = [{
                    "tipo_servicio_id": tipo_servicio_prestado.tipo_servicio_id,
                    "tipo_servicio_prestado": tipo_servicio_prestado.tipo_servicio_prestado
                }]
                
                return dict_tipo_servicio
            else:
                lista_tipo_servicio_prestado = self.filtrar_todos_tipos_servicio_controlador()
                return lista_tipo_servicio_prestado
        except TipoServicioValidacionError as error:
            raise error
    
    def seleccionar_tipo_servicio_controlador(self, tipo_servicio_id: int):
        try:
            tipo_servicio_prestado = self.listar_tipos_servicio.obtener_por_id(tipo_servicio_id)
            
            dict_tipo_servicio = {
                "tipo_servicio_id": tipo_servicio_prestado.tipo_servicio_id,
                "tipo_servicio_prestado": tipo_servicio_prestado.tipo_servicio_prestado
            }
            
            return dict_tipo_servicio
        except TipoServicioValidacionError as error:
            raise error
    
    def actualizar_tipo_servicio_controlador(self, tipo_servicio_id: int, nuevo_tipo_servicio_prestado: str):
        try:
            nuevos_datos = {
                "tipo_servicio_prestado": nuevo_tipo_servicio_prestado
            }
            
            self.actualizar_info_tipo_servicio.ejecutar(tipo_servicio_id, nuevos_datos)
        except TipoServicioValidacionError as error:
            raise error
    
    def eliminar_tipo_servicio_controlador(self, tipo_servicio_id: int):
        try:
            self.eliminar_tipo_servicio.ejecutar(tipo_servicio_id)
        except TipoServicioValidacionError as error:
            raise error
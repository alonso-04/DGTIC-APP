from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo

from aplicacion.casos_uso.usuarios.registrar_usuario import RegistrarUsuario
from aplicacion.casos_uso.usuarios.listar_usuarios import ListarUsuarios
from aplicacion.casos_uso.usuarios.actualizar_info_usuario import ActualizarInfoUsuario
from aplicacion.casos_uso.usuarios.eliminar_usuario import EliminarUsuario
from aplicacion.casos_uso.usuarios.sesion_usuario import SesionUsuario
from aplicacion.casos_uso.roles.listar_roles import ListarRoles

from aplicacion.casos_uso.departamentos.registrar_departamento import RegistrarDepartamento
from aplicacion.casos_uso.departamentos.listar_departamentos import ListarDepartamentos
from aplicacion.casos_uso.departamentos.actualizar_info_departamento import ActualizarInfoDepartamento
from aplicacion.casos_uso.departamentos.eliminar_departamento import EliminarDepartamento
from aplicacion.casos_uso.servicios_tecnicos.registrar_servicio import RegistrarServicio
from aplicacion.casos_uso.servicios_tecnicos.listar_servicios import ListarServicios
from aplicacion.casos_uso.servicios_tecnicos.actualizar_info_servicio import ActualizarInfoServicio
from aplicacion.casos_uso.servicios_tecnicos.eliminar_servicio import EliminarServicio
from aplicacion.casos_uso.tipos_servicio.registrar_tipo_servicio import RegistrarTipoServicio
from aplicacion.casos_uso.tipos_servicio.listar_tipos_servicio import ListarTiposServicio
from aplicacion.casos_uso.tipos_servicio.actualizar_info_tipo_servicio import ActualizarInfoTipoServicio
from aplicacion.casos_uso.tipos_servicio.eliminar_tipo_servicio import EliminarTipoServicio

from ui.controladores.usuario_controlador import UsuarioControlador
from ui.controladores.servicio_controlador import ServicioControlador


class ContenedorDependencias:
    def __init__(self):
        # CASOS DE USO DE LOS USUARIOS Y ROLES
        self._registrar_usuario = RegistrarUsuario(SQLAlchemyUnidadTrabajo)
        self._listar_usuarios = ListarUsuarios(SQLAlchemyUnidadTrabajo)
        self._actualizar_info_usuario = ActualizarInfoUsuario(SQLAlchemyUnidadTrabajo)
        self._eliminar_usuario = EliminarUsuario(SQLAlchemyUnidadTrabajo)
        self._sesion_usuario = SesionUsuario(SQLAlchemyUnidadTrabajo)
        self._listar_roles = ListarRoles(SQLAlchemyUnidadTrabajo)
        
        # CASOS DE USO DE LOS DEPARTAMENTOS
        self._registrar_departamento = RegistrarDepartamento(SQLAlchemyUnidadTrabajo)
        self._listar_departamentos = ListarDepartamentos(SQLAlchemyUnidadTrabajo)
        self._actualizar_info_departamento = ActualizarInfoDepartamento(SQLAlchemyUnidadTrabajo)
        self._eliminar_departamento = EliminarDepartamento(SQLAlchemyUnidadTrabajo)
        
        # CASOS DE USO DE LOS SERVICIOS TÉCNICOS
        self._registrar_servicio = RegistrarServicio(SQLAlchemyUnidadTrabajo)
        self._listar_servicios = ListarServicios(SQLAlchemyUnidadTrabajo)
        self._actualizar_info_servicio = ActualizarInfoServicio(SQLAlchemyUnidadTrabajo)
        self._eliminar_servicio = EliminarServicio(SQLAlchemyUnidadTrabajo)
        
        # CASOS DE USO DE LOS TIPOS DE SERVICIO TÉCNICO
        self._registrar_tipo_servicio = RegistrarTipoServicio(SQLAlchemyUnidadTrabajo)
        self._listar_tipos_servicio = ListarTiposServicio(SQLAlchemyUnidadTrabajo)
        self._actualizar_info_tipo_servicio = ActualizarInfoTipoServicio(SQLAlchemyUnidadTrabajo)
        self._eliminar_tipo_servicio = EliminarTipoServicio(SQLAlchemyUnidadTrabajo)
    
    def obtener_usuario_controlador(self) -> UsuarioControlador:
        usuario_controlador = UsuarioControlador(
            registrar_usuario = self._registrar_usuario,
            listar_usuarios = self._listar_usuarios,
            actualizar_info_usuario = self._actualizar_info_usuario,
            eliminar_usuario = self._eliminar_usuario,
            sesion_usuario = self._sesion_usuario,
            listar_roles = self._listar_roles
        )
        
        return usuario_controlador
    
    def obtener_servicio_controlador(self) -> ServicioControlador:
        servicio_controlador = ServicioControlador(
            registrar_departamento = self._registrar_departamento,
            listar_departamentos = self._listar_departamentos,
            actualizar_info_departamento = self._actualizar_info_departamento,
            eliminar_departamento = self._eliminar_departamento,
            registrar_servicio = self._registrar_servicio,
            listar_servicios = self._listar_servicios,
            actualizar_info_servicio = self._actualizar_info_servicio,
            eliminar_servicio = self._eliminar_servicio,
            registrar_tipo_servicio = self._registrar_tipo_servicio,
            listar_tipos_servicio = self._listar_tipos_servicio,
            actualizar_info_tipo_servicio = self._actualizar_info_tipo_servicio,
            eliminar_tipo_servicio = self._eliminar_tipo_servicio
        )
        
        return servicio_controlador


contenedor_dependencias = ContenedorDependencias()
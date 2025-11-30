from typing import List

class DominioValidacionError(Exception):
    def __init__(self, errores: List[str]):
        self.errores = errores
        super().__init__()

class DepartamentoValidacionError(DominioValidacionError):
    pass

class TipoServicioValidacionError(DominioValidacionError):
    pass

class ServicioValidacionError(DominioValidacionError):
    pass

class RolValidacionError(DominioValidacionError):
    pass

class UsuarioValidacionError(DominioValidacionError):
    pass
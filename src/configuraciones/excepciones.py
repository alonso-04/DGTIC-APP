from typing import List

class ErroresBase(Exception):
    def __init__(self, errores: List[str]):
        self.errores = errores
        super().__init__()

class LogicaError(ErroresBase):
    pass

class ValidacionError(ErroresBase):
    pass

class NoEncontradoError(ErroresBase):
    pass
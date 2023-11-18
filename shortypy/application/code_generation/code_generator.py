import os
import base64
from abc import ABC, abstractmethod


class CodeValidator(ABC):
    @abstractmethod
    def validate(self, code: str) -> bool:
        raise NotImplementedError


class CodeGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError


class CodeGeneratorImpl(CodeGenerator):
    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    def generate(self) -> str:
        return base64.b64encode(os.urandom(32))[:self.min_length].decode()

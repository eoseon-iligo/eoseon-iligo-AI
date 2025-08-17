# DocumentRendererPort (추상 인터페이스)
from abc import ABC, abstractmethod

from .dto import GenerateCommand, GenerateResult


class DocumentRendererPort(ABC):
    @abstractmethod
    def render(self, command: GenerateCommand) -> GenerateResult:
        """Renders a document according to the AST and target format."""
        raise NotImplementedError

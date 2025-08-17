# GenerateDocumentUseCase
from app.application.dto import GenerateCommand, GenerateResult
from app.application.ports import DocumentRendererPort

class GenerateDocumentUseCase:
    def __init__(self, renderer: DocumentRendererPort):
        self._renderer = renderer

    def execute(self, cmd: GenerateCommand) -> GenerateResult:
        return self._renderer.render(cmd)
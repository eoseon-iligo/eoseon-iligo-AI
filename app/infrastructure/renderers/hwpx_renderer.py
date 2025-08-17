# HWPX 파일 생성

from pathlib import Path
from app.application.ports import DocumentRendererPort
from app.application.dto import GenerateCommand, GenerateResult
from app.infrastructure.config import settings
from app.infrastructure.utils.zip_utils import replace_in_zip_bytes
import zipfile 
import io

class HwpxRenderer(DocumentRendererPort):
    """
    전제:
    - templates/hwpx_template.hwpx 파일이 존재
    - 내부 XML(예: Contents/section0.xml)에 {{TITLE}}, {{BODY}} 플레이스홀더가 있음
    - 복잡한 표/이미지는 템플릿과 XML 조작 로직 확장 필요
    """
    TEMPLATE_FILE = settings.templates_dir / "inch.hwp"

    def render(self, cmd: GenerateCommand) -> GenerateResult:
        if not self.TEMPLATE_FILE.exists():
            raise FileNotFoundError("templates/inch.hwp 가 필요합니다.")

        with open(self.TEMPLATE_FILE, "rb") as f:
            zip_bytes = f.read()

        if not zipfile.is_zipfile(io.BytesIO(zip_bytes)):
            raise ValueError(
                f"HWPX 템플릿이 유효한 Zip이 아닙니다: {self.TEMPLATE_FILE}. "
                "한글에서 'HWPX 형식'으로 다시 저장해 주세요."
        )

        ast = cmd.ast
        body_text = "\n\n".join([
            ((s.heading or "") + ("\n" + (s.body or "") if s.body else "")).strip()
            for s in ast.sections
        ]).strip()

        replacements = {
            "Contents/section0.xml": [
                ("{{TITLE}}", ast.title or ""),
                ("{{BODY}}", body_text),
            ]
        }

        out = replace_in_zip_bytes(zip_bytes, replacements)
        return GenerateResult(
            filename="document.hwpx",
            content_type="application/haansofthwp",  # 일부 환경에선 application/zip 인식 가능성
            data=out,
        )

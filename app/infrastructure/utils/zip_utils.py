# ZIP 내 XML 치환 유팅
import io
import zipfile

# def replace_in_zip_bytes(zip_data: bytes, replacements: dict) -> bytes:
#     """ZIP 바이트 내부 파일 텍스트 치환. replacements: {arcname: [(old, new), ....]}"""
#     mem_in = io.BytesIO(zip_data)
#     mem_out = io.BytesIO()
#     with zipfile.ZipFile(mem_in, 'r') as zin, zipfile.ZipFile(mem_out, 'w',
#         zipfile.ZIP_DEFLATED) as zout:
#         for item in zin.infolist():
#             if item.filename in replacements:
#                 text = data.devode('utf-8')
#                 for old, new in replacements[item.filename]:
#                     text = text.replace(old, new)
#                 data = text.encode('utf-8')
#             zout.writestr(item, data)
#     return mem_out.getvalue()

# app/infrastructure/utils/zip_utils.py

import io
import zipfile

def replace_in_zip_bytes(zip_data: bytes, replacements: dict) -> bytes:
    """
    ZIP 바이트 내부 파일 텍스트 치환.
    replacements: {arcname: [(old, new), ...]}
    주의: 텍스트(XML) 파일만 치환, 이진 파일은 원본 그대로 복사.
    """
    mem_in = io.BytesIO(zip_data)
    mem_out = io.BytesIO()

    with zipfile.ZipFile(mem_in, 'r') as zin, zipfile.ZipFile(mem_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            # 항상 원본 데이터를 먼저 읽어 두기
            data = zin.read(item.filename)

            # 치환 대상이 아니면 그대로 기록
            if item.filename not in replacements:
                zout.writestr(item, data)
                continue

            # 치환 대상인 경우: 텍스트로 디코드 → 치환 → 다시 인코드
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                # 텍스트가 아니면 치환 불가: 원본 그대로 기록
                zout.writestr(item, data)
                continue

            for old, new in replacements[item.filename]:
                text = text.replace(old, new)

            zout.writestr(item, text.encode('utf-8'))

    return mem_out.getvalue()
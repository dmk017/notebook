import io
import zipfile

from src.utils.io.types import FileBufferContent


def create_zip_buffer(files: list[FileBufferContent]) -> io.BytesIO:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file in files:
            zip_file.writestr(file.name, file.buffer.getvalue())

    return zip_buffer

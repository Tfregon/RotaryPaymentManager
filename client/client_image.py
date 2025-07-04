import base64
from PIL import Image
import io

class ClientImage:
    @staticmethod
    def image_to_base64(caminho_arquivo: str) -> str:
        with open(caminho_arquivo, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    @staticmethod
    def base64_to_image(b64_data: str):
        return Image.open(io.BytesIO(base64.b64decode(b64_data)))

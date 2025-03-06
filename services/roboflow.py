import requests
from typing import Any, Dict
from core.config import settings
from fastapi import HTTPException


def process_image(image_bytes: bytes, confidence_threshold: int = 50) -> Dict[str, Any]:
    """Envia a imagem para o Roboflow e retorna os resultados da deteccao."""
    response = requests.post(
        settings.ROBOFLOW_URL,
        files={"file": ("image.jpg", image_bytes, "image/jpeg")},
        params={"confidence": confidence_threshold},
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Erro ao enviar imagem para o Roboflow.",
        )
    return response.json()

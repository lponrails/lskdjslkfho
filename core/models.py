from pydantic import BaseModel
from typing import List


class PredictionResult(BaseModel):
    """Representa um resultado de deteccao de objetos."""

    predictions: List[dict]

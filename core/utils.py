from pydantic import BaseModel, Field
from datetime import datetime
from typing import ClassVar
import re, pandas as pd


REGEX_RM_KM_FROM_NAME = re.compile(r"\s-\skm\s\d+,\d+")
REGEX_FILENAME_VALIDATION = re.compile("")  # TODO


class ImgLabelInfo(BaseModel):
    _id_counter: ClassVar[int] = -1
    iid: int = Field(default_factory=lambda: ImgLabelInfo._get_next_id())

    img_name: str
    line: str
    date: datetime
    image_id: str
    railway_km: str
    is_second_img: bool

    @classmethod
    def _get_next_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter


def extract_data_from_image_name(img_name) -> ImgLabelInfo | None:
    """Extrai informacoes do nome da imagem."""
    # TODO: validar nome da imagem
    if "Copia" in img_name or "(2)" in img_name or not img_name.startswith("_LP"):
        return {"img_name": img_name}

    img_name = re.sub(REGEX_RM_KM_FROM_NAME, "", img_name.strip()[1:])

    data_extracted = img_name.strip().split("_")
    second_from_meter = data_extracted[-1] == "01"

    data = ImgLabelInfo(
        img_name=img_name,
        line=data_extracted[0],
        date=datetime.strptime(data_extracted[1], "%Y%m%d").date(),
        image_id=data_extracted[2],
        railway_km=data_extracted[4].replace(".jpeg", ""),
        is_second_img=second_from_meter,
    )

    return data.json()


def data_to_dataframe(data: list[dict]) -> pd.DataFrame:
    """Converte um dicionario em um DataFrame."""
    all_predictions = []
    for inference in data["predictions"]:
        inference_id = inference["inference_id"]
        image_height = inference["image"]["height"]
        image_width = inference["image"]["width"]

        for pred in inference["predictions"]:
            pred_data = {
                "inference_id": inference_id,
                "image_height": image_height,
                "image_width": image_width,
                "x": pred["x"],
                "y": pred["y"],
                "width": pred["width"],
                "height": pred["height"],
                "confidence": pred["confidence"],
                "class": pred["class"],
                "class_id": pred["class_id"],
                "detection_id": pred["detection_id"],
            }
            all_predictions.append(pred_data)

    df = pd.DataFrame(all_predictions)
    return df

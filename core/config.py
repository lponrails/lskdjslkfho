import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ROBOFLOW_API_KEY: str = os.getenv("ROBOFLOW_API_KEY")
    ROBOFLOW_MODEL: str = os.getenv("ROBOFLOW_MODEL")
    ROBOFLOW_URL: str = (
        f"https://detect.roboflow.com/{ROBOFLOW_MODEL}?api_key={ROBOFLOW_API_KEY}&format=json"
    )


settings = Settings()

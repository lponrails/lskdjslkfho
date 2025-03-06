import cv2
from fastapi import FastAPI, File, UploadFile
from core.models import PredictionResult
from services.roboflow import process_image

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict/image", response_model=PredictionResult)
async def predict_image(file: UploadFile = File(...), confidence_threshold: int = 40):
    """Recebe uma imagem e retorna a predicao em JSON"""
    image_bytes = await file.read()
    result = process_image(image_bytes, confidence_threshold=confidence_threshold)
    return PredictionResult(predictions=[result])


@app.post("/predict/images", response_model=PredictionResult)
async def predict_images(
    files: list[UploadFile] = File(...), confidence_threshold: int = 40
):
    """Recebe multiplas imagens e retorna um DataFrame com as predicoes."""
    results = []
    for img_file in files:
        image_bytes = await img_file.read()
        result = process_image(image_bytes, confidence_threshold=confidence_threshold)
        results.append(result)
    return PredictionResult(predictions=results)


@app.post("/predict/video", response_model=PredictionResult)
async def predict_video(file: UploadFile = File(...), confidence_threshold: int = 40):
    """Recebe um video e retorna um DataFrame com as predicoes quadro a quadro."""
    video_bytes = await file.read()
    cap = cv2.VideoCapture(video_bytes)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    results = []
    for frame in frames:
        _, buffer = cv2.imencode(".jpg", frame)
        image_bytes = buffer.tobytes()
        result = process_image(image_bytes, confidence_threshold=confidence_threshold)
        results.append(result)
    return PredictionResult(predictions=results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

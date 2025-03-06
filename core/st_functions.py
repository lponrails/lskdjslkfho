import requests

API_URL = "http://127.0.0.1:8000"


def predict_image(image_bytes: bytes, confidence_threshold: int = 50):
    response = requests.post(
        f"{API_URL}/predict/image?confidence={confidence_threshold}",
        files={"file": image_bytes},
    )
    return response.json()


def predict_images(images_bytes: list[bytes], confidence_threshold: int = 50):
    response = requests.post(
        f"{API_URL}/predict/images?confidence={confidence_threshold}",
        files=[("files", img) for img in images_bytes],
    )
    return response.json()


def predict_video(video_bytes: bytes, confidence_threshold: int = 50):
    response = requests.post(
        f"{API_URL}/predict/video?confidence={confidence_threshold}",
        files={"file": video_bytes},
    )
    return response.json()


def bounding_box(predictions: list[dict]) -> tuple:
    collected_bboxes = []
    for rai_flaw_list in predictions:
        for prediction in rai_flaw_list["predictions"]:
            x0 = int(prediction["x"] - prediction["width"] / 2)
            x1 = int(prediction["x"] + prediction["width"] / 2)
            y0 = int(prediction["y"] - prediction["height"] / 2)
            y1 = int(prediction["y"] + prediction["height"] / 2)
            bbox = (x0, x1, y0, y1)

            class_name = prediction["class"]
            confidence = prediction["confidence"]
            collected_bboxes.append((bbox, class_name, confidence))

    return collected_bboxes

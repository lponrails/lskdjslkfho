import streamlit as st
import cv2, json, pandas as pd
from PIL import Image, ImageFile
import numpy as np
from core import st_functions, utils

# usado porque as imagens dos trilhos sao muito grandes. remover esta linha
# resulta no erro "OSError: image file is truncated (4 bytes not processed)"
ImageFile.LOAD_TRUNCATED_IMAGES = True


st.title("Detecção Automática de Defeitos")
st.info(
    """
        **Modelo:** YOLOv12 | prototipo-1/3
        
        **Stack:** `Streamlit`, `FastAPI`, `Roboflow`
    """
)

# option = st.selectbox("Select Input Type", ["Image", "Multiple Images", "Video"])
option = st.selectbox("Selecione o Tipo de Entrada", ["Imagem", "Múltiplas Imagens"])
confidence_threshold = st.slider("Limiar de confiança", 5, 100, 50, 5)

if option == "Imagem":
    uploaded_file = st.file_uploader(
        "Escolha uma imagem...", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None and st.button("Fazer detecção"):
        image_bytes = uploaded_file.read()

        st.write("## Imagem Carregada")
        st.image(image_bytes, caption="Imagem Enviada", use_container_width=True)

        result = st_functions.predict_image(image_bytes, confidence_threshold)

        image_bytes = np.frombuffer(image_bytes, np.uint8)
        image_bytes = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if "predictions" in result:
            result_bboxes = st_functions.bounding_box(result["predictions"])

            for predictions in result_bboxes:
                bbox, class_name, confidence = predictions
                x0, x1, y0, y1 = bbox
                start_point, end_point = (x0, y0), (x1, y1)

                cv2.rectangle(
                    image_bytes, start_point, end_point, color=(0, 255, 0), thickness=1
                )
                cv2.rectangle(
                    image_bytes,
                    (x0, y1),
                    (x0 + 120, y1 + 20),
                    color=(0, 0, 255),
                    thickness=-1,
                )
                cv2.putText(
                    image_bytes,
                    f"{class_name}({confidence:.0%})",
                    (x0, y1 + 12),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255),
                )

        results_tab, json_tab, rail_info = st.tabs(
            [
                "Resultos da Detecção",
                "Tabela de Detecção",
                "Informação - Nome da Imagem",
            ]
        )

        with results_tab:
            st.write("## Defeitos Detectados")
            image_bytes = Image.fromarray(cv2.cvtColor(image_bytes, cv2.COLOR_BGR2RGB))
            st.image(
                image_bytes, caption="Defeitos Detectados", use_container_width=True
            )

        with json_tab:
            st.write("## Tabela de Detecção dos Defeitos")
            st.dataframe(utils.data_to_dataframe(result))

        with rail_info:
            st.write("## Informação dos Trilhos")
            st.write("Informações extraídas do nome do arquivo.")
            railway_extr_info = utils.extract_data_from_image_name(uploaded_file.name)
            st.dataframe(
                pd.json_normalize(json.loads(railway_extr_info)).set_index("iid")
            )


if option == "Múltiplas Imagens":
    uploaded_files = st.file_uploader(
        "Escolha múltiplas imagens...",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    if uploaded_files and st.button("Fazer detecção"):
        results, predicted_images, railway_info_list = [], [], []

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Carregada")
        with col2:
            st.subheader("Detecção")

        for uploaded_file in uploaded_files:
            image_bytes = uploaded_file.read()
            image_array = np.frombuffer(image_bytes, np.uint8)
            image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            with col1:
                st.image(
                    image_bytes,
                    caption=f"Carregado: {uploaded_file.name}",
                    use_container_width=True,
                )

            result = st_functions.predict_image(image_bytes, confidence_threshold)
            results.append(result)

            railway_info = utils.extract_data_from_image_name(uploaded_file.name)
            railway_info_list.append(railway_info)

            if "predictions" in result:
                result_bboxes = st_functions.bounding_box(result["predictions"])

                for predictions in result_bboxes:
                    bbox, class_name, confidence = predictions
                    x0, x1, y0, y1 = bbox
                    start_point, end_point = (x0, y0), (x1, y1)

                    cv2.rectangle(
                        image_array,
                        start_point,
                        end_point,
                        color=(0, 0, 255),
                        thickness=2,
                    )
                    cv2.rectangle(
                        image_array,
                        (x0, y1),
                        (x0 + 120, y1 + 20),
                        color=(0, 0, 255),
                        thickness=-1,
                    )
                    cv2.putText(
                        image_array,
                        f"{class_name}({confidence:.0%})",
                        (x0, y1 + 12),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(255, 255, 255),
                    )

            predicted_image = Image.fromarray(
                cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            )
            predicted_images.append(predicted_image)

            with col2:
                st.image(
                    predicted_image,
                    caption=f"Detectado: {uploaded_file.name}",
                    use_container_width=True,
                )

        json_tab, rail_info = st.tabs(
            ["Tabela de Detecção", "Informação - Nome da Imagem"]
        )

        with json_tab:
            st.write("## Tabela de Detecção de Defeitos")
            # print(results)
            # st.json(result)
            st.dataframe(
                pd.concat(
                    [
                        utils.data_to_dataframe(result)
                        for result in results
                        if "predictions" in result
                    ]
                )
            )

        with rail_info:
            st.write("## Informação dos Trilhos")
            # st.json(railway_info_list)

            st.dataframe(
                pd.concat(
                    [
                        pd.json_normalize(json.loads(railway_info))
                        for railway_info in railway_info_list
                    ]
                ).set_index("iid")
            )

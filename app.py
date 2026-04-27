import streamlit as st
from PIL import Image
from io import BytesIO
import os

st.set_page_config(
    page_title="Convertidor JPG a PNG",
    layout="centered"
)

st.markdown("""
<style>
    .main-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    .title {
        font-size: 34px;
        font-weight: bold;
        color: #222222;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 17px;
        color: #555555;
        margin-bottom: 20px;
    }

    .instructions {
        background-color: #f5f7fa;
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #ff7a00;
        color: #333333;
        line-height: 1.6;
    }
</style>

<div class="main-container">
    <div class="title">Convertidor JPG a PNG</div>
    <div class="subtitle">
        Sube una imagen JPG o JPEG y conviértela a formato PNG.
    </div>

    <div class="instructions">
        <strong>Instrucciones:</strong><br><br>
        1. Da clic en el botón para subir tu imagen.<br>
        2. Selecciona un archivo JPG o JPEG desde tu computadora.<br>
        3. La app mostrará una vista previa de la imagen.<br>
        4. Da clic en descargar para obtener tu archivo en PNG.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Sube tu archivo JPG o JPEG",
    type=["jpg", "jpeg"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)

        st.subheader("Vista previa")
        st.image(image, use_container_width=True)

        png_buffer = BytesIO()

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGBA")
        else:
            image = image.convert("RGB")

        image.save(png_buffer, format="PNG")
        png_buffer.seek(0)

        original_name = os.path.splitext(uploaded_file.name)[0]
        new_file_name = f"{original_name}.png"

        st.success("Imagen convertida correctamente.")

        st.download_button(
            label="Descargar imagen en PNG",
            data=png_buffer,
            file_name=new_file_name,
            mime="image/png"
        )

    except Exception:
        st.error("No se pudo convertir la imagen. Verifica que el archivo sea un JPG válido.")

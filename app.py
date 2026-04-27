import streamlit as st
from PIL import Image
from io import BytesIO
import os
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Convertidor JPG a PNG",
    layout="centered"
)

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

logo_html = ""

if os.path.exists("logo.jpg"):
    logo_base64 = image_to_base64("logo.jpg")
    logo_html = f'<img class="logo" src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: transparent;
    }}

    .card {{
        background: #ffffff;
        border-radius: 26px;
        padding: 38px 34px;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.28);
        text-align: center;
        max-width: 760px;
        margin: 0 auto;
    }}

    .logo {{
        width: 145px;
        height: 145px;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.30);
    }}

    .logo-placeholder {{
        width: 145px;
        height: 145px;
        border-radius: 50%;
        background: #111827;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 18px auto;
        font-weight: bold;
    }}

    .title {{
        font-size: 40px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 10px;
    }}

    .subtitle {{
        font-size: 18px;
        color: #4b5563;
        margin-bottom: 28px;
        line-height: 1.5;
    }}

    .instructions {{
        background: #f4f6f8;
        border-radius: 18px;
        padding: 22px;
        text-align: left;
        border-left: 6px solid #f97316;
    }}

    .instructions h3 {{
        margin: 0 0 16px 0;
        font-size: 21px;
        color: #111827;
    }}

    .step {{
        display: flex;
        gap: 12px;
        align-items: flex-start;
        margin-bottom: 13px;
        font-size: 16px;
        color: #374151;
        line-height: 1.45;
    }}

    .number {{
        min-width: 30px;
        height: 30px;
        background: #f97316;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
    }}

    .note {{
        margin-top: 18px;
        font-size: 14px;
        color: #6b7280;
        text-align: center;
    }}
</style>
</head>

<body>
    <div class="card">
        {logo_html}

        <div class="title">Convertidor JPG a PNG</div>

        <div class="subtitle">
            Sube una imagen en formato JPG o JPEG y conviértela fácilmente a PNG.
        </div>

        <div class="instructions">
            <h3>Instrucciones</h3>

            <div class="step">
                <div class="number">1</div>
                <div>Selecciona una imagen en formato JPG o JPEG.</div>
            </div>

            <div class="step">
                <div class="number">2</div>
                <div>Espera a que la app cargue la vista previa de tu imagen.</div>
            </div>

            <div class="step">
                <div class="number">3</div>
                <div>La conversión a PNG se hará automáticamente.</div>
            </div>

            <div class="step">
                <div class="number">4</div>
                <div>Da clic en el botón de descarga para guardar tu archivo PNG.</div>
            </div>

            <div class="note">
                No necesitas instalar nada adicional. Solo sube tu archivo y descarga el resultado.
            </div>
        </div>
    </div>
</body>
</html>
""", height=570)

st.markdown("### Sube tu imagen")
st.caption("Formatos permitidos: JPG y JPEG")

uploaded_file = st.file_uploader(
    "Selecciona tu archivo",
    type=["jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)

        st.markdown("### Vista previa")
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
        st.error("No se pudo convertir la imagen. Verifica que el archivo sea válido.")

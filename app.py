import streamlit as st
from PIL import Image, ImageOps
from io import BytesIO
import os
import base64
import streamlit.components.v1 as components
from rembg import remove, new_session

st.set_page_config(
    page_title="Quitar fondo de imagen",
    layout="centered"
)

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

@st.cache_resource
def load_rembg_session():
    return new_session("u2net")

logo_html = ""

if os.path.exists("logo.jpg"):
    logo_base64 = image_to_base64("logo.jpg")
    logo_html = f'<img class="logo" src="data:image/jpeg;base64,{logo_base64}" alt="Logo">'
else:
    logo_html = '<div class="logo-placeholder">LOGO</div>'

st.markdown("""
<style>
    .stApp {
        background: #eef2f7;
    }

    .block-container {
        max-width: 980px;
        padding-top: 30px;
        padding-bottom: 50px;
    }

    h3 {
        color: #0f172a !important;
        font-size: 28px !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
    }

    .stCaptionContainer {
        color: #475569 !important;
        font-size: 15px !important;
    }

    div[data-testid="stFileUploader"] {
        width: 100% !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        padding: 22px !important;
        border-radius: 18px !important;
        min-height: 90px !important;
        background-color: #ffffff !important;
        border: 1px solid #dbe3ec !important;
        overflow: visible !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06) !important;
    }

    div[data-testid="stFileUploaderDropzone"] > div {
        width: 100% !important;
        overflow: visible !important;
    }

    div[data-testid="stFileUploaderFile"] {
        width: 100% !important;
        max-width: 100% !important;
        min-height: 56px !important;
        overflow: visible !important;
    }

    div[data-testid="stFileUploaderFile"] > div {
        width: 100% !important;
        max-width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 14px !important;
        overflow: visible !important;
    }

    div[data-testid="stFileUploaderFileName"] {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        max-width: calc(100% - 60px) !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow: visible !important;
        padding-right: 12px !important;
    }

    button[data-testid="stFileUploaderDeleteBtn"] {
        flex: 0 0 auto !important;
        position: relative !important;
        z-index: 999 !important;
        margin-left: 12px !important;
        min-width: 32px !important;
        min-height: 32px !important;
    }

    div[data-testid="stFileUploaderDropzoneInstructions"] {
        width: 100% !important;
        color: #475569 !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px !important;
    }

    .stDownloadButton button {
        width: 100%;
        border-radius: 12px;
        padding: 12px 18px;
        font-weight: 700;
        background: #f97316 !important;
        color: white !important;
        border: none !important;
    }

    .stDownloadButton button:hover {
        background: #ea580c !important;
        color: white !important;
    }

    .result-box {
        background: #ffffff;
        border: 1px solid #dbe3ec;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        margin-top: 20px;
    }

    .section-card {
        background: #ffffff;
        border: 1px solid #dbe3ec;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        margin-top: 24px;
    }
</style>
""", unsafe_allow_html=True)

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
        border: 1px solid #dbe3ec;
        border-radius: 28px;
        padding: 40px 36px;
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
        text-align: center;
        max-width: 820px;
        margin: 0 auto;
    }}

    .logo {{
        width: 140px;
        height: 140px;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 18px;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.18);
    }}

    .logo-placeholder {{
        width: 140px;
        height: 140px;
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
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 12px;
    }}

    .subtitle {{
        font-size: 18px;
        color: #475569;
        margin-bottom: 30px;
        line-height: 1.5;
    }}

    .instructions {{
        background: #f8fafc;
        border-radius: 22px;
        padding: 24px;
        text-align: left;
        border: 1px solid #e2e8f0;
        border-left: 7px solid #f97316;
    }}

    .instructions h3 {{
        margin: 0 0 18px 0;
        font-size: 22px;
        color: #0f172a;
    }}

    .step {{
        display: flex;
        gap: 13px;
        align-items: flex-start;
        margin-bottom: 14px;
        font-size: 16px;
        color: #334155;
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
        color: #64748b;
        text-align: center;
    }}
</style>
</head>

<body>
    <div class="card">
        {logo_html}

        <div class="title">Quitar fondo de imagen</div>

        <div class="subtitle">
            Sube una imagen y descarga una versión PNG con fondo transparente.
        </div>

        <div class="instructions">
            <h3>Instrucciones</h3>

            <div class="step">
                <div class="number">1</div>
                <div>Selecciona una imagen en formato JPG, JPEG o PNG.</div>
            </div>

            <div class="step">
                <div class="number">2</div>
                <div>La app procesará la imagen automáticamente.</div>
            </div>

            <div class="step">
                <div class="number">3</div>
                <div>Revisa el resultado sin fondo.</div>
            </div>

            <div class="step">
                <div class="number">4</div>
                <div>Descarga tu imagen en formato PNG transparente.</div>
            </div>

            <div class="note">
                El resultado puede variar dependiendo de la calidad de la imagen y del contraste con el fondo.
            </div>
        </div>
    </div>
</body>
</html>
""", height=620)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### Sube tu imagen")
st.caption("Formatos permitidos: JPG, JPEG y PNG")

uploaded_file = st.file_uploader(
    "Selecciona tu archivo",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        input_image = Image.open(uploaded_file)
        input_image = ImageOps.exif_transpose(input_image)
        input_image = input_image.convert("RGBA")

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.markdown("### Imagen original")
        st.image(input_image, use_container_width=True)

        with st.spinner("Quitando el fondo de la imagen..."):
            session = load_rembg_session()
            output_image = remove(input_image, session=session)
            output_image = output_image.convert("RGBA")

        png_buffer = BytesIO()
        output_image.save(png_buffer, format="PNG")
        png_buffer.seek(0)

        original_name = os.path.splitext(uploaded_file.name)[0]
        new_file_name = f"{original_name}_sin_fondo.png"

        st.markdown("### Resultado sin fondo")
        st.image(output_image, use_container_width=True)

        st.success("Fondo eliminado correctamente.")

        st.download_button(
            label="Descargar imagen sin fondo",
            data=png_buffer,
            file_name=new_file_name,
            mime="image/png"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("No se pudo quitar el fondo de la imagen.")
        st.write("Detalle del error:")
        st.code(str(e))

from io import BytesIO

import qrcode

# from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import streamlit as st


def create_qrcode(data: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=36,
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # img = qr.make_image(fill="black", back_color="white", image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img = qr.make_image(fill="black", back_color="white")

    # Save the image to a bytes object
    byte_io = BytesIO()
    img.save(byte_io, format="PNG")  # You can specify different formats like 'JPEG' or 'BMP'

    # Get the bytes data
    return byte_io.getvalue()


if "qr" not in st.session_state:
    st.session_state.qr = create_qrcode(st.session_state.token)


st.warning(":material/engineering: The AI Tutor Mobile App is currently in active development. Coming soon :eyes:")

st.title("Log in with Mobile")
st.write("---")
st.image(
    st.session_state.qr, caption="Scan the QR code to log on on the AI Tutor mobile app", use_container_width=False
)

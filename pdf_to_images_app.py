import streamlit as st
from pdf2image import convert_from_bytes
import os
from io import BytesIO
from zipfile import ZipFile

st.title("📄 PDF to Images Converter")

pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
folder_path = st.text_input("Enter folder path to save images locally (optional)")

if st.button("Convert PDF to Images"):
    if pdf_file is None:
        st.error("❌ Please upload a PDF file first.")
    else:
        pages = convert_from_bytes(pdf_file.read())
        st.success(f"✅ PDF converted! {len(pages)} pages.")

        if folder_path.strip() != "":
            os.makedirs(folder_path, exist_ok=True)
            for i, page in enumerate(pages):
                image_path = os.path.join(folder_path, f"page_{i+1}.png")
                page.save(image_path, "PNG")
            st.info(f"📂 Images saved locally at: {folder_path}")

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for i, page in enumerate(pages):
                img_buffer = BytesIO()
                page.save(img_buffer, format="PNG")
                zip_file.writestr(f"page_{i+1}.png", img_buffer.getvalue())

        zip_buffer.seek(0)
        st.download_button(
            label="Download All Pages as ZIP",
            data=zip_buffer,
            file_name="pdf_pages.zip",
            mime="application/zip"
        )

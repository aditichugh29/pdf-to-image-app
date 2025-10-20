import streamlit as st
from pdf2image import convert_from_bytes
import os

st.title("PDF to Images Converter 🖼️")

pdf_file = st.file_uploader("Upload your PDF", type="pdf")

if pdf_file is not None:
    output_folder = "PDF_Pages"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    st.info("Converting PDF pages to images. This may take a few seconds...")

    try:
        images = convert_from_bytes(pdf_file.read(), dpi=80)
        st.success(f"PDF has {len(images)} pages. Saving images now...")

        for i, page in enumerate(images):
            page_path = os.path.join(output_folder, f"page_{i+1}.png")
            page.save(page_path, "PNG")

        st.success(f"All pages saved in '{output_folder}' folder!")

        show_images = st.checkbox("Show pages here")
        if show_images:
            for i, page in enumerate(images):
                st.image(page, caption=f"Page {i+1}")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")

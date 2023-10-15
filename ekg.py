import streamlit as st
from PIL import Image
import fitz  # PyMuPDF

def main():
    st.title("PDF zu Bild Konverter")
    
    uploaded_file = st.file_uploader("Wählen Sie eine PDF-Datei aus", type=["pdf"])
    
    if uploaded_file is not None:
        st.write("Datei erfolgreich hochgeladen. Hier ist die konvertierte Seite:")
        
        doc = fitz.open(uploaded_file)
        zoom = 4.17  # 300 dpi / 72 dpi
        
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_resized = img.resize((3300, 2550), Image.ANTIALIAS)
            output = f"converted_page_{i}.png"
            img_resized.save(output)
            st.image(output)

if __name__ == "__main__":
    main()

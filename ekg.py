import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import tempfile
import os

def main():
    st.title("PDF zu Bild Konverter")
    
    uploaded_file = st.file_uploader("Wählen Sie eine PDF-Datei aus", type=["pdf"])
    
    if uploaded_file is not None:
        st.write("Datei erfolgreich hochgeladen. Hier ist die konvertierte Seite:")
        
        # Erstellen einer temporären Datei auf dem Server
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_pdf_file_path = temp_file.name
        
        # Öffnen der temporären Datei mit fitz
        doc = fitz.open(temp_pdf_file_path)
        
        zoom = 4.17  # 300 dpi / 72 dpi
        
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = Image.frombuffer("RGB", [pix.width, pix.height], pix.samples, "raw", "RGB", 0, 1)
            img_resized = img.resize((3300, 2550), Image.LANCZOS)
            output = f"converted_page_{i}.png"
            img_resized.save(output)
            st.image(output)
            
            # Hinzufügen des Download-Buttons
            with open(output, "rb") as file:
                btn_label = f"Download Seite {i+1}"
                bytes_data = file.read()
                st.download_button(
                    label=btn_label,
                    data=bytes_data,
                    file_name=f"Seite_{i+1}.png",
                    mime="image/png"
                )
        
        # Schließen des fitz Dokuments und Löschen der temporären Datei
        doc.close()
        os.remove(temp_pdf_file_path)

if __name__ == "__main__":
    main()
    


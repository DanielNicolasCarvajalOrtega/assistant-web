from docx import Document
from gtts import gTTS
import pandas as pd
import matplotlib.pyplot as plt


def process_text_file(file_path):
    """Procesa un archivo de texto y retorna su contenido."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_docx_file(file_path):
    """Procesa un archivo .docx y retorna su contenido."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def convert_text_to_audio(text, output_path):
    """Convierte texto a audio usando gTTS."""
    tts = gTTS(text=text, lang='es')
    tts.save(output_path)

def process_excel_file(file_path):
    """Procesa un archivo Excel y retorna un DataFrame."""
    return pd.read_excel(file_path)

def generate_graph(df, output_path):
    """Genera un gráfico basado en los datos de un DataFrame y lo guarda como PNG."""
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar')  # Gráfico de barras, personalízalo según tus necesidades
    plt.title('Gráfico Generado')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

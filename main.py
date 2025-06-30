import tkinter as tk
from tkinter import scrolledtext
import pytesseract
from PIL import ImageGrab
from deep_translator import GoogleTranslator

# Configurações
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text_area = (0, 700, 1920, 1020)


def capturar_e_traduzir():

    # DEBUG
    '''
    x1, y1, x2, y2 = text_area
    width = x2 - x1
    height = y2 - y1
    janela = tk.Tk()
    janela.attributes("-topmost", True)
    janela.overrideredirect(True)  # Remove borda
    janela.attributes("-alpha", 0.3)  # Transparência

    # Posiciona a janela sobre a área desejada
    janela.geometry(f"{width}x{height}+{x1}+{y1}")

    # Cria um canvas para desenhar o retângulo
    canvas = tk.Canvas(janela, width=width, height=height)
    canvas.pack()

    # Desenha um retângulo vermelho com borda grossa
    canvas.create_rectangle(0, 0, width, height, outline="red", width=3)
    '''
    #DEBUG END

    #---
    imagem = ImageGrab.grab(bbox=text_area)
    texto_extraido = pytesseract.image_to_string(imagem, lang='eng').strip()
    texto_extraido = texto_extraido.replace('|', 'I')

    if texto_extraido:
        try:
            traducao = GoogleTranslator(source='en', target='pt').translate(texto_extraido)
        except Exception as e:
            traducao = f"Erro na tradução: {e}"
    else:
        texto_extraido = "Nenhum texto detectado."
        traducao = ""


    resultado_texto.config(state='normal')
    resultado_texto.delete('1.0', tk.END)
    resultado_texto.insert(tk.END, f"Texto original:\n{texto_extraido}\n\nTradução:\n{traducao}")
    resultado_texto.config(state='disabled')

root = tk.Tk()
root.title("Tradutor Novel")
root.geometry("500x300")
root.attributes("-topmost", True)  # Janela sempre no topo

botao = tk.Button(root, text="Capturar e Traduzir", command=capturar_e_traduzir)
botao.pack(pady=10)

resultado_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=12, state='disabled')
resultado_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()

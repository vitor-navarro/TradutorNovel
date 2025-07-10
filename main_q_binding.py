import tkinter as tk
from tkinter import scrolledtext
import pytesseract
from PIL import ImageGrab
from deep_translator import GoogleTranslator
import threading
import keyboard
from PIL import ImageOps


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text_area = (0, 250, 1920, 1025)


def preprocess_image(img):
    '''
    # A utilidade disso irá depender de como vai ser sua tela, gera caracteres aleatórios, pode fazer com que textos não identificados sejam identificados
    warning: cenários com cores muito parecidas das letras podem causar interferências e fazer o texto ser traduzido com ruído ou não ser traduzido.
    :param img: image to process
    :return: image binarized
    '''

    gray = ImageOps.grayscale(img)

    enhanced = ImageOps.autocontrast(gray)

    binarized = enhanced.point(lambda x: 0 if x < 160 else 255, '1')

    return binarized

def capturar_e_traduzir():
    imagem = ImageGrab.grab(bbox=text_area)
    #optional
    imagem = preprocess_image(imagem)
    custom_config = r'--oem 3 --psm 6'
    texto_extraido = pytesseract.image_to_string(imagem, lang='eng', config=custom_config).strip()

    #Irá evitar o I (eu em inglês) ser identificado como pipeline
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
    resultado_texto.insert(tk.END, traducao)
    resultado_texto.config(state='disabled')

def iniciar_atalho_global():
    keyboard.add_hotkey('q', lambda: capturar_e_traduzir())
    keyboard.wait()

root = tk.Tk()
root.overrideredirect(True)  # Remove bordas
root.geometry("500x150+100+100")  # Tamanho e posição (pode ajustar)
root.attributes("-topmost", True)  # Sempre por cima
root.attributes("-alpha", 0.7)     # Transparência da janela (0.0 a 1.0)

resultado_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, state='disabled', bg="#000000", fg="#00FF00", insertbackground="white", font=("Arial", 16))
resultado_texto.pack(fill=tk.BOTH, expand=True)

threading.Thread(target=iniciar_atalho_global, daemon=True).start()

root.mainloop()

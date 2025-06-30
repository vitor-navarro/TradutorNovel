import tkinter as tk
from PIL import ImageGrab
from PIL import ImageOps

# Área da tela onde será feita a captura (ajuste conforme necessário)
text_area = (0, 250, 1920, 1020)

# Calcula largura e altura do retângulo
x1, y1, x2, y2 = text_area
width = x2 - x1
height = y2 - y1

# Cria uma janela transparente
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

# Roda a janela em loop (vai ficar sempre em cima)
janela.mainloop()

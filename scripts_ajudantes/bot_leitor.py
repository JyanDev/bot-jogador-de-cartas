import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import os
import pyautogui
import time

pytesseract.pytesseract.tesseract_cmd = r'E:\jyand\Documents\projectnew\Tesseract\tesseract.exe'

def capture_around_mouse(width=240, height=60, save_path="res/current_text.png"):
    """Captura um screenshot ao redor da posição atual do mouse."""
    x, y = pyautogui.position()
    screenshot = pyautogui.screenshot(region=(x - width // 2, y - height // 2, width, height))
    screenshot.save(save_path)
    return save_path

def extrair_percentagens(image_path):
    """Extrai texto de uma imagem."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem {image_path}")
        return ""
    pil_img = Image.fromarray(img) 
    pil_img.save("processed_image.png")  # Salvando a imagem processada para verificaçã
    text = pytesseract.image_to_string(pil_img)
    return text

def real_time_text_read():
    """Lê texto em tempo real ao redor do cursor do mouse."""
    try:
        print("Iniciando leitura em tempo real. Mova o cursor sobre o texto. Pressione Ctrl+C para parar.")
        while True:
            image_path = capture_around_mouse()
            text = extrair_percentagens(image_path)
            print("Texto Extraído:", text)
            time.sleep(3)  # Intervalo para não sobrecarregar o CPU
    except KeyboardInterrupt:
        print("Leitura em tempo real interrompida.")

# Uso das funções
real_time_text_read()

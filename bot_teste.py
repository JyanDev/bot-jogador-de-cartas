import pyautogui
import cv2
import os
import numpy as np
import json
from time import sleep
from pynput import mouse
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'E:\jyand\Documents\projectnew\Tesseract\tesseract.exe'

class BotTest:
    def __init__(self, image_folder="res/loop", resolution_file="res2/backup/resolutions.json"):
        self.image_folder = image_folder
        self.target_position = None
        self.janela_cords = self.janela()
        self.running = True
        self.log_file = "image_similarity_log.txt"
        self.resolution_file = resolution_file
        self.resolutions = self.load_resolutions()

    def janela(self, titulo="MEmu"):
        janela = pyautogui.getWindowsWithTitle(titulo)[0]
        if janela:
            janela.activate()
            sleep(0.3)
            return janela.left, janela.top, janela.width, janela.height
        else:
            return False

    def convert_to_hsv(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv_image

    def log_similarity(self, filename, similarity):
        with open(self.log_file, 'a') as file:
            file.write(f"{filename} - semelhança: {similarity}\n")

    def compare_images(self, template, screen, template_filename):
        template_hsv = self.convert_to_hsv(template)
        screen_hsv = self.convert_to_hsv(screen)

        # Garantir que o diretório res2 exista
        os.makedirs("res2", exist_ok=True)
        
        # Convertendo para BGR para salvar e visualizar como o bot vê
        #screen_bgr_from_hsv = cv2.cvtColor(screen_hsv, cv2.COLOR_HSV2BGR)
        #template_bgr_from_hsv = cv2.cvtColor(template_hsv, cv2.COLOR_HSV2BGR)
        
        # Salvar as imagens convertidas
        cv2.imwrite(f"res2/screen.png", screen_hsv)
        cv2.imwrite(f"res2/{template_filename}", template_hsv)

        result = cv2.matchTemplate(screen_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val

    def capture_screenshot(self):
        screen = pyautogui.screenshot(region=self.janela_cords)
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        return screen

    def on_click(self, x, y, button, pressed):
        if pressed:
            sleep(0.5)
            self.target_position = (x, y)
            self.running = False
            return False

    def load_resolutions(self):
        if os.path.exists(self.resolution_file):
            with open(self.resolution_file, 'r') as file:
                return json.load(file)
        return {}

    def apply_resolutions(self, image, filename):
        if filename in self.resolutions:
            new_width, new_height = self.resolutions[filename]
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return image
        return image

    def run_test(self):
        print("Clique em um elemento na tela para iniciar o teste...")
        with mouse.Listener(on_click=self.on_click) as listener:
            while self.running:
                sleep(0.1)
            listener.join()

        screen = self.capture_screenshot()
        screen_image = Image.fromarray(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        if 'screen' in self.resolutions:
            screen_image = screen_image.resize(self.resolutions['screen'], Image.Resampling.LANCZOS)
            screen = np.array(screen_image)
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg')):
                file_path = os.path.join(self.image_folder, filename)
                template = Image.open(file_path)
                template = self.apply_resolutions(template, filename)
                template = np.array(template)
                template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
                if template is None:
                    print(f"Erro ao carregar a imagem {file_path}")
                    continue
                similarity = self.compare_images(template, screen, filename)
                self.log_similarity(filename, similarity)
                print(f"{filename} - semelhança: {similarity}")

if __name__ == "__main__":
    bot_test = BotTest(image_folder="res/loop", resolution_file="res2/backup/resolutions.json")
    bot_test.run_test()

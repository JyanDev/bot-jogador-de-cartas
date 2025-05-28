import pyautogui
import cv2
import os
import numpy as np
from time import sleep
from pynput import keyboard
import pytesseract
from PIL import Image
import re
import pygetwindow as gw

pytesseract.pytesseract.tesseract_cmd = r'E:\jyand\Documents\projectnew\Tesseract\tesseract.exe'

class BotCartas:
    def __init__(self, janela_titulo="MEmu"):
        self.loop = True
        self.count = 0
        self.num_val = 0.8
        self.cont = 0
        self.janela_cords = self.janela(janela_titulo)
        self.pause = 0

    def janela(self, titulo="MEmu"):
        janela = gw.getWindowsWithTitle(titulo)[0]
        if janela:
            janela.activate()
            sleep(0.3)
            return janela.left, janela.top, janela.width, janela.height
        else:
            return False

    def log_message(self, message):
        file_path = "cache/Logs.txt"
        with open(file_path, 'a') as file:
            file.write(message + "\n")
        raise Exception("Um erro crítico ocorreu. Verifique o arquivo de log para mais detalhes.")

    def log_progresso(self, message):
        file_path = "cache/Progresso.txt"
        with open(file_path, 'a') as file:
            file.write(message + "\n")

    def capture_location_porcentagem(self, location):
        width, height, save_path = 240, 60, "res/reiniciar_etapa/location.png"
        x, y = location
        screenshot = pyautogui.screenshot(region=(x - 120, y - 30, width, height))
        screenshot.save(save_path)
        return save_path

    def extrair_percentagens(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Erro ao carregar a imagem {image_path}")
            return []
        pil_img = Image.fromarray(img)
        pil_img.save("processed_image.png")
        text = pytesseract.image_to_string(pil_img)
        print("Texto Extraído:", text)
        return re.findall(r'\d+', text)

    def Rolar_telaDown(self):
        value, positionDown = self.localizar("res/fundo_none/7volta.png", "7volta.png")
        if value:
            x, y = positionDown
            x_Dw, y_Dw = x * 1.2, y * 5.00
            pyautogui.moveTo(x_Dw, y_Dw)
            pyautogui.scroll(-1)
            sleep(0.5)
            pyautogui.click(x_Dw, y_Dw)

    def Rolar_telaUp(self):
        value, positionUp = self.localizar("res/fundo_none/7volta.png", "7volta.png")
        if value:
            x, y = positionUp
            x_up, y_up = x * 1.2, y * 5.00
            pyautogui.moveTo(x_up, y_up)
            pyautogui.scroll(1)
            sleep(0.5)
            pyautogui.click(x_up, y_up)

    def convert_to_hsv(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv_image

    def localizar(self, image_path, filename, num_val=0.80):
        try:
            template = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if template is None:
                raise ValueError(f"A imagem {image_path} não pôde ser carregada.")

            template_hsv = self.convert_to_hsv(template)
            screen = pyautogui.screenshot(region=self.janela_cords)
            screen_color = np.array(screen)
            screen_hsv = self.convert_to_hsv(screen_color)

            result = cv2.matchTemplate(screen_hsv, template_hsv, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > num_val:
                center_x = max_loc[0] + template.shape[1] // 2 + self.janela_cords[0]
                center_y = max_loc[1] + template.shape[0] // 2 + self.janela_cords[1]
                return True, (center_x, center_y)
            return False, None

        except Exception as e:
            print(f"Erro ao verificar a imagem na tela: {e}")
            return False, None

    def click(self, position):
        pyautogui.click(position)

    def click_bots(self, image):
        value, position = self.localizar(image)
        if value:
            self.click(position)
            return True
        else:
            return None

    def carta_true(self, image, name):
        if name == "1carta_true.png":
            value, position = self.localizar("res/loop/1carta_true.png", "1carta_true.png", self.num_val)
            valueg, positiong = self.localizar("res/loop/2ok.png", "2ok.png")
            while value or valueg:
                if value: pyautogui.click(position)
                if valueg: pyautogui.click(positiong)
                sleep(0.3)
                value, position = self.localizar("res/loop/1carta_true.png", "1carta_true.png", self.num_val)
                valueg, positiong = self.localizar("res/loop/2ok.png", "2ok.png")
                if valueg:
                    self.count = 0
                    pyautogui.click(positiong)
                    sleep(1)
                elif not valueg and value:
                    if self.num_val < 0.90:
                        self.num_val += 0.02
                        self.count = 0
                        return False
                    elif self.num_val >= 0.88:
                        self.num_val = 0.80
                        self.count = 0
                        self.Rolar_telaUp()
                        return False

            if not value:
                value, position = self.localizar("res/loop/3carta_batle.png", "3carta_batle.png")
                valuef, positionf = self.localizar("res/fundo_none/1afundo_none.png", "1afundo_none.png")
                while valuef and not value:
                    self.Rolar_telaUp()
                    sleep(1)
                    valuef, positionf = self.localizar("res/fundo_none/1afundo_none.png", "1afundo_none.png")
                value2, position2 = self.localizar("res/loop/1carta_true.png", "1carta_true.png", self.num_val)
                if value:
                    return False
                if self.count >= 5 and not value2:
                    self.fundo_none()
                    return False
                elif self.count < 5 and not value2:
                    self.count += 1
                    self.Rolar_telaDown()
                    return True
        else:
            return False

    def carta_batle(self, image, name):
        value, position = self.localizar(image, name)

        if name == "3carta_batle.png":
            value, position = self.localizar(image, name)
            while value and self.cont <= 2:
                if value: pyautogui.click(position)
                sleep(1)
                value, position = self.localizar(image, name)
                valuef, positionf = self.localizar("res/loop/4ataque.png", "4ataque.png")
                if valuef:
                    self.count = 0
                    pyautogui.click(positionf)
                    sleep(1)
                    valuef, positionf = self.localizar("res/loop/5desafiar.png", "5desafiar.png")
                    if valuef:
                        pyautogui.click(positionf)
                        sleep(1)
                        valuef, positionf = self.localizar("res/loop/6x.png", "6x.png")
                        while not value:
                            valuef, positionf = self.localizar("res/loop/6x.png", "6x.png")
                            if valuef:
                                pyautogui.click(positionf)
                                self.cont = 0
                                return True
                self.cont += 1
            if self.cont >= 2:
                self.cont = 0
                return False
        else:
            return False

    def verifica_porcentagem(self):
        value2, position2 = self.localizar("res/loop/2ok.png", "2ok.png")
        value, position = self.localizar("res/reiniciar_etapa/porcent_very.png", "porcent_very.png")
        if not value and not value2:
            value, position = self.localizar("res/fundo_none/7volta.png", "7volta.png")
            if value:
                pyautogui.click(position)
                sleep(2)
                value, position = self.localizar("res/reiniciar_etapa/porcent_very.png", "porcent_very.png")
                if value:
                    image_path = self.capture_location_porcentagem(position)
                    porcentagem = self.extrair_percentagens(image_path)
                    if porcentagem:
                        if porcentagem[0] == "100":
                            self.pause += 1
                            self.log_progresso(f"AGR ESTA: {self.pause}")
                            if self.pause == 4:
                                self.log_message("Pausado")
                            value, position = self.localizar("res/reiniciar_etapa/porcent_very.png", "porcent_very.png")
                            if value:
                                pyautogui.click(position)
                                sleep(1)
                                value, position = self.localizar("res/reiniciar_etapa/reinicio.png", "reinicio.png")
                                if value:
                                    pyautogui.click(position)
                                    sleep(3)
                                    value, position = self.localizar("res/loop/2ok.png", "2ok.png")
                                    pyautogui.click(position)
                                    sleep(2)
                                    value, position = self.localizar("res/reiniciar_etapa/porcent_very.png", "porcent_very.png")
                                    pyautogui.click(position)
                                    sleep(1)
                                    value, position = self.localizar("res/loop/2ok.png", "2ok.png")
                                    pyautogui.click(position)
                                    sleep(2)
                                    return True
                        else:
                            return False
                    else:
                        self.log_message("Erro: Lista de porcentagens está vazia.")
                        return False
                else:
                    self.log_message("Recurso faltando, corrompido ou indetectável!! [Porcent_very.png]")
        else:
            value2, position2 = self.localizar("res/loop/2ok.png", "2ok.png")
            if value2:
                pyautogui.click(position2)
                return True
            else:
                return False

    def fundo_none(self):
        self.count = 0
        self.num_val = 0.8
        result = self.verifica_porcentagem()
        if result:
            return True
        if not result:
            value, position = self.localizar("res/fundo_none/banner.png", "banner.png")
            if value:
                pyautogui.click(position)
                return True
            if not value:
                for filename in os.listdir("res/loop"):
                    file_path = os.path.join("res/loop", filename)
                    if file_path.lower().endswith(('.png', '.jpg')):
                        value, position = self.localizar(file_path, filename)
                        if value:
                            pyautogui.moveTo(position)
                            pyautogui.click(position[0], position[1] + 80)
                            return True
                self.log_message(f"Banner não encontrado")

    def process_images(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if file_path.lower().endswith(('.png', '.jpg')) and filename == "1carta_true.png":
                result = self.carta_true(file_path, filename)
                if result:
                    print(f"{filename} TRUE")
                else:
                    print(f"{filename} false")
            elif file_path.lower().endswith(('.png', '.jpg')) and filename == "3carta_batle.png":
                result = self.carta_batle(file_path, filename)
                if result:
                    print(f"{filename} TRUE")
                else:
                    print(f"{filename} false")

    def run_bot(self):
        def on_press(key):
            try:
                if key.char == 'w':
                    self.loop = False
                    return False
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            while self.loop:
                self.process_images("res/loop")
            listener.join()

if __name__ == "__main__":
    bot = BotCartas()
    bot.run_bot()

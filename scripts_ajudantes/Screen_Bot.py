from pynput import mouse, keyboard
import pyautogui
import tkinter as tk
import cv2
import numpy as np
import os

# Criação das pastas se não existirem
os.makedirs('clicks', exist_ok=True)
os.makedirs('assets', exist_ok=True)

# Variáveis globais para a região de captura
width = 100
height = 60
x_offset = 60
y_offset = 20
active = True

# Configuração inicial da janela
root = tk.Tk()
root.attributes('-alpha', 0.3)  # Torna a janela transparente
root.overrideredirect(True)  # Remove a borda da janela
root.lift()  # Mantém a janela acima de outras janelas
root.configure(bg='white')  # Cor de fundo da janela

def update_window_position(x, y):
    global x_offset, y_offset
    x_offset = width // 2
    y_offset = height // 2
    root.geometry(f"{width}x{height}+{x - x_offset}+{y - y_offset}")

def hide_window():
    root.withdraw()

def show_window():
    root.deiconify()
    root.lift()
    root.attributes('-alpha', 0.3)
    update_window_position(pyautogui.position().x, pyautogui.position().y)

def on_click(x, y, button, pressed):
    global active
    if active and pressed:
        hide_window()
        click_count = len(os.listdir('clicks')) + 1
        with open(f'clicks/click_{click_count}.txt', 'w') as f:
            f.write(f"Posicao do clique: {x}, {y}\n")
        capture_element(x, y, click_count)
        show_window()

def on_move(x, y):
    if active:
        update_window_position(x, y)




def capture_element(x, y, click_count):
    # Captura a screenshot da área especificada
    screen = pyautogui.screenshot(region=(x - x_offset, y - y_offset, width, height))
    #screen_color = np.array(screen)

    # Salvar a imagem filtrada
    screen.save(f'assets/element_{click_count}.png')

def on_key_press(key):
    global width, height, active
    try:
        if key.char == 'w' and height > 10:
            height -= 1
        elif key.char == 's':
            height += 1
        elif key.char == 'a' and width > 10:
            width -= 1
        elif key.char == 'd':
            width += 1

        if key.char == "0":
            hide_window()
            active = False
        elif key.char == '1':
            show_window()
            active = True

        update_window_position(pyautogui.position().x, pyautogui.position().y)
    except AttributeError:
        pass  # Ignora outras teclas que não são caracteres

def start_listeners():
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener.start()
    keyboard_listener.start()
    root.mainloop()
    mouse_listener.join()
    keyboard_listener.join()

if __name__ == '__main__':
    print("Aguardando cliques. Use 'WASD' para ajustar a área de captura. Pressione Ctrl+C para parar.")
    start_listeners()

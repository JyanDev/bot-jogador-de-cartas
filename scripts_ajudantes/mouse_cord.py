from pynput.mouse import Listener

def on_move(x, y):
    print(f"Posição do Mouse: x={x}, y={y}")

def start_mouse_listener():
    with Listener(on_move=on_move) as listener:
        listener.join()

if __name__ == "__main__":
    start_mouse_listener()

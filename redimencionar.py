import os
import json
from PIL import Image

class ImageResizer:
    def __init__(self, image_folder="res/loop", resolution_file="res2/backup/resolutions.json"):
        self.image_folder = image_folder
        self.resolution_file = resolution_file
        self.screen_resolution = None

    def load_resolutions(self):
        if os.path.exists(self.resolution_file):
            with open(self.resolution_file, 'r') as file:
                return json.load(file)
        return {}

    def save_resolutions(self, resolutions):
        os.makedirs(os.path.dirname(self.resolution_file), exist_ok=True)
        with open(self.resolution_file, 'w') as file:
            json.dump(resolutions, file, indent=4)

    def resize_images(self, target_size=(100, 100), quality=95):
        resolutions = self.load_resolutions()

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg')):
                file_path = os.path.join(self.image_folder, filename)
                image = Image.open(file_path)
                original_width, original_height = image.size

                # Calcula a nova largura e altura mantendo a proporção
                aspect_ratio = original_width / original_height
                if original_width > original_height:
                    new_width = target_size[0]
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = target_size[1]
                    new_width = int(new_height * aspect_ratio)
                
                resolutions[filename] = (new_width, new_height)

                # Redimensiona a imagem mantendo a proporção
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Salva a imagem com a nova qualidade
                image.save(file_path, quality=quality)
                print(f"Imagem {filename} redimensionada para {new_width}x{new_height} com qualidade {quality}")

        self.save_resolutions(resolutions)

if __name__ == "__main__":
    resizer = ImageResizer(image_folder="res/loop", resolution_file="res2/backup/resolutions.json")
    resizer.resize_images(target_size=(100, 100), quality=95)

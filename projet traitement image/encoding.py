# encoding.py
from image import Image
from pixel import Pixel
from typing import List

# encoding.py
class Encoder:
    def __init__(self, img: Image):
        self._img = img
    
    #def __init__(self, width: int, height: int, pixels: List[Pixel]):
     #   self.width = width
      #  self.height = height
       # self.pixels = pixels


    def save_to(self, path: str):
        header = b'ULBMP\x01\x0c\x00' + self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        with open(path, 'wb') as f:
            f.write(header)
            for pixel in self._img.pixels:
                f.write(bytes(pixel))

    def is_ulbmp(filename: str) -> bool:
        # Ouvrir le fichier en mode lecture binaire
        with open(filename, 'rb') as f:
            # Lire les premiers octets pour vérifier l'en-tête ULBMP
            header = f.read(6)
            # Vérifier si les premiers octets correspondent à l'en-tête ULBMP
            return header == b'ULBMP\x01'
    
    @classmethod
    def create_from_pixels(cls, pixels: List[Pixel]) -> 'Encoder':
        width = height = int(len(pixels) ** 0.5)
        img = Image(width, height, pixels)
        return cls(img)

# encoding.py
class Decoder:
    @staticmethod
    def load_from(path: str) -> Image:
        with open(path, 'rb') as f:
            header = f.read(12)
            width = int.from_bytes(header[6:8], 'little')
            height = int.from_bytes(header[8:10], 'little')
            pixels = []
            for _ in range(width * height):
                try:
                    red, green, blue = f.read(3)
                    pixels.append(Pixel(red, green, blue))
                except ValueError:
                    raise ValueError("Invalid pixel data")
        return Image(width, height, pixels)


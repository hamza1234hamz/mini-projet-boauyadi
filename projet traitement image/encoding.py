# encoding.py
from image import Image
from pixel import Pixel
from typing import List

# encoding.py
class Encoder:
    def __init__(self, img: Image, ulbmp_version: int = 1):
        if ulbmp_version not in (1, 2):
            raise ValueError("ULBMP version must be either 1 or 2")
        self._img = img
        self._ulbmp_version = ulbmp_version
    #def __init__(self, width: int, height: int, pixels: List[Pixel]):
     #   self.width = width
      #  self.height = height
       # self.pixels = pixels


    def save_to(self, path: str):
        if self._ulbmp_version == 1:
            self._save_ulbmp_v1(path)
        elif self._ulbmp_version == 2:
            self._save_ulbmp_v2(path)
    
    def _save_ulbmp_v1(self, path: str):
        header = b'ULBMP\x01\x0c\x00' + self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        print("header ",header)
        with open(path, 'wb') as f:
            f.write(header)
            for pixel in self._img.pixels:
                f.write(bytes(pixel))
                
    def _save_ulbmp_v2(self, path: str):
        header = b'ULBMP\x02\x0c\x00' + self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        with open(path, 'wb') as f:
            f.write(header)
            current_pixel = self._img[0, 0]
            count = 1
            for y in range(self._img.height):
                for x in range(self._img.width):
                    pixel = self._img[x, y]
                    if pixel == current_pixel and count < 255:
                        count += 1
                    else:
                        f.write(bytes([count]) + bytes(current_pixel))
                        current_pixel = pixel
                        count = 1
            f.write(bytes([count]) + bytes(current_pixel))


    @staticmethod
    def is_ulbmp(filename: str) -> bool:
        with open(filename, 'rb') as f:
            header = f.read(6)
            return header == b'ULBMP\x01' or header == b'ULBMP\x02'
    
    @classmethod
    def create_from_pixels(cls, pixels: List[Pixel], ulbmp_version: int = 1) -> 'Encoder':
        width = height = int(len(pixels) ** 0.5)
        print("width ", width)
        print("height  ",height)
        img = Image(width, height, pixels)
        return cls(img, ulbmp_version)


class Decoder:
    @staticmethod
    def load_from(path: str) -> Image:
        with open(path, 'rb') as f:
            header = f.read(12) 
            print("Header:", header)
            width = int.from_bytes(header[6:8], 'little')
            height = int.from_bytes(header[8:10], 'little')
            print("Width:", width)
            print("Height:", height)
            pixels = []
            for _ in range(width * height):
                try:
                    red, green, blue = f.read(3)
                    pixels.append(Pixel(red, green, blue))
                except ValueError as e:
                    print("Error while reading pixel data:", e)
                    break  # Stop reading when there are not enough bytes left
        print("Number of pixels read:", len(pixels))
        print("Expected number of pixels:", width * height)
        return Image(width, height, pixels)


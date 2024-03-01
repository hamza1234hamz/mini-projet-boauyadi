# image.py
from pixel import Pixel

class Image:
    def __init__(self, width: int, height: int, pixels: list[Pixel]):
        if len(pixels) != width * height:
            print("pixels:",len(pixels))
            raise ValueError("Le nombre de pixels ne correspond pas aux dimensions de l'image.")
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers")
        if not all(isinstance(pixel, Pixel) for pixel in pixels):
            raise TypeError("All elements in pixels must be Pixel objects")
        
        self.width = width
        self.height = height
        self.pixels = pixels


    def __getitem__(self, pos: tuple[int,int]) -> Pixel:
        x, y = pos
        if not (0 <= x <= self.width and 0 <= y <= self.height):
            raise IndexError("Position de pixel invalide.")
        return self.pixels[y * self.width + x]

    def __setitem__(self, pos: tuple[int,int], pix: Pixel) -> None:
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Position de pixel invalide.")
        self.pixels[y * self.width + x] = pix

    def __eq__(self, other: 'Image') -> bool:
        if self.width != other.width or self.height != other.height:
            return False
        return all(pix1 == pix2 for pix1, pix2 in zip(self.pixels, other.pixels))



# b'ULBMP\x01\x0c\x00\x04\x00\x04\x00'
# b'ULBMP\x01\x0c\x00\x04\x00\x04\x00'
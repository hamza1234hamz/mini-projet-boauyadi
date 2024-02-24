# createimage.py
from encoding import Encoder
from pixel import Pixel

def create_ulbmp(filename: str):
    # Création des pixels de l'image de test
    pixels = [
        Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0),
        Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255),
        Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0),
        Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)
    ]
    
    # Création de l'encodeur ULBMP
    encoder = Encoder.create_from_pixels(pixels)
    
    # Enregistrement de l'image ULBMP
    encoder.save_to(filename)

if __name__ == "__main__":
    create_ulbmp("test_image.png")

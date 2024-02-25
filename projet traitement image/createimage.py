from encoding import Encoder
from pixel import Pixel

def create_ulbmp(filename: str):
    
    # Create pixels for the image with a simple pattern (4x4 pixels)
    pixels = [
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)],
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)],
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)],
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)],
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)],
        [Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0)],
        [Pixel(0, 0, 0), Pixel(255, 255, 255), Pixel(0, 0, 0), Pixel(255, 255, 255)]
        
    ]
    
    # Création de l'encodeur ULBMP
    encoder = Encoder.create_from_pixels(pixels)
    
    # Save the ULBMP image
    encoder.save_to(filename)

if __name__ == "__main__":
    create_ulbmp("test_image.ulbmp")

from encoding import Encoder
from pixel import Pixel

def create_ulbmp(filename: str):
    
    # Create pixels for the image with a simple pattern (4x4 pixels)
    pixels = []
    for i in range(640):
            row = []
            for j in range(480):
                if (i // 60) % 2 == (j // 80) % 2:
                    row.append(Pixel(0, 0, 0))  # Black pixel
                else:
                    row.append(Pixel(255, 255, 255))  # White pixel
            pixels.append(row)

    print(len(pixels))
    
    # Création de l'encodeur ULBMP
    encoder = Encoder.create_from_pixels(pixels)
    
    # Save the ULBMP image
    encoder.save_to(filename)

if __name__ == "__main__":
    create_ulbmp("test_image.ulbmp")

from encoding import Encoder
from pixel import Pixel

def create_ulbmp(filename: str):
    
    # Create pixels for the image with a simple pattern
    pixels = [
        [Pixel(255, 0, 0), Pixel(0, 255, 0), Pixel(0, 0, 255), Pixel(255, 255, 255)],
        [Pixel(255, 0, 0), Pixel(0, 255, 0), Pixel(0, 0, 255), Pixel(255, 255, 255)],
        [Pixel(255, 0, 0), Pixel(0, 255, 0), Pixel(0, 0, 255), Pixel(255, 255, 255)],
        [Pixel(255, 0, 0), Pixel(0, 255, 0), Pixel(0, 0, 255), Pixel(255, 255, 255)],
    ]
     # Print the generated pixels
    for i, pixel in enumerate(pixels):
        print(f"Pixel {i}: {pixel}")
    
    # Create the ULBMP encoder
    encoder = Encoder.create_from_pixels(pixels)
    
    # Save the ULBMP image
    encoder.save_to(filename)

if __name__ == "__main__":
    create_ulbmp("test_image.ulbmp")


    ''' # Generate ULBMP image data
    ulbmp_header = b'\x55\x4c\x42\x4d\x50\x01\x0c\x00\x02\x00\x02\x00'
    pixel_data = b'\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\xff\xff\xff'

    # Write data to a file
    with open("example.ulbmp", "wb") as file:
        file.write(ulbmp_header)
        file.write(pixel_data)
'''
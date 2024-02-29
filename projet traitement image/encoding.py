# encoding.py
from image import Image
from pixel import Pixel
from typing import List

from collections import defaultdict
from typing import Tuple



# encoding.py
class Encoder:
    ### updated for ulpmb v3
    def __init__(self, img: Image, ulbmp_version: int = 1, **kwargs):
        if ulbmp_version not in (1, 2, 3):
            raise ValueError("ULBMP version must be either 1, 2 or 3")
        self._img = img
        self._ulbmp_version = ulbmp_version
        self._depth = kwargs.get("depth", 1)
        self._rle = kwargs.get("rle", False)

        
    ### updated for ulpmb v3
    def save_to(self, path: str):
        if self._ulbmp_version == 1:
            self._save_ulbmp_v1(path)
        elif self._ulbmp_version == 2:
            self._save_ulbmp_v2(path)
        elif self._ulbmp_version == 3:
            self._save_ulbmp_v3(path)

    def _save_ulbmp_v1(self, path: str):
        header_length = 12 
        header = b'ULBMP\x01' + \
                 header_length.to_bytes(2, 'little') + \
                 self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        #header = b'ULBMP\x01\x0c\x00' + self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        print("header ",header)
        with open(path, 'wb') as f:
            f.write(header)
            #print(self._img.pixels)
            for row in self._img.pixels : 
                f.write(bytes(row))
                #for pixel in row:
                    #f.write(bytes([pixel._red, pixel._green, pixel._blue]))
               

    def _save_ulbmp_v2(self, path: str):
        header = b'ULBMP\x02' + \
                len(b'ULBMP\x02\x00\x00\x00\x00\x00\x00').to_bytes(2, 'little') + \
                self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little')
        with open(path, 'wb') as f:
            f.write(header)
            current_pixel = self._img[0, 0]
            count = 0
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
        print("header ",header)

    ### aded for ulpmb v3
    def _save_ulbmp_v3(self, path: str):
        header_length = 14
        header = b'ULBMP\x03' + \
                header_length.to_bytes(2, 'little') + \
                self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little') + \
                self._depth.to_bytes(1, 'little') + \
                (b'\x01' if self._rle else b'\x00') + \
                self._get_palette_bytes()

        with open(path, 'wb') as f:
            f.write(header)
            f.write(Encoder.encode_pixels(self._img, self._depth, self._palette))


    def get_unique_colors(image):
        # Initialize a dictionary to store the count of each color
        color_counts = defaultdict(int)

        # Iterate through each pixel in the image
        width, height = image.size
        for x in range(width):
            for y in range(height):
                # Get the RGB value of the pixel
                pixel = image.getpixel((x, y))
                # Increment the count for this color
                color_counts[pixel] += 1

        # Extract unique colors from the dictionary keys
        unique_colors = list(color_counts.keys())
        
        return unique_colors

    def _get_palette_bytes(self) -> bytes:
        if self._depth == 24:
            # Profondeur de couleur 24 bits par pixel
            return b''
        elif self._depth in [1, 2, 4, 8]:
            # Profondeur de couleur inférieure à 24 bits par pixel
            palette_size = 2 ** self._depth
            # Liste des couleurs uniques dans l'image
            unique_colors = self.get_unique_colors(self._img)
            # Vérifier que le nombre de couleurs uniques ne dépasse pas la taille de la palette
            if len(unique_colors) > palette_size:
                raise ValueError("Nombre de couleurs uniques dépasse la taille de la palette")
            
            # Créer la palette en associant chaque couleur à un encodage spécifique
            palette = b''
            for color in unique_colors:
                # Ajouter la couleur RVB à la palette
                palette += bytes(color)  # Supposons que la couleur est une liste [red, green, blue]

            return palette
        else:
            raise ValueError("Profondeur de couleur non prise en charge")

    

                    

## mn hna 18:43   ###########################################################################################################################
    def encode_rle(image: Image, palette: List[Tuple[int, int, int]]) -> bytes:
        encoded_pixels = []

        current_pixel = None
        run_length = 0

        for pixel in image:
            if pixel == current_pixel:
                run_length += 1
                if run_length == 256:
                    encoded_pixels.extend([255, current_pixel[0], current_pixel[1], current_pixel[2]])
                    run_length = 0
            else:
                if run_length > 0:
                    encoded_pixels.extend([run_length - 1, current_pixel[0], current_pixel[1], current_pixel[2]])
                current_pixel = pixel
                run_length = 1

        if run_length > 0:
            encoded_pixels.extend([run_length - 1, current_pixel[0], current_pixel[1], current_pixel[2]])

        return bytes(encoded_pixels)


    def encode_non_rle(image: Image, depth: int, palette: List[Tuple[int, int, int]]) -> bytes:
        encoded_pixels = []
        bits_per_pixel = 8 // depth

        current_byte = 0
        current_bit_index = 0

        for pixel in image:
            color_index = palette.index(pixel)
            current_byte = (current_byte << bits_per_pixel) | color_index
            current_bit_index += bits_per_pixel

            if current_bit_index >= 8:
                encoded_pixels.append(current_byte)
                current_byte = 0
                current_bit_index = 0

        if current_bit_index > 0:
            current_byte = current_byte << (8 - current_bit_index)
            encoded_pixels.append(current_byte)

        return bytes(encoded_pixels)

    
    
    
    def encode_pixels(image: Image, depth: int, palette: List[Tuple[int, int, int]]) -> bytes:
        # Vérifier si la profondeur est prise en charge
        if depth not in [1, 2, 4, 8, 24]:
            raise ValueError("Profondeur de couleur non prise en charge")

        # Si la profondeur est 24 bits par pixel, utiliser l'encodage RLE
        if depth == 24:
            return Encoder.encode_rle(image, palette)

        # Si la profondeur est 8 bits par pixel, utiliser l'encodage RLE
        if depth == 8:
            return Encoder.encode_rle(image, palette)

        # Si la profondeur est 1, 2 ou 4 bits par pixel, utiliser l'encodage sans compression
        return Encoder.encode_non_rle(image, depth, palette)



                    
                    
                    
                    
                
   



    @staticmethod
    def is_ulbmp(filename: str) -> bool:
        with open(filename, 'rb') as f:
            header = f.read(6)
            return header == b'ULBMP\x01' or header == b'ULBMP\x02'
    
    @classmethod
    def create_from_pixels(cls, pixels: List[Pixel], ulbmp_version: int = 1) -> 'Encoder':
        width = height = int(len(pixels) ** 0.5)
        #width = len(pixels)
        #height = len(pixels[0])
        print("width ", width)
        print("height  ",height)
        img = Image(width, height, pixels)
        return cls(img, ulbmp_version)




#####################################################

class Decoder:
    def __init__(self, path: str):
        self._path = path
        self._f = open(path, 'rb')
        self._header = self._read_header()
        self._width, self._height, self._depth, self._rle = self._parse_header()

    def _read_header(self) -> bytes:
        header_length = int.from_bytes(self._f.read(2), 'little')
        return self._f.read(header_length)

    def _parse_header(self) -> Tuple[int, int, int, bool]:
        ulbmp_version = self._header[:5]
        assert ulbmp_version == b'ULBMP\x03', "Invalid ULBMP version"
        width = int.from_bytes(self._header[5:7], 'little')
        height = int.from_bytes(self._header[7:9], 'little')
        depth = int.from_bytes(self._header[9:10], 'little')
        rle = bool(self._header[10])
        return width, height, depth, rle

    def _get_palette_bytes(self) -> bytes:
        if self._depth == 24:
            return b''
        elif self._depth in [1, 2, 4, 8]:
            palette_size = 2 ** self._depth
            palette_entry_bits = 24 if self._depth != 1 else 1
            total_palette_bits = palette_size * palette_entry_bits
            total_palette_bytes = (total_palette_bits + 7) // 8
            palette_data = self._f.read(total_palette_bytes)
            return palette_data
        else:
            raise ValueError("Profondeur de couleur non prise en charge")

    def decode_pixels_from_file(self) -> List[Pixel]:
        if self._rle:
            return self._decode_rle_pixels()
        else:
            return self._decode_non_rle_pixels()

    def _decode_rle_pixels(self) -> List[Pixel]:
            decoded_pixels = []
            remaining_pixels = self._width * self._height
            while remaining_pixels > 0:
                run_length = self._f.read(1)[0]
                pixel_data = self._f.read(3)
                pixel = Pixel(*pixel_data)
                decoded_pixels.extend([pixel] * (run_length + 1))
                remaining_pixels -= (run_length + 1)
            return decoded_pixels

    def _decode_non_rle_pixels(self) -> List[Pixel]:
        decoded_pixels = []
        bits_per_pixel = 8 // self._depth
        palette = self._get_palette()
        for _ in range(self._width * self._height):
            byte = self._f.read(1)[0]
            for _ in range(bits_per_pixel):
                index = (byte >> (8 - bits_per_pixel)) & ((1 << bits_per_pixel) - 1)
                pixel = palette[index]
                decoded_pixels.append(pixel)
                byte <<= bits_per_pixel
        return decoded_pixels


    def decode_image(self) -> Image:
        pixels = self.decode_pixels_from_file()
        image = Image.new('RGB', (self._width, self._height))
        image.putdata(pixels)
        return image

    @staticmethod
    def load_from(path: str) -> Image:
        decoder = Decoder(path)
        return decoder.decode_image()
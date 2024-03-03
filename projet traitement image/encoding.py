# encoding.py
from image import Image
from pixel import Pixel
from typing import List

from collections import defaultdict
from typing import Tuple

class Encoder:
    ### updated for ulpmb v3
    def __init__(self, img: Image, ulbmp_version: int = 1, **kwargs):
        if ulbmp_version not in (1, 2, 3, 4):
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
        print("header encoder",header)
        with open(path, 'wb') as f:
            f.write(header)
            print(self._img.pixels)
            for row in self._img.pixels : 
                f.write(bytes(row))
               

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
        header_length = 6 + 2 + 2 + 2 + 1 + 1 + len(self._get_palette_bytes())
        header = b'ULBMP\x03' + \
                header_length.to_bytes(2, 'little') + \
                self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little') + \
                self._depth.to_bytes(1, 'little') + \
                (b'\x01' if self._rle else b'\x00') + \
                self._get_palette_bytes()

        with open(path, 'wb') as f:
            f.write(header)
            f.write(Encoder.encode_pixels(self._img, self._depth,self.get_unique_colors()))


    def get_unique_colors(self): 
        # Initialize a dictionary to store the count of each color
        color_counts = defaultdict(int)

        # Iterate through each pixel in the image
        width, height = self._img.width, self._img.height
        for x in range(width):
            for y in range(height):
                # Get the RGB value of the pixel
                pixel = self._img[x, y]
                # Increment the count for this color
                color_counts[pixel] += 1
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
            unique_colors = self.get_unique_colors()
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

        for y in range(image.height):
            for x in range(image.width):
                pixel = image[x, y]
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

    
    
    def encode_pixels(self, depth: int, palette: List[Tuple[int, int, int]]) -> bytes:
        # Vérifier si la profondeur est prise en charge
        if depth not in [1, 2, 4, 8, 24]:
            raise ValueError("Profondeur de couleur non prise en charge")

        # Si la profondeur est 24 bits par pixel, utiliser l'encodage RLE
        if depth == 24:
            return Encoder.encode_rle(self, palette)

        # Si la profondeur est 8 bits par pixel, utiliser l'encodage RLE
        if depth == 8:
            return Encoder.encode_rle(self, palette)

        # Si la profondeur est 1, 2 ou 4 bits par pixel, utiliser l'encodage sans compression
        return Encoder.encode_non_rle(self, depth, palette)

    @staticmethod
    def is_ulbmp(filename: str) -> bool:
        with open(filename, 'rb') as f:
            header = f.read(6)
            return header == b'ULBMP\x01' or header == b'ULBMP\x02' or header == b'ULBMP\x03'
    
    @classmethod
    def create_from_pixels(cls, pixels: List[Pixel], ulbmp_version: int = 1) -> 'Encoder':
        width = height = int(len(pixels) ** 0.5)
        print("width ", width)
        print("height  ",height)
        img = Image(width, height, pixels)
        return cls(img, ulbmp_version)

################### DECODER ##################################

class Decoder:
    def __init__(self, path: str):
        self._path = path
        self._depth = None
        self._f = open(path, 'rb')
        self._ulbmp_version = self._f.read(6)
       
        self._header = self._read_header()
        self._width, self._height, self._depth, self._rle = self._parse_header()

    def _read_header(self) -> bytes:
        return self._f.read()

    def _parse_header(self) -> Tuple[int, int, int, bool , bytes]:
        ulbmp_version = self._ulbmp_version
        print("ulbmp_version ",ulbmp_version) 
        print("header ",self._header) 
        ##############################################################################
        if ulbmp_version == b'ULBMP\x01':
            width = int.from_bytes(self._header[2:4], 'little')
            height = int.from_bytes(self._header[4:6], 'little')
            #print("width ",width)
            #print("height ",height)
            depth = 24 
            rle = False
            return width, height, depth, rle
        #################################################################################
        elif ulbmp_version == b'ULBMP\x02':
            width = int.from_bytes(self._header[5:7], 'little')
            height = int.from_bytes(self._header[7:9], 'little')
            depth = 24
            rle = True
            return width, height, depth, rle
        ##################################################################################
        elif ulbmp_version == b'ULBMP\x03':
            width = int.from_bytes(self._header[2:4], 'little')
            height = int.from_bytes(self._header[4:6], 'little')
            depth = int.from_bytes(self._header[6:7], 'little')
            print("depth ",depth)
            print("width ",width)
            print("height ",height)
            rle = bool(self._header[9])
            return width, height, depth, rle
        else:
            raise ValueError("Invalid ULBMP version")

    def _get_palette_bytes(self, unique_colors: List[Pixel]) -> bytes:
        if self._depth == 24:
            return b''  # For 24-bit depth, no palette is needed

        elif self._depth in [1, 2, 4, 8]:
            palette_size = 2 ** self._depth
            if len(unique_colors) > palette_size:
                raise ValueError("Number of unique colors exceeds palette size")
            palette = b''
            for color in unique_colors:
                # Append RGB values of each color to the palette
                palette += bytes(color)

            # Pad the palette with black if necessary to reach the palette size
            while len(palette) < 3 * palette_size:
                palette += b'\x00\x00\x00'

            return palette
        else:
            raise ValueError("Unsupported color depth")


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
        if self._depth == 24: # 24 bits per pixel (ULBMP v1 and v2)
            print("header non rle ", self._header)
            i=6
            j=9
            for _ in range(self._width * self._height):
                pixel_data = self._header[i:j] # Read 3 bytes for the RGB values  
                print("pixel_data ",pixel_data)
                if len(pixel_data) != 3:
                    raise ValueError("Expected 3 bytes for pixel data, got {}: {}".format(len(pixel_data), pixel_data))
                pixel = Pixel(*pixel_data)
                decoded_pixels.append(pixel)
                i+=3
                j += 3
        else:
            bits_pixel = 8 // self._depth
            palette = self._get_palette_bytes(get_unique_colors(self.decode_pixels_from_file()))
            print("bits per pixel" , bits_pixel)
            current_byte = 0
            current_bit_index = 0
            for _ in range(self._width * self._height):
                if current_bit_index == 0:
                    current_byte = int.from_bytes(self._f.read(1), byteorder='big')
                index = (current_byte >> (8 - bits_pixel)) & ((1 << bits_pixel) - 1)
                current_byte <<= bits_pixel
                current_bit_index += bits_pixel
                if current_bit_index >= 8:
                    current_bit_index = 0
                decoded_pixels.append(palette[index])
        return decoded_pixels


    def decode_image(self) -> Image:
        pixels = self.decode_pixels_from_file()
        image = Image(self._width, self._height, pixels)
        image.pixels = pixels
        return image

    @staticmethod
    def load_from(path: str) -> Image:
        decoder = Decoder(path)
        return decoder.decode_image()
    

def get_unique_colors(decoded_pixels: List[Pixel]) -> List[Pixel]:
    color_counts = defaultdict(int)
    for pixel in decoded_pixels:
        color_counts[pixel] += 1

    unique_colors = list(color_counts.keys())
    return unique_colors
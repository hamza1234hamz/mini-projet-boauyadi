# encoding.py
from image import Image
from pixel import Pixel
from typing import List
from typing import Optional


# encoding.py
class Encoder:
    ### updated for ulpmb v3
    def __init__(self, image: Image, version: int=1, **kwargs):
        if version not in (1, 2, 3):
            raise ValueError("ULBMP version must be either 1, 2, or 3")
        self._img = image
        self._ulbmp_version = version
        self._depth = kwargs.get('depth', None)
        self._rle = kwargs.get('rle', False)
        self._palette = kwargs.get('palette', None)
        self._palette = kwargs.get('palette', None)  
    
        if version == 3 and (self._depth is None or self._rle is None):
            raise ValueError("Both depth and rle must be specified for ULBMP version 3 encoding")
        

        
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
        header = b'ULBMP\x03' + \
                 len(b'ULBMP\x03\x00\x00\x00\x00\x00\x00\x00').to_bytes(2, 'little') + \
                 self._img.width.to_bytes(2, 'little') + self._img.height.to_bytes(2, 'little') + \
                 self._depth.to_bytes(1, 'little') + int(self._rle).to_bytes(1, 'little')
        with open(path, 'wb') as f:
            f.write(header)
            f.write(self._encode_pixels())
            
            
    ### aded for ulpmb v3
    def _encode_pixels(self) -> bytes:
        encoded_data = bytearray()
    # Loop through each pixel in the image
        for y in range(self._img.height):
            for x in range(self._img.width):
                pixel = self._img[x, y]
                # Encode pixel color components based on depth
                if self._depth == 1:  # 1 bit per color component
                    encoded_data.append((pixel.red << 2) | (pixel.green << 1) | pixel.blue)
                elif self._depth == 2:  # 2 bits per color component
                    encoded_data.append((pixel.red << 4) | (pixel.green << 2) | pixel.blue)
                elif self._depth == 4:  # 4 bits per color component
                    encoded_data.append((pixel.red << 4) | pixel.green)
                    encoded_data.append((pixel.blue << 4) | pixel.alpha)  # Assuming alpha channel for 4-bit depth
                else:
                    raise ValueError("Unsupported depth for encoding")

        if self._rle:
            # Apply Run-Length Encoding if enabled
            encoded_data = self._apply_rle(encoded_data)

        return bytes(encoded_data)
    
    ### added for ulpmb v3
    def _apply_rle(self, data: bytearray) -> bytearray:
        compressed_data = bytearray()
        count = 1
        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                count += 1
            else:
                compressed_data.append(count)
                compressed_data.append(data[i - 1])
                count = 1
        compressed_data.append(count)
        compressed_data.append(data[-1])
        return compressed_data


    @classmethod
    def from_bytes(cls, data: bytes) :
        if data[:6] != b'ULBMP\x01' and data[:6] != b'ULBMP\x02' and data[:6] != b'ULBMP\x03':
            raise ValueError("Invalid ULBMP header")
        
        version = int(data[5])
        width = int.from_bytes(data[8:10], 'little')
        height = int.from_bytes(data[10:12], 'little')
        depth = int(data[12])
        rle = bool(data[13])

        palette_data = None
        if version == 3:
            palette_length = int.from_bytes(data[14:16], 'little')
            palette_data = data[16:16 + palette_length]

        return cls(version, width, height, depth, rle, palette_data)

    def has_palette(self) -> bool:
        return self.palette_data is not None

    def get_palette(self) -> List[Pixel]:
        if self.palette_data is None:
            raise ValueError("No palette data available")
        
        palette = []
        for i in range(0, len(self.palette_data), 3):
            red, green, blue = self.palette_data[i:i+3]
            palette.append(Pixel(red, green, blue))
        return palette


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


class Decoder:
    @staticmethod
    def load_from(path: str) -> Image:
        with open(path, 'rb') as f:
            header = f.read(12) 
            if header[:6] != b'ULBMP\x01' and header[:6] != b'ULBMP\x02':
                raise ValueError("Invalid ULBMP header")
            elif header[:6] == b'ULBMP\x01':
                print("Header:", header)
                width = int.from_bytes(header[8:10], 'little')
                height = int.from_bytes(header[10:], 'little')   # b'ULBMP\x01\x0c\x00\x04\x00\x04\x00'
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
            elif header[:6] == b'ULBMP\x02':
                print("Header:", header)
                width = int.from_bytes(header[8:10], 'little')
                height = int.from_bytes(header[10:], 'little')
                print("Width:", width)
                print("Height:", height)
                pixels = []
                current_pixel = Pixel(*f.read(3))
                while len(pixels) < width * height:
                    count = int.from_bytes(f.read(1), 'little')
                    pixels.extend([current_pixel] * count)
                    current_pixel = Pixel(*f.read(3))
                print("Number of pixels read:", len(pixels))
                print("Expected number of pixels:", width * height)
                return Image(width, height, pixels)
            
            elif header[:6] == b'ULBMP\x03':
                width = int.from_bytes(header[8:10], 'little')
                height = int.from_bytes(header[10:12], 'little')
                depth = header[12]
                rle = header[13] == 0x01
                # Read palette (not implemented here)
                # Read pixels and decode them
                pixels = f.read()
                image = Decoder._decode_ulbmp_v3(width, height, depth, rle, None, pixels)
                return image
            
    
    @staticmethod
    def _decode_ulbmp_v3(width: int, height: int, depth: int, rle: bool, palette_data: Optional[bytes], pixel_data: bytes) -> Image:
        pass
                 
            
             
 





class Pixel:
####
    def __init__(self, red, green, blue):
        if any(c < 0 for c in (red, green, blue)):
            raise ValueError("Les valeurs de red, green et blue ne peuvent pas être négatives")
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self):
        return self._red

    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue
    
    
    def __bytes__(self):
        return bytes([self.red, self.green, self.blue])

    def __eq__(self, other):
        if isinstance(other, Pixel):
            return self.red == other.red and self.green == other.green and self.blue == other.blue
        return False
    
    def __hash__(self):
        return hash((self._red, self._green, self._blue))

####
    @blue.setter
    def blue(self, value):
        self._blue = value
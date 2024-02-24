from PIL import Image

# Définir la taille de l'image
width = 640
height = 480

# Créer une nouvelle image
image = Image.new("RGB", (width, height))

# Définir les couleurs
black = (0, 0, 0)
white = (255, 255, 255)

# Parcourir les pixels
for x in range(width):
    for y in range(height):
        # Déterminer la couleur du pixel
        if (x // 16) % 2 == (y // 16) % 2:
            color = black
        else:
            color = white

        # Définir la couleur du pixel
        image.putpixel((x, y), color)

# Enregistrer l'image
image.save("checkers.png")


from PySide6 import QtCore, QtGui, QtWidgets 
from encoding import Decoder, Encoder


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialisation des widgets
        self.load_image_button = QtWidgets.QPushButton("Load Image")
        self.canvas = QtWidgets.QGraphicsView()
        self.save_image_button = QtWidgets.QPushButton("Save Image")
        self.save_image_button.setEnabled(False)

        # Mise en page
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.load_image_button)
        self.main_layout.addWidget(self.save_image_button)

        # Définition de la fenêtre principale
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Connexions des signaux et slots
        self.load_image_button.clicked.connect(self.load_image)
        self.save_image_button.clicked.connect(self.save_image)

        # Ajouter du style à la fenêtre
        self.setStyleSheet("background-color: black;")

        # Ajuster la taille de la fenêtre
        self.resize(800, 600)

    def load_image(self):
        # Ouvrir une boîte de dialogue de sélection de fichier
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "All Files (*)")
        if filename:
            # Vérifier si le fichier est au format ULBMP
            if not Encoder.is_ulbmp(filename):
                QtWidgets.QMessageBox.critical(self, "Error", "Missing format ULBMP")
                return

            try:
                # Charger l'image à partir du fichier ULBMP
                image = Decoder.load_from(filename)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", str(e))
                return

            # Convertir l'objet image en pixmap
            pixmap = QtGui.QPixmap(image.width, image.height)
            painter = QtGui.QPainter(pixmap)
            for x in range(image.width):
                for y in range(image.height):
                    pixel = image[x, y]
                    color = QtGui.QColor(pixel.red, pixel.green, pixel.blue)
                    painter.setPen(color)
                    painter.drawPoint(x, y)
            painter.end()

            # Créer un label pour afficher l'image
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)

            # Ajouter le label à la mise en page principale
            self.main_layout.addWidget(label)

            # Redimensionner la fenêtre
            self.resize(image.width, image.height)

            # Mettre à jour self.image
            self.image = image

            # Activer le bouton de sauvegarde
            self.save_image_button.setEnabled(True)

    def save_image(self):
        # Vérifier si self.image est défini
        if not hasattr(self, 'image') or self.image is None:
            QtWidgets.QMessageBox.critical(self, "Error", "No image loaded")
            
        # Demander à l'utilisateur la version du format ULBMP
        version, ok = QtWidgets.QInputDialog.getInt(self, "Save Image", "Enter ULBMP version (1 or 2):", 1, 1, 2)
        if ok:
            # Demander à l'utilisateur le nom du fichier de sauvegarde
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "ULBMP Files (*.ulbmp)")
            if filename:
                # Enregistrer l'image avec la version spécifiée du format ULBMP
                
                encoder = Encoder(self.image, version)
                encoder.save_to(filename)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

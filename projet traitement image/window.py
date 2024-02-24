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
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addWidget(self.save_image_button)

        # Définition de la fenêtre principale
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Connexions des signaux et slots
        self.load_image_button.clicked.connect(self.load_image)
        self.save_image_button.clicked.connect(self.save_image)

    def load_image(self):
        # Ouvrir une boîte de dialogue de sélection de fichier
       # filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "ULBMP Files (*.ulbmp)")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "All Files (*)")

        if filename:
            if not Encoder.is_ulbmp(filename):
                # Afficher un message d'erreur si le format n'est pas ULBMP
                QtWidgets.QMessageBox.critical(self, "Error", "Missing format ULBMP")
                return

            

        # Vérifier si le fichier est valide
        try:
            image = Decoder.load_from(filename)
        except Exception as e:
            # Afficher une boîte de dialogue d'erreur
            error_message = QtWidgets.QErrorMessage()
            error_message.showMessage(str(e))
            return

        # Convertir l'objet image en pixmap
        pixmap = QtGui.QPixmap.fromImage(image)

        # Créer un label pour afficher l'image
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)

        # Créer un widget de défilement pour afficher l'image
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(label)

        # Ajouter le widget de défilement à la mise en page principale
        self.main_layout.addWidget(scroll_area)

        # Redimensionner la fenêtre
        self.resize(image.width(), image.height())

        # Activer le bouton de sauvegarde
        self.save_image_button.setEnabled(True)

    def save_image(self):
        # Fonction de sauvegarde de l'image
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

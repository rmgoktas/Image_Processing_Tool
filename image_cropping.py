import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt  # Qt sınıfını burada içe aktarıyoruz





class ImageCropper(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.cropped_image = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Cropper")
        self.setGeometry(100, 100, 400, 300)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.crop_button = QPushButton("Crop", self)
        self.crop_button.clicked.connect(self.crop_image)

        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.crop_button)
        self.setLayout(layout)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaledToWidth(300))

    def crop_image(self):
        if self.image_path:
            image = cv2.imread(self.image_path)
            roi = cv2.selectROI("Select ROI", image)
            if roi[2] and roi[3]:
                self.cropped_image = image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
                cv2.imshow("Cropped Image", self.cropped_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec_())

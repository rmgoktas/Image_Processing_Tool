import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageCropper(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.image = None
        self.cropped_image = None
        self.roi_start = None
        self.roi_end = None
        self.selecting = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Cropper")
        self.setGeometry(100, 100, 800, 600)

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
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            self.image_path = file_name
            self.image = cv2.imread(self.image_path)
            self.display_image()

    def display_image(self):
        if self.image is not None:
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def crop_image(self):
        if self.image is not None:
            cv2.namedWindow("Select ROI")
            cv2.setMouseCallback("Select ROI", self.mouse_callback)
            while True:
                temp_image = self.image.copy()
                if self.roi_start and self.roi_end:
                    cv2.rectangle(temp_image, self.roi_start, self.roi_end, (255, 0, 0), 2)
                cv2.imshow("Select ROI", temp_image)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC key
                    break
                elif key == ord('c') and self.roi_start and self.roi_end:
                    x1, y1 = self.roi_start
                    x2, y2 = self.roi_end
                    self.cropped_image = self.image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
                    cv2.imshow("Cropped Image", self.cropped_image)
                    cv2.waitKey(0)
                    cv2.destroyWindow("Cropped Image")
            cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi_start = (x, y)
            self.selecting = True
        elif event == cv2.EVENT_MOUSEMOVE and self.selecting:
            self.roi_end = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.roi_end = (x, y)
            self.selecting = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    sys.exit(app.exec_())

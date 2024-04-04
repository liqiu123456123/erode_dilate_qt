import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QImage, QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import cv2
import numpy as np


class ImageDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.resize(820, 620)

        self.open_button = QPushButton('打开图片')
        self.open_button.clicked.connect(self.open_image)

        self.img_win = QWidget()
        img_win_layout = QHBoxLayout()
        orgin_layout = QVBoxLayout()
        img_layout = QVBoxLayout()
        self.img_win.setLayout(img_win_layout)

        self.orgin_img_label = QLabel()
        self.orgin_name = QLabel("原图")
        # 设置QLabel内部文本居中
        self.orgin_name.setAlignment(Qt.AlignCenter)
        # 将QLabel添加到布局中，并设置居中对齐
        orgin_layout.addWidget(self.orgin_img_label, alignment=Qt.AlignCenter)
        orgin_layout.addWidget(self.orgin_name, alignment=Qt.AlignCenter)
        self.image_label = QLabel()
        self.image_name = QLabel("处理后的图")
        self.image_name.setAlignment(Qt.AlignCenter)  # 设置QLabel内部文本居中
        img_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        img_layout.addWidget(self.image_name, alignment=Qt.AlignCenter)
        img_win_layout.addLayout(orgin_layout)
        img_win_layout.addLayout(img_layout)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.process_image)
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setMinimum(1)
        self.slider2.setMaximum(100)
        self.slider2.valueChanged.connect(self.process_image)
        self.slider_value_label = QLabel("矩形核大小: 0x0")
        self.slider_value_label2 = QLabel("腐蚀次数: 0")
        controls_layout = QHBoxLayout()
        self.kernal_label = QLabel("矩形核大小（kernel）:")
        controls_layout.addWidget(self.kernal_label)
        controls_layout.addWidget(self.slider)
        controls_layout.addWidget(self.slider_value_label)
        controls_layout2 = QHBoxLayout()
        self.iter_label = QLabel("腐蚀次数（iterations）:")
        controls_layout2.addWidget(self.iter_label)
        controls_layout2.addWidget(self.slider2)
        controls_layout2.addWidget(self.slider_value_label2)
        self.main_layout.addWidget(self.open_button)
        self.main_layout.addWidget(self.img_win)
        self.main_layout.addLayout(controls_layout)
        self.main_layout.addLayout(controls_layout2)
        self.setLayout(self.main_layout)
        self.setWindowTitle('腐蚀效果调试器')
        self.set_common_style(self.open_button)
        self.set_common_style(self.image_name)
        self.set_common_style(self.orgin_name)
        self.set_common_style(self.slider_value_label)
        self.set_common_style(self.slider_value_label2)
        self.set_common_style(self.kernal_label)
        self.set_common_style(self.iter_label)
        self.show()

    def set_common_style(self,label):
        label.setStyleSheet("""  
            QLabel {  
                font-family: '微软雅黑';  
                font-size: 12pt;  
                color: red;  
            }
                        QPushButton {  
                font-family: '微软雅黑';  
                font-size: 12pt;  
                color: red;  
            }  
        """)
    def open_image(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, '打开图片', '.', '图片文件 (*.png *.jpg *.jpeg *.bmp)')
        if self.filename:
            self.image = cv2.imread(self.filename)
            or_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, ch = or_img.shape
            bytes_per_line = ch * w
            q_img = QImage(or_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            if pixmap.width() > 600 or pixmap.height() > 600:
                pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.orgin_img_label.setPixmap(pixmap)
            self.process_image()

    def process_image(self):
        if self.image is None:
            return
        kernel_size = self.slider.value()
        iterations = self.slider2.value()
        self.slider_value_label.setText(f"矩形核大小: {kernel_size}x{kernel_size}")
        self.slider_value_label2.setText(f"腐蚀次数: {iterations}")
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
        processed_image = cv2.erode(self.image, kernel, iterations=iterations)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        h, w, ch = processed_image.shape
        bytes_per_line = ch * w
        q_img = QImage(processed_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        if pixmap.width() > 600 or pixmap.height() > 600:
            pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageDisplayWidget()
    sys.exit(app.exec_())

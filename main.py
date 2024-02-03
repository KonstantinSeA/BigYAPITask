from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import sys
import io
import os
from PyQt5 import uic


template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>586</width>
    <height>530</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Большая задача по Maps API</string>
  </property>
  <widget class="QLabel" name="map_label">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>30</y>
     <width>511</width>
     <height>431</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class MapApi(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = '0.002'
        self.coordinates = ['37.530887', '55.703118']
        self.delta_x, self.delta_y = 0, 0
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.get_image()
        self.initUI()

    def get_image(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join((str(float(self.coordinates[0]) + self.delta_x * 0.0001), str(float(self.coordinates[1]) + self.delta_y * 0.0001)))}&spn={self.scale},0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def initUI(self):
        pass

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.update_delta('up')
        if event.key() == Qt.Key_Left:
            self.update_delta('left')
        if event.key() == Qt.Key_Right:
            self.update_delta('right')
        if event.key() == Qt.Key_Down:
            self.update_delta('down')
        if event.key() == Qt.Key_PageUp:
            self.update_scale('up')
        if event.key() == Qt.Key_PageDown:
            self.update_scale('down')

    def update_delta(self, ori):
        if ori == 'up':
            self.delta_y += 10
        elif ori == 'left':
            self.delta_x -= 10
        elif ori == 'down':
            self.delta_y -= 10
        elif ori == 'right':
            self.delta_x += 10
        if self.delta_y > 100:
            self.delta_y -= 10
        elif self.delta_y < -100:
            self.delta_y += 10
        if self.delta_x > 100:
            self.delta_x -= 10
        elif self.delta_x < -100:
            self.delta_x += 10
        self.get_image()
        self.initUI()

    def update_scale(self, ori):
        '''if ori == 'up':
            self.scale_delta = str(float(self.scale) - 0.0001)
        elif ori == 'down':
            self.scale = str(float(self.scale) - 0.0001)'''
        print(self.scale)
        self.get_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApi()
    ex.show()
    sys.exit(app.exec())

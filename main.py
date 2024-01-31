from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
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


SCALE = '0.002'
COORDINATES = '37.530887,55.703118'


class MapApi(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.get_image()
        self.initUI()

    def get_image(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={COORDINATES}&spn={SCALE}" \
                      ",0.002&l=map"
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

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApi()
    ex.show()
    sys.exit(app.exec())

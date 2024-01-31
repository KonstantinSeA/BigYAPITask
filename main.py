from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import sys
import io
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
   <string>Form</string>
  </property>
  <widget class="QLabel" name="map_label">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>30</y>
     <width>511</width>
     <height>441</height>
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


SCALE = '0.02'


class MapApi(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApi()
    ex.show()
    sys.exit(app.exec())

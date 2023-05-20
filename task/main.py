# This is a sample Python script.
import os
import re
import sys
from PyQt5 import uic
from PyQt5 import sip
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPen
# from config import db
# from excel import ExcelSpec
import math


class CountAreaOfTentMenu(QMainWindow):
    # Главное меню
    def __init__(self, parent=None):
        super().__init__(parent)  # Call the inherited classes __init__ method
        uic.loadUi('ui/menu_cout_sq.ui', self)
        self.widget_6.hide()
        self.register = 1
        self.next_btn.clicked.connect(self.press_next_btn)
        self.back_btn.clicked.connect(self.press_back_btn)
        self.calcul_btn.clicked.connect(self.press_to_calc_btn)
        self.calcul_btn_2.clicked.connect(self.press_to_calc_btn)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView_2.setScene(self.scene)
        # Надписи внешнего тента
        self.text_height_full = self.scene.addText("Hнт")
        self.text_height_full.setPos(-30, 180)
        self.text_height_full.setRotation(270)
        self.text_height_wall = self.scene.addText("Hнc")
        self.text_height_wall.setPos(-5, 180)
        self.text_height_wall.setRotation(270)
        self.text_width = self.scene.addText("Wнc")
        self.text_width.setPos(80, 270)
        self.text_lenght = self.scene.addText("Lнc")
        self.text_lenght.setPos(250, 260)
        self.text_lenght.setRotation(360 - 21)
        # Надписи внутреннего тента
        self.text_height_full_2 = self.scene.addText("Hвт")
        self.text_height_full_2.setPos(-30, 180)
        self.text_height_full_2.setRotation(270)
        self.text_height_wall_2 = self.scene.addText("Hвc")
        self.text_height_wall_2.setPos(-5, 180)
        self.text_height_wall_2.setRotation(270)
        self.text_width_2 = self.scene.addText("Wвc")
        self.text_width_2.setPos(80, 270)
        self.text_lenght_2 = self.scene.addText("Lвc")
        self.text_lenght_2.setPos(250, 260)
        self.text_lenght_2.setRotation(360 - 21)
        # Прячем лишнее
        self.text_height_full_2.hide()
        self.text_height_wall_2.hide()
        self.text_lenght_2.hide()
        self.text_width_2.hide()
        self.outer_tent_draw()

    def outer_tent_draw(self):
        # Ручка основная
        black_pen_main = QPen(Qt.black)
        black_pen_main.setWidth(2)
        # Ручка для размеров
        green_pen_dobl = QPen(Qt.green)
        green_pen_dobl.setWidth(1)
        # Крыша тоца Ангара
        self.scene.addLine(100, 0, 15, 60, black_pen_main)  # Кырша правая линия
        self.scene.addLine(200, 60, 100, 0, black_pen_main)  # Кырша левая линия
        # Торец ангара
        self.scene.addLine(15, 60, 15, 270, black_pen_main)  # Торец левая линия
        self.scene.addLine(15, 270, 200, 270, black_pen_main)  # Торец нижняя линия
        self.scene.addLine(200, 60, 200, 270, black_pen_main)  # Торец правая линия
        self.scene.addLine(15, 60, 200, 60, black_pen_main)  # Торец верхня линия
        # Cтенка и крыша изометрия
        self.scene.addLine(200, -50, 100, 0, black_pen_main) # Линия конька
        self.scene.addLine(200, 60, 307, 0, black_pen_main)  # Линия разграничения крыши и стены
        self.scene.addLine(200, 270, 307, 230, black_pen_main)  # Линия стены нижняя
        self.scene.addLine(307, 0, 307, 230, black_pen_main)  # правая соед средню или нижнию линии
        self.scene.addLine(307, 0, 200, -50, black_pen_main)  # правая соед средню или верхнюю линии
        # Рамзерная линия
        self.scene.addLine(100, 0, -10, 0, green_pen_dobl)  # Линия размерная от конька
        self.scene.addLine(-10, 270, -10, 0, green_pen_dobl)  # Линия размерная вертикальная
        self.scene.addLine(-10, 270, 15, 270, green_pen_dobl)  # Линия размерная до основнания
        self.hight_full_doubleSpinBox.editingFinished.connect(self.set_height_full_text)
        self.hight_full_doubleSpinBox_2.editingFinished.connect(self.set_height_full_text)
        self.hight_wall_doubleSpinBox.editingFinished.connect(self.set_height_wall_text)
        self.hight_wall_doubleSpinBox_2.editingFinished.connect(self.set_height_wall_text)
        self.lenght_walldoubleSpinBox.editingFinished.connect(self.set_lenght_text)
        self.lenght_walldoubleSpinBox_2.editingFinished.connect(self.set_lenght_text)
        self.width_doubleSpinBox.editingFinished.connect(self.set_width_text)
        self.width_doubleSpinBox_2.editingFinished.connect(self.set_width_text)

    def set_height_full_text(self):
        if self.register == 1:
            self.text_height_full.setPlainText(str(self.hight_full_doubleSpinBox.value()))
        else:
            self.text_height_full_2.setPlainText(str(self.hight_full_doubleSpinBox_2.value()))

    def set_height_wall_text(self):
        if self.register == 1:
            self.text_height_wall.setPlainText(str(self.hight_wall_doubleSpinBox.value()))
        else:
            self.text_height_wall_2.setPlainText(str(self.hight_wall_doubleSpinBox_2.value()))

    def set_lenght_text(self):
        if self.register == 1:
            self.text_lenght.setPlainText(str(self.lenght_walldoubleSpinBox.value()))
        else:
            self.text_lenght_2.setPlainText(str(self.lenght_walldoubleSpinBox_2.value()))

    def set_width_text(self):
        if self.register == 1:
            self.text_width.setPlainText(str(self.width_doubleSpinBox.value()))
        else:
            self.text_width_2.setPlainText(str(self.width_doubleSpinBox_2.value()))

    def press_next_btn(self):
        self.register = 0
        self.text_height_full_2.show()
        self.text_height_wall_2.show()
        self.text_lenght_2.show()
        self.text_width_2.show()
        self.text_height_full.hide()
        self.text_height_wall.hide()
        self.text_lenght.hide()
        self.text_width.hide()
        self.widget_5.hide()
        self.widget_6.show()

    def press_back_btn(self):
        self.register = 1
        self.text_height_full.show()
        self.text_height_wall.show()
        self.text_lenght.show()
        self.text_width.show()
        self.text_height_full_2.hide()
        self.text_height_wall_2.hide()
        self.text_lenght_2.hide()
        self.text_width_2.hide()
        self.widget_6.hide()
        self.widget_5.show()

    def press_to_calc_btn(self):
        # Получаем данные о внешнем тенте
        # Высота конька(полная высота ангара) внешняя в м
        height_full_outer = self.hight_full_doubleSpinBox.value() / 1000
        height_wall_outer = self.hight_wall_doubleSpinBox.value() / 1000  # Высота стенки ангара внешняя в м
        lenght_wall_outer = self.lenght_walldoubleSpinBox.value() / 1000  # Длина ангара полная внешняя в м
        width_outer = self.width_doubleSpinBox.value() / 1000  # Ширина анагара полная внешняя в м
        # Расчет площади внешнего тентового полотна ангара
        inaccuracy = 150 / 1000
        # Площадь торца внешнего ангара
        outer_area_end_face = (height_wall_outer - inaccuracy) * (width_outer - inaccuracy * 2) \
                              + (height_full_outer - height_wall_outer - inaccuracy) * (width_outer - inaccuracy * 2) / 2
        # Площадь стены внешней ангара
        outer_area_wall = (lenght_wall_outer - inaccuracy * 2) * (height_wall_outer - inaccuracy * 2)
        # Площадь крыши внеш ангара
        tagle_hypotenuse = ((height_full_outer - height_wall_outer - inaccuracy) ** 2
                            + ((width_outer - inaccuracy * 2) / 2) ** 2) ** (1 / 2)
        outer_area_roof = tagle_hypotenuse * (lenght_wall_outer - inaccuracy * 2)
        # Итого общая площадь наружнего тента
        full_outer_area = round(outer_area_end_face * 2 + outer_area_wall * 2 + outer_area_roof * 2, 2)
        # Получаем данные о внутреннем тенте
        # Высота конька(полная высота ангара) внутренняя в м
        height_full_inside = self.hight_full_doubleSpinBox_2.value() / 1000
        height_wall_inside = self.hight_wall_doubleSpinBox_2.value() / 1000  # Высота стенки ангара внутр в м
        lenght_wall_inside = self.lenght_walldoubleSpinBox_2.value() / 1000  # Длина ангара полная внутр в м
        width_inside = self.width_doubleSpinBox_2.value() / 1000  # Ширина анагара полная внутр в м
        # Расчет площади внутреннего тентового полотна ангара
        # Площадь торца внутрен ангара
        inside_area_end_face = (height_wall_inside - inaccuracy) * (width_inside - inaccuracy * 2) \
                               + (height_full_inside - height_wall_inside - inaccuracy) \
                               * (width_inside - inaccuracy * 2) / 2
        # Площадь стены внутенней ангара
        inside_area_wall = (lenght_wall_inside - inaccuracy * 2) * (height_wall_inside - inaccuracy * 2)
        # Площадь крыши внутр ангара
        inside_tagle_hypotenuse = ((height_full_inside - height_wall_inside - inaccuracy) ** 2
                                   + ((width_inside - inaccuracy * 2) / 2) ** 2) ** (1 / 2)
        inside_area_roof = inside_tagle_hypotenuse * (lenght_wall_inside - inaccuracy * 2)
        # Итого общая площадь внутреннего тента
        full_inside_area = round(inside_area_end_face * 2 + inside_area_wall * 2 + inside_area_roof * 2, 2)
        # общая площадь ангара внутр и внешнего
        total_area = full_outer_area + full_inside_area
        # Выводим на дисплей
        # Наружний
        self.outer_area_tent_line.setPlaceholderText(str(full_outer_area))
        self.outer_area_tent_line_2.setPlaceholderText(str(full_outer_area))
        # Внутренний
        self.inside_area_tent_line.setPlaceholderText(str(full_inside_area))
        self.inside_area_tent_line_2.setPlaceholderText(str(full_inside_area))
        # Общая
        self.full_area_line.setPlaceholderText(str(total_area))
        self.full_area_line_2.setPlaceholderText(str(total_area))


def application():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/report.png'))
    MainWindow = CountAreaOfTentMenu()
    MainWindow.show()
    sys.exit(app.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    application()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import _ctypes
import os
import re
import sys

import pywintypes
import win32com.client
from PyQt5.QtCore import Qt
from win32com.client import VARIANT
import pythoncom
import xlsxwriter
from PyQt5 import uic
from PyQt5 import sip
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from pyautocad import APoint
import math
from pyautocad import Autocad
import images_store
from xlsxwriter.exceptions import FileCreateError
from export_to_excel import ExcelExport


class MainMenu(QMainWindow):
    # Главное меню
    def __init__(self, parent=None, flag=Qt.Window):
        super().__init__(parent, flag)  # Call the inherited classes __init__ method
        uic.loadUi('ui/calcul_menuv2.ui', self)
        self.acad = ""
        self.acadModel = ""
        self.MainWindow = ""
        self.comboBox.currentIndexChanged.connect(self.indexChanged)
        self.first_try = True
        self.status_Error = False
        self.load_menu(self.comboBox.currentText())
        self.batten_2g_height_doubleSpinBox_3.setValue(700.00)
        self.size_to_sl_doubleSpinBox.setValue(1.00)
        self.step_bw_sl_doubleSpinBox.setValue(1.00)
        self.main_data_for_spec = {}  # Словарь зависимость марка - словарь полуфабрикатов
        self.area_of_product = []
        self.check_the_autocad()

    def APoint(self, x, y, z=0):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))

    def aDouble(self, xyz):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, xyz)

    def aVariant(self, vObject):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, vObject)

    def indexChanged(self):
        choose_tp = self.comboBox.currentText()
        self.load_menu(choose_tp)

    def check_the_autocad(self):
        try:
            self.status_Error = False
            self.acad = win32com.client.Dispatch("AutoCAD.Application")
            self.acad.Visible = True
            self.acadModel = self.acad.ActiveDocument.ModelSpace
        except pywintypes.com_error:
            self.status_Error = True
            error = 'Чертежный вид в Автокаде (модель) не открыт! Откройте чертеж перед запуском раскроя!'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()

    def load_menu(self, choose_tp):
        if choose_tp == 'ТП-1' or choose_tp == 'ТП-2':
            # Скрываем меню для ТП-3
            self.tp_3_widget.hide()
            self.dop_infa_for_sl_tp3_widget.hide()
            # Показываекм меню для ТП-1
            self.tp_1_widget.show()
            self.quantity_spinBox.setValue(2)
            MainMenu.setMinimumSize(self, 624, 580)
            if self.first_try is False:
                self.secondlayout_checkBox.clicked.disconnect(self.show_the_dop_info_for_tp3)
                self.tp_pushButton.clicked.disconnect(self.draw_tp3_btn)
                self.first_try = True
            self.tp_pushButton.clicked.connect(self.count_and_drow_tp_btn)

        else:
            # Скрываем меню для ТП-1 и ТП-2
            MainMenu.setMinimumSize(self, 624, 720)
            self.tp_pushButton.clicked.disconnect(self.count_and_drow_tp_btn)
            self.tp_pushButton.clicked.connect(self.draw_tp3_btn)
            self.tp_1_widget.hide()
            self.first_try = False
            # Показываекм меню для ТП-3
            self.secondlayout_checkBox.setChecked(False)
            self.secondlayout_checkBox.clicked.connect(self.show_the_dop_info_for_tp3)
            self.tp_3_widget.show()

    def show_the_dop_info_for_tp3(self):
        if self.secondlayout_checkBox.isChecked():
            self.dop_infa_for_sl_tp3_widget.show()
        else:
            self.dop_infa_for_sl_tp3_widget.hide()

    def draw_a_tp_3(self):
        if self.status_Error is False:
            self.draw_tp3_btn()
        else:
            self.check_the_autocad()

    def count_and_drow_tp_btn(self):
        width_tp = self.width_doubleSpinBox_2.value()
        size_of_tp_width = width_tp - 150 * 2
        # расчет релеватности решения
        count_size_int_polotn_w = self.count_doubleSpinBox_2.value()
        relev = (size_of_tp_width + 130 * 2) / count_size_int_polotn_w
        if relev >= 100:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowIcon(QIcon("images/dop/attantion.png"))
            msg.setWindowTitle("Подтверждение раскроя")
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setIconPixmap(QPixmap("images/dop/attantion.png"))
            msg.setText(f"Вы точно уверены, что хотите рассчитать раскрой равный {count_size_int_polotn_w} мм?\n")
            msg.setFocus()
            msg.setStyleSheet("font: 75 12pt bold \"Times New Roman\";")
            button_aceptar = msg.addButton("Да", QtWidgets.QMessageBox.YesRole)
            button_cancelar = msg.addButton("Отменить", QtWidgets.QMessageBox.RejectRole)
            msg.setDefaultButton(button_aceptar)
            msg.exec_()
            if msg.clickedButton() == button_aceptar:
                if self.status_Error is False:
                    self.draw_and_count_the_polotno()
                else:
                    self.check_the_autocad()
        else:
            if self.status_Error is False:
                self.draw_and_count_the_polotno()
            else:
                self.check_the_autocad()

    def draw_and_count_the_polotno(self):
        type_of_tp = self.comboBox.currentText()
        main_num_of_tp = 1
        if type_of_tp == 'ТП-1':
            main_num_of_tp = 1
        elif type_of_tp == 'ТП-2':
            main_num_of_tp = 2
        # AutoCAD = win32com.client.Dispatch("AutoCAD.Application")
        acad = Autocad(create_if_not_exists=False)
        acad.Visible = True
        acadModel = acad.ActiveDocument.ModelSpace
        # acad = win32com.client.Dispatch("AutoCAD.Application")
        width_tp = self.width_doubleSpinBox_2.value()
        length_tp = self.length_doubleSpinBox_2.value()
        quantity = self.quantity_spinBox.value()
        size_of_tp_width = width_tp - 150 * 2
        size_of_tp_length = length_tp - 150 * 2
        size_of_batten_1v_width = 700
        size_of_batten_1v_length = size_of_tp_length
        size_of_batten_2g_width = 700
        size_of_batten_2g_length = size_of_tp_width - 110 * 2
        quantity_batten_1v = quantity * 2
        quantity_batten_1g = quantity
        quantity_of_tp12 = self.quantity_spinBox_tp2.value()
        general_size_tp1_1_w = size_of_tp_width + 550 * 2
        general_size_tp1_1_l = size_of_tp_length
        y_point_batten_2g_width = size_of_batten_2g_width
        x_point_batten_2g_length = size_of_batten_2g_length
        p_1 = 0.0
        p_2 = 0.0
        p_12 = 0.0
        p_13 = size_of_batten_1v_width
        p_for_text = general_size_tp1_1_w / 2 - 1000
        p_for_text_2 = general_size_tp1_1_l + 1500
        quantity_of_tp12 = self.quantity_spinBox_tp2.value()
        quantity_of_tp_common = [1, 2]
        dem_const = size_of_batten_1v_length
        # Размеры
        p_razmer_1 = -500.0
        p_razmer_2 = -100.0
        p_razmer_3 = 100.0
        p_razmer_4 = size_of_batten_1v_length + 1000
        p_razmer_5 = -100.0
        p_razmer_6 = -500
        # точки текста
        y_text_about_dop = - 1000
        y_size_of_polotna_l = size_of_tp_length + 130 * 2
        y_pocket_lenght = size_of_tp_width - 100 * 2
        x_pocket_in_main_pic = size_of_tp_width - 100 * 2
        p_y_pocket_in_main_pic = (size_of_batten_1v_length - 100) / 2
        y_batten_vertic = 0
        # Постоянные длинны
        add_lenght_of_second_layout = size_of_tp_length - 100 * 2
        add_size_of_polotna_l = size_of_tp_length + 130 * 2
        dem_const_batten_1v_length = size_of_batten_1v_length
        dem_const_batten_2g_length = size_of_batten_2g_length
        dem_const_pocket_length = y_pocket_lenght
        y_pocket_in_main_pic = 0
        if type_of_tp == 'ТП-1':
            y_batten_vertic = size_of_batten_1v_length
            y_pocket_in_main_pic = y_batten_vertic / 2 - 75
        elif type_of_tp == 'ТП-2':
            y_batten_vertic = size_of_batten_1v_length + 600
            y_pocket_in_main_pic = y_batten_vertic / 2 - 75
        for tp in quantity_of_tp_common:
            data_for_spec = {}  # Словарь зависимость полуфабрикат - его данные(кол-во, ширина, длинна)
            p_text = APoint(p_for_text, p_for_text_2)
            acadModel.AddText(f'Монтажный вид {type_of_tp}.{tp} - {quantity} шт (в сборе)', p_text, 100)
            # Чертим нащельник 1в
            if tp == 1:
                # Назначаем точки для нащельника 1в
                points_pocket = self.aDouble([p_1, p_2, p_12, y_batten_vertic, p_13, y_batten_vertic,
                                              p_13, p_2, p_1, p_2])
                self.acadModel.AddLightWeightPolyline(points_pocket)
            # Назначаем точки для полотная ТП 1.1
            p_polotno_x_1 = p_13 - 150
            p_polotno_y_1 = size_of_batten_1v_length
            p_polotno_x_2 = p_13 + size_of_tp_width - 150
            p_polotno_y_2 = size_of_batten_1v_length
            p_polotno_x_3 = p_13 + size_of_tp_width - 150
            p_polotno_y_3 = y_point_batten_2g_width - 150
            p_polotno_x_4 = p_13 - 150
            p_polotno_y_4 = y_point_batten_2g_width - 150
            points_polotno = self.aDouble([p_polotno_x_1, p_polotno_y_1, p_polotno_x_2, p_polotno_y_2,
                                           p_polotno_x_3, p_polotno_y_3, p_polotno_x_4, p_polotno_y_4,
                                           p_polotno_x_1, p_polotno_y_1])
            # Чертим полотно полилинией
            polotno_main_tp1_2 = self.acadModel.AddLightWeightPolyline(points_polotno)
            polotno_main_tp1_2.Offset(100)  # Строим подгиб полотна
            # Назначаем точки для нащельника 1г
            if tp == 1:
                size_of_batten_2g_x3_real = p_polotno_x_2 + 550
                p_batten_1g_x_1 = p_1
                p_batten_1g_y_1 = p_2
                p_batten_1g_x_2 = p_1
                p_batten_1g_y_2 = y_point_batten_2g_width
                p_batten_1g_x_3 = p_1 + size_of_batten_2g_x3_real
                p_batten_1g_y_3 = y_point_batten_2g_width
                p_batten_1g_x_4 = p_1 + size_of_batten_2g_x3_real
                p_batten_1g_y_4 = p_2
            else:
                size_of_batten_2g_x3_real = p_polotno_x_2
                p_batten_1g_x_1 = p_13 - 150
                p_batten_1g_y_1 = p_2
                p_batten_1g_x_2 = p_13 - 150
                p_batten_1g_y_2 = y_point_batten_2g_width
                p_batten_1g_x_3 = p_13 - 150 + size_of_batten_2g_x3_real
                p_batten_1g_y_3 = y_point_batten_2g_width
                p_batten_1g_x_4 = p_13 - 150 + size_of_batten_2g_x3_real
                p_batten_1g_y_4 = p_2
                size_of_batten_2g_x3_real += p_batten_1g_y_1
            # Чертим нащельник 1г
            points_batten_1g = self.aDouble([p_batten_1g_x_1, p_batten_1g_y_1, p_batten_1g_x_2,
                                             p_batten_1g_y_2, p_batten_1g_x_3, p_batten_1g_y_3,
                                             p_batten_1g_x_4, p_batten_1g_y_4, p_batten_1g_x_1,
                                             p_batten_1g_y_1])
            self.acadModel.AddLightWeightPolyline(points_batten_1g)
            # Назначаем точки для нащельника 2в
            p_batten_1v2_x_1 = p_13 - 40 * 2 + x_point_batten_2g_length
            p_batten_1v2_y_1 = p_2
            p_batten_1v2_x_2 = p_13 - 40 * 2 + x_point_batten_2g_length
            p_batten_1v2_y_2 = y_batten_vertic
            p_batten_1v2_x_3 = p_13 - 40 * 2 + x_point_batten_2g_length + size_of_batten_1v_width
            p_batten_1v2_y_3 = y_batten_vertic
            p_batten_1v2_x_4 = p_13 - 40 * 2 + x_point_batten_2g_length + size_of_batten_1v_width
            p_batten_1v2_y_4 = p_2
            # Чертим нащельник 2в
            points_batten_1v2 = self.aDouble([p_batten_1v2_x_1, p_batten_1v2_y_1, p_batten_1v2_x_2,
                                              p_batten_1v2_y_2, p_batten_1v2_x_3, p_batten_1v2_y_3,
                                              p_batten_1v2_x_4, p_batten_1v2_y_4, p_batten_1v2_x_1,
                                              p_batten_1v2_y_1])
            self.acadModel.AddLightWeightPolyline(points_batten_1v2)
            # Проверяем выбран ли второй слой для его отображение на чертеже
            if self.secondlayout_checkBox.isChecked():
                # Назначаем точки для второго слоя на общем виде
                p_second_layer_x_1 = p_13 - 300 + size_of_tp_width / 2
                p_second_layer_y_1 = y_point_batten_2g_width - 50
                p_second_layer_x_2 = p_13 - 300 + size_of_tp_width / 2
                p_second_layer_y_2 = size_of_batten_1v_length - 100
                p_second_layer_x_3 = p_13 + size_of_tp_width / 2
                p_second_layer_y_3 = size_of_batten_1v_length - 100
                p_second_layer_x_4 = p_13 + size_of_tp_width / 2
                p_second_layer_y_4 = y_point_batten_2g_width - 50
                # Чертим второй слой
                points_second_layer = self.aDouble([p_second_layer_x_1, p_second_layer_y_1,
                                                    p_second_layer_x_2, p_second_layer_y_2,
                                                    p_second_layer_x_3, p_second_layer_y_3,
                                                    p_second_layer_x_4, p_second_layer_y_4,
                                                    p_second_layer_x_1, p_second_layer_y_1])
                self.acadModel.AddLightWeightPolyline(points_second_layer)
            # Точки для размеров
            p_batten_1v_1 = APoint(p_1, p_2)
            p_batten_1v_2 = APoint(p_12, y_batten_vertic)
            p_batten_1v2_4 = APoint(p_13 - 40 * 2 + x_point_batten_2g_length + size_of_batten_1v_width, p_2)
            p_razmer_l = APoint(p_razmer_1, p_razmer_2)
            p_razmer_w = APoint(p_razmer_3, p_razmer_4)
            p_razmer_w_down = APoint(p_razmer_5, p_razmer_6)
            p_polotno_1_2 = APoint(p_13 - 150, size_of_batten_1v_length)
            p_polotno_1_3 = APoint(p_13 + size_of_tp_width - 150, size_of_batten_1v_length)
            if tp == 1:
                acad.model.AddDimAligned(p_batten_1v_1, p_batten_1v_2, p_razmer_l)
                acad.model.AddDimAligned(p_polotno_1_2, p_polotno_1_3, p_razmer_w)
                acad.model.AddDimAligned(p_batten_1v_1, p_batten_1v2_4, p_razmer_w_down)
            elif tp == 2:
                p_batten_1g_1 = APoint(p_13 - 150, p_2)
                acad.model.AddDimAligned(p_batten_1g_1, p_polotno_1_2, p_razmer_l)
                acad.model.AddDimAligned(p_polotno_1_2, p_polotno_1_3, p_razmer_w)
                p_batten_1g_1 = APoint(p_13 - 150, p_2)
                acad.model.AddDimAligned(p_batten_1g_1, p_batten_1v2_4, p_razmer_w_down)

            if type_of_tp == 'ТП-2':
                # Назначаем точки для нащельника 2г
                if tp == 1:
                    p_batten_2g_x_1 = p_1
                    p_batten_2g_y_1 = size_of_batten_1v_length - 150
                    p_batten_2g_x_2 = p_1
                    p_batten_2g_y_2 = size_of_batten_1v_length + 600
                    p_batten_2g_x_3 = p_1 + size_of_batten_2g_x3_real
                    p_batten_2g_y_3 = size_of_batten_1v_length + 600
                    p_batten_2g_x_4 = p_1 + size_of_batten_2g_x3_real
                    p_batten_2g_y_4 = size_of_batten_1v_length - 150
                else:
                    p_batten_2g_x_1 = p_13 - 150
                    p_batten_2g_y_1 = size_of_batten_1v_length - 150
                    p_batten_2g_x_2 = p_13 - 150
                    p_batten_2g_y_2 = size_of_batten_1v_length + 600
                    p_batten_2g_x_3 = p_13 - 150 + size_of_batten_2g_x3_real
                    p_batten_2g_y_3 = size_of_batten_1v_length + 600
                    p_batten_2g_x_4 = p_13 - 150 + size_of_batten_2g_x3_real
                    p_batten_2g_y_4 = size_of_batten_1v_length - 150

                points_batten_2g = self.aDouble([p_batten_2g_x_1, p_batten_2g_y_1,
                                                 p_batten_2g_x_2, p_batten_2g_y_2,
                                                 p_batten_2g_x_3, p_batten_2g_y_3,
                                                 p_batten_2g_x_4, p_batten_2g_y_4,
                                                 p_batten_2g_x_1, p_batten_2g_y_1])
                self.acadModel.AddLightWeightPolyline(points_batten_2g)
            if self.pocket_checkBox.isChecked():
                # Назначаем точки для кармана монтажного 2.1
                p_km_1_x_1 = p_13 - 50
                p_km_1_y_1 = y_pocket_in_main_pic
                p_km_1_x_2 = p_13 - 50
                p_km_1_y_2 = y_pocket_in_main_pic + 150
                p_km_1_x_3 = p_13 - 50 + x_pocket_in_main_pic
                p_km_1_y_3 = y_pocket_in_main_pic + 150
                p_km_1_x_4 = p_13 - 50 + x_pocket_in_main_pic
                p_km_1_y_4 = y_pocket_in_main_pic
                # Чертим карман монтажный 2.1
                points_km_1 = self.aDouble([p_km_1_x_1, p_km_1_y_1,
                                            p_km_1_x_2, p_km_1_y_2,
                                            p_km_1_x_3, p_km_1_y_3,
                                            p_km_1_x_4, p_km_1_y_4,
                                            p_km_1_x_1, p_km_1_y_1])
                self.acadModel.AddLightWeightPolyline(points_km_1)
            # Раскрой отдельный для ТП1.1
            size_int_polotn_w = self.count_doubleSpinBox_2.value()
            size_of_polotna_l = size_of_tp_length + 130 * 2
            pr_1 = p_13 - 40 * 2 + size_of_batten_2g_length + size_of_batten_1v_width + 3000
            pr_2 = 0.0
            pr_3 = size_of_polotna_l
            # Кол-во полуфабрикатов и габариты остатков
            quantity_of_p_true = (size_of_tp_width + 130 * 2) / size_int_polotn_w
            quantity_of_p = math.floor((size_of_tp_width + 130 * 2) / size_int_polotn_w)
            do_we_have_remains = quantity_of_p_true - quantity_of_p
            width_remains = 0
            if do_we_have_remains != 0:
                width_remains = (size_of_tp_width + 130 * 2) - (
                        size_int_polotn_w * quantity_of_p) + 30 * quantity_of_p
                if width_remains > size_int_polotn_w:
                    width_remains_new = width_remains - size_int_polotn_w + 30
                    width_remains = width_remains_new
            pr_4 = p_13 - 40 * 2 + size_of_batten_2g_length + size_of_batten_1v_width + 3000 + size_int_polotn_w
            length_remains = size_of_polotna_l

            def make_dimension_length(first_point, scond_point):
                p_razmer_first = first_point - 500.0
                p_razmer_second = scond_point - 100.0
                p_razmer_l = APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(first_point, scond_point, p_razmer_l)

            def make_dimension_width(first_point, scond_point):
                p_razmer_first = first_point - 500.0
                p_razmer_second = scond_point + 500.0
                p_razmer_w = APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(first_point, scond_point, p_razmer_w)

            for p in range(quantity_of_p):
                # Координаты полуфабриката П 1.1
                points_pp_11 = self.aDouble([pr_1, p_2,
                                             pr_1, pr_3,
                                             pr_4, pr_3,
                                             pr_4, p_2,
                                             pr_1, p_2])
                self.acadModel.AddLightWeightPolyline(points_pp_11)
                p_polyfabr1_1_1 = APoint(pr_1, p_2)
                p_polyfabr1_1_2 = APoint(pr_1, pr_3)
                p_polyfabr1_1_4 = APoint(pr_4, p_2)
                # Раскрой отдельный П 1.1
                if tp == 1:
                    p_text_about_p_1_1 = APoint(pr_1 + (size_int_polotn_w / 3), pr_3 / 2)
                elif tp == 2:
                    p_text_about_p_1_1 = APoint(pr_1 + (size_int_polotn_w / 3),
                                                pr_3 - y_size_of_polotna_l / 2)
                acadModel.AddText(f'П - {main_num_of_tp}-1', p_text_about_p_1_1, 100)
                make_dimension_length(p_polyfabr1_1_1, p_polyfabr1_1_2)
                make_dimension_width(p_polyfabr1_1_1, p_polyfabr1_1_4)
                pr_1 += size_int_polotn_w - 30
                pr_4 += size_int_polotn_w - 30

            pr_44 = pr_4 - size_int_polotn_w
            # Координаты полуфабриката П 1.2 (остатки)
            p_polyfa1_2_1 = APoint(pr_44, p_2)
            p_polyfa1_2_2 = APoint(pr_44, pr_3)
            p_polyfa1_2_4 = APoint(pr_44 + width_remains, p_2)
            name_of_pp_1 = f'ПП-{main_num_of_tp}-1'
            data_for_spec[name_of_pp_1] = [quantity_of_p, size_int_polotn_w, add_size_of_polotna_l]
            if do_we_have_remains != 0:
                if tp == 1:
                    p_text_about_p_1_2 = APoint(pr_44 + (width_remains / 4), length_remains / 2)
                    acadModel.AddText(f'П - {main_num_of_tp}-2', p_text_about_p_1_2, 100)
                elif tp == 2:
                    p_text_about_p_1_2 = APoint(pr_44 + (width_remains / 4), length_remains -
                                                y_size_of_polotna_l / 2)
                    acadModel.AddText(f'П - {main_num_of_tp}-2', p_text_about_p_1_2, 100)
                data_for_spec[f'ПП-{main_num_of_tp}-2'] = [1, width_remains, add_size_of_polotna_l]
                # Чертим П-1-2
                points_pp_21 = self.aDouble([pr_44, p_2,
                                             pr_44, pr_3,
                                             pr_44 + width_remains, pr_3,
                                             pr_44 + width_remains, p_2,
                                             pr_44, p_2])
                self.acadModel.AddLightWeightPolyline(points_pp_21)
                make_dimension_length(p_polyfa1_2_1, p_polyfa1_2_2)
                make_dimension_width(p_polyfa1_2_1, p_polyfa1_2_4)

            # Показываем элементы раскроя отдельно
            # Координаты полуфабриката П 1.1 отдельного, dop - дополнительный вид
            p_dop_r_1 = pr_44 + width_remains + 2000
            p_dop_r_2 = size_of_polotna_l
            p_dop_r_4 = p_dop_r_1 + size_int_polotn_w
            points_pp_21 = self.aDouble([p_dop_r_1, p_2,
                                         p_dop_r_1, p_dop_r_2,
                                         p_dop_r_4, p_dop_r_2,
                                         p_dop_r_4, p_2,
                                         p_dop_r_1, p_2])
            # Чертим П-1-1
            self.acadModel.AddLightWeightPolyline(points_pp_21)
            p_dop_polyfabr1_1_1 = APoint(p_dop_r_1, p_2)
            p_dop_polyfabr1_1_2 = APoint(p_dop_r_1, p_dop_r_2)
            p_dop_polyfabr1_1_4 = APoint(p_dop_r_4, p_2)
            if tp == 1:
                p_text_about_dop_p_1_1 = APoint(p_dop_r_1 + (size_int_polotn_w / 3), size_of_polotna_l / 2)
            else:
                p_text_about_dop_p_1_1 = APoint(p_dop_r_1 + (size_int_polotn_w / 3),
                                                size_of_polotna_l - y_size_of_polotna_l / 2)

            acadModel.AddText(f'П - {main_num_of_tp}-1 \n{quantity * quantity_of_p} шт',
                              p_text_about_dop_p_1_1, 100)
            make_dimension_length(p_dop_polyfabr1_1_1, p_dop_polyfabr1_1_2)
            make_dimension_width(p_dop_polyfabr1_1_1, p_dop_polyfabr1_1_4)
            if do_we_have_remains != 0:
                # Координаты полуфабриката П 1-2 остатки отдельного, dop - дополнительный вид
                points_pp_21 = self.aDouble([p_dop_r_4 + 1000, p_2,
                                             p_dop_r_4 + 1000, p_dop_r_2,
                                             p_dop_r_4 + 1000 + width_remains, p_dop_r_2,
                                             p_dop_r_4 + 1000 + width_remains, p_2,
                                             p_dop_r_4 + 1000, p_2])
                p_dop_polyfabr1_2_1 = APoint(p_dop_r_4 + 1000, p_2)
                p_dop_polyfabr1_2_2 = APoint(p_dop_r_4 + 1000, p_dop_r_2)
                p_dop_polyfabr1_2_4 = APoint(p_dop_r_4 + 1000 + width_remains, p_2)
                print(quantity_of_p)
                # Чертим П-1-2
                self.acadModel.AddLightWeightPolyline(points_pp_21)
                if tp == 1:
                    p_text_about_dop_p_1_2 = APoint(p_dop_r_4 + 1000 + (width_remains / 4),
                                                    size_of_polotna_l / 2)
                elif tp == 2:
                    p_text_about_dop_p_1_2 = APoint(p_dop_r_4 + 1000 + (width_remains / 4),
                                                    size_of_polotna_l - y_size_of_polotna_l / 2)
                acadModel.AddText(f'П - {main_num_of_tp}-2 \n{quantity} шт',
                                  p_text_about_dop_p_1_2, 100)
                make_dimension_length(p_dop_polyfabr1_2_1, p_dop_polyfabr1_2_2)
                make_dimension_width(p_dop_polyfabr1_2_1, p_dop_polyfabr1_2_4)
            # Выносим второй слой отдельно
            p_second_layer_dop_11 = p_dop_r_4 + 3000 + width_remains
            p_second_layer_dop_12 = size_of_tp_length - 100 * 2
            p_second_layer_dop_14 = p_dop_r_4 + 3000 + width_remains + 300
            # Координаты Второй Слой
            p_sl_1_dop_1 = APoint(p_second_layer_dop_11, p_2)
            p_sl_1_dop_2 = APoint(p_second_layer_dop_11, p_second_layer_dop_12)
            p_sl_1_dop_4 = APoint(p_second_layer_dop_14, p_2)
            # Чертим В 1 отдельно
            if self.secondlayout_checkBox.isChecked():
                points_sl_21 = self.aDouble([p_second_layer_dop_11, p_2,
                                             p_second_layer_dop_11, p_second_layer_dop_12,
                                             p_second_layer_dop_14, p_second_layer_dop_12,
                                             p_second_layer_dop_14, p_2,
                                             p_second_layer_dop_11, p_2])
                self.acadModel.AddLightWeightPolyline(points_sl_21)
                p_text_about_dop_sl_1 = APoint(p_second_layer_dop_11 + 300 / 4, y_text_about_dop)
                acadModel.AddText(f'В - {main_num_of_tp}-1 \n{quantity} шт',
                                  p_text_about_dop_sl_1, 100)
                data_for_spec[f'В-{main_num_of_tp}-1'] = [1, 300, add_lenght_of_second_layout]
                make_dimension_length(p_sl_1_dop_1, p_sl_1_dop_2)
                make_dimension_width(p_sl_1_dop_1, p_sl_1_dop_4)
            # Чертим Нащельники отдельно
            # Точки нащельника 1 в
            points_bv1 = self.aDouble([p_second_layer_dop_14 + 1000, p_2,
                                       p_second_layer_dop_14 + 1000, size_of_batten_1v_length,
                                       p_second_layer_dop_14 + 1000 + size_of_batten_1v_width,
                                       size_of_batten_1v_length,
                                       p_second_layer_dop_14 + 1000 + size_of_batten_1v_width, p_2,
                                       p_second_layer_dop_14 + 1000, p_2])
            self.acadModel.AddLightWeightPolyline(points_bv1)  # Наносим чертеж в автокад
            p_batten_1v_dop_1 = APoint(p_second_layer_dop_14 + 1000, p_2)
            p_batten_1v_dop_2 = APoint(p_second_layer_dop_14 + 1000, size_of_batten_1v_length)
            p_batten_1v_dop_4 = APoint(p_second_layer_dop_14 + 1000 + size_of_batten_1v_width, p_2)
            # Чертим Н 1 вертик отдельно
            p_text_about_dop_b11 = APoint(p_second_layer_dop_14 + 1000 + (size_of_batten_1v_width / 4),
                                          y_text_about_dop)
            if tp == 1:
                acadModel.AddText(f'Н - {main_num_of_tp}-1 \n{quantity * 2} шт',
                                  p_text_about_dop_b11, 100)

                qount_of_batten_1v = 2
            else:
                acadModel.AddText(f'Н - {main_num_of_tp}-1 \n{quantity} шт',
                                  p_text_about_dop_b11, 100)
                qount_of_batten_1v = 1
            data_for_spec[f'Н-{main_num_of_tp}-1'] = [qount_of_batten_1v, size_of_batten_1v_width,
                                                      dem_const_batten_1v_length]
            make_dimension_length(p_batten_1v_dop_1, p_batten_1v_dop_2)
            make_dimension_width(p_batten_1v_dop_1, p_batten_1v_dop_4)
            # Точки нащельника горизонтального Н2 Г
            p_bg2_x1 = p_second_layer_dop_14 + 2000 + size_of_batten_1v_width
            p_bg2_y1 = p_2
            p_bg2_x2 = p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + size_of_batten_2g_width
            p_bg2_y2 = size_of_batten_2g_x3_real
            points_bg2 = self.aDouble([p_bg2_x1, p_bg2_y1,
                                       p_bg2_x1, p_bg2_y2,
                                       p_bg2_x2, p_bg2_y2,
                                       p_bg2_x2, p_bg2_y1,
                                       p_bg2_x1, p_bg2_y1])
            if tp == 2:
                print(points_bg2)
            self.acadModel.AddLightWeightPolyline(points_bg2)  # Чертим Н 2 гориз отдельно
            p_batten_2g_dop_1 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width, p_2)
            p_batten_2g_dop_2 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width,
                                       size_of_batten_2g_x3_real)
            p_batten_2g_dop_4 = APoint(
                p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + size_of_batten_2g_width, p_2)
            p_text_about_dop_b12 = APoint(
                p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + (size_of_batten_1v_width / 4),
                size_of_batten_2g_x3_real)
            qount_of_batten = 1
            # Добавляем надписи по нащельникам
            if type_of_tp == 'ТП-1':
                text_about_buttn = f'Н - {main_num_of_tp}-2 \n{quantity} шт'
                qount_of_batten = 1
            else:
                text_about_buttn = f'Н - {main_num_of_tp}-2 \n{quantity * 2} шт'
                qount_of_batten = 2
            acadModel.AddText(text_about_buttn, p_text_about_dop_b12, 100)
            data_for_spec[f'Н-{main_num_of_tp}-2'] = [qount_of_batten, size_of_batten_2g_width,
                                                      dem_const_batten_2g_length]
            make_dimension_length(p_batten_2g_dop_1, p_batten_2g_dop_2)
            make_dimension_width(p_batten_2g_dop_1, p_batten_2g_dop_4)
            # Очерчиваем отдельно карман, если он был выбран в меню
            if self.pocket_checkBox.isChecked():
                points_pocket = self.aDouble([p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500, p_2,
                                           p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500,
                                           y_pocket_lenght,
                                           p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500 + 150,
                                           y_pocket_lenght,
                                           p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500 + 150,
                                           p_2,
                                           p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500, p_2])
                self.acadModel.AddLightWeightPolyline(points_pocket)  # Чертим карман полилинией
                p_pocket_km_dop_1 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500,
                                           p_2)
                p_pocket_km_dop_2 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500,
                                           y_pocket_lenght)
                p_pocket_km_dop_4 = APoint(
                    p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500 + 150,
                    p_2)
                p_text_about_dop_km = APoint(
                    p_second_layer_dop_14 + 4500 + size_of_batten_1v_width + (size_of_batten_1v_width / 4),
                    y_text_about_dop)
                acadModel.AddText(f'КМ - {main_num_of_tp}-2 \n{quantity} шт',
                                  p_text_about_dop_km, 100)
                make_dimension_length(p_pocket_km_dop_1, p_pocket_km_dop_2)
                make_dimension_width(p_pocket_km_dop_1, p_pocket_km_dop_4)
                data_for_spec[f'КМ-{main_num_of_tp}-2'] = [1, 300, dem_const_pocket_length]
            self.main_data_for_spec[f'{type_of_tp}-{tp}'] = [data_for_spec]
            quantity = quantity_of_tp12
            y_pocket_in_main_pic += size_of_batten_2g_length + size_of_tp_length
            y_pocket_lenght += size_of_batten_2g_length + size_of_tp_length
            y_batten_vertic += size_of_batten_2g_length + size_of_tp_length
            p_2 += size_of_batten_2g_length + size_of_tp_length
            p_for_text_2 += size_of_batten_2g_length + size_of_tp_length
            y_text_about_dop += size_of_batten_2g_length + size_of_tp_length
            p_razmer_6 += size_of_batten_2g_length + size_of_tp_length - 500
            p_razmer_4 += size_of_batten_2g_length + size_of_tp_length
            p_razmer_2 += size_of_batten_2g_length + size_of_tp_length
            y_point_batten_2g_width += size_of_batten_2g_length + size_of_tp_length
            size_of_polotna_l += size_of_batten_2g_length + size_of_tp_length
            size_of_batten_1v_length += size_of_batten_2g_length + size_of_tp_length
            old_size_batten_2g_length = size_of_batten_2g_length
            size_of_batten_2g_length += size_of_batten_2g_length + size_of_tp_length
            size_of_tp_length += old_size_batten_2g_length + size_of_tp_length
        self.print_specification(quantity)

    def print_specification(self, quantity):
        try:
            if self.count_doubleSpinBox_2.value() == 2510:
                plotnost_polotna = 'ПВХ - 650 г/м2'
            elif self.count_doubleSpinBox_2.value() == 3010:
                plotnost_polotna = 'ПВХ - 900 г/м2'
            else:
                plotnost_polotna = '------'
            ExcelExport(quantity, plotnost_polotna, self.main_data_for_spec)
        except FileCreateError:
            error = 'Ошибка перезаписи и открытия файла! Возможно файл уже открыт, либо отсуствует папка' \
                    ' "Спецификации".'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()

    def draw_tp3_btn(self):
        try:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True
            acadModel = acad.ActiveDocument.ModelSpace
            data_for_spec = {}  # Словарь зависимость полуфабрикат - его данные(кол-во, ширина, длинна)
            # Изначальные данные
            # Ширина торца ангара
            with_end_face = self.width_doubleSpinBox_4.value()
            # Высота стенки ангара
            wall_height = self.wall_haight_doubleSpinBox_2.value()
            # Полная высота ангара
            full_height = self.full_height_doubleSpinBox_3.value()
            # Высота нащельника  горизонального
            size_of_batten_2g_height = self.batten_2g_height_doubleSpinBox_3.value()
            # Ширина квадртаного блока ТП 3 и нащельника
            width_square_block_tp3 = with_end_face - 300 * 2
            # Точки конструкции ангара
            p_x_1 = 0.0
            p_y_1 = 0.0
            p_y_2 = wall_height
            # Координаты конька
            p_x_2 = with_end_face / 2
            p_y_3 = full_height
            # Координата торца
            p_x_3 = with_end_face
            # Координаты нащельника
            x_batten_1 = 150
            y_batten_1 = 300
            x_batten_2 = with_end_face - 150
            y_batten_2 = - size_of_batten_2g_height + 300
            # Координаты второго слоя
            x_slayout_1 = self.size_to_sl_doubleSpinBox.value() - 150
            y_slayout_1 = 250
            x_slayout_2 = self.size_to_sl_doubleSpinBox.value() + 150
            y_slayout_2 = full_height
            # Вычисляем размеры. Вычиялем угол прилежащий к коньку ангара
            angle_b = 180 - 90 - math.floor(math.atan2(full_height - wall_height, with_end_face / 2) * 180 / math.pi)
            up_point_of_tp_3 = 150 / math.sin(math.radians(angle_b))
            # Найдем верхнюю точку стены
            angle_a = 180 - angle_b
            part_of_angle_a = angle_a / 2
            gepotinuza = 150 / math.sin(math.radians(part_of_angle_a))
            catet_b = math.sqrt(gepotinuza ** 2 - 150 ** 2)
            wall_height_y_coord_2 = wall_height - catet_b
            # Выставляем координаты для размеров
            x_zero_dim_1 = 150
            y_zero_dim_1 = 150
            y_height_dim_2 = full_height - up_point_of_tp_3
            y_height_wall_dim_2 = wall_height_y_coord_2
            x_height_dim_2 = 150
            x_width_dim_3 = x_batten_2
            # Cчитаем площадь полотна
            area_square = (y_height_wall_dim_2 - 150) * (x_width_dim_3 - 150)
            area_triangle = (((x_width_dim_3 - 150) * (y_height_dim_2 - y_height_wall_dim_2 - 300)) / 2)
            full_area_tp_3 = round(((area_square + area_triangle) / 1000000), 2)
            # Cчитаем площадь нащельника
            full_area_batten = (size_of_batten_2g_height * (x_width_dim_3 - 150)) / 1000000

            def make_dimension_height(first_point, scond_point, third_point, forth_point, otstup):
                # Размер по длине
                f_point = self.APoint(first_point, scond_point)
                s_point = self.APoint(third_point, forth_point)
                p_razmer_first = first_point - otstup
                p_razmer_second = forth_point - 100.0
                p_razmer_l = self.APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(f_point, s_point, p_razmer_l)

            def make_dimension_width(first_point, scond_point, third_point, forth_point):
                # Размер по ширине
                f_point = self.APoint(first_point, scond_point)
                s_point = self.APoint(third_point, forth_point)
                size_of_batten_2g_height = self.batten_2g_height_doubleSpinBox_3.value()
                p_razmer_first = first_point - size_of_batten_2g_height - 500
                p_razmer_second = scond_point - size_of_batten_2g_height - 500
                p_razmer_w = self.APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(f_point, s_point, p_razmer_w)

            # Назначаем точки для конструкции
            # Чертим Торец ангара по размерам заданным
            # Точки торца ангара
            points_wall_end = self.aDouble(
                [p_x_1, p_y_1, p_x_1, p_y_2, p_x_2, p_y_3, p_x_3, p_y_2, p_x_3, p_y_1, p_x_1, p_y_1])
            # Чертим торец ангара с помощью полилинии
            well_end_drawing = acadModel.AddLightWeightPolyline(points_wall_end)
            # Добавляем информацию о полотне в списки
            data_for_spec['ТП-3'] = [1, x_batten_2 - 150, y_height_dim_2 - 150, full_area_tp_3]
            # Смещаем полилинию
            well_end_drawing.Offset(150)
            # Контур Второго слоя
            well_end_drawing.Offset(250)
            well_end_drawing.Delete()
            # Назначаем точки для конструкции
            # Точки нащельника
            points_batten = self.aDouble(
                [x_batten_1, y_batten_1, x_batten_2, y_batten_1, x_batten_2, y_batten_2, x_batten_1, y_batten_2,
                 x_batten_1,
                 y_batten_1])
            # Чертим нащельник c помощью полилинии
            acadModel.AddLightWeightPolyline(points_batten)
            # Добавляем информацию о нащельнике в списки
            data_for_spec['Н-3-1'] = [1, x_batten_2 - 150, size_of_batten_2g_height]
            # Считаем количетсво вторых слоев
            # Средняя линия точки
            print(with_end_face, full_height)
            align_line_1 = self.APoint(with_end_face / 2, 0)
            align_line_2 = self.APoint(with_end_face / 2, full_height)
            step_of_sl = self.step_bw_sl_doubleSpinBox.value()
            if self.secondlayout_checkBox.isChecked():
                quantity_of_sl = math.ceil(
                    (with_end_face / 2 - self.size_to_sl_doubleSpinBox.value()) / step_of_sl)
                print(quantity_of_sl)
                count_sl = 1
                if quantity_of_sl != 0:
                    for sl in range(quantity_of_sl):
                        # Точки второго слоя
                        points_sl = self.aDouble(
                            [x_slayout_1, y_slayout_1, x_slayout_1, y_slayout_2, x_slayout_2, y_slayout_2, x_slayout_2,
                             y_slayout_1])
                        # Чертим второй слой с помощью полилинии acadModel.AddLightWeightPolyline(points_wall_end)
                        secondl_drawing = acadModel.AddLightWeightPolyline(points_sl)
                        print(secondl_drawing, align_line_1, align_line_2)
                        secondl_drawing.Mirror(align_line_1, align_line_2)
                        x_slayout_1 += step_of_sl
                        x_slayout_2 += step_of_sl
                        # Добавляем инфу в словарь о полуфабрикате
                        data_for_spec[f'В-3-{count_sl}'] = [2, 100, y_slayout_2]
                        count_sl += 1
                else:
                    points_sl = self.aDouble(
                        [x_slayout_1, y_slayout_1, x_slayout_1, y_slayout_2, x_slayout_2, y_slayout_2, x_slayout_2,
                         y_slayout_1])
                    # Чертим второй слой с помощью полилинии
                    secondl_drawing = acadModel.AddLightWeightPolyline(points_sl)
                    secondl_drawing.Mirror(align_line_1, align_line_2)
                    data_for_spec[f'В-3-{count_sl}'] = [2, 100, y_slayout_2]
            if self.pocket_checkBox.isChecked():
                # Координаты для кармана КМ
                x_pocket_1 = with_end_face / 2 - ((with_end_face / 2) / 3) * 2 + 400
                y_pocket_1 = ((full_height - wall_height) / 4) + wall_height
                x_pocket_2 = with_end_face - x_pocket_1
                y_pocket_2 = y_pocket_1 + 150
                # Точки кармана
                points_pocket = self.aDouble(
                    [x_pocket_1, y_pocket_1, x_pocket_1, y_pocket_2, x_pocket_2, y_pocket_2, x_pocket_2, y_pocket_1,
                     x_pocket_1, y_pocket_1])
                acadModel.AddLightWeightPolyline(points_pocket)
                # Cчитаем площадь кармана
                full_area_pocket = (x_pocket_2 - x_pocket_1) * 150 / 1000000
                data_for_spec[f'КМ-3-1'] = [1, x_pocket_2 - x_pocket_1, 150]
            self.main_data_for_spec[f'ТП-3'] = [data_for_spec]
            # Cтавим размер полотна по высоте
            make_dimension_height(x_zero_dim_1, y_zero_dim_1, x_height_dim_2, y_height_dim_2, 1500)
            # Cтавим размер высоты стенки полотна
            make_dimension_height(x_zero_dim_1, y_zero_dim_1, x_height_dim_2, y_height_wall_dim_2, 500)
            # Cтавим размер по ширине стенки
            make_dimension_width(x_zero_dim_1, y_zero_dim_1, x_width_dim_3, y_zero_dim_1)
            quantity_of_tp3 = self.quantity_spinBox_tp_3.value()
            self.print_specification(quantity_of_tp3)
        except _ctypes.COMError:
            error = 'Ошибка. Автокад не запущен. Запустите автокад с чертежным видом и попробуйте снова.'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()


class ErrorAddReport(QDialog):
    def __init__(self, data, parent=None, flag=Qt.Dialog):
        super().__init__(parent, flag)
        uic.loadUi('ui/errors/error_dialog_report.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.text_error = data
        self.label_dscr_of_error.clear()
        self.label_dscr_of_error.setText(self.text_error)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusOutEvent(self, event):
        self.activateWindow()
        self.raise_()
        self.show()

    def ok_btn_press(self):
        self.close()


def application():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/report.png'))
    MainWindow = MainMenu()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()

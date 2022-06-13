import os
import re
import sys
import win32com.client
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
import imain_image


class Main_menu(QMainWindow):
    # Главное меню
    def __init__(self, parent=None):
        super().__init__(parent)  # Call the inherited classes __init__ method
        uic.loadUi('ui/calcul_menu.ui', self)
        self.comboBox.currentIndexChanged.connect(self.indexChanged)
        self.load_menu(self.comboBox.currentText())
        self.batten_2g_height_doubleSpinBox_3.setValue(700.00)
        self.size_to_sl_doubleSpinBox.setValue(1.00)
        self.step_bw_sl_doubleSpinBox.setValue(1.00)
        self.data_of_product = []
        self.qount_of_product = []
        self.width_of_product = []
        self.length_of_product = []
        self.area_of_product = []

    def indexChanged(self):
        choose_tp = self.comboBox.currentText()
        self.load_menu(choose_tp)

    def load_menu(self, choose_tp):
        if choose_tp == 'ТП-1' or choose_tp == 'ТП-2':
            # Скрываем меню для ТП-3
            self.frame_tp_3.hide()
            self.frame_sl.hide()
            # Показываекм меню для ТП-1
            self.frame_tp_1.show()
            self.quantity_spinBox.setValue(2)
            try:
                self.tp_pushButton.clicked.disconnect(self.draw_tp3_btn)
            except:
                pass
            self.tp_pushButton.clicked.connect(self.count_and_drow_tp_btn)
        else:
            # Скрываем меню для ТП-1 и ТП-2
            self.tp_pushButton.clicked.disconnect(self.count_and_drow_tp_btn)
            self.tp_pushButton.clicked.connect(self.draw_tp3_btn)
            self.frame_tp_1.hide()
            # Показываекм меню для ТП-3
            self.frame_tp_3.show()
            self.frame_sl.show()

    def count_and_drow_tp_btn(self):
        try:
            width_tp = self.width_doubleSpinBox_2.value()
            size_of_tp_width = width_tp - 150 * 2
            # расчет релеватности решения
            count_size_int_polotn_w = self.count_doubleSpinBox_2.value()
            relev = (size_of_tp_width + 130 * 2) / count_size_int_polotn_w
            def draw_and_count_the_polotno():
                type_of_tp = self.comboBox.currentText()
                main_num_of_tp = 1
                if type_of_tp == 'ТП-1':
                    main_num_of_tp = 1
                elif type_of_tp == 'ТП-2':
                    main_num_of_tp = 2
                # AutoCAD = win32com.client.Dispatch("AutoCAD.Application")
                acad = Autocad(create_if_not_exists=False)
                acad.Visible = True
                # acad = win32com.client.Dispatch("AutoCAD.Application")
                width_tp = self.width_doubleSpinBox_2.value()
                length_tp = self.length_doubleSpinBox_2.value()
                quantity = self.quantity_spinBox.value()
                size_of_tp_width = width_tp - 150 * 2
                size_of_tp_length = length_tp - 150 * 2
                size_of_batten_1v_width = 700
                size_of_batten_1v_length = size_of_tp_length + 550
                size_of_batten_2g_width = 700
                size_of_batten_2g_length = size_of_tp_width - 110 * 2
                quantity_batten_1v = quantity * 2
                quantity_batten_1g = quantity
                quantity_of_tp12 = self.quantity_spinBox_tp2.value()
                general_size_tp1_1_w = size_of_tp_width + 550 * 2
                general_size_tp1_1_l = size_of_tp_length + 550
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
                    y_batten_vertic = size_of_batten_1v_length + 550
                    y_pocket_in_main_pic = y_batten_vertic / 2 - 75
                elif type_of_tp == 'ТП-2':
                    y_batten_vertic = size_of_batten_1v_length + 600
                    y_pocket_in_main_pic = y_batten_vertic / 2 - 75
                try:
                    workbook = xlsxwriter.Workbook(f'Спецификация/Спецификация.xlsx')
                    for tp in quantity_of_tp_common:
                        p_text = APoint(p_for_text, p_for_text_2)
                        text = acad.model.AddText(f'Монтажный вид {type_of_tp}.{tp} - {quantity} шт (в сборе)', p_text, 100)
                        def draw_a_drawing(point_1, point_2, point_3, point_4):
                            acad.model.AddLine(point_1, point_2)
                            acad.model.AddLine(point_2, point_3)
                            acad.model.AddLine(point_3, point_4)
                            acad.model.AddLine(point_4, point_1)
                        # Назначаем точки для нащельника 1в
                        p_batten_1v_1 = APoint(p_1, p_2)
                        p_batten_1v_2 = APoint(p_12, y_batten_vertic)
                        p_batten_1v_3 = APoint(p_13, y_batten_vertic)
                        p_batten_1v_4 = APoint(p_13, p_2)
                        # Чертим нащельник 1в
                        if tp == 1:
                            draw_a_drawing(p_batten_1v_1,p_batten_1v_2, p_batten_1v_3, p_batten_1v_4)
                        # Назначаем точки для полотная ТП 1.1
                        p_polotno_1_2 = APoint(p_13 - 150, size_of_batten_1v_length)
                        p_polotno_1_3 = APoint(p_13 + size_of_tp_width - 150, size_of_batten_1v_length)
                        p_polotno_1_4 = APoint(p_13 + size_of_tp_width- 150, y_point_batten_2g_width - 150)
                        p_polotno_1_1 = APoint(p_13 - 150, y_point_batten_2g_width - 150)
                        # Чертим полотно
                        draw_a_drawing(p_polotno_1_2, p_polotno_1_3, p_polotno_1_4, p_polotno_1_1)
                        # Назначаем точки для нащельника 1г
                        p_batten_1g_1 = APoint(p_13 - 40, p_2)
                        p_batten_1g_2 = APoint(p_13 - 40, y_point_batten_2g_width)
                        p_batten_1g_3 = APoint(p_13 - 40 + x_point_batten_2g_length, y_point_batten_2g_width)
                        p_batten_1g_4 = APoint(p_13 - 40 + x_point_batten_2g_length, p_2)
                        # Чертим нащельник 1г
                        draw_a_drawing(p_batten_1g_1, p_batten_1g_2, p_batten_1g_3, p_batten_1g_4)
                        # Назначаем точки для нащельника 2в
                        p_batten_1v2_1 = APoint(p_13 - 40 * 2 + x_point_batten_2g_length, p_2)
                        p_batten_1v2_2 = APoint(p_13 - 40 * 2 + x_point_batten_2g_length, y_batten_vertic)
                        p_batten_1v2_3 = APoint(p_13 - 40 * 2 + x_point_batten_2g_length + size_of_batten_1v_width, y_batten_vertic)
                        p_batten_1v2_4 = APoint(p_13 - 40 * 2 + x_point_batten_2g_length + size_of_batten_1v_width, p_2)
                        # Чертим нащельник 2в
                        draw_a_drawing(p_batten_1v2_1,p_batten_1v2_2, p_batten_1v2_3, p_batten_1v2_4)
                        # Назначаем точки для второго слоя на общем виде
                        p_second_layer_11_1 = APoint(p_13 - 300 + size_of_tp_width/2, y_point_batten_2g_width - 50)
                        p_second_layer_11_2 = APoint(p_13 - 300 + size_of_tp_width/2, size_of_batten_1v_length - 100)
                        p_second_layer_11_3 = APoint(p_13 + size_of_tp_width/2, size_of_batten_1v_length - 100)
                        p_second_layer_11_4 = APoint(p_13 + size_of_tp_width/2, y_point_batten_2g_width - 50)
                        # Чертим второй слой
                        if self.secondlayout_checkBox.isChecked():
                            draw_a_drawing(p_second_layer_11_1, p_second_layer_11_2, p_second_layer_11_3, p_second_layer_11_4)
                        p_razmer_l = APoint(p_razmer_1, p_razmer_2)
                        p_razmer_w = APoint(p_razmer_3, p_razmer_4)
                        p_razmer_w_down = APoint(p_razmer_5, p_razmer_6)
                        if tp == 1:
                            acad.model.AddDimAligned(p_batten_1v_1, p_batten_1v_2, p_razmer_l)
                            acad.model.AddDimAligned(p_polotno_1_2, p_polotno_1_3, p_razmer_w)
                            acad.model.AddDimAligned(p_batten_1v_1, p_batten_1v2_4, p_razmer_w_down)
                        elif tp == 2:
                            p_batten_1g_1 = APoint(p_13 - 40 - 110, p_2)
                            acad.model.AddDimAligned(p_batten_1g_1, p_polotno_1_2, p_razmer_l)
                            acad.model.AddDimAligned(p_polotno_1_2, p_polotno_1_3, p_razmer_w)
                            p_batten_1g_1 = APoint(p_13 - 40, p_2)
                            acad.model.AddDimAligned(p_batten_1g_1, p_batten_1v2_4, p_razmer_w_down)
                        if type_of_tp == 'ТП-2':
                            # Назначаем точки для нащельника 2г
                            p_batten_2g_1 = APoint(p_13 - 40, size_of_batten_1v_length - 150)
                            p_batten_2g_2 = APoint(p_13 - 40, size_of_batten_1v_length + 600)
                            p_batten_2g_3 = APoint(p_13 - 40 + x_point_batten_2g_length, size_of_batten_1v_length + 600)
                            p_batten_2g_4 = APoint(p_13 - 40 + x_point_batten_2g_length, size_of_batten_1v_length - 150)
                            draw_a_drawing(p_batten_2g_1, p_batten_2g_2, p_batten_2g_3, p_batten_2g_4)

                        if self.pocket_checkBox.isChecked():
                            # Назначаем точки для кармана монтажного 2.1
                            p_km_1 = APoint(p_13 - 50, y_pocket_in_main_pic)
                            p_km_2 = APoint(p_13 - 50, y_pocket_in_main_pic + 150)
                            p_km_3 = APoint(p_13 - 50 + x_pocket_in_main_pic, y_pocket_in_main_pic + 150)
                            p_km_4 = APoint(p_13 - 50 + x_pocket_in_main_pic, y_pocket_in_main_pic)
                            draw_a_drawing(p_km_1, p_km_2, p_km_3, p_km_4)

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
                            width_remains = (size_of_tp_width + 130 * 2) - (size_int_polotn_w * quantity_of_p) + 30 * quantity_of_p
                            if width_remains > size_int_polotn_w:
                                width_remains_new = width_remains - size_int_polotn_w + 30
                                width_remains = width_remains_new
                        pr_4 = p_13 - 40 * 2 + size_of_batten_2g_length + size_of_batten_1v_width + 3000 + size_int_polotn_w
                        print(width_remains , quantity_of_p_true, quantity_of_p, do_we_have_remains)
                        length_remains = size_of_polotna_l

                        def make_dimension_length(first_point, scond_point,):
                            p_razmer_first = first_point - 500.0
                            p_razmer_second = scond_point - 100.0
                            p_razmer_l = APoint(p_razmer_first, p_razmer_second)
                            acad.model.AddDimAligned(first_point, scond_point, p_razmer_l)

                        def make_dimension_width(first_point, scond_point,):
                            p_razmer_first = first_point - 500.0
                            p_razmer_second = scond_point + 500.0
                            p_razmer_w = APoint(p_razmer_first, p_razmer_second)
                            acad.model.AddDimAligned(first_point, scond_point, p_razmer_w)

                        for p in range(quantity_of_p):
                            # Координаты полуфабриката П 1.1
                            p_polyfabr1_1_1 = APoint(pr_1, p_2)
                            p_polyfabr1_1_2 = APoint(pr_1, pr_3)
                            p_polyfabr1_1_3 = APoint(pr_4, pr_3)
                            p_polyfabr1_1_4 = APoint(pr_4, p_2)
                            # Чертим П.1.1
                            draw_a_drawing(p_polyfabr1_1_1, p_polyfabr1_1_2, p_polyfabr1_1_3, p_polyfabr1_1_4)
                            # Раскрой отдельный П 1.1
                            if tp == 1:
                                p_text_about_p_1_1 = APoint(pr_1 + (size_int_polotn_w/3), pr_3 / 2)
                            elif tp == 2:
                                p_text_about_p_1_1 = APoint(pr_1 + (size_int_polotn_w / 3), pr_3 - y_size_of_polotna_l / 2)
                            text_pr1_1 = acad.model.AddText(f'П - {main_num_of_tp}.1', p_text_about_p_1_1, 100)
                            make_dimension_length(p_polyfabr1_1_1, p_polyfabr1_1_2)
                            make_dimension_width(p_polyfabr1_1_1, p_polyfabr1_1_4)
                            pr_1 += size_int_polotn_w - 30
                            pr_4 += size_int_polotn_w - 30

                        self.width_of_product.append(size_int_polotn_w)
                        self.length_of_product.append(add_size_of_polotna_l)
                        pr_44 = pr_4 - size_int_polotn_w
                        # Координаты полуфабриката П 1.2 (остатки)
                        p_polyfa1_2_1 = APoint(pr_44, p_2)
                        p_polyfa1_2_2 = APoint(pr_44, pr_3)
                        p_polyfa1_2_3 = APoint(pr_44 + width_remains, pr_3)
                        p_polyfa1_2_4 = APoint(pr_44 + width_remains, p_2)
                        self.data_of_product.append(f'ПП-{main_num_of_tp}.1')

                        if do_we_have_remains != 0:
                            if tp == 1:
                                p_text_about_p_1_2 = APoint(pr_44 + (width_remains/4), length_remains / 2)
                                text_pr_p1_2 = acad.model.AddText(f'П - {main_num_of_tp}.2', p_text_about_p_1_2, 100)
                            elif tp == 2:
                                p_text_about_p_1_2 = APoint(pr_44 + (width_remains / 4), length_remains - y_size_of_polotna_l / 2)
                                text_pr_p1_2 = acad.model.AddText(f'П - {main_num_of_tp}.2', p_text_about_p_1_2, 100)
                            self.data_of_product.append(f'ПП-{main_num_of_tp}.2')
                            self.width_of_product.append(width_remains)
                            self.length_of_product.append(add_size_of_polotna_l)
                            # Чертим П.1.2
                            draw_a_drawing(p_polyfa1_2_1, p_polyfa1_2_2, p_polyfa1_2_3, p_polyfa1_2_4)
                            make_dimension_length(p_polyfa1_2_1 , p_polyfa1_2_2)
                            make_dimension_width(p_polyfa1_2_1, p_polyfa1_2_4)

                        # Показываем элементы раскроя отдельно
                        # Координаты полуфабриката П 1.1 отдельного, dop - дополнительный вид
                        p_dop_r_1 = pr_44 + width_remains + 2000
                        p_dop_r_2 = size_of_polotna_l
                        p_dop_r_4 = p_dop_r_1 + size_int_polotn_w
                        p_dop_polyfabr1_1_1 = APoint(p_dop_r_1, p_2)
                        p_dop_polyfabr1_1_2 = APoint(p_dop_r_1, p_dop_r_2)
                        p_dop_polyfabr1_1_3 = APoint(p_dop_r_4, p_dop_r_2)
                        p_dop_polyfabr1_1_4 = APoint(p_dop_r_4, p_2)
                        # Чертим П.1.1
                        draw_a_drawing(p_dop_polyfabr1_1_1, p_dop_polyfabr1_1_2, p_dop_polyfabr1_1_3, p_dop_polyfabr1_1_4)

                        if tp == 1:
                            p_text_about_dop_p_1_1 = APoint(p_dop_r_1 + (size_int_polotn_w/3), size_of_polotna_l / 2)
                        elif tp == 2:
                            p_text_about_dop_p_1_1 = APoint(p_dop_r_1 + (size_int_polotn_w / 3), size_of_polotna_l - y_size_of_polotna_l / 2)

                        text_dop_pr_p1_1 = acad.model.AddText(f'П - {main_num_of_tp}.1 \n{quantity*quantity_of_p} шт', p_text_about_dop_p_1_1, 100)
                        make_dimension_length(p_dop_polyfabr1_1_1 , p_dop_polyfabr1_1_2)
                        make_dimension_width(p_dop_polyfabr1_1_1, p_dop_polyfabr1_1_4)
                        # Координаты полуфабриката П 1.2 остатки отдельного, dop - дополнительный вид
                        p_dop_polyfabr1_2_1 = APoint(p_dop_r_4 + 1000, p_2)
                        p_dop_polyfabr1_2_2 = APoint(p_dop_r_4 + 1000, p_dop_r_2)
                        p_dop_polyfabr1_2_3 = APoint(p_dop_r_4+ 1000 + width_remains, p_dop_r_2)
                        p_dop_polyfabr1_2_4 = APoint(p_dop_r_4 + 1000 + width_remains, p_2)
                        self.qount_of_product.append(quantity_of_p)
                        print(quantity_of_p)
                        if do_we_have_remains != 0:
                            # Чертим П.1.2
                            draw_a_drawing(p_dop_polyfabr1_2_1, p_dop_polyfabr1_2_2, p_dop_polyfabr1_2_3, p_dop_polyfabr1_2_4)
                            if tp == 1:
                                p_text_about_dop_p_1_2 = APoint(p_dop_r_4 + 1000 + (width_remains/4), size_of_polotna_l / 2)
                            elif tp == 2:
                                p_text_about_dop_p_1_2 = APoint(p_dop_r_4 + 1000 + (width_remains / 4), size_of_polotna_l - y_size_of_polotna_l / 2)
                            text_dop_pr_p1_2 = acad.model.AddText(f'П - {main_num_of_tp}.2 \n{quantity} шт', p_text_about_dop_p_1_2, 100)
                            make_dimension_length(p_dop_polyfabr1_2_1 , p_dop_polyfabr1_2_2)
                            make_dimension_width(p_dop_polyfabr1_2_1, p_dop_polyfabr1_2_4)
                            self.qount_of_product.append('1')
                        # Выносим второй слой отдельно
                        p_second_layer_dop_11 = p_dop_r_4 + 3000 + width_remains
                        p_second_layer_dop_12 = size_of_tp_length - 100 * 2
                        p_second_layer_dop_14 = p_dop_r_4 + 3000 + width_remains + 300
                        # Координаты Второй Слой
                        p_sl_1_dop_1 = APoint(p_second_layer_dop_11, p_2)
                        p_sl_1_dop_2 = APoint(p_second_layer_dop_11, p_second_layer_dop_12)
                        p_sl_1_dop_3 = APoint(p_second_layer_dop_14, p_second_layer_dop_12)
                        p_sl_1_dop_4 = APoint(p_second_layer_dop_14, p_2)
                        # Чертим В 1 отдельно
                        if self.secondlayout_checkBox.isChecked():
                            draw_a_drawing(p_sl_1_dop_1, p_sl_1_dop_2, p_sl_1_dop_3, p_sl_1_dop_4)
                            p_text_about_dop_sl_1 = APoint(p_second_layer_dop_11 + 300 / 4, y_text_about_dop )
                            text_dop_pr_sl_1 = acad.model.AddText(f'В - {main_num_of_tp}.1 \n{quantity} шт', p_text_about_dop_sl_1, 100)
                            self.data_of_product.append(f'В-{main_num_of_tp}.1')
                            self.qount_of_product.append('1')
                            self.width_of_product.append('300')
                            self.length_of_product.append(add_lenght_of_second_layout)
                            make_dimension_length(p_sl_1_dop_1, p_sl_1_dop_2)
                            make_dimension_width(p_sl_1_dop_1, p_sl_1_dop_4)
                        # Чертим Нащельники отдельно
                        # Точки нащельника 1 в
                        p_batten_1v_dop_1 = APoint(p_second_layer_dop_14 + 1000, p_2)
                        p_batten_1v_dop_2 = APoint(p_second_layer_dop_14 + 1000, size_of_batten_1v_length)
                        p_batten_1v_dop_3 = APoint(p_second_layer_dop_14 + 1000 + size_of_batten_1v_width, size_of_batten_1v_length)
                        p_batten_1v_dop_4 = APoint(p_second_layer_dop_14 + 1000 + size_of_batten_1v_width, p_2)
                        # Чертим Н 1 вертик отдельно
                        draw_a_drawing(p_batten_1v_dop_1, p_batten_1v_dop_2, p_batten_1v_dop_3, p_batten_1v_dop_4)
                        p_text_about_dop_b11 = APoint(p_second_layer_dop_14 + 1000 + (size_of_batten_1v_width/4), y_text_about_dop )
                        if tp == 1:
                            text_dop_pr_b11 = acad.model.AddText(f'Н - {main_num_of_tp}.1 \n{quantity * 2} шт',  p_text_about_dop_b11 , 100)
                            self.qount_of_product.append('2')
                        else:
                            text_dop_pr_b11 = acad.model.AddText(f'Н - {main_num_of_tp}.1 \n{quantity} шт', p_text_about_dop_b11, 100)
                            self.qount_of_product.append('1')

                        self.width_of_product.append(size_of_batten_1v_width)
                        self.length_of_product.append(dem_const_batten_1v_length)
                        self.data_of_product.append(f'Н-{main_num_of_tp}.1')
                        make_dimension_length(p_batten_1v_dop_1 , p_batten_1v_dop_2)
                        make_dimension_width(p_batten_1v_dop_1, p_batten_1v_dop_4)
                        # Точки нащельника 2
                        p_batten_2g_dop_1 = APoint(p_second_layer_dop_14 + 2000  + size_of_batten_1v_width, p_2)
                        p_batten_2g_dop_2 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width, size_of_batten_2g_length)
                        p_batten_2g_dop_3 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + size_of_batten_2g_width, size_of_batten_2g_length)
                        p_batten_2g_dop_4 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + size_of_batten_2g_width, p_2)
                        # Чертим Н 2 гориз отдельно
                        draw_a_drawing(p_batten_2g_dop_1, p_batten_2g_dop_2, p_batten_2g_dop_3, p_batten_2g_dop_4)
                        p_text_about_dop_b12 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + (size_of_batten_1v_width / 4), y_text_about_dop )

                        if type_of_tp == 'ТП-1':
                            text_dop_pr_b12 = acad.model.AddText(f'Н - {main_num_of_tp}.2 \n{quantity} шт',  p_text_about_dop_b12, 100)
                            self.qount_of_product.append('1')
                        if type_of_tp == 'ТП-2':
                            text_dop_pr_b12 = acad.model.AddText(f'Н - {main_num_of_tp}.2 \n{quantity * 2} шт', p_text_about_dop_b12, 100)
                            self.qount_of_product.append('2')

                        self.data_of_product.append(f'Н-{main_num_of_tp}.2')
                        self.width_of_product.append(size_of_batten_2g_width)
                        self.length_of_product.append(dem_const_batten_2g_length)
                        make_dimension_length(p_batten_2g_dop_1, p_batten_2g_dop_2)
                        make_dimension_width(p_batten_2g_dop_1, p_batten_2g_dop_4)

                        if self.pocket_checkBox.isChecked():
                            p_pocket_km_dop_1 = APoint(p_second_layer_dop_14 + 2000  + size_of_batten_1v_width + 2500, p_2)
                            p_pocket_km_dop_2 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500, y_pocket_lenght)
                            p_pocket_km_dop_3 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500 + 150,
                                                       y_pocket_lenght)
                            p_pocket_km_dop_4 = APoint(p_second_layer_dop_14 + 2000 + size_of_batten_1v_width + 2500 + 150,
                                                       p_2)
                            draw_a_drawing(p_pocket_km_dop_1, p_pocket_km_dop_2, p_pocket_km_dop_3, p_pocket_km_dop_4)
                            p_text_about_dop_km = APoint(
                                p_second_layer_dop_14 + 4500 + size_of_batten_1v_width + (size_of_batten_1v_width / 4),
                                y_text_about_dop)
                            text_dop_km = acad.model.AddText(f'КМ - {main_num_of_tp}.2 \n{quantity} шт', p_text_about_dop_km,
                                                                 100)
                            make_dimension_length(p_pocket_km_dop_1, p_pocket_km_dop_2)
                            make_dimension_width(p_pocket_km_dop_1, p_pocket_km_dop_4)
                            self.data_of_product.append(f'КМ-{main_num_of_tp}.2')
                            self.qount_of_product.append('1')
                            self.width_of_product.append('150')
                            self.length_of_product.append(dem_const_pocket_length)

                        # Форматы format()
                        name_format = workbook.add_format(
                            {'border': 1, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
                        name_format_main = workbook.add_format(
                            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
                        special_numb = workbook.add_format(
                            {'border': 1, 'num_format': '#0', 'align': 'center', 'valign': 'vcenter'})
                        float_numb_w_board = workbook.add_format(
                            {'border': 1, 'num_format': '#0.00', 'align': 'center', 'valign': 'vcenter'})
                        numb_w_border = workbook.add_format(
                            {'num_format': '#0.00', 'align': 'center', 'valign': 'vcenter'})
                        name_merge_format = workbook.add_format({
                            'align': 'center',
                            'valign': 'vcenter',
                            'num_format': '#0',
                        })
                        name_merge_format_right = workbook.add_format({
                            'align': 'right',
                            'valign': 'vcenter',
                            'num_format': '#0',
                        })
                        worksheet_0 = workbook.add_worksheet(f'Спецификация {type_of_tp}.{tp}')
                        # Размер колонок
                        size_of_column = [14, 20, 14, 17, 19, 13, 14]
                        num_of_colmn = 0
                        for size in size_of_column:
                            worksheet_0.set_column(num_of_colmn, num_of_colmn, size)
                            num_of_colmn += 1
                        worksheet_0.merge_range(0, 0, 0, 8, f'Спецификация по тентовому полотну {type_of_tp}.{tp}',
                                                name_merge_format)
                        row_name = ['Поз', 'Обозначение', 'Наименование', 'Ширина, мм',
                                    'Длина, мм', 'Кол-во на 1 полотно, шт', 'Кол-во итого, шт', 'Площадь ед., м2',
                                    'Площадь итого, м2']
                        curnt_numb_row = 7
                        num = 1
                        worksheet_0.write_row(1, 0, row_name, name_format)
                        count_row = len(self.data_of_product)
                        num_for_formuls = 3
                        current_row = 2
                        plotnost_polotna = ''
                        if self.count_doubleSpinBox_2.value() == 2510:
                            plotnost_polotna = 'ПВХ - 650 г/м2'
                        elif self.count_doubleSpinBox_2.value() == 3010:
                            plotnost_polotna = 'ПВХ - 900 г/м2'
                        else:
                            plotnost_polotna = '------'

                        for prod in self.data_of_product:
                            # Поз
                            worksheet_0.write(current_row, 0, num, special_numb)
                            # Марка
                            worksheet_0.write(current_row, 1, str(prod), special_numb)
                            # Наименование
                            worksheet_0.write(current_row, 2, str(plotnost_polotna), special_numb)
                            # Общее количество
                            worksheet_0.write_formula(current_row, 6, f'=F{num_for_formuls}*{quantity}',
                                                      special_numb)
                            # Площадь 1
                            worksheet_0.write_formula(current_row, 7,
                                                      f'=D{num_for_formuls}*E{num_for_formuls} / 1000000',
                                                      float_numb_w_board)
                            # Площадь Итого
                            worksheet_0.write_formula(current_row, 8,
                                                      f'=H{num_for_formuls}*G{num_for_formuls}',
                                                      float_numb_w_board)
                            num += 1
                            current_row +=1
                            num_for_formuls +=1

                        current_row = 2
                        # Количество ед
                        for qount in self.qount_of_product:
                            worksheet_0.write(current_row, 5, int(qount), special_numb)
                            current_row += 1

                        current_row = 2
                        # Ширина
                        for width in self.width_of_product:
                            worksheet_0.write(current_row, 3, float(width), float_numb_w_board)
                            current_row += 1
                            print(width)
                        # КДлина
                        current_row = 2
                        for length in self.length_of_product:
                            worksheet_0.write(current_row, 4, float(length), float_numb_w_board)
                            current_row += 1
                        worksheet_0.merge_range(current_row, 0, current_row, 7, f'Итого {type_of_tp}.{tp}:',
                                                name_merge_format_right)
                        worksheet_0.write(current_row, 8, f'=SUM(I3:I{current_row})', special_numb)
                        self.data_of_product.clear()
                        self.qount_of_product.clear()
                        self.length_of_product.clear()
                        self.width_of_product.clear()
                        quantity = quantity_of_tp12
                        y_pocket_in_main_pic += size_of_batten_2g_length + size_of_tp_length
                        y_pocket_lenght += size_of_batten_2g_length + size_of_tp_length
                        y_batten_vertic += size_of_batten_2g_length + size_of_tp_length
                        p_2 += size_of_batten_2g_length + size_of_tp_length
                        p_for_text_2 += size_of_batten_2g_length + size_of_tp_length
                        y_text_about_dop += size_of_batten_2g_length + size_of_tp_length
                        p_razmer_6 += size_of_batten_2g_length + size_of_tp_length - 500
                        p_razmer_4 += size_of_batten_2g_length + size_of_tp_length
                        p_razmer_2 += size_of_batten_2g_length + size_of_tp_length - 100.0
                        y_point_batten_2g_width += size_of_batten_2g_length + size_of_tp_length
                        size_of_polotna_l += size_of_batten_2g_length + size_of_tp_length
                        size_of_batten_1v_length += size_of_batten_2g_length + size_of_tp_length
                        old_size_batten_2g_length = size_of_batten_2g_length
                        size_of_batten_2g_length += size_of_batten_2g_length + size_of_tp_length
                        size_of_tp_length += old_size_batten_2g_length + size_of_tp_length
                    workbook.close()
                    os.startfile(f'Спецификация\Спецификация.xlsx')
                except:
                    error = 'Ошибка записи excel. Зайкройте файл Спецификация.xlsx.'
                    self.MainWindow = ErrorAddReport(error)
                    self.MainWindow.show()

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
                    draw_and_count_the_polotno()
                else:
                    pass
            else:
                draw_and_count_the_polotno()

        except:
            error = 'Ошибка. Автокад не запущен. Запустите автокад с чертежным видом и попробуйте снова.'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()

    def draw_tp3_btn(self):
        try:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True
            acadModel = acad.ActiveDocument.ModelSpace

            def APoint(x, y, z=0):
                return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))

            def aDouble(xyz):
                return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, xyz)

            def aVariant(vObject):
                return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, vObject)

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

            def draw_a_drawing_4coord(point_1, point_2, point_3, point_4):
                acadModel.AddLine(point_1, point_2)
                acadModel.AddLine(point_2, point_3)
                acadModel.AddLine(point_3, point_4)
                acadModel.AddLine(point_4, point_1)

            def draw_a_drawing_5coord(point_1, point_2, point_3, point_4, point_5):
                line_1 = acadModel.AddLine(point_1, point_2)
                line_2 = acadModel.AddLine(point_2, point_3)
                line_3 = acadModel.AddLine(point_3, point_4)
                line_4 = acadModel.AddLine(point_4, point_5)
                line_5 = acadModel.AddLine(point_5, point_1)
                list_ofline = [line_1, line_2, line_3, line_4, line_5]
                for line in list_ofline:
                    print(line.Offset(-150))

            def make_dimension_height(first_point, scond_point, third_point, forth_point, otstup):
                # Размер по длине
                f_point = APoint(first_point, scond_point)
                s_point = APoint(third_point, forth_point)
                p_razmer_first = first_point - otstup
                p_razmer_second = forth_point - 100.0
                p_razmer_l = APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(f_point, s_point, p_razmer_l)

            def make_dimension_width(first_point, scond_point, third_point, forth_point):
                # Размер по ширине
                f_point = APoint(first_point, scond_point)
                s_point = APoint(third_point, forth_point)
                size_of_batten_2g_height = self.batten_2g_height_doubleSpinBox_3.value()
                p_razmer_first = first_point - size_of_batten_2g_height - 500
                p_razmer_second = scond_point - size_of_batten_2g_height - 500
                p_razmer_w = APoint(p_razmer_first, p_razmer_second)
                acadModel.AddDimAligned(f_point, s_point, p_razmer_w)

            # Назначаем точки для конструкции
            # Чертим Торец ангара по размерам заданным
            # Точки торца ангара
            points_wall_end = aDouble([p_x_1, p_y_1, p_x_1, p_y_2, p_x_2, p_y_3, p_x_3, p_y_2, p_x_3, p_y_1, p_x_1, p_y_1])
            # Чертим торец ангара с помощью полилинии
            well_end_drawing = acadModel.AddLightWeightPolyline(points_wall_end)
            # Добавляем информацию о полотне в списки
            self.data_of_product.append('ТП-3')
            self.qount_of_product.append(1)
            self.width_of_product.append(x_batten_2 - 150)
            self.length_of_product.append(y_height_dim_2 - 150)
            self.area_of_product.append(full_area_tp_3)
            # Смещаем полилинию
            tp3_offset = well_end_drawing.Offset(150)
            # Контур Второго слоя
            tp3_offset_for_sl = well_end_drawing.Offset(250)
            well_end_drawing.Delete()
            # Назначаем точки для конструкции
            # Точки нащельника
            points_batten = aDouble(
                [x_batten_1, y_batten_1, x_batten_2, y_batten_1, x_batten_2, y_batten_2, x_batten_1, y_batten_2, x_batten_1,
                 y_batten_1])
            # Чертим нащельник c помощью полилинии
            batten_drawing = acadModel.AddLightWeightPolyline(points_batten)
            # Добавляем информацию о нащельнике в списки
            self.data_of_product.append('Н')
            self.width_of_product.append(x_batten_2 - 150)
            self.length_of_product.append(size_of_batten_2g_height)
            self.area_of_product.append(full_area_batten)
            self.qount_of_product.append(1)
            # Считаем количетсво вторых слоев
            # Средняя линия точки
            align_line_1 = APoint(with_end_face / 2, 0)
            align_line_2 = APoint(with_end_face / 2, full_height)
            step_of_sl = self.step_bw_sl_doubleSpinBox.value()
            if self.secondlayout_checkBox.isChecked():
                quantity_of_sl = math.ceil(
                    (with_end_face / 2 - self.size_to_sl_doubleSpinBox.value()) / step_of_sl)
                print(quantity_of_sl)
                count_sl = 1
                if quantity_of_sl != 0:
                    for sl in range(quantity_of_sl):
                        # Точки второго слоя
                        points_sl = aDouble(
                            [x_slayout_1, y_slayout_1, x_slayout_1, y_slayout_2, x_slayout_2, y_slayout_2, x_slayout_2,
                             y_slayout_1])
                        # Чертим второй слой с помощью полилинии
                        secondl_drawing = acadModel.AddLightWeightPolyline(points_sl)
                        secondl_drawing.Mirror(align_line_1, align_line_2)
                        x_slayout_1 += step_of_sl
                        x_slayout_2 += step_of_sl
                        self.data_of_product.append(f'В-3.{count_sl}')
                        self.width_of_product.append(100)
                        self.length_of_product.append(0)
                        self.area_of_product.append(0)
                        self.qount_of_product.append(2)
                        count_sl += 1
                else:
                    points_sl = aDouble(
                        [x_slayout_1, y_slayout_1, x_slayout_1, y_slayout_2, x_slayout_2, y_slayout_2, x_slayout_2,
                         y_slayout_1])
                    # Чертим второй слой с помощью полилинии
                    secondl_drawing = acadModel.AddLightWeightPolyline(points_sl)
                    secondl_drawing.Mirror(align_line_1, align_line_2)
                    self.data_of_product.append(f'В-3.{count_sl}')
                    self.width_of_product.append(100)
                    self.length_of_product.append(0)
                    self.area_of_product.append(0)
                    self.qount_of_product.append(2)

            if self.pocket_checkBox.isChecked():
                # Координаты для кармана КМ
                x_pocket_1 = with_end_face / 2 - ((with_end_face / 2) / 3) * 2 + 400
                y_pocket_1 = ((full_height - wall_height) / 4) + wall_height
                x_pocket_2 = with_end_face - x_pocket_1
                y_pocket_2 = y_pocket_1 + 150
                # Точки кармана
                points_pocket = aDouble(
                    [x_pocket_1, y_pocket_1, x_pocket_1, y_pocket_2, x_pocket_2, y_pocket_2, x_pocket_2, y_pocket_1, x_pocket_1,
                     y_pocket_1])
                points_drawing = acadModel.AddLightWeightPolyline(points_pocket)
                # Cчитаем площадь кармана
                full_area_pocket = (x_pocket_2 - x_pocket_1) * 150 / 1000000
                self.data_of_product.append(f'КМ-3.1')
                self.width_of_product.append(x_pocket_2 - x_pocket_1)
                self.length_of_product.append(150)
                self.area_of_product.append(full_area_pocket)
                self.qount_of_product.append(1)
            # Cтавим размер полотна по высоте
            make_dimension_height(x_zero_dim_1, y_zero_dim_1, x_height_dim_2, y_height_dim_2, 1500)
            # Cтавим размер высоты стенки полотна
            make_dimension_height(x_zero_dim_1, y_zero_dim_1, x_height_dim_2, y_height_wall_dim_2, 500)
            # Cтавим размер по ширине стенки
            make_dimension_width(x_zero_dim_1, y_zero_dim_1, x_width_dim_3, y_zero_dim_1)
        except:
            error = 'Ошибка. Автокад не запущен. Запустите автокад с чертежным видом и попробуйте снова.'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()
        try:
            workbook = xlsxwriter.Workbook(f'Спецификация/Спецификация ТП3.xlsx')
            # Форматы format()
            name_format = workbook.add_format(
                {'border': 1, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            name_format_main = workbook.add_format(
                {'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            special_numb = workbook.add_format(
                {'border': 1, 'num_format': '#0', 'align': 'center', 'valign': 'vcenter'})
            float_numb_w_board = workbook.add_format(
                {'border': 1, 'num_format': '#0.00', 'align': 'center', 'valign': 'vcenter'})
            numb_w_border = workbook.add_format(
                {'num_format': '#0.00', 'align': 'center', 'valign': 'vcenter'})
            name_merge_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'num_format': '#0',
            })
            name_merge_format_right = workbook.add_format({
                'align': 'right',
                'valign': 'vcenter',
                'num_format': '#0',
            })
            worksheet_0 = workbook.add_worksheet(f'Спецификация ТП3')
            # Размер колонок
            size_of_column = [14, 20, 14, 17, 19, 13, 14]
            num_of_colmn = 0
            for size in size_of_column:
                worksheet_0.set_column(num_of_colmn, num_of_colmn, size)
                num_of_colmn += 1
            worksheet_0.merge_range(0, 0, 0, 8, f'Спецификация по тентовому полотну ТП3',
                                    name_merge_format)
            row_name = ['Поз', 'Обозначение', 'Наименование', 'Ширина, мм',
                        'Длина, мм', 'Кол-во на 1 полотно, шт', 'Кол-во итого, шт', 'Площадь ед., м2',
                        'Площадь итого, м2']
            curnt_numb_row = 7
            num = 1
            worksheet_0.write_row(1, 0, row_name, name_format)
            count_row = len(self.data_of_product)
            num_for_formuls = 3
            current_row = 2
            plotnost_polotna = 'ПВХ'

            for prod in self.data_of_product:
                # Поз
                worksheet_0.write(current_row, 0, num, special_numb)
                # Марка
                worksheet_0.write(current_row, 1, str(prod), special_numb)
                # Наименование
                worksheet_0.write(current_row, 2, str(plotnost_polotna), special_numb)
                # Общее количество
                worksheet_0.write_formula(current_row, 6, f'=F{num_for_formuls}*{2}',
                                          special_numb)
                # Площадь Итого
                worksheet_0.write_formula(current_row, 8, f'=H{num_for_formuls}*G{num_for_formuls}', float_numb_w_board)
                num += 1
                current_row += 1
                num_for_formuls += 1

            current_row = 2
            # Количество ед
            for qount in self.qount_of_product:
                worksheet_0.write(current_row, 5, int(qount), special_numb)
                current_row += 1

            current_row = 2
            # Ширина
            for width in self.width_of_product:
                worksheet_0.write(current_row, 3, float(width), float_numb_w_board)
                current_row += 1
                print(width)

            current_row = 2
            # Площадь
            for area in self.area_of_product:
                worksheet_0.write(current_row, 7, float(area), float_numb_w_board)
                current_row += 1
            # Длина
            current_row = 2
            for length in self.length_of_product:
                worksheet_0.write(current_row, 4, float(length), float_numb_w_board)
                current_row += 1
            worksheet_0.merge_range(current_row, 0, current_row, 7, f'Итого ТП-3:',
                                    name_merge_format_right)
            worksheet_0.write(current_row, 8, f'=SUM(I3:I{current_row})', float_numb_w_board)
            current_row += 1
            workbook.close()
            os.startfile(f'Спецификация\Спецификация ТП3.xlsx')
        except:
            error = 'Ошибка запуска excel-файла. Возможно файл открыт, либо в редактируемом стостоянии.'
            self.MainWindow = ErrorAddReport(error)
            self.MainWindow.show()

        self.data_of_product.clear()
        self.width_of_product.clear()
        self.length_of_product.clear()
        self.area_of_product.clear()
        self.qount_of_product.clear()


class ErrorAddReport(QDialog):
    def __init__(self, data):
        super().__init__()
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
    app.setWindowIcon(QIcon('images/program_logo.png'))
    MainWindow = Main_menu()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
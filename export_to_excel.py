import ast
import locale
import math
import os
import re
from datetime import datetime

import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements
import xlsxwriter


class ExcelExport:
    def __init__(self, quantity, material, dict_of_data):
        super().__init__()
        # Стандартные величины
        self.report_main = dict_of_data
        self.type_of_tp = dict_of_data.keys()
        self.curnt_special_row_for_1w = 2  # для первого листа
        self.quantity = quantity
        self.material = material
        print(self.type_of_tp)
        print(self.quantity, self.material, self.report_main)
        # Получаем даты
        # Словарь номер месяца - название месяца
        locale.setlocale(locale.LC_ALL, 'ru_RU')
        propertys_for_wb = {
            'title': f'Спецификация материала ТП',
            'subject': 'With document properties',
            'author': 'Ivan Metliaev',
            'manager': '',
            'company': 'Тентовые конструкции',
            'category': 'ПВХ-полотна',
            'keywords': 'ПВХ, Ангары, Тент',
            'created': datetime.today(),
            'comments': 'Created with Python and Ivan Metliaev program'}
        self.workbook = xlsxwriter.Workbook(f'Спецификация/Спецификация.xlsx')  # Создаем файл excel
        # Свойства файла
        self.workbook.set_properties(propertys_for_wb)
        # Форматы format()
        self.percent_format = self.workbook.add_format(
            {'border': 1, 'num_format': '0.00%', 'align': 'left', 'valign': 'vcenter'})
        self.percent_format_for_plan = self.workbook.add_format(
            {'num_format': '0.00%', 'color': 'red', 'align': 'left', 'valign': 'vcenter'})
        self.name_format = self.workbook.add_format(
            {'border': 1, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        self.name_format_without_bold = self.workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        self.name_format_main = self.workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        self.date_format = self.workbook.add_format(
            {'border': 1, 'text_wrap': True, 'num_format': 'dd MMM yy', 'align': 'center', 'valign': 'vcenter'})
        self.date_format_main = self.workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd MMM yy', 'align': 'center', 'valign': 'vcenter'})
        self.ready_numb = self.workbook.add_format(
            {'border': 1, 'num_format': '#0', 'align': 'center', 'valign': 'vcenter', 'fg_color': '#A8FF37'})
        self.nothing_numb = self.workbook.add_format(
            {'border': 1, 'num_format': '#0', 'align': 'center', 'valign': 'vcenter', 'fg_color': '#8088A0'})
        self.special_numb = self.workbook.add_format(
            {'border': 1, 'num_format': '#0', 'align': 'center', 'valign': 'vcenter'})
        self.float_numb_w_board = self.workbook.add_format(
            {'border': 1, 'num_format': '0.00', 'align': 'center', 'valign': 'vcenter'})
        self.numb_w_border = self.workbook.add_format(
            {'num_format': '#0.00', 'align': 'center', 'valign': 'vcenter'})
        # Форматы для объединнеых ячеек
        self.name_merge_format = self.workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#0',
        })
        self.name_merge_format_main = self.workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#0',
            'bold': True
        })
        self.name_merge_format_spec = self.workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#0',
            'bold': True
        })
        self.name_merge_format_spec_2 = self.workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#0',
            'bold': True
        })
        self.name_merge_format_2 = self.workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#0',
            'fg_color': '#DDEBF7'
        })
        # Названия колонок
        column_name = ['Поз', 'Обозначение', 'Наименование', 'Ширина, мм',
                       'Длина, мм', 'Кол-во на 1 полотно, шт', 'Кол-во итого, шт', 'Площадь ед., м2',
                       'Площадь итого, м2']
        # Для каждого типа ТП создаем лист и записываем данные
        for type_of_tp in self.type_of_tp:
            worksheet_0 = self.workbook.add_worksheet(f'Спецификация {type_of_tp}')
            # Размер колонок
            size_of_column = [14, 20, 14, 17, 19, 13, 14]
            num_of_colmn = 0
            for size in size_of_column:
                worksheet_0.set_column(num_of_colmn, num_of_colmn, size)
                num_of_colmn += 1
            worksheet_0.merge_range(0, 0, 0, len(column_name), f'Спецификация по тентовому полотну'
                                                               f' {type_of_tp}',
                                    self.name_merge_format)  # Записываем объедин. строку с названием таблицы
            worksheet_0.write_row(1, 0, column_name, self.name_format)  # Записываем строку наименований колонок
            # Изначальные точки колонок для записи
            current_row = 2
            num = 1
            num_for_formuls = 3
            # Записываем данные в таблицу
            list_of_data = self.report_main[type_of_tp][0]
            for sameproduct_key in list_of_data.keys():
                # Поз
                worksheet_0.write(current_row, 0, num, self.special_numb)
                # Марка
                worksheet_0.write(current_row, 1, sameproduct_key, self.name_format_without_bold)
                # Материал
                worksheet_0.write(current_row, 2, self.material, self.name_format_without_bold)
                # Ширина
                worksheet_0.write(current_row, 3, list_of_data[sameproduct_key][1], self.float_numb_w_board)
                # Длина
                worksheet_0.write(current_row, 4, float(list_of_data[sameproduct_key][2]), self.float_numb_w_board)
                # Количество ТП
                worksheet_0.write(current_row, 5, str(list_of_data[sameproduct_key][0]), self.special_numb)
                # Общее количество
                worksheet_0.write_formula(current_row, 6, f'=F{num_for_formuls}*{self.quantity}',
                                          self.special_numb)
                # Площадь 1
                if sameproduct_key == 'ТП-3':
                    worksheet_0.write(current_row, 7,
                                              float(list_of_data[sameproduct_key][3]), self.float_numb_w_board)
                else:
                    worksheet_0.write_formula(current_row, 7,
                                              f'=D{num_for_formuls}*E{num_for_formuls} / 1000000',
                                              self.float_numb_w_board)
                # Площадь Итого
                worksheet_0.write_formula(current_row, 8,
                                          f'=H{num_for_formuls}*G{num_for_formuls}',
                                          self.float_numb_w_board)
                num += 1
                current_row += 1
                num_for_formuls += 1
            worksheet_0.merge_range(current_row, 0, current_row, 7, f'Итого {type_of_tp}:',
                                    self.name_merge_format_2)
            worksheet_0.write(current_row, 8, f'=SUM(I3:I{current_row - 1})', self.float_numb_w_board)
        self.workbook.close()
        os.startfile(f'Спецификация\Спецификация.xlsx')

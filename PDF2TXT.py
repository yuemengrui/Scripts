# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import re
import json
import pdfplumber
from collections import defaultdict


class PDFExtractor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = pdfplumber.open(filepath)
        self.all_text = defaultdict(dict)
        self.all_row = 0

    @staticmethod
    def extract_text_within_a_certain_range(page, top, bottom, left=None, right=None):
        """
        提取范围内的文字。
        如top=100, bottom=200, left=50, right=150, 则提取坐标在[50,100,150,200]区域内的文字
        :param page: 第几页
        :param top: 文字的y_min
        :param bottom: 文字的y_max
        :param left: 文字的x_min
        :param right: 文字的y_max
        :return:
        """
        lines = page.extract_words()[::]
        text = ''
        last_top = 0
        last_text_height = 0
        for l in range(len(lines)):
            each_line = lines[l]

            if each_line['top'] > top and each_line['bottom'] < bottom:
                if last_top == 0:
                    text += each_line['text']
                else:
                    if abs(last_top - each_line['top']) > last_text_height * 2:
                        text += '\n' + each_line['text']
                    else:
                        text += each_line['text']

            last_top = each_line['bottom']
            last_text_height = each_line['bottom'] - each_line['top']

        return text

    @staticmethod
    def extract_table(table):
        r_count = 0
        for r in range(len(table)):
            row = table[r]
            if row[0] is None:
                r_count += 1
                for c in range(len(row)):
                    if row[c] is not None and row[c] not in ['', ' ']:
                        if table[r - r_count][c] is None:
                            table[r - r_count][c] = row[c]
                        else:
                            table[r - r_count][c] += row[c]
                        table[r][c] = None
            else:
                r_count = 0

        new_table = []
        for row in table:
            if row[0] != None:
                cell_list = []
                cell_check = False
                for cell in row:
                    if cell != None:
                        cell = cell.replace('\n', '')
                    else:
                        cell = ''
                    if cell != '':
                        cell_check = True
                    cell_list.append(cell)
                if cell_check == True:
                    new_table.append(cell_list)

        return new_table

    def extract_text_and_tables(self, page):
        text_top = 0
        tables = page.find_tables(table_settings={'intersection_x_tolerance': 1})
        if len(tables) >= 1:
            count = len(tables)
            for table in tables:
                count -= 1
                text = self.extract_text_within_a_certain_range(page, text_top, table.bbox[1])
                text_list = text.split('\n')
                for _t in range(len(text_list)):
                    self.all_text[self.all_row] = {'page': page.page_number, 'row_id': self.all_row,
                                                   'type': 'text', 'content': text_list[_t]}
                    self.all_row += 1

                text_top = table.bbox[3]
                table_data = table.extract()
                new_table = self.extract_table(table_data)
                for row in new_table:
                    self.all_text[self.all_row] = {'page': page.page_number, 'row_id': self.all_row,
                                                   'type': 'table', 'content': row}

                    self.all_row += 1

            text = self.extract_text_within_a_certain_range(page, text_top, page.height)
            text_list = text.split('\n')
            for _t in range(len(text_list)):
                self.all_text[self.all_row] = {'page': page.page_number, 'row_id': self.all_row,
                                               'type': 'text', 'content': text_list[_t]}
                self.all_row += 1
        else:
            text = self.extract_text_within_a_certain_range(page, 0, page.height)
            text_list = text.split('\n')
            for _t in range(len(text_list)):
                self.all_text[self.all_row] = {'page': page.page_number, 'row_id': self.all_row,
                                               'type': 'text', 'content': text_list[_t]}
                self.all_row += 1

    def run_extract(self):
        for page in self.pdf.pages[1:]:
            self.extract_text_and_tables(page)

    def save_all_text(self, path):
        for key in self.all_text.keys():
            with open(path, 'a+', encoding='utf-8') as file:
                file.write(json.dumps(self.all_text[key], ensure_ascii=False) + '\n')

    def save_text(self, path):
        page_list = []
        temp = []
        page_num = 0
        for v in self.all_text.values():
            if page_num == 0:
                temp.append(v)
                page_num = v['page']
            else:
                if page_num == v['page']:
                    temp.append(v)
                else:
                    page_list.append(temp[1:-1])
                    temp = []
                    temp.append(v)
                    page_num = v['page']

        page_list.append(temp[1:-1])

        all_data = []
        for page_data in page_list:
            table = []
            for d in page_data:
                if d['type'] == 'text':
                    if table:
                        text = 'table: '
                        for t in table:
                            text += '\t'.join(t) + '\n'

                        all_data.append('[' + text + ']')
                        table = []

                    if len(d['content']) > 0 and '....................' not in d['content']:
                        all_data.append(d['content'])
                else:
                    table.append(d['content'])

            if table:
                text = 'table: '
                for t in table:
                    text += '\t'.join(t) + '\n'

                all_data.append('[' + text + ']')

        max_length = max([len(x) for x in all_data])
        print(max_length)

        with open(path, 'w') as fff:
            json.dump(all_data, fff, ensure_ascii=False)


if __name__ == '__main__':
    pdf_extractor = PDFExtractor(pdf_path)
    pdf_extractor.run_extract()
    pdf_extractor.save_text(text_path)

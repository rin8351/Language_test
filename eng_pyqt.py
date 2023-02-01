import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QLineEdit, QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import (QFont,QPalette, QColor, QBrush, QPixmap)
import pandas as pd
import ast
import json

class Language(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowss = QFrame()
        self.shet = 0
        self.sh2 = 0
        self.stat = dict()
        self.shet_know = 0
        self.shet_prodol_or_snulya=0 # продолжить незаконченный тест в прошлый раз или весь список проходить
        self.slovo_dlya_povtora_testa=0
        self.shet_for_povtor=0
        self.bez_otvet=[] # массив для слов без ответа, чтобы повторно пройти тест
        self.sp = ['Англ', 'Русс']
        self.vib=[]
        self.data_from_xls()
        self.main()

    def data_from_xls(self):
        self.xl = pd.ExcelFile('Words.xlsx')
        self.df = self.xl.parse('Words')
        self.alls  = self.df.reset_index().to_dict('records')

    def com_vib_dict(self):     
        if self.shet_prodol_or_snulya==1:
            places2 = []
            with open('num_less.txt', 'r') as filehandle:
                for line in filehandle:
                    currentPlace = line[:-1]
                    places2.append(currentPlace)
            self.st=int(places2[0])
            self.en=int(places2[1])
        else:
            self.st = int(self.ent_less.text())
            self.en = int(self.ent_less_end.text())

        if self.st == 0 and self.en == 0:
            er = 'Выберите номера\n уроков'
            self.lb_err.config(text=er, font="Arial 14", fg='red')

        elif self.st > self.en:
            er = 'Номер конечного урока\n должен быть больше\n начального'
            self.lb_err.config(text=er, font="Arial 14", fg='red')

        else:
            self.alls2 = []
            new_stat = {'Words': {}}
            self.alls_all_sheet = {}
            for i in new_stat:
                df_l = self.xl.parse(i)
                self.alls_all_sheet[i] = df_l.reset_index().to_dict('records')

            for i in self.alls:
                if i['Lesson'] >= self.st and i['Lesson'] <= self.en:
                    self.alls2.append(i)
            self.alls = self.alls2

            with open('stat.txt',encoding='utf-8') as f:
                data = f.read()
            self.stat = ast.literal_eval(data)
            if self.stat == {}:
                self.stat = {'Words': {}}
            alls_coly = self.alls_all_sheet.copy()
            for s in alls_coly:
                sp_all_cop = ['Англ', 'Русс']
                for i in alls_coly[s]:
                    j_dict = {}
                    for j in i:
                        if j in sp_all_cop and type(i[j]) != int and i[j] != '0':
                            j_dict[i[j]] = 0
                    num_str = str(i['Num'])
                    new_stat[s][num_str] = j_dict

            for k in new_stat:
                for i in new_stat[k]:
                    if i not in self.stat[k]:
                        self.stat[k][i] = {}
                    if self.stat[k][i] != new_stat[k][i]:
                        new_line = {}
                        for f in new_stat[k][i]:
                            if f not in self.stat[k][i]:
                                self.stat[k][i][f] = 0
                            stat_copy = self.stat[k].copy()
                            new_line[f] = stat_copy[i][f]
                            self.stat[k][i].pop(f)
                        self.stat[k][i] = new_line
            stat_copy = self.stat.copy()
            for i in stat_copy:
                copy_3 = stat_copy[i].copy()
                for j in copy_3:
                    if j not in new_stat[i]:
                        del self.stat[i][j]

            with open('stat.txt', 'w+', encoding='utf-8') as fle:
                json.dump(self.stat, fle, indent='    ', ensure_ascii=False)


    def main(self):
        self.frame_main = QFrame()
        self.frame_up = QFrame()
        font = QFont("Times", 10)
        nbur=[]
        for i in self.alls:
            nbur.append(i['Lesson'])
        self.lb_start = QLabel('Первый урок')
        self.lb_start.setFont(font)
        self.ent_less = QLineEdit(text='0')
        self.lb_end = QLabel('Последний урок')
        self.lb_end.setFont(font)
        self.ent_less_end = QLineEdit(text=str(max(nbur)))
        self.ent_less.setFixedWidth(50)
        self.ent_less_end.setFixedWidth(50)
        self.lb_err = QLabel()
        font_error = QFont("Times", 12)
        self.lb_err.setStyleSheet("color: red")
        self.lb_err.setFont(font_error)
        self.frame_down = QFrame()
        self.lb_max_ur = QLabel(f'Всего уроков = {max(nbur)}')
        self.lb_max_ur.setFont(font)
        self.check_r_or_st = QCheckBox('Если стоит галочка- показывать рандомно')
        self.choose_lang = QLabel('Выберите язык')
        self.choose_lang .setFont(font)
        self.sp = ['Англ', 'Русс']
        self.radios = []
        for i in self.sp:
            rb = QRadioButton(i)
            self.radios.append(rb)
        self.btn3 = QPushButton("Начать")

        layout_frame_up = QVBoxLayout()
        layout_frame_up.addWidget(self.lb_start)
        layout_frame_up.addWidget(self.ent_less)
        layout_frame_up.addWidget(self.lb_end)
        layout_frame_up.addWidget(self.ent_less_end)
        self.frame_up.setLayout(layout_frame_up)

        layout_frame_down = QVBoxLayout()
        layout_frame_down.addWidget(self.lb_max_ur)
        layout_frame_down.addWidget(self.check_r_or_st)
        layout_frame_down.addWidget(self.choose_lang)
        for rb in self.radios:
            layout_frame_down.addWidget(rb)
        layout_frame_down.addWidget(self.lb_err)
        layout_frame_down.addWidget(self.btn3)
        self.frame_down.setLayout(layout_frame_down)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_up)
        main_layout.addWidget(self.frame_down)
        self.frame_main.setLayout(main_layout)
        self.setCentralWidget(self.frame_main)
        self.btn3.clicked.connect(self.checks)

    def checks(self):
        for rb in self.radios:
            if rb.isChecked():
                self.vib  = rb.text()
                break
        if self.vib == []:
            self.lb_err.setText('Выберите язык')
        else:
            self.lb_err.setText('')
            self.menu2()

    def menu2(self):
        self.frame_main.deleteLater()
        self.frame_main = QFrame()
        self.frame_up2 = QFrame()
        self.frame_down2 = QFrame()
        self.btn_back = QPushButton("В начальное меню")
        self.btn_save = QPushButton("Сохранить")

        layout_frame_up = QHBoxLayout()
        layout_frame_up.addWidget(self.btn_back)
        layout_frame_up.addWidget(self.btn_save)
        self.frame_up2.setLayout(layout_frame_up)

        self.btn_continue = QPushButton("Продолжить")
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setFixedWidth(100)
        self.txt_knowledge = QLabel("Знаешь?")
        self.label_stat = QLabel("Статистика слова")
        self.label_total = QLabel("Всего слов")
        self.label_question = QLabel("")
        self.label_answer = QLabel("")
        layout_frame_down = QVBoxLayout()
        layout_frame_down.addWidget(self.btn_continue)
        layout_frame_down.addWidget(self.txt_knowledge)
        layout_frame_down.addWidget(self.label_stat)
        layout_frame_down.addWidget(self.label_total)
        layout_frame_down.addWidget(self.label_question)
        layout_frame_down.addWidget(self.label_answer)
        self.frame_down2.setLayout(layout_frame_down)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_up2)
        main_layout.addWidget(self.frame_down2)
        self.frame_main.setLayout(main_layout)
        self.setCentralWidget(self.frame_main)
        self.btn_back.clicked.connect(self.back)
        self.btn_continue.clicked.connect(self.continue_)

    def continue_(self):
        self.label_question.setText("Привет")
        self.label_answer.setText("Hello")

    def back(self):
        self.frame_main.deleteLater()
        self.main()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    language = Language()
    language.show()
    # set window size
    language.setFixedSize(400, 400)
    # set color
    language.setStyleSheet("background-color: #E6E6FA;")
    sys.exit(app.exec_())
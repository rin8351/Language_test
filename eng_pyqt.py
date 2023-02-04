import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QLineEdit, QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import (QFont,QPalette, QColor, QBrush, QPixmap)
import pandas as pd
import ast
import json
import random

class Language(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowss = QFrame()
        self.shet = 0
        self.stat = dict()
        self.shet_know = 0
        self.shet_prodol_or_snulya=0 # продолжить незаконченный тест в прошлый раз или весь список проходить
        self.slovo_dlya_povtora_testa=0
        self.shet_for_povtor=0
        self.bez_otvet=[] # массив для слов без ответа, чтобы повторно пройти тест
        self.sp = ['Англ', 'Русс']
        self.vib=[]
        self.check_value =False
        self.test_is_filled = False
        self.data_from_xls()
        self.main()

    def data_from_xls(self):
        self.xl = pd.ExcelFile('Words.xlsx')
        self.df = self.xl.parse('Words')
        self.alls  = self.df.reset_index().to_dict('records')

    def com_vib_dict(self):   # Проверка и сравнение текстового файла Words и словаря в файле stat.txt
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
        self.sh2 = 0
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
        self.check_r_or_st = QCheckBox('Показывать слова рандомно')
        self.choose_lang = QLabel('Выберите язык')
        self.choose_lang .setFont(font)
        self.radios = []
        for i in self.sp:
            rb = QRadioButton(i)
            self.radios.append(rb)
        self.btn3 = QPushButton("Начать тест")
        self.btn_witn_zero = QPushButton("Пройти тест с нуля")
        self.but_contin = QPushButton("Продолжить\n сохраненный тест")
        self.clear_save = QPushButton("Очистить\n сохраненный тест")
        self.clear_save.setVisible(False)
        self.but_contin.setVisible(False)
        self.btn_witn_zero.setVisible(False)
        with open('sohranen.txt', 'r') as f:
            if f.read():
                self.but_contin.setVisible(True)
                self.clear_save.setVisible(True)
                self.btn3.setText('Начать тест с нуля')
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
        layout_frame_down.addWidget(self.btn_witn_zero)
        layout_frame_down.addWidget(self.but_contin)
        layout_frame_down.addWidget(self.clear_save)
        self.frame_down.setLayout(layout_frame_down)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_up)
        main_layout.addWidget(self.frame_down)
        self.frame_main.setLayout(main_layout)
        self.setCentralWidget(self.frame_main)
        self.btn3.clicked.connect(self.checks)
        self.but_contin.clicked.connect(self.continue_funk)
        self.clear_save.clicked.connect(self.ochist_file)
        self.btn_witn_zero.clicked.connect(self.checks_zero)

    def checks_zero(self):
        self.data_from_xls()
        self.over()
        self.sh2 = 0
        self.checks()

    def continue_funk(self):
        self.shet_prodol_or_snulya +=1
        with open('sohranen.txt',encoding='utf-8') as f:
            data = f.read()
        self.test_from_file = ast.literal_eval(data)
        places2 = []
        with open('num_less.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                places2.append(currentPlace)
        places3 = []
        with open('for_sohr.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                places3.append(currentPlace)
        self.vib=places3[0]
        self.for_table_sp=places3[1].split(",")  
        self.checks() 
        self.com_vib_dict()
        self.testting()

    def checks(self):
        self.check_value = self.check_r_or_st.isChecked()
        for rb in self.radios:
            if rb.isChecked():
                self.vib  = rb.text()
                break
        if self.vib == []:
            self.lb_err.setText('Выберите язык')
        else:
            self.lb_err.setText('')
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
                self.lb_err.setText('Выберите номера\n уроков')

            elif self.st > self.en:
                self.lb_err.setText('Номер конечного урока\n должен быть больше\n начального')
            else:
                self.com_vib_dict()
                self.menu2()

    def menu2(self):
        self.frame_main.deleteLater()
        self.frame_main = QFrame()
        self.frame_up2 = QFrame()
        self.frame_down2 = QFrame()
        self.frame_know = QFrame()
        self.frame_repeat = QFrame()
        self.btn_back = QPushButton("В начальное меню")
        self.btn_save = QPushButton("Сохранить")

        layout_frame_up = QHBoxLayout()
        layout_frame_up.addWidget(self.btn_back)
        layout_frame_up.addWidget(self.btn_save)
        self.frame_up2.setLayout(layout_frame_up)

        self.btn_continue = QPushButton("Начать тест")
        self.btn_continue.setFixedHeight(40)
        self.btn_continue.setFixedWidth(100)
        self.label_stat = QLabel("Статистика слова")
        self.label_total = QLabel("Всего слов")
        font = QFont("Times", 16)
        self.label_question = QLabel("")  # Слово
        self.label_question.setFont(font)
        self.label_answer = QLabel("")    # Перевод
        self.label_answer.setFont(font)
        layout_frame_down = QVBoxLayout()
        layout_frame_down.addWidget(self.btn_continue)
        layout_frame_down.addWidget(self.label_stat)
        layout_frame_down.addWidget(self.label_total)
        layout_frame_down.addWidget(self.label_question)
        layout_frame_down.addWidget(self.label_answer)
        self.frame_down2.setLayout(layout_frame_down)

        layout_frame_know = QHBoxLayout()
        self.but_know = QPushButton("Знаю")
        self.but_know.setVisible(False)
        layout_frame_know.addWidget(self.but_know)
        self.frame_know.setLayout(layout_frame_know)

        layout_frame_repeat = QVBoxLayout()  # Блок для повтора, статистики вернух слов и кнопки "Повторить"
        self.label_end = QLabel("")
        font3 = QFont("Times", 14)
        self.label_end.setFont(font3)
        self.label_count_right = QLabel("")
        font2 = QFont("Times", 10)
        self.label_count_right.setFont(font2)
        self.again_but = QPushButton("Повторить")
        self.again_label = QLabel("")
        self.again_label.setFont(font2)
        layout_frame_repeat.addWidget(self.label_end)
        layout_frame_repeat.addWidget(self.label_count_right)
        layout_frame_repeat.addWidget(self.again_but)
        layout_frame_repeat.addWidget(self.again_label)
        self.frame_repeat.setLayout(layout_frame_repeat)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame_up2)
        main_layout.addWidget(self.frame_down2)
        main_layout.addWidget(self.frame_know)
        main_layout.addWidget(self.frame_repeat)
        self.frame_main.setLayout(main_layout)
        self.setCentralWidget(self.frame_main)
        self.btn_back.clicked.connect(self.back)
        self.btn_continue.clicked.connect(self.testting)
        self.but_know.clicked.connect(self.know)
        self.again_but.clicked.connect(self.again)
        self.btn_save.clicked.connect(self.sohran)

    def sohran(self):
        with open('sohranen.txt', 'w+', encoding='utf-8') as file:
            json.dump(self.test, file, indent='    ', ensure_ascii=False)
        if self.vib == 'Русс':
            otvet='Англ'
        else:
            otvet='Русс'
        places = [self.vib,otvet]
        with open('for_sohr.txt', 'w') as filehandle:  
            for listitem in places:
                filehandle.write('%s\n' % listitem)
        a=[self.st,self.en,'Words']
        with open('num_less.txt', 'w') as filehandle:  
            for listitem in a:
                filehandle.write('%s\n' % listitem)

    def again(self):
        self.shet_for_povtor=1
        self.testting()

    def know(self):
        self.but_know.setStyleSheet('QPushButton {background-color: lime; color: white;}')
        self.count_right += 1
        self.shet_know = 1

        for i in self.stat['Words']:
            if self.r in self.stat['Words'][i]:
                self.stat['Words'][i][self.r] += 1

        with open('stat.txt', 'w+', encoding='utf-8') as file:
            json.dump(self.stat, file, indent='    ', ensure_ascii=False)

    def sohran(self):
        with open('sohranen.txt', 'w+', encoding='utf-8') as file:
            json.dump(self.test, file, indent='    ', ensure_ascii=False)
        if self.vib == 'Русс':
            otvet='Англ'
        else:
            otvet='Русс'
        places = [self.vib,otvet]
        with open('for_sohr.txt', 'w') as filehandle:  
            for listitem in places:
                filehandle.write('%s\n' % listitem)
        a=[self.st,self.en,'Words']
        with open('num_less.txt', 'w') as filehandle:  
            for listitem in a:
                filehandle.write('%s\n' % listitem)

    def ochist_file(self):
        f=open('sohranen.txt', 'w')
        f.close()
        file=open('for_sohr.txt','w')
        file.close()
        self.frame_main.deleteLater()
        self.main()

    def prodoljit(self):
        self.shet_prodol_or_snulya +=1
        with open('sohranen.txt',encoding='utf-8') as f:
            data = f.read()
        self.test_from_file = ast.literal_eval(data)
        places2 = []
        with open('num_less.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                places2.append(currentPlace)
        places3 = []
        with open('for_sohr.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                places3.append(currentPlace)
        self.vib=places3[0]
        self.for_table_sp=places3[1].split(",")
        self.com_vib_dict()
        self.menu2()

    def testting(self):
        if self.shet_prodol_or_snulya==0:
            self.for_table_sp = []
            if self.vib != []:
                if self.vib == 'Англ':
                    self.for_table_sp.append('Русс')
                else:
                    self.for_table_sp.append('Англ')
        if self.shet == 0:  # Начало теста, заполнение его
            self.count_all = 0
            self.count_right = 0
            if self.shet_for_povtor==0:  # Если это тест с нуля, а не с повторным проходом неузнанных слов
                if self.shet_prodol_or_snulya==1:
                    self.test=self.test_from_file
                else:
                    self.test = []
                    self.test = self.alls.copy()
            else:
                self.test=self.bez_otvet
                self.bez_otvet=[]

            self.stat_min_score = {}  # Второй сбор Словаря всех слов для теста (уже без нулевых значений)
            # И выбора из них миним по очкам
            test2 = []
            self.test_count = []
            for i in self.test:
                num_str = str(i['Num'])
                if i[self.vib] != 0 and i[self.vib] != '0' and type(i[self.vib]) != int:
                    ku = i[self.vib]
                    self.stat_min_score[num_str] = {}
                    self.stat_min_score[num_str] = self.stat['Words'][num_str][ku]
                    test2.append(i)
                    if i[self.vib] not in self.test_count:
                        self.test_count.append(i[self.vib])
            self.test = test2
        self.test_is_filled = True
        if self.test != [] and self.stat_min_score != {}:  # Продолжение теста, каждое нажатие кнопки "Next"
            self.btn_continue.setText('Дальше')
            self.again_label.setText('')
            self.label_count_right.setText('')
            self.but_know.setVisible(True)
            self.again_but.setVisible(False)
            self.label_end.setText('')
            if self.sh2 % 2 == 0: # Четное нажатие клавиши, показывает вопрос
                self.shet_know=0
                self.but_know.setStyleSheet('QPushButton {background-color: red; color: white;}')
                self.but_know.setDisabled(False)
                self.label_answer.setText('')  
                self.for_table_main = dict()
                if self.check_value==True:
                    self.rand_num = random.choice(list(self.stat_min_score.keys()))
                    self.c_test=self.stat_min_score[self.rand_num]
                else:
                    self.rand_num = random.choice([key for key in self.stat_min_score if
                                                    self.stat_min_score[key] == min(self.stat_min_score.values())])
                    self.c_test = min(self.stat_min_score.values())
                self.r = 'n'
                self.table2 = []  # записывает в таблицу все пхожие эл на случайно выбранный для теста
                while self.r == 'n':
                    for i in self.test:
                        if i['Num'] == int(self.rand_num):
                            self.r = i[self.vib]
                        if self.r != 'n':
                            break
                if '、' in self.r:
                    self.r_l = self.r.split('、')
                else:
                    self.r_l = [self.r]
                for i in self.test:
                    for j in self.r_l:
                        if '、' in i[self.vib]:
                            isv = i[self.vib].split('、')
                            if j in isv:
                                if i not in self.table2:
                                    self.table2.append(i)
                        else:
                            if j == i[self.vib]:
                                if i not in self.table2:
                                    self.table2.append(i)
                self.ts = []
                for j in self.table2:
                    shetcik = 0
                    self.for_table_main = dict()
                    for i in self.for_table_sp:
                        if len(self.r_l) > 1:
                            if shetcik == 0:
                                self.for_table_main[i] = str(j[i]) + ' , On=  ' + str(j['On'])
                                shetcik += 1
                            else:
                                self.for_table_main[i] = j[i]
                        else:
                            self.for_table_main[i] = j[i]
                    self.ts.append(self.for_table_main)
                t = f'Количество слов= {len(self.test_count)}.'
                self.label_total.setText(t)
    
                self.label_stat.setText('Статистика слова: ' + str(self.c_test))

                self.label_question.setText(self.r)  # Вывод слова для теста
                self.shet += 1
                self.sh2 += 1
            else:   # Нечетное нажатие клавиши прохождения теста, открытие результата
                self.but_know.setDisabled(True)
                self.count_all += 1
                self.sh2 += 1
                for i in self.ts:
                    for j in i:
                        self.label_answer.setText(i[j])                      

                for i in self.test:
                    if i[self.vib] == self.r:
                        nm = str(i['Num'])
                        self.slovo_dlya_povtora_testa=i
                        self.test.remove(i)
                        self.stat_min_score.pop(nm)
                        if i[self.vib] in self.test_count:
                            self.test_count.remove(i[self.vib])
                if self.shet_know==0:
                    if self.slovo_dlya_povtora_testa!=0:
                        self.bez_otvet.append(self.slovo_dlya_povtora_testa)
        else:
            self.label_count_right.setText('')
            self.but_know.setVisible(False)
            if self.shet_know==0:
                if self.slovo_dlya_povtora_testa!=0:
                    self.bez_otvet.append(self.slovo_dlya_povtora_testa)
            self.label_end.setText('Список слов закончился,\n начинается заново')
            self.label_end.setStyleSheet('color: red')
            self.label_total.setText('')
            self.label_stat.setText('')
            self.label_answer.setText('')
            self.label_question.setText('')
            if self.count_all != 0:
                prots = int(round((100 / self.count_all * self.count_right), 2))
                self.label_count_right.setText(f'Общее число={self.count_all}, Верно={self.count_right}, процент верных = {prots}.')
            if self.bez_otvet !=[]:
                self.again_label.setText('Есть слова без ответа, повторить?')
                self.again_but.setVisible(True)
            self.data_from_xls()
            self.over()

    def over(self):
        self.shet = 0
        self.alls2 = []
        for i in self.alls:
            if i['Lesson'] >= self.st and i['Lesson'] <= self.en:
                self.alls2.append(i)
        self.alls = self.alls2
        self.slovo_dlya_povtora_testa=0

    def back(self):
        self.frame_main.deleteLater()
        self.main()
        if self.test_is_filled==True and len(self.alls) != len(self.test):
            self.btn_witn_zero.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    language = Language()
    language.show()
    # set window size
    language.setFixedSize(440, 540)
    # set color
    language.setStyleSheet("background-color: #E6E6FA;")
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:20:14 2019

@author: gs104755
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_level()

    def init_ui(self):
        self.setWindowTitle('MyGame')
        self.setWindowState(Qt.WindowMaximized)

    def init_level(self):
        self.operators = [add_same(), add_same(), two_plus_three(),
                          one_plus_one(), add_w(), Filter('x')]
        self.sources = [base('w'), base('x'), base('y'), base('z')]
        self.inputs = ['', '']
        self.index = 0
        self.create_level_ui()

    def create_level_ui(self):
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
#        main_layout.addWidget(QLabel('Transformations'), 0, 0)
#        main_layout.addWidget(QLabel('Outputs'), 1, 0)
        main_layout.addWidget(QLabel('sources'), 2, 0)
#        transformations = ['add same', 'add same', 'two plus three',
#                           'one plus one', 'add w', 'filter x']
#        for i, t in enumerate(transformations):
#            button1 = QPushButton(t)
#            button2 = QPushButton('')
#            button1.clicked.connect(lambda s, a=i: self.operators[a].w(self.inputs[0], self.inputs[1]))
#            button1.clicked.connect(lambda s, a=i, b=button2: b.setText(self.operators[a].output))
#            button1.clicked.connect(lambda s, a=i: self.check(self.operators[a]))
#            button1.clicked.connect(lambda: self.reset_index())
#            button2.clicked.connect(lambda s, a=i: self.set_input(self.operators[a]))
#            button2.clicked.connect(lambda s, b=button2: b.setText(''))
#            main_layout.addWidget(button1, 0, i+1)
#            main_layout.addWidget(button2, 1, i+1)
        for index, operator in enumerate(self.operators):
            main_layout.addWidget(operator.get_ui_elements(), 0,index)

        for i, s in enumerate(self.sources):
            button = QPushButton(s.value)
            button.clicked.connect(lambda s, a=i: self.set_input(self.sources[a]))
            main_layout.addWidget(button, 2, i+1)
        main_layout.addWidget(QLabel('produce wwxxyyzz'))
        self.setCentralWidget(main_widget)

    def set_input(self, operator):
        self.inputs[self.index] = operator.get_output()
        self.index = (self.index + 1) % 2
        print(self.inputs)

    def reset_index(self):
        self.index = 0
        self.inputs = ['', '']

    def check(self, operator):
        if operator.output == 'wwxxyyzz':
            self.setCentralWidget(QLabel('You Won!', font = QFont('SanSerif', 70)))


class operator():
    def __init__(self, n_inputs, n_outputs):
        self.name = 'operator'
        self.inputs = []
        self.outputs = []
        for i in range(n_inputs):
            self.inputs.append(str(i))

        for i in range(n_outputs):
            self.outputs.append('')

        self.ui_elements = QWidget()
        layout = QVBoxLayout()
        self.ui_elements.setLayout(layout)
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        button = QPushButton(self.name)
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_widget.setLayout(bottom_layout)
        layout.addWidget(top_widget)
        layout.addWidget(button)
        layout.addWidget(bottom_widget)
        for i in self.inputs:
            top_layout.addWidget(QLabel(i))
        for i in self.outputs:
            bottom_layout.addWidget(QPushButton())

    def get_ui_elements(self):
        return self.ui_elements

    def get_output(self):
        temp = self.output
        self.output = ''
        return temp

    def w(self, *args, **kwargs):
        self.work(*args, **kwargs)

    def work(self, *args, **kwargs):
        pass


class base():
    def __init__(self, value):
        self.value = value

    def get_output(self):
        return self.value


class add_same(operator):

    def __init__(self):
        operator.__init__(self, 2, 1)

    def work(self, input1, input2):
        input1 = ''.join(sorted(input1))
        input2 = ''.join(sorted(input2))
        if input1 == input2:
            string = input1 + input2
            string = ''.join(sorted(string))
            self.output = string


class two_plus_three(operator):

    def __init__(self):
        operator.__init__(self, 2, 1)

    def work(self, input1, input2):
        len1 = len(input1)
        len2 = len(input2)
        if (len1 == 2 and len2 == 3) or (len1 == 3 and len2 == 2):
            self.output = ''.join(sorted(input1 + input2))


class one_plus_one(operator):

    def __init__(self):
        operator.__init__(self, 2, 1)

    def work(self, input1, input2):
        len1 = len(input1)
        len2 = len(input2)
        if (len1 == 1 and len2 == 1):
            self.output = ''.join(sorted(input1 + input2))


class add(operator):

    def __init__(self):
        operator.__init__(self, 2, 1)

    def work(self, input1, input2):
        self.output = ''.join(sorted(input1 + input2))


class add_w(operator):

    def __init__(self):
        operator.__init__(self, 2, 1)

    def work(self, input1, input2):
        if input1 == 'w' or input2 == 'w':
            self.output = ''.join(sorted(input1 + input2))


class Filter(operator):

    def __init__(self, target):
        operator.__init__(self, 1, 1)
        self.target = target

    def work(self, input1, input2):
        in_all = True
        copy = input1
        for i in self.target:
            if i in input1:
                input1 = input1.replace(i, '', 1)
            else:
                in_all = False
        if in_all:
            self.output = input1
        else:
            self.output = copy


#w1_1 = add_same()
#w1_2 = add_same()
#w2 = two_plus_three()
#w3 = one_plus_one()
#w4 = add_w()
#w5 = Filter('x')
#wandler = {'1': w1_1, '11': w1_2, '2': w2, '3': w3, '4': w4, '5': w5,
#           'w': base('w'), 'x': base('x'), 'y': base('y'), 'z': base('z')}
#
#
#def use(using, input1, input2=None):
#    if input2 is None:
#        wandler[using].w(wandler[input1].get_output())
#    else:
#        wandler[using].w(wandler[input1].get_output(),
#                         wandler[input2].get_output())
#
#
#def sequence_generator(liste, elements):
#    sequences = []
#    for i in liste:
#        sequences.append([i])
#    for i in range(elements-1):
#        old = sequences
#        sequences = []
#        for j in old:
#            for k in liste:
#                list2 = j.copy()
#                list2.append(k)
#                sequences.append(list2)
#    return sequences
#
#
#def all_posibilitys(operator_dict, base_dict, turns):
#    posibilitys = []
#    if turns == 0:
#        for key in base_dict:
#            posibilitys.append((base_dict[key].get_output(), key))
#    else:
#        prev_pos = all_posibilitys(operator_dict, base_dict, turns-1)
#        posibilitys = prev_pos.copy()
#        for in1, key1 in prev_pos:
#            for in2, key2 in prev_pos:
#                if key1 != key2 or key1 in base_dict:
#                    for operator_key in operator_dict:
#                        operator_dict[operator_key].work(in1, in2)
#                        out = operator_dict[operator_key].get_output()
#                        if out != '' and (out, operator_key) not in posibilitys:
#                            posibilitys.append((out, operator_key))
#
#    return posibilitys
#
#
#dict1 = {'1': one_plus_one(), '2': add_same(), '3': add_w()}
#dict2 = {'w': base('w'), 'x': base('x'), 'y': base('y')}
#
#print(all_posibilitys(dict1, dict2, 20))
#
#use('1', 'x', 'x')
#use('11', 'x', 'x')
#use('1', '1', '11')
#use('5', '1')
#use('3', 'y', 'z')
#use('2', '5', '3')
#use('5', '2')
#use('5', '5')
#use('3', 'y', 'z')
#use('4', '3', 'w')
#use('1', 'x', 'x')
#use('2', '4', '1')
#use('4', '5', 'w')
#use('5', '2')
#use('1', '4', '5')
#print(w1_1.get_output())

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
#        print('App')

    ex = App()
    ex.show()
    sys.exit(app.exec_())

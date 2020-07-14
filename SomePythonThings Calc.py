def print_number(n):
    print(n)
def print_operation(o):
    print(o)
def print_bracket(b):
    print(b)
def dot():
    print('.')
def calculate():
    print('=')
def delete():
    print('del')
def clear():
    print('clear')
def clear_all():
    print('clear_all')


def resizeWidgets():
    global buttons
    global calc
    big_width = 25/100*calc.width()
    small_width = 16.66/100*calc.width()
    height = 14/100*calc.height()
    first_row = 30/100*calc.height()
    second_row= (30+14)/100*calc.height()
    third_row= (30+14*2)/100*calc.height()
    fourth_row= (30+14*3)/100*calc.height()
    fifth_row= (30+14*4)/100*calc.height()
    big_1st_column = (25*0)/100*calc.width()
    big_2nd_column = (25*1)/100*calc.width()
    big_3rd_column = (25*2)/100*calc.width()
    big_4th_column = (25*3)/100*calc.width()
    small_1st_column = (16.66666*0)/100*calc.width()
    small_2nd_column = (16.66666*1)/100*calc.width()
    small_3rd_column = (16.7*2)/100*calc.width()
    small_4th_column = (16.66666*3)/100*calc.width()
    small_5th_column = (16.66666*4)/100*calc.width()
    small_6th_column = (16.66666*5)/100*calc.width()
    width = 84
    buttons[0].move(big_2nd_column, fifth_row)
    buttons[0].resize(big_width, height) #Resize button
    buttons[1].move(big_1st_column, fourth_row)
    buttons[1].resize(big_width, height) #Resize button
    buttons[2].move(big_2nd_column, fourth_row)
    buttons[2].resize(big_width, height) #Resize button
    buttons[3].move(big_3rd_column, fourth_row)
    buttons[3].resize(big_width, height) #Resize button
    buttons[4].move(big_1st_column, third_row)
    buttons[4].resize(big_width, height) #Resize button
    buttons[5].move(big_2nd_column, third_row)
    buttons[5].resize(big_width, height) #Resize button
    buttons[6].move(big_3rd_column, third_row)
    buttons[6].resize(big_width, height) #Resize button
    buttons[7].move(big_1st_column, second_row)
    buttons[7].resize(big_width, height) #Resize button
    buttons[8].move(big_2nd_column, second_row)
    buttons[8].resize(big_width, height) #Resize button
    buttons[9].move(big_3rd_column, second_row)
    buttons[9].resize(big_width, height) #Resize button
    buttons['/'].move(big_4th_column, second_row)
    buttons['/'].resize(big_width, height) #Resize button
    buttons['*'].move(big_4th_column, third_row)
    buttons['*'].resize(big_width, height) #Resize button
    buttons['**('].move(small_3rd_column, first_row)
    buttons['**('].resize(small_width, height) #Resize button
    buttons['+'].move(big_4th_column, fourth_row)
    buttons['+'].resize(big_width, height) #Resize button
    buttons['-'].move(big_4th_column, fifth_row)
    buttons['-'].resize(big_width, height) #Resize button
    buttons['='].move(big_3rd_column, fifth_row)
    buttons['='].resize(big_width, height) #Resize button
    buttons['.'].move(big_1st_column, fifth_row)
    buttons['.'].resize(big_width, height) #Resize button
    buttons['('].move(small_1st_column, first_row)
    buttons['('].resize(small_width, height) #Resize button
    buttons[')'].move(small_2nd_column, first_row)
    buttons[')'].resize(small_width, height) #Resize button
    buttons['Del'].move(small_4th_column, first_row)
    buttons['Del'].resize(small_width, height) #Resize button
    buttons['CO'].move(small_5th_column, first_row)
    buttons['CO'].resize(small_width, height) #Resize button
    buttons['CA'].move(small_6th_column, first_row)
    buttons['CA'].resize(small_width, height) #Resize button
import sys
from PyQt5 import QtWidgets, QtGui
from functools import partial
from random import randint
app = QtWidgets.QApplication(sys.argv)
calc = QtWidgets.QWidget()
calc.setGeometry(0, 0, 900, 500)
calc.setWindowTitle('SomePythonThings Calc')
try:
    calc.setWindowIcon(QtGui.QIcon("icon.png"))
except: pass
buttons = {}
for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    buttons[number] = QtWidgets.QPushButton(calc) # humber button
    buttons[number].setText(str(number))
    buttons[number].move(randint(0, 500), randint(0, 500))
    buttons[number].clicked.connect(partial(print_number, str(number)))
for operation in ['*', '/', '+', '-', '**(']:
    buttons[operation] = QtWidgets.QPushButton(calc) # operation button
    buttons[operation].setText(str(operation))
    buttons[operation].move(randint(0, 500), randint(0, 500))
    buttons[operation].clicked.connect(partial(print_operation, str(operation)))
for bracket in ['(', ')']:
    buttons[bracket] = QtWidgets.QPushButton(calc) # bracket button
    buttons[bracket].setText(str(bracket))
    buttons[bracket].move(randint(0, 500), randint(0, 500))
    buttons[bracket].clicked.connect(partial(print_bracket, str(bracket)))

buttons['.'] = QtWidgets.QPushButton(calc) # Dot button
buttons['.'].setText('.')
buttons['.'].move(randint(0, 500), randint(0, 500))
buttons['.'].clicked.connect(dot)

buttons['='] = QtWidgets.QPushButton(calc) # "=" button
buttons['='].setText('=')
buttons['='].move(randint(0, 500), randint(0, 500))
buttons['='].clicked.connect(calculate)

buttons['Del'] = QtWidgets.QPushButton(calc) # Backspace button (clear one charartcer)
buttons['Del'].setText('Delete')
buttons['Del'].move(randint(0, 500), randint(0, 500))
buttons['Del'].clicked.connect(delete)

buttons['CO'] = QtWidgets.QPushButton(calc) # Clear Operation (CO)
buttons['CO'].setText('Clear')
buttons['CO'].move(randint(0, 500), randint(0, 500))
buttons['CO'].clicked.connect(clear)

buttons['CA'] = QtWidgets.QPushButton(calc) # Clear All (CA)
buttons['CA'].setText('Clear All')
buttons['CA'].move(randint(0, 500), randint(0, 500))
buttons['CA'].clicked.connect(clear_all)
resizeWidgets()
calc.show()
sys.exit(app.exec_())

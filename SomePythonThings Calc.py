true = True
false = False

def scrollBottom():
    print('scroll')

def appendText(t):
    global textbox
    textbox.setPlainText(str(textbox.toPlainText())+str(t))

canWrite = True
operationAvailable = False
dotAvailable = True
bracketsToClose = 0
needClear = False
previousResult = 0
calcHistory = ''
currentOperation = ''

def print_number(n):
    global textbox, needClear, currentOperation, operationAvailable
    if needClear:
        appendText('\n\n')
        needClear = False
        currentOperation = ''
    appendText(n)
    scrollBottom()
    currentOperation += n
    operationAvailable=True
    



def print_operation(o):
    global previousResult, currentOperation, needClear, dotAvailable, bracketsToClose, operationAvailable
    scrollBottom()
    if needClear:
        appendText("\n\n" + str(previousResult))
        currentOperation = previousResult
        needClear = False
    if o in '^(*/':
        if operationAvailable:
            appendText(' '+o+' ')
            currentOperation += ' '+o+' '
    else:
        appendText(' '+o+' ')
        currentOperation += ' '+o+' '
    operationAvailable = False
    dotAvailable = False
    if o == '^(':
        bracketsToClose += 1



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
    global textbox
    global calc
    big_width = 25/100*calc.width()
    small_width = 17/100*calc.width()
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
    small_1st_column = (16.6666*0)/100*calc.width()
    small_2nd_column = (16.6666*1)/100*calc.width()
    small_3rd_column = (16.6666*2)/100*calc.width()
    small_4th_column = (16.6666*3)/100*calc.width()
    small_5th_column = (16.6666*4)/100*calc.width()
    small_6th_column = (16.6666*5)/100*calc.width()
    width = 84
    textbox.resize(calc.width() ,calc.height()/100*30)
    buttons['0'].move(big_2nd_column, fifth_row)
    buttons['0'].resize(big_width, height) #Resize button
    buttons['1'].move(big_1st_column, fourth_row)
    buttons['1'].resize(big_width, height) #Resize button
    buttons['2'].move(big_2nd_column, fourth_row)
    buttons['2'].resize(big_width, height) #Resize button
    buttons['3'].move(big_3rd_column, fourth_row)
    buttons['3'].resize(big_width, height) #Resize button
    buttons['4'].move(big_1st_column, third_row)
    buttons['4'].resize(big_width, height) #Resize button
    buttons['5'].move(big_2nd_column, third_row)
    buttons['5'].resize(big_width, height) #Resize button
    buttons['6'].move(big_3rd_column, third_row)
    buttons['6'].resize(big_width, height) #Resize button
    buttons['7'].move(big_1st_column, second_row)
    buttons['7'].resize(big_width, height) #Resize button
    buttons['8'].move(big_2nd_column, second_row)
    buttons['8'].resize(big_width, height) #Resize button
    buttons['9'].move(big_3rd_column, second_row)
    buttons['9'].resize(big_width, height) #Resize button
    buttons['/'].move(big_4th_column, second_row)
    buttons['/'].resize(big_width, height) #Resize button
    buttons['*'].move(big_4th_column, third_row)
    buttons['*'].resize(big_width, height) #Resize button
    buttons['^('].move(small_3rd_column, first_row)
    buttons['^('].resize(small_width, height) #Resize button
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
    for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(']:
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #333333; color: white;font-size:20px; color: #DDDDDD; font-family: "Consolas", monospace; width: 25%}  QPushButton::hover {background-color: #111111;}')# Set Style
    for button in ['.', '+', '-', '*', '/']:
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #49525C; color: white;font-size:20px; color: #DDDDDD; font-family: "Consolas", monospace;}  QPushButton::hover {background-color: #111111;}')# Set Style
    for button in ['Del', 'CO', 'CA']:
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #202020; color: white;font-size:20px; color: #DDDDDD; font-family: "Consolas", monospace;}  QPushButton::hover {background-color: #111111;}')# Set Style
    buttons['='].setStyleSheet('QPushButton { border: none; background-color: #00BFB2; color: white;font-size:20px; color: #DDDDDD; font-family: "Consolas", monospace;}  QPushButton::hover {background-color: #111111;}')# Set Style
    textbox.setStyleSheet('border:none; background-color: #222222; color:white;font-size:20px; color: #DDDDDD; font-family: "Consolas", monospace; ')

from PyQt5 import QtWidgets, QtGui, QtCore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(200, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.resized.connect(resizeWidgets)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def someFunction(self):
        print("someFunction")

import sys
from functools import partial
resized = QtCore.pyqtSignal()
app = QtWidgets.QApplication(sys.argv)
calc = Window()
calc.setGeometry(0, 0, 900, 500)
calc.setWindowTitle('SomePythonThings Calc')
calc.setStyleSheet("background-color: #333333;")
try:
    calc.setWindowIcon(QtGui.QIcon("icon.png"))
except: pass
buttons = {}
for number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    buttons[number] = QtWidgets.QPushButton(calc, objectName="button") # number button
    buttons[number].setText(str(number))
    buttons[number].move(0, 0)
    buttons[number].clicked.connect(partial(print_number, str(number)))
for operation in ['*', '/', '+', '-', '^(']:
    buttons[operation] = QtWidgets.QPushButton(calc) # operation button
    buttons[operation].setText(str(operation))
    buttons[operation].move(0, 0)
    buttons[operation].clicked.connect(partial(print_operation, str(operation)))
for bracket in ['(', ')']:
    buttons[bracket] = QtWidgets.QPushButton(calc) # bracket button
    buttons[bracket].setText(str(bracket))
    buttons[bracket].move(0, 0)
    buttons[bracket].clicked.connect(partial(print_bracket, str(bracket)))
buttons['.'] = QtWidgets.QPushButton(calc) # Dot button
buttons['.'].setText('.')
buttons['.'].move(0, 0)
buttons['.'].clicked.connect(dot)
buttons['='] = QtWidgets.QPushButton(calc) # "=" button
buttons['='].setText('=')
buttons['='].move(0, 0)
buttons['='].clicked.connect(calculate)
buttons['Del'] = QtWidgets.QPushButton(calc) # Backspace button (clear one charartcer)
buttons['Del'].setText('Delete')
buttons['Del'].move(0, 0)
buttons['Del'].clicked.connect(delete)
buttons['CO'] = QtWidgets.QPushButton(calc) # Clear Operation (CO)
buttons['CO'].setText('Clear')
buttons['CO'].move(0, 0)
buttons['CO'].clicked.connect(clear)
buttons['CA'] = QtWidgets.QPushButton(calc) # Clear All (CA)
buttons['CA'].setText('Clear all')
buttons['CA'].move(0, 0)
buttons['CA'].clicked.connect(clear_all)
textbox =  QtWidgets.QPlainTextEdit(calc)
textbox.move(0, 0)
textbox.setReadOnly(True)
resizeWidgets()
calc.show()
sys.exit(app.exec_())

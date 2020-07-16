

def scrollBottom():
    global textbox
    textbox.moveCursor(QtGui.QTextCursor.End)


def appendText(t):
    global textbox
    textbox.setPlainText(str(textbox.toPlainText())+str(t))
    scrollBottom()

canWrite = True
operationAvailable = False
dotAvailable = True
bracketsToClose = 0
needClear = False
previousResult = 0
calcHistory = ''
currentOperation = ''

def print_number(n):
    n = str(n)
    global textbox, needClear, currentOperation, operationAvailable, canWrite
    if canWrite:
        if needClear:
            appendText('\n\n')
            needClear = False
            currentOperation = ''
        appendText(n)
        scrollBottom()
        currentOperation += n
        operationAvailable=True
    scrollBottom()
    



def print_operation(o):
    global previousResult, currentOperation, needClear, dotAvailable, bracketsToClose, operationAvailable, canWrite
    if canWrite:
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
        dotAvailable = True
        if o == '^(':
            bracketsToClose += 1
    scrollBottom()



def print_bracket(b):
    global operationAvailable, bracketsToClose, currentOperation, needClear, canWrite, dotAvailable
    if canWrite:    
        operationAvailable = False
        if b == ')':
            if bracketsToClose > 0:
                appendText(' '+b)
                currentOperation += ' ' + b
                bracketsToClose -= 1
                dotAvailable = True
                operationAvailable = True
        else: 
            if needClear:
                appendText('\n\n')
                currentOperation = ''
                needClear = False
            bracketsToClose += 1
            currentOperation += b+' '
            appendText(b+' ')
            dotAvailable = True
    scrollBottom()
        

def dot():
    global needClear, dotAvailable, currentOperation, canWrite
    if canWrite:    
        if needClear:
            appendText('\n\n')
            currentOperation = ''
            needClear = False
        if dotAvailable:
            appendText('.')
            dotAvailable = False
            currentOperation += '.'
    scrollBottom()



def calculate():
    global currentOperation, needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox
    disableAll()
    try:
        while str(currentOperation[0:1]) == '0':
            currentOperation = str(currentOperation)[1:]
        result = eval(str(currentOperation).replace('^', '**'))
        needClear = True
        previousResult = str(result)
        dotAvailable = True
    except:
        result = "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!"
        needClear = True
        dotAvailable = False
        operationAvailable = False
        bracketsToClose = 0
    calcHistory =  textbox.toPlainText()
    appendText('\n = '+str(result))
    scrollBottom()
    enableAll()



def disableAll():
    global canWrite
    canWrite = False

def enableAll():
    global canWrite
    canWrite = True

def clear():
    global textbox, canWrite, operationAvailable, dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation
    if calcHistory == '':
        textbox.setPlainText('')
    else:
        textbox.setPlainText(calcHistory + "\n\n")
    currentOperation = ''
    dotAvailable = True
    operationAvailable = False
    bracketsToClose = 0
    needClear = False
    previousResult = 0
    scrollBottom()



def clear_all():
    global textbox, canWrite, operationAvailable, dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation
    textbox.setPlainText('')
    canWrite = True
    operationAvailable = False
    dotAvailable = True
    bracketsToClose = 0
    needClear = False
    previousResult = 0
    calcHistory = ''
    currentOperation = ''
    scrollBottom()

    



def delete():
    global textbox, currentOperation
    scrollBottom()
    text = textbox.toPlainText()
    char = text[-1:]
    checkChar(char)
    if char == ' ':
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        delAfterSpace()
    else:
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
    scrollBottom()


def delAfterSpace():
    global textbox, currentOperation
    scrollBottom()
    text = textbox.toPlainText()
    char = text[-1:]
    checkChar(char)
    if char == ' ':
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        delAfterSpace()
    else:
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        delOnlyIfSpace()
    scrollBottom()

def delOnlyIfSpace():
    global textbox, currentOperation
    scrollBottom()
    text = textbox.toPlainText()
    char = text[-1:]
    checkChar(char)
    if char == ' ':
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        delOnlyIfSpace()
    scrollBottom()

def checkChar(c):
    global dotAvailable, bracketsToClose, operationAvailable
    if c == '.':
        dotAvailable = True
    elif c == '(':
        bracketsToClose -= 1
    elif c == ')':
        bracketsToClose += 1
    elif c in '*/^':
        operationAvailable = True





def on_key(key):
    # test for a specific key
    if key == QtCore.Qt.Key_Return:
        calculate()
    elif key == QtCore.Qt.Key_Enter:
        calculate()
    elif key == QtCore.Qt.Key_0:
        print_number(0)
    elif key == QtCore.Qt.Key_1:
        print_number(1)
    elif key == QtCore.Qt.Key_2:
        print_number(2)
    elif key == QtCore.Qt.Key_3:
        print_number(3)
    elif key == QtCore.Qt.Key_4:
        print_number(4)
    elif key == QtCore.Qt.Key_5:
        print_number(5)
    elif key == QtCore.Qt.Key_6:
        print_number(6)
    elif key == QtCore.Qt.Key_7:
        print_number(7)
    elif key == QtCore.Qt.Key_8:
        print_number(8)
    elif key == QtCore.Qt.Key_9:
        print_number(9)
    elif key == QtCore.Qt.Key_Asterisk:
        print_operation('*')
    elif key == QtCore.Qt.Key_Slash:
        print_operation('/')
    elif key == 00:
        print_operation('^(')
    elif key == QtCore.Qt.Key_Plus:
        print_operation('+')
    elif key == QtCore.Qt.Key_Minus:
        print_operation('-')
    elif key == QtCore.Qt.Key_ParenLeft:
        print_bracket('(')
    elif key == QtCore.Qt.Key_ParenRight:
        print_bracket(')')
    elif key == QtCore.Qt.Key_Equal:
        calculate()
    elif key == QtCore.Qt.Key_Backspace:
        delete()
    elif key == QtCore.Qt.Key_Comma:
        dot()
    elif key == 46:
        dot()


















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
    keyRelease = QtCore.pyqtSignal(int)
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.resized.connect(resizeWidgets)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def keyReleaseEvent(self, event):
        super(Window, self).keyReleaseEvent(event)
        self.keyRelease.emit(event.key())


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
buttons['^('].setText('^')
textbox =  QtWidgets.QPlainTextEdit(calc)
textbox.move(0, 0)
textbox.setReadOnly(True)
resizeWidgets()
calc.keyRelease.connect(on_key)
calc.show()
sys.exit(app.exec_())

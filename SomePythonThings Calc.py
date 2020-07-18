def checkUpdates():
    global calc
    actualVersion = 3.1
    if True:
        from urllib.request import urlopen
        response = urlopen("http://www.somepythonthings.tk/versions/calc.ver")
        response = response.read().decode("utf8")
        if float(response.split('///')[0])>actualVersion:
            from PyQt5.QtWidgets import QMessageBox
            buttonReply = QMessageBox.question(calc, 'SomePythonThings Calc Updater', "An update for SomePythonThings Calc has been released:\nYour version: "+str(actualVersion)+"\nNew version: "+str(response.split('///')[0])+"\nUpdate Info:\n"+str(response.split('///')[1])+"\n\nDo you want to go to the web and download it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                import webbrowser
                webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-calc/')
        else:
            return False
    else:
        return False
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
previousResult = ''
calcHistory = ''
currentOperation = ''
result = 0
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
            currentOperation = str(previousResult)
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
def pure_calculate(s):
    global result
    try:
        result = str(eval(str(s)))
    except:
        result = "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!"
def calculate():
    global currentOperation, needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc
    disableAll()
    while str(currentOperation[0:1]) == '0':
        currentOperation = str(currentOperation)[1:]

    from threading import Thread
    from time import sleep as wait
    t = Thread(target=pure_calculate, args=(currentOperation.replace('^', '**'),), daemon=True)
    t.start()
    wait(0.05)
    if t.isAlive():
        from PyQt5.QtWidgets import QMessageBox
        buttonReply = QMessageBox.question(calc, 'SomePythonThings Calc', "It seems that you entered a huuuuuge operation and the program may crash. Do you want to continue?\nIf you continue, the program may hang up until it finishes the calculation.", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonReply == QMessageBox.Cancel:
            t.killed = True
        else:
            while t.isAlive():
                wait(0.1)
                print('Calculating...')
            t.join()
            if  not str(result) == "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!":
                needClear = True
                previousResult = str(result)
                dotAvailable = True
            else:
                needClear = True
                dotAvailable = False
                operationAvailable = False
                bracketsToClose = 0
            calcHistory =  textbox.toPlainText()
            appendText('\n = '+str(result))
            scrollBottom()
            enableAll()
    else:
        if  not str(result) == "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!":
            needClear = True
            previousResult = str(result)
            dotAvailable = True
        else:
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
    previousResult = ''
    scrollBottom()
def clear_all():
    global textbox, canWrite, operationAvailable, dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation
    textbox.setPlainText('')
    canWrite = True
    operationAvailable = False
    dotAvailable = True
    bracketsToClose = 0
    needClear = False
    previousResult = ''
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
    elif key == 94:
        print_operation('^(')
    elif key == 33554431:
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
    #else:
    #   print('key pressed: %i' % key)
def resizeWidgets():
    global buttons
    global textbox
    global calc
    big_width = 25/100*calc.width()
    small_width = 17/100*calc.width()
    height = 14/100*calc.height()+1
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
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #333333; font-size:20px; color: #DDDDDD; font-family: "'+font+'", monospace;font-weight: bold;  width: 25%}  QPushButton::hover {background-color: #111111;}')# Set Style
    for button in ['.', '+', '-', '*', '/']:
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #49525C; font-size:20px; color: #DDDDDD; font-family: "'+font+'", monospace;font-weight: bold; }  QPushButton::hover {background-color: #111111;}')# Set Style
    for button in ['Del', 'CO', 'CA']:
        buttons[button].setStyleSheet('QPushButton { border: none; background-color: #202020; font-size:20px; color: #DDDDDD; font-family: "'+font+'", monospace;font-weight: bold; }  QPushButton::hover {background-color: #111111;}')# Set Style
    buttons['='].setStyleSheet('QPushButton { border: none; background-color: #00BFB2; font-size:20px; color: #DDDDDD; font-family: "'+font+'", monospace;font-weight: bold; }  QPushButton::hover {background-color: #111111;}')# Set Style
    textbox.setStyleSheet('border:none; background-color: #222222; font-size:20px; color: #DDDDDD; font-family: "'+font+'", monospace;font-weight: bold;  ')
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
from sys import argv, exit
from functools import partial
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    font = "Ubuntu Mono"
elif _platform == "darwin":
    font = "Courier New"
elif _platform == "win32":
    font = "Consolas"
elif _platform == "win64":
    font = "Consolas"
resized = QtCore.pyqtSignal()
QtWidgets.QApplication.setStyle('Fusion')
app = QtWidgets.QApplication(argv)
QtWidgets.QApplication.setStyle('Fusion')
calc = Window()
calc.setGeometry(0, 0, 900, 500)
calc.setWindowTitle('SomePythonThings Calc')
calc.setStyleSheet('''
    background-color: #333333;
    color:#EEEEEE; 
    font-family: "'''+font+'''";
    font-weight: bold; 
    font-size:15px;
''')
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
calc.keyRelease.connect(on_key)
checkUpdates()
calc.show()
exit(app.exec_())

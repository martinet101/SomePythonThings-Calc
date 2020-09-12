def checkUpdates():
    global x_char, y_char, e_char, pi_char,  calc
    actualVersion = 3.3
    try:
        from urllib.request import urlopen
        response = urlopen("http://www.somepythonthings.tk/versions/calc.ver")
        response = response.read().decode("utf8")
        if float(response.split('///')[0])>actualVersion:
            from PyQt5 import QtWidgets
            buttonReply = QtWidgets.QMessageBox.question(calc, 'SomePythonThings Calc Updater', "An update for SomePythonThings Calc has been released:\nYour version: "+str(actualVersion)+"\nNew version: "+str(response.split('///')[0])+"\nUpdate Info:\n"+str(response.split('///')[1])+"\n\nDo you want to go to the web and download it?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if buttonReply == QtWidgets.QMessageBox.Yes:
                import webbrowser
                webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-calc/')
        else:
            return False
    except:
        return False
def scrollBottom():
    global x_char, y_char, e_char, pi_char,  textbox
    textbox.moveCursor(QtGui.QTextCursor.End)
def appendText(t):
    global x_char, y_char, e_char, pi_char,  textbox
    textbox.setPlainText(str(textbox.toPlainText())+str(t))
    scrollBottom()
canWrite = True
operationAvailable = False
dotAvailable = True
numberAvailable = True
symbolAvailable = True
bracketsToClose = 0
needClear = False
previousResult = ''
calcHistory = ''
currentOperation = ''
result = 0
reWriteOperation = False
x_prev_value = 0
y_prev_value = 0
def print_symbol_and_close(s):
    print_symbol(s)
    show_popup()
def print_symbol(s):
    s = str(s)
    global x_char, y_char, e_char, pi_char,  textbox, needClear, currentOperation, operationAvailable, canWrite, symbolAvailable, numberAvailable, dotAvailable
    if canWrite and symbolAvailable:
        if needClear:
            appendText('\n\n')
            needClear = False
            currentOperation = ''
        appendText(s)
        scrollBottom()
        currentOperation += s
        dotAvailable = False 
        symbolAvailable = False
        numberAvailable = False
        operationAvailable=True
    scrollBottom()
def print_number(n):
    n = str(n)
    global x_char, y_char, e_char, pi_char,  textbox, needClear, currentOperation, operationAvailable, canWrite, numberAvailable, symbolAvailable
    if canWrite and numberAvailable:
        if needClear:
            appendText('\n\n')
            needClear = False
            currentOperation = ''
        appendText(n)
        scrollBottom()
        currentOperation += n
        symbolAvailable = False
        numberAvailable = True
        operationAvailable=True
    scrollBottom()
def print_operation(o):
    global x_char, y_char, e_char, pi_char,  previousResult, currentOperation, needClear, dotAvailable, bracketsToClose, operationAvailable, canWrite, symbolAvailable, numberAvailable
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
        symbolAvailable = True
        numberAvailable = True
        if o == '^(':
            bracketsToClose += 1
    scrollBottom()
def print_bracket(b):
    global x_char, y_char, e_char, pi_char,  operationAvailable, bracketsToClose, currentOperation, needClear, canWrite, dotAvailable, numberAvailable, symbolAvailable
    if canWrite:
        operationAvailable = False
        if b == ')':
            if bracketsToClose > 0:
                appendText(' '+b)
                currentOperation += ' ' + b
                bracketsToClose -= 1
                dotAvailable = True
                operationAvailable = True
                symbolAvailable = False
                numberAvailable = False
        else: 
            if needClear:
                appendText('\n\n')
                currentOperation = ''
                needClear = False
            bracketsToClose += 1
            currentOperation += b+' '
            appendText(b+' ')
            dotAvailable = True
            symbolAvailable = True
            numberAvailable = True
    scrollBottom()
def dot():
    global x_char, y_char, e_char, pi_char,  needClear, dotAvailable, currentOperation, canWrite, numberAvailable, symbolAvailable
    if canWrite:
        symbolAvailable = False
        numberAvailable = True  
        if needClear:
            appendText('\n\n')
            currentOperation = ''
            needClear = False
        if dotAvailable:
            appendText('.')
            dotAvailable = False
            currentOperation += '.'
    scrollBottom()
def huge_calculate(currentOperation):
    global x_char, y_char, e_char, pi_char,  textbox,calc, operationAvailable, reWriteOperation,needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc, numberAvailable, symbolAvailable
    from time import sleep as wait
    from qt_thread_updater import get_updater
    result = pure_calculate(currentOperation)
    reWriteOperation = False
    from time import sleep as wait
    from qt_thread_updater import get_updater
    if  not "  " in str(result):
        needClear = True
        previousResult = str(result)
        dotAvailable = True
        symbolAvailable = True
        numberAvailable = True
    else:
        if not "Syntax" in str(result):
            needClear = True
            dotAvailable = False
            operationAvailable = False
            bracketsToClose = 0
            symbolAvailable = True
            numberAvailable = True
        else:
            reWriteOperation = True
    calcHistory =  textbox.toPlainText()
    try:
        result = int(result)
        #appendText('\n = '+f"{result:,}")
        get_updater().call_latest(textbox.appendPlainText, ' = '+f"{result:,}")
    except:
        #appendText('\n = '+result)
        get_updater().call_latest(textbox.appendPlainText, ' = '+result)
    get_updater().call_latest(textbox.moveCursor, QtGui.QTextCursor.End)
    enableAll()



def pure_calculate(s):
    try:
        result = str(eval(str(s)))
    except OverflowError:
        result = "Well, even the Windows calculator doesn't know that...\ud83c\udf1a\n\nThis error is caused because the result was supposed to be a huuuge number with decimals, but it was that big that it overflowed the system. Try to simplify your operation, and avoid divisions if you can.  "
    except SyntaxError:
        result = "Syntax Error\u2639 Please check your operation and try again!  "
    except:
        result = "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!  "
    return result
def calculate():
    global x_prev_value, y_prev_value, x_char, y_char, e_char, pi_char,  calc, currentOperation, operationAvailable, needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc, numberAvailable, symbolAvailable
    if(not needClear):
        disableAll()
        calc.setWindowTitle('SomePythonThings Calc:  '+currentOperation)
        while str(currentOperation[0:1]) == '0':
            currentOperation = str(currentOperation)[1:]
        if(pi_char in currentOperation):
            currentOperation = currentOperation.replace(pi_char, "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
        if(e_char in currentOperation):
            currentOperation = currentOperation.replace(e_char, "2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274")
        if(x_char in currentOperation):
            x = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+x_char+" on the operation.\nEnter value for "+x_char+": ", QtWidgets.QLineEdit.Normal, str(x_prev_value))
            x_prev_value = int(x[0].replace(",", "."))
            currentOperation = currentOperation.replace(x_char, x[0].replace(",", "."))
        if(y_char in currentOperation):
            y = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+y_char+" on the operation.\nEnter value for "+y_char+": ", QtWidgets.QLineEdit.Normal, str(y_prev_value))
            y_prev_value = int(y[0].replace(",", "."))
            currentOperation = currentOperation.replace(y_char, y[0].replace(",", "."))
        from threading import Thread
        from time import sleep as wait
        t = Thread(target=huge_calculate, args=(currentOperation.replace('^', '**'),))
        t.daemon = (True)
        t.start()
        
def disableAll():
    global x_char, y_char, e_char, pi_char,  canWrite
    canWrite = False
def enableAll():
    global x_char, y_char, e_char, pi_char,  canWrite
    canWrite = True
def clear():
    global x_char, y_char, e_char, pi_char,  textbox, canWrite, operationAvailable, symbolAvailable,numberAvailable,dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation
    if calcHistory == '':
        textbox.setPlainText('')
    else:
        textbox.setPlainText(calcHistory + "\n\n")
    currentOperation = ''
    dotAvailable = True
    operationAvailable = False
    bracketsToClose = 0
    needClear = False
    symbolAvailable = True
    numberAvailable = True
    previousResult = ''
    scrollBottom()
def clear_all():
    global x_char, y_char, e_char, pi_char,  textbox, canWrite, operationAvailable, dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation, symbolAvailable, numberAvailable
    textbox.setPlainText('')
    canWrite = True
    operationAvailable = False
    dotAvailable = True
    bracketsToClose = 0
    needClear = False
    symbolAvailable = True
    numberAvailable = True
    previousResult = ''
    calcHistory = ''
    currentOperation = ''
    scrollBottom()
def delete():
    global x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global x_char, y_char, e_char, pi_char,  dotAvailable, bracketsToClose, operationAvailable, numberAvailable, symbolAvailable
    if c == '.':
        dotAvailable = True
    elif c == '(':
        bracketsToClose -= 1
    elif c == ')':
        bracketsToClose += 1
    elif c in '*/^':
        operationAvailable = True
    elif (str(c) == str(pi_char)) or (str(c) == str(e_char)) or (str(c) == str(x_char)) or (str(c) == str(y_char)):
        numberAvailable = True
        symbolAvailable = True
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
    elif key == 94:#Windows "^" sign's key code
        print_operation('^(')
    elif key == 33554431:#macOS "^" sign's key code
        print_operation('^(')
    elif key == 16781906:#ubuntu "^" sign's key code
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
    elif key == QtCore.Qt.Key_P:# or key == QtCore.Qt.Key_p:
        print_symbol(pi_char)
    elif key == QtCore.Qt.Key_E:# or key == QtCore.Qt.Key_e:
        print_symbol(e_char)
    elif key == QtCore.Qt.Key_X:# or key == QtCore.Qt.Key_x:
        print_symbol(x_char)
    elif key == QtCore.Qt.Key_Y:# or key == QtCore.Qt.Key_y:
        print_symbol(y_char)
    #else:
    #   print('key pressed: %i' % key)
    
def show_popup():
    global x_char, y_char, e_char, pi_char,  popup, buttons
    if(popup):
        popup=False
        buttons["POPUP"].setText("<  ")
    else:
        popup=True
        buttons["POPUP"].setText(">  ")
    resizeWidgets()
def resizeWidgets():
    global x_char, y_char, e_char, pi_char,  buttons, popup, textbox, calc
    big_width = int(25/100*calc.width())
    small_width = int(17/100*calc.width())
    height = int(14/100*calc.height()+1)
    first_row = int(30/100*calc.height())
    second_row= int((30+14)/100*calc.height())
    third_row= int((30+14*2)/100*calc.height())
    fourth_row= int((30+14*3)/100*calc.height())
    fifth_row= int((30+14*4)/100*calc.height())
    big_1st_column = int((25*0)/100*calc.width())
    big_2nd_column = int((25*1)/100*calc.width())
    big_3rd_column = int((25*2)/100*calc.width())
    big_4th_column = int((25*3)/100*calc.width())
    small_1st_column = int((16.6666*0)/100*calc.width())
    small_2nd_column = int((16.6666*1)/100*calc.width())
    small_3rd_column = int((16.6666*2)/100*calc.width())
    small_4th_column = int((16.6666*3)/100*calc.width())
    small_5th_column = int((16.6666*4)/100*calc.width())
    small_6th_column = int((16.6666*5)/100*calc.width())
    textbox.resize(calc.width() ,int(calc.height()/100*30))
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
    if(not popup):
        buttons['POPUP'].move(calc.width()-25, int(calc.height()/2)-25)
        pX = int(calc.width())
        pY = int(calc.height()/2)
        pWidth = int(calc.width()/100*20)
        pHeight = int(height)
        buttons["X"].move(pX, (pY-height*2))
        buttons["X"].resize(pWidth, pHeight)
        buttons["Y"].move(pX, pY-height)
        buttons["Y"].resize(pWidth, pHeight)
        buttons["PI"].move(pX, pY)
        buttons["PI"].resize(pWidth, pHeight)
        buttons["E"].move(pX, pY+height)
        buttons["E"].resize(pWidth, pHeight)
    else:
        pX = int(calc.width()/100*80)
        pY = int(calc.height()/2)
        pWidth = int(calc.width()/100*20)
        pHeight = height
        buttons['POPUP'].move(pX-25, int(calc.height()/2)-25)
        buttons["X"].move(pX, pY-height*2)
        buttons["X"].resize(pWidth, pHeight+1)
        buttons["Y"].move(pX, pY-height)
        buttons["Y"].resize(pWidth, pHeight+1)
        buttons["PI"].move(pX, pY)
        buttons["PI"].resize(pWidth, pHeight+1)
        buttons["E"].move(pX, pY+height)
        buttons["E"].resize(pWidth, pHeight+1)
    buttons['POPUP'].resize(50, 50) #Resize button
    for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(']: #Grey (#333333)
        buttons[button].setStyleSheet("""
        QPushButton
        {
            border: none;
            background-color: #333333;
            font-size:20px;
            color: #DDDDDD;
            font-family: \""""+font+"""\", monospace;
            font-weight: bold;
            width: 25%;
        }
        QPushButton::hover
        {
            background-color: #111111;
        }
        """)
    for button in ['.', '+', '-', '*', '/']:# blue grey (#49525C)
        buttons[button].setStyleSheet("""
        QPushButton
        { 
            border: none; 
            background-color: #49525C; 
            font-size:20px; 
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold; 
        }
        QPushButton::hover
        {
            background-color: #111111;
        }
        """)
    for button in ['Del', 'CO', 'CA']:#Dark Grey (#202020)
        buttons[button].setStyleSheet("""
        QPushButton 
        { 
            border: none; 
            background-color: #202020; 
            font-size:20px; color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold; 
        }  
        QPushButton::hover
        {
            background-color: #111111;
        }
        """)
    for button in ['PI', 'X', 'Y', 'E', '=']: #Turquoise (#33998a)
        buttons[button].setStyleSheet("""
        QPushButton
        {
            border: none; 
            background-color: #33998a; 
            font-size:20px; 
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold; 
        }  
        QPushButton::hover
        {
            background-color: #111111;
        }
        """)
    textbox.setStyleSheet("""
    QPlainTextEdit
    {
        border:none; 
        background-color: #222222; 
        font-size:20px; 
        color: #DDDDDD; 
        font-family: \""""+font+"""\", monospace;
        font-weight: bold;
    }
    """)
    buttons["POPUP"].setStyleSheet("""
    QPushButton
    { 
        border-radius: 25px;
        background-color: "#33998a";
    }
    QPushButton::hover
    {
        background-color: "#111111";
    }
    """)
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
if(__name__=="__main__"):
    popup=False
    import os
    from sys import argv, exit
    from functools import partial
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        os.chdir("/bin/")
        font = "Ubuntu Mono"
        x_char = "x"
        y_char = "y"
        e_char = "e"
        pi_char = "π"
    elif _platform == "darwin":
        font = "Courier New"
        x_char = "x"
        y_char = "y"
        e_char = "e"
        pi_char = "π"
    elif _platform == "win32":
        font = "Consolas"
        x_char = "𝑥"
        y_char = "𝑦"
        e_char = "𝜋"
        pi_char = "𝑒"
    else:
        font = "Ubuntu Mono"
        x_char = "x"
        y_char = "y"
        e_char = "e"
        pi_char = "π"
    resized = QtCore.pyqtSignal()
    QtWidgets.QApplication.setStyle('Fusion')
    app = QtWidgets.QApplication(argv)
    app.setStyle('Fusion')
    calc = Window()
    calc.setGeometry(0, 0, 900, 500)
    calc.setWindowTitle('SomePythonThings Calc')
    calc.setStyleSheet('''
        * {
            background-color: #333333;
            color:#EEEEEE; 
            font-family: "'''+font+'''";
            font-weight: bold; 
            font-size:15px;
        }
        QScrollBar:vertical {
            background-color: #222222
        }
    ''')
    try:
        calc.setWindowIcon(QtGui.QIcon("calc-icon.png"))
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
    buttons['POPUP'] = QtWidgets.QPushButton(calc) # Clear All (CA)
    buttons['POPUP'].setText("<  ")
    buttons['POPUP'].move(0, 0)
    buttons['POPUP'].clicked.connect(show_popup)
    
    
    
    textbox =  QtWidgets.QPlainTextEdit(calc)
    textbox.move(0, 0)
    textbox.setReadOnly(True)
    
    buttons['PI'] = QtWidgets.QPushButton(calc)
    buttons['PI'].setText(pi_char)
    buttons['PI'].move(0, 0)
    buttons['PI'].clicked.connect(partial(print_symbol_and_close, pi_char))
    
    buttons['E'] = QtWidgets.QPushButton(calc)
    buttons['E'].setText(e_char)
    buttons['E'].move(0, 0)
    buttons['E'].clicked.connect(partial(print_symbol_and_close, e_char))
    
    buttons['X'] = QtWidgets.QPushButton(calc)
    buttons['X'].setText(x_char)
    buttons['X'].move(0, 0)
    buttons['X'].clicked.connect(partial(print_symbol_and_close, x_char))
    
    buttons['Y'] = QtWidgets.QPushButton(calc)
    buttons['Y'].setText(y_char)
    buttons['Y'].move(0, 0)
    buttons['Y'].clicked.connect(partial(print_symbol_and_close, y_char))
    resizeWidgets()
    calc.keyRelease.connect(on_key)
    checkUpdates()
    calc.show()
    exit(app.exec_())

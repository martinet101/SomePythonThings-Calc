#Modules
import os
import sys
import time
import platform
import subprocess
import webbrowser
from sys import argv
from sys import platform as _platform
from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
from threading import Thread
from urllib.request import urlopen
from qt_thread_updater import get_updater

#Globals definition
debugging=False
actualVersion = 3.7

popup=False
use_x = False
use_y = False
use_z = False
use_a = False
use_b = False
use_c = False
maximize=False
canWrite = True
needClear = False
dotAvailable = True
numberAvailable = True
symbolAvailable = True
reWriteOperation = False
showOnTopEnabled = False
operationAvailable = False

result = 0
x_prev_value = 0
y_prev_value = 0
z_prev_value = 0
a_prev_value = 0
b_prev_value = 0
c_prev_value = 0
bracketsToClose = 0

calcHistory = ''
previousResult = ''
currentOperation = ''

needResize=[False, 900, 500]

#Essential functions
def log(s):
    global debugging
    if(debugging or not(("[   OK   ]" in s) or ("[  INFO  ]" in s))):
        print(str(time.strftime('[%H:%M:%S] ', time.gmtime(time.time())))+str(s))

def run(s):
    process =  subprocess.run(s.split(' '), shell=True)
    return process.returncode

#Update Functions
def checkUpdates(bypass=False):
    global a_char, b_char, c_char, z_char, calc, actualVersion
    try:
        response = urlopen("http://www.somepythonthings.tk/versions/calc.ver")
        response = response.read().decode("utf8")
        if(bypass=="True"):
            get_updater().call_in_main(askForUpdates, response, actualVersion, bypass="True")
        elif float(response.split("///")[0]) > actualVersion:
            get_updater().call_in_main(askForUpdates, response, actualVersion)
        else:
            log("[   OK   ] No updates found")
            return "No"
    except:
        log("[  WARN  ] Unacble to reach http://www.somepythonthings.tk/versions/calc.ver. Are you connected to the internet?")
        return "Unable"
    
def askForUpdates(response, actualVersion, bypass=False):
    if(bypass=="True"):
        downloadUpdates({'debian': response.split("///")[2].replace('\n', ''), 'win32': response.split("///")[3].replace('\n', ''), 'win64': response.split("///")[4].replace('\n', ''), 'macos':response.split("///")[5].replace('\n', '')})
    elif QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.question(calc, 'SomePythonThings Calc', "There are some updates available for SomePythonThings Calc:\nYour version: "+str(actualVersion)+"\nNew version: "+str(response.split("///")[0])+"\nNew features: \n"+response.split("///")[1]+"\nDo you want to go download and install them?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes):
        #                'debian': debian link in posotion 2                   'win32' Windows 32bits link in position 3            'win64' Windows 64bits in position 4                 'macos' macOS 64bits INTEL in position 5
        downloadUpdates({'debian': response.split("///")[2].replace('\n', ''), 'win32': response.split("///")[3].replace('\n', ''), 'win64': response.split("///")[4].replace('\n', ''), 'macos':response.split("///")[5].replace('\n', '')})
        return True
    else:
        log("[  WARN  ] User aborted update!")

def download_win(url):
    try:
        global a_char, b_char, c_char, z_char, textbox
        disableAll()
        run('cd %windir%\\..\\ & mkdir SomePythonThings')
        time.sleep(0.01)
        os.chdir("{0}/../SomePythonThings".format(os.environ['windir']))
        get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        time.sleep(0.07)
        get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        time.sleep(0.05)
        filedata = urlopen(url)
        datatowrite = filedata.read()
        filename = ""
        with open("{0}/../SomePythonThings/SomePythonThings-Calc-Updater.exe".format(os.environ['windir']), 'wb') as f:
            f.write(datatowrite)
            filename = f.name
        get_updater().call_in_main(textbox.setPlainText, "Please follow on-screen instructions to continue")
        time.sleep(0.05)
        get_updater().call_in_main(textbox.setPlainText, "Please follow on-screen instructions to continue")
        time.sleep(0.05)
        log(
            "[   OK   ] file downloaded to C:\\SomePythonThings\\{0}".format(filename))
        get_updater().call_in_main(install_win, filename)
    except Exception as e:
        enableAll()
        get_updater().call_in_main(throw_error, "SomePythonThings Calc", "An error occurred when downloading the SomePythonTings Calc installer. Please check your internet connection and try again later\n\nError Details:\n{0}".format(str(e)))

def install_win(filename):
    try:
        throw_info("SomePythonThings Calc Updater", "The file has been downloaded successfully and the setup will start now. When clicking OK, the application will close and a User Account Control window will appear. Click Yes on the User Account Control Pop-up asking for permissions to launch SomePythonThings-Calc-Updater.exe. Then follow the on-screen instructions.")
        run('start /B {0} /silent'.format(filename))
        get_updater().call_in_main(sys.exit)
        sys.exit()
    except Exception as e:
        throw_error("SomePythonThings Calc Updater", "An error occurred when downloading the SomePythonTings Calc installer. Please check your internet connection and try again later\n\nError Details:\n{0}".format(str(e)))

def downloadUpdates(links):
    log(
        '[   OK   ] Reached downloadUpdates. Download links are "{0}"'.format(links))
    if _platform == 'linux' or _platform == 'linux2':  # If the OS is linux
        log("[   OK   ] platform is linux, starting auto-update...")
        throw_info("SomePythonThings Updater", "The new version is going to be downloaded and installed automatically. \nThe installation time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nPlease DO NOT kill the program until the update is done, because it may corrupt the executable files.\nClick OK to start downloading.")
        get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        time.sleep(0.07)
        get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        time.sleep(0.07)
        p1 = os.system(
            'cd; rm somepythonthings-calc_update.deb; wget -O "somepythonthings-calc_update.deb" {0}'.format(links['debian']))
        if(p1 == 0):  # If the download is done
            get_updater().call_in_main(textbox.setPlainText, "The program is being installed. Please wait until the installation process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
            time.sleep(0.07)
            get_updater().call_in_main(textbox.setPlainText, "The program is being installed. Please wait until the installation process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
            time.sleep(0.07)
            p2 = os.system('cd; echo "{0}" | sudo -S apt install ./"somepythonthings-calc_update.deb"'.format(QtWidgets.QInputDialog.getText(calc, "Autentication needed - SomePythonThings Calc", "Please write your password to perform the update. \nThis password is NOT going to be stored anywhere in any way and it is going to be used ONLY for the update.\nIf you want, you can check that on the source code on github: \n(https://github.com/martinet101/SomePythonThings-Calc/)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0]))
            if(p2 == 0):  # If the installation is done
                p3 = os.system(
                    'cd; rm "./somepythonthings-calc_update.deb"')
                if(p3 != 0):  # If the downloaded file cannot be removed
                    log("[  WARN  ] Could not delete update file.")
                throw_info("SomePythonThings Calc Updater",
                           "The update has been applied succesfully. Please reopen the application")
                sys.exit()
            else:  # If the installation is falied on the 1st time
                p4 = os.system('cd; echo "{0}" | sudo -S apt install ./"somepythonthings-calc_update.deb" -y '.format(QtWidgets.QInputDialog.getText(calc, "Autentication needed - SomePythonThings Calc",
                                                                                                                                                        "An error occurred while autenticating. Insert your password again (This attempt will be the last one)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0]))
                if(p4 == 0):  # If the installation is done on the 2nd time
                    throw_info("SomePythonThings Calc Updater",
                               "The update has been applied succesfully. Please reopen the application")
                    os.system(
                        'cd; rm "./somepythonthings-calc_update.deb"')
                    sys.exit()
                else:  # If the installation is falied on the 2nd time
                    throw_error("SomePythonThings Calc", "An error occurred while downloading the update. You have to be logged on with an administrator account to perform this operation. If the problem persists, try to download and install the program manually.")
                    webbrowser.open_new(
                        'http://www.somepythonthings.tk/programs/somepythonthings-calc/')
        else:  # If the download is falied
            throw_error("SomePythonThings Calc", "An error occurred while downloading the update. Check your internet connection. If the problem persists, try to download and install the program manually.")
            webbrowser.open_new(
                'http://www.somepythonthings.tk/programs/somepythonthings-calc/')
    elif _platform == 'win32':  # if the OS is windows
        log('win32')
        url = ""
        if(platform.architecture()[0] == '64bit'):  # if OS is 64bits
            url = (links["win64"])
        else:  # is os is not 64bits
            url = (links['win32'])
        log(url)
        get_updater().call_in_main(throw_info, "SomePythonThings Update", "The new version is going to be downloaded and prepared for the installation. \nThe download time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nClick OK to continue.")
        t = Thread(target=download_win, args=(url,))
        t.start()
        #throw_info("SomePythonThings Calc Updater","The update is being downloaded and the installer is going to be launched at the end. Please, don't quit the application until the process finishes.")
    elif _platform == 'darwin':
        log("[   OK   ] platform is macOS, starting auto-update...")
        t = Thread(target=download_macOS, args=(links,))
        t.start()
    else:  # If os is unknown
        webbrowser.open_new(
            '://www.somepythonthings.tk/programs/somepythonthings-calc/')

def download_macOS(links):
    get_updater().call_in_main(throw_info, "SomePythonThings Updater", "The new version is going to be downloaded and installed automatically. \nThe installation time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nPlease DO NOT kill the program until the update is done, because it may corrupt the executable files.\nClick OK to start downloading.")
    get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
    os.system('cd; rm somepythonthings-calc_update.dmg')
    try:  
        filedata = urlopen(links['macos'])
        datatowrite = filedata.read()
        os.chdir(os.path.expanduser("~"))
        with open("somepythonthings-calc_update.dmg", 'wb') as f:
            f.write(datatowrite)
        get_updater().call_in_main(install_macOS)
        log("[   OK   ] Download is done, starting launch process.")
    except:  
        throw_error("SomePythonThings Calc Updater", "An error occurred while downloading the update. Check your internet connection. If the problem persists, try to download and install the program manually.")
        webbrowser.open_new('http://www.somepythonthings.tk/programs/somepythonthings-calc/')

def install_macOS():
    get_updater().call_in_main(textbox.setPlainText, "Please follow on-screen instructions to continue")
    time.sleep(0.05)
    get_updater().call_in_main(textbox.setPlainText, "Please follow on-screen instructions to continue")
    time.sleep(0.05)
    throw_info("SomePythonThings Calc Updater", "The updaye file has been downloaded successfully. When you click OK, SomePythonThings Calc is going to be closed and a DMG file will automatically be opened. Then, you'll need to drag the application on the DMG to the applications folder (also on the DMG). Click OK to continue")
    p2 = os.system('cd; open ./"somepythonthings-calc_update.dmg"')
    log("[  INFO  ] macOS installation unix output code is \"{0}\"".format(p2))
    sys.exit()
#End of updates functions

def throw_info(title, body, icon="calc-icon.png"):
    global a_char, b_char, c_char, z_char, calc
    if(icon==False):
        icon='calc-icon.png'
    log("[  INFO  ] "+body)
    msg = QtWidgets.QMessageBox(calc)
    if(os.path.exists(str(realpath)+"/"+str(icon))):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/"+str(icon)))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_warning(title, body, warning="Not Specified"):
    global a_char, b_char, c_char, z_char, calc
    log("[  WARN  ] "+body+"\n\tWarning reason: "+warning)
    msg = QtWidgets.QMessageBox(calc)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_error(title, body, error="Not Specified"):
    global a_char, b_char, c_char, z_char, calc
    log("[ FAILED ] "+body+"\n\tError reason: "+error)
    msg = QtWidgets.QMessageBox(calc)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def scrollBottom():
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox
    textbox.moveCursor(QtGui.QTextCursor.End)

def appendText(t):
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox
    textbox.setPlainText(str(textbox.toPlainText())+str(t))
    scrollBottom()

def changeFontSize(button, size):
    global font, buttons
    buttons[button].setFont(QtGui.QFont(str(font), int(size)))
    #button.setStyleSheet(f"* {{font-size: {size}px;}}")

def print_symbol_and_close(s):
    print_symbol(s)
    show_popup()

def ANSWER():
    global previousResult
    if (not(previousResult=="")):
        print_symbol_and_close("Ans")

def pasteOperation():
    show_popup()
    global textbox, currentOperation, needClear
    log("[  INFO  ] Starting pasteOperaion()")
    toPaste = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "Paste here your custom operation: ", QtWidgets.QLineEdit.Normal, str(0))[0]
    if needClear:
        needClear=False
        currentOperation = toPaste
        textbox.appendPlainText('\n'+toPaste+' ')
    else:
        currentOperation += toPaste
        appendText(' '+toPaste+' ')
    scrollBottom()

def editOperation():
    show_popup()
    global currentOperation, calcHistory, needClear
    log("[  INFO  ] Starting editOperation()")
    toEdit = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "Edit your operation: (This will erase the history)", QtWidgets.QLineEdit.Normal, str(currentOperation))[0]
    textbox.setPlainText(toEdit)
    currentOperation = toEdit
    needClear = False
    scrollBottom()

def print_symbol(s):
    s = str(s)
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, needClear, currentOperation, operationAvailable, canWrite, symbolAvailable, numberAvailable, dotAvailable
    if canWrite:
        if not symbolAvailable:
            print_operation("*")
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, needClear, currentOperation, operationAvailable, canWrite, numberAvailable, symbolAvailable
    if canWrite:
        if not numberAvailable:
            print_operation("*")
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  previousResult, currentOperation, needClear, dotAvailable, bracketsToClose, operationAvailable, canWrite, symbolAvailable, numberAvailable
    log("[  INFO  ] Starting print_operation(): canWrite={0}, needClear={1}, operationAvailable={2}, o={3}".format(canWrite, needClear, operationAvailable, o))
    if canWrite:
        scrollBottom()
        if needClear:
            if not '√' in o:
                appendText("\n\n" + str(previousResult))
                currentOperation = str(previousResult)
            else:
                appendText('\n\n')
                currentOperation=""
            needClear = False
        if o in '^(*/':
            if operationAvailable:
                appendText(' '+o+' ')
                currentOperation += ' '+o+' '
        else:
            if o=="√":
                o += '('
            appendText(' '+o+' ')
            currentOperation += ' '+o+' '
        operationAvailable = False
        dotAvailable = True
        symbolAvailable = True
        numberAvailable = True
        if o == '^(' or o=='√(':
            bracketsToClose += 1
    scrollBottom()

def print_bracket(b):
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  operationAvailable, bracketsToClose, currentOperation, needClear, canWrite, dotAvailable, numberAvailable, symbolAvailable
    log("[  INFO  ] Starting print_bracket(): canWrite={0}, needClear={1}, operationAvailable={2}, o={3}".format(canWrite, needClear, operationAvailable, b))
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  needClear, dotAvailable, currentOperation, canWrite, numberAvailable, symbolAvailable
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

def huge_calculate():
    global a_char, b_char, c_char, z_char, x_char, canWrite, y_char, use_x, use_y, e_char, pi_char,  textbox,calc, operationAvailable, reWriteOperation,needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc, numberAvailable, symbolAvailable
    reWriteOperation = False
    global currentOperation
    while currentOperation.count('(')>currentOperation.count(')'):
        log("[  WARN  ] Brackets Missing !(missing {0} brackets)".format(currentOperation.count('(')-currentOperation.count(')')))
        canWrite=True
        missingBrackets = currentOperation.count('(')-currentOperation.count(')')
        get_updater().call_in_main(print_bracket, ')')
        while(missingBrackets==currentOperation.count('(')-currentOperation.count(')')):
            continue
        canWrite=False
    log("[   OK   ] No missing brackets")
    result = pure_calculate(currentOperation.replace('^', '**').replace('√', 'sqr'))
    if  not "  " in str(result):
        needClear = True
        previousResult = str(result)
        dotAvailable = True
        symbolAvailable = True
        numberAvailable = True
    else:
        if not("Syntax" in str(result)) and not("divide by zero" in str(result)):
            needClear = True
            dotAvailable = False
            operationAvailable = False
            bracketsToClose = 0
            symbolAvailable = True
            numberAvailable = True
        else:
            log("[  WARN  ] SyntaxError or ZeroDivisionError raised by eval(). Rewriting operation...")
            reWriteOperation = True
            get_updater().call_in_main(textbox.appendPlainText, result+'\n\n'+currentOperation.replace('**', '^'))
            enableAll()
            sys.exit()
    calcHistory =  textbox.toPlainText()
    if use_x or use_y:
        log("[   OK   ] X, Y, Z, A, B or C detected.")
        try:
            result = int(result)
            get_updater().call_in_main(textbox.appendPlainText, ' result = '+f"{result:,}".replace('e+', ' * 10^'))
        except:
            log("[  WARN  ] Unable to int() result. Result value is "+result)
            get_updater().call_in_main(textbox.appendPlainText, ' result = '+str(result).replace('e+', ' * 10^'))
    else:
        log("[  WARN  ] X, Y, Z, A, B or C NOT detected.")
        try:
            result = int(result)
            get_updater().call_in_main(textbox.appendPlainText, ' = '+f"{result:,}".replace('e+', ' * 10^'))
        except:
            log("[  WARN  ] Unable to int() result.")
            get_updater().call_in_main(textbox.appendPlainText, ' = '+str(result).replace('e+', ' * 10^'))
    get_updater().call_in_main(textbox.moveCursor, QtGui.QTextCursor.End)
    enableAll()

def pure_calculate(s):
    try:
        result = str(eval(str(s)))
    except OverflowError:
        result = "Well, even the Windows calculator doesn't know that...\ud83c\udf1a\n\nThis error is caused because the result was supposed to be a huuuge number with decimals, but it was that big that it overflowed the system.  "
    except SyntaxError:
        result = "Syntax Error! Please check your operation and try again:  "
    except ZeroDivisionError:
        result = "Wait! Can't divide by zero! Please check your operation and try again:  "
    except:
        result = "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!  "
    return result
def calculate():
    global a_char, b_char, title, showOnTopEnabled, c_char, z_char, x_prev_value, use_x, use_y, use_z, use_a, use_b, use_c, y_prev_value, z_prev_value, a_prev_value, b_prev_value, c_prev_value, x_char, y_char, e_char, pi_char,  calc, currentOperation, operationAvailable, needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc, numberAvailable, symbolAvailable
    if(not needClear):
        disableAll()
        use_x = False
        use_y = False
        use_z = False
        use_a = False
        use_b = False
        use_c = False
        if(_platform=='darwin'):
            title.setText('SomePythonThings Calc:  '+currentOperation)
        calc.setWindowTitle('SomePythonThings Calc:  '+currentOperation)
        while str(currentOperation[0:1]) == '0':
            currentOperation = str(currentOperation)[1:]
        if(pi_char in currentOperation):
            currentOperation = currentOperation.replace(pi_char, "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
        if(fi_char in currentOperation):
            currentOperation = currentOperation.replace(fi_char, "1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374")
        if(e_char in currentOperation):
            currentOperation = currentOperation.replace(e_char, "2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274")
        if("Ans" in currentOperation):
            currentOperation = currentOperation.replace("Ans", previousResult)
        if(x_char in currentOperation):
            x = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+x_char+" on the operation.\nEnter value for "+x_char+": ", QtWidgets.QLineEdit.Normal, str(x_prev_value))
            x_prev_value = (x[0].replace(",", "."))
            use_x = True
            currentOperation = currentOperation.replace(x_char, '({0})'.format(x[0].replace(",", ".")))
        if(y_char in currentOperation):
            y = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+y_char+" on the operation.\nEnter value for "+y_char+": ", QtWidgets.QLineEdit.Normal, str(y_prev_value))
            y_prev_value = (y[0].replace(",", "."))
            use_y = True
            currentOperation = currentOperation.replace(y_char, '({0})'.format(y[0].replace(",", ".")))
        if(z_char in currentOperation):
            z = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+z_char+" on the operation.\nEnter value for "+z_char+": ", QtWidgets.QLineEdit.Normal, str(z_prev_value))
            z_prev_value = (z[0].replace(",", "."))
            use_z = True
            currentOperation = currentOperation.replace(z_char, '({0})'.format(z[0].replace(",", ".")))
        if(a_char in currentOperation):
            a = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+a_char+" on the operation.\nEnter value for "+a_char+": ", QtWidgets.QLineEdit.Normal, str(a_prev_value))
            a_prev_value = (a[0].replace(",", "."))
            use_a = True
            currentOperation = currentOperation.replace(a_char, '({0})'.format(a[0].replace(",", ".")))
        if(b_char in currentOperation):
            b = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+b_char+" on the operation.\nEnter value for "+b_char+": ", QtWidgets.QLineEdit.Normal, str(b_prev_value))
            b_prev_value = (b[0].replace(",", "."))
            use_b = True
            currentOperation = currentOperation.replace(b_char, '({0})'.format(b[0].replace(",", ".")))
        if(c_char in currentOperation):
            c = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+c_char+" on the operation.\nEnter value for "+c_char+": ", QtWidgets.QLineEdit.Normal, str(c_prev_value))
            c_prev_value = (c[0].replace(",", "."))
            use_c = True
            currentOperation = currentOperation.replace(c_char, '({0})'.format(c[0].replace(",", ".")))
        if use_x:
            textbox.appendPlainText(' {0} value is "{1}" '.format(x_char, x_prev_value))
        if use_y:
            textbox.appendPlainText(' {0} value is "{1}"'.format(y_char, y_prev_value))
        if use_z:
            textbox.appendPlainText(' {0} value is "{1}" '.format(z_char, z_prev_value))
        if use_a:
            textbox.appendPlainText(' {0} value is "{1}"'.format(a_char, a_prev_value))
        if use_b:
            textbox.appendPlainText(' {0} value is "{1}" '.format(b_char, b_prev_value))
        if use_c:
            textbox.appendPlainText(' {0} value is "{1}"'.format(c_char, c_prev_value))
        t = Thread(target=huge_calculate)
        t.daemon = (True)
        t.start()
        
def disableAll():
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  canWrite
    canWrite = False

def enableAll():
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  canWrite
    canWrite = True

def sqr(n):
    return n**0.5

def clear():
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, canWrite, operationAvailable, symbolAvailable,numberAvailable,dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, canWrite, operationAvailable, dotAvailable, bracketsToClose, needClear, previousResult, calcHistory, currentOperation, symbolAvailable, numberAvailable
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, currentOperation
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
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  dotAvailable, bracketsToClose, operationAvailable, numberAvailable, symbolAvailable
    if c == '.':
        dotAvailable = True
    elif c == '(':
        bracketsToClose -= 1
    elif c == ')':
        bracketsToClose += 1
    elif c in '*/^√+-':
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
    elif key == QtCore.Qt.Key_V:
        print_operation('√')
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
    elif key == QtCore.Qt.Key_P:
        print_symbol(pi_char)
    elif key == QtCore.Qt.Key_E:
        print_symbol(e_char)
    elif key == QtCore.Qt.Key_X:
        print_symbol(x_char)
    elif key == QtCore.Qt.Key_Y:
        print_symbol(y_char)
    elif key == QtCore.Qt.Key_Z:
        print_symbol(z_char)
    elif key == QtCore.Qt.Key_A:
        print_symbol(a_char)
    elif key == QtCore.Qt.Key_B:
        print_symbol(b_char)
    elif key == QtCore.Qt.Key_C:
        print_symbol(c_char)
    #else:
    #   log('key pressed: %i' % key)
    
def show_popup():
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  popup, buttons
    if(popup):
        popup=False
        buttons["POPUP"].setText("<  ")
    else:
        popup=True
        buttons["POPUP"].setText(">  ")
    resizeWidgets()

def quitCalc():
    log("[  INFO  ] Quitting application...")
    global calc
    calc.close()

def minimizeCalc():
    log("[  INFO  ] Minimizing application...")
    global calc
    calc.showMinimized()

def maximizeCalc(side='center'):
    global maximize, calc, _platform, needResize
    log("[   OK   ] Starting maximizeCalc(), side value is '{0}'".format(side))
    if(side=='center'):
        if(not maximize):
            log("[  INFO  ] Not maximized")
            needResize=[True, calc.height(), calc.width()]
            if(_platform=="darwin"):
                calc.showFullScreen()
                log("[   OK   ] Fullscreening")
            else:
                calc.showMaximized()
                log("[   OK   ] Maximizing")
            maximize=True
        else:
            maximize=False
            calc.showNormal()
            log("[   OK   ] Restoring")
    elif(side=='right'):
        if(_platform=='darwin'):
            log("[  INFO  ] Aligning to the right...")
            needResize=[True, calc.height(), calc.width()]
            screen = calc.screen()
            size = screen.availableGeometry()
            calc.setGeometry(0, 0, int(size.width()/2), size.height())
    elif(side=='left'):
        if(_platform=='darwin'):
            log("[  INFO  ] Aligning to the left...")
            needResize=[True, calc.height(), calc.width()]
            screen = calc.screen()
            size = screen.availableGeometry()
            calc.setGeometry(int(calc.screen().size().width()/2), 0, int(size.width()/2), size.height())

def saveHistory():
    global calc, textbox
    try:
        f = open(QtWidgets.QFileDialog.getSaveFileName(calc, 'Save the SomePythonThings Calc history', "SomePythonThings Calc History.txt", ('Text Files (*.txt);;All files (*.*)'))[0], 'w')
        log("[   OK   ] File {0} opened successfully.".format(f.name))
        text = textbox.toPlainText()
        for old, new in [(x_char, 'x'), (y_char, 'y'), (z_char, 'z'), (a_char, 'a'), (b_char, 'b'), (c_char, 'c'), (pi_char, 'π'), (e_char, 'e'), (fi_char, 'φ')]:
            text = text.replace(old, new)
        f.write(text)
        fname = os.path.abspath(f.name)
        f.close()
        throw_info("SomePythonThings Calc", "SomePythonThings Calc History saved sucessfully to {0}".format(fname))
        if(_platform=='win32'):
            p = subprocess.Popen('start /B notepad.exe "'+fname.replace('\\', '/')+'"', shell=True)
        else:
            p = subprocess.Popen('open "'+fname.replace('\\', '/')+'"', shell=True)
    except Exception as e:
        if(debugging):
            raise e
        if (not str(e)=="[Errno 2] No such file or directory: ''"):
            throw_error("SomePythonThings Calc", "Unable to save SomePythonThings Calc History.\n\nError Reason: {0}".format(e))
        else:
            log("[  WARN  ] User cancelled the dialog")

def checkDirectUpdates():
    global actualVersion
    result = checkUpdates()
    if(result=='No'):
        throw_info("SomePythonThings Calc Updater", "There aren't updates available at this time. \n(actual version is {0})".format(actualVersion))
    elif(result=="Unable"):
        throw_warning("SomePythonThings Calc Updater", "Can't reach SomePythonThings Servers!\n  - Are you connected to the internet?\n  - Is your antivirus or firewall blocking SomePythonThings Calc?\nIf none of these solved the problem, please check back later.")

def openHelp():
    webbrowser.open_new("http://www.somepythonthings.tk/programs/somepythonthings-calc/help/")

def reinstallCalc():
    log('[        ] starting reinstall process...')
    Thread(target=checkUpdates, args=("True",), daemon=True).start()

def showOnTop():
    global showOnTopEnabled, title, calc, topAction
    if(not(showOnTopEnabled)):
        showOnTopEnabled = True
        if(_platform=='darwin'):
            flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.BypassWindowManagerHint)# | QtCore.Qt.X11BypassWindowManagerHint)
        else:
            flags = QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint)#| QtCore.Qt.X11BypassWindowManagerHint)# | QtCore.Qt.BypassWindowManagerHint)# | QtCore.Qt.X11BypassWindowManagerHint)
        calc.setWindowFlags(flags)
        if(_platform=='darwin'):
            buttons['exit'].show()
            buttons['minimize'].show()
            buttons['maximize'].show()
        topAction.setCheckable(True)
        if(_platform=='darwin'):
            title.setText(calc.windowTitle())
            title.setGeometry(170, 1, calc.width()-292, 28)
            title.show()
        log("[   OK   ] Re-showing Window...")
        calc.show()
        resizeWidgets()
    else:
        showOnTopEnabled = False
        if(_platform=='darwin'):
            flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        else:
            flags = QtCore.Qt.WindowFlags()
        calc.setWindowFlags(flags)
        topAction.setCheckable(True)
        log("[   OK   ] Re-showing Window...")
        calc.hide()
        calc.show()
        resizeWidgets()

def resizeWidgets(resizeWindow=False, winHeight=600, winWidth=900):
    log("[  INFO  ] Starting resizeWidgets()")
    global a_char, b_char, c_char, z_char, title, grips, x_char, y_char, e_char, pi_char,  buttons, popup, textbox, calc
    if(not(resizeWindow)):
        winHeight = calc.height()
        winWidth = calc.width()
    else:
        calc.resize(winWidth, winHeight)
    log("[   OK   ] Window size is {0}*{1}px".format(winHeight, winWidth))
    buttons['POPUP'].show()
    if(winWidth<=1099):
        fullWinWidth = winWidth
        big_width = int(25/100*winWidth)+1
        tiny_width = int(12.5/100*winWidth)+1
        small_width = int(17/100*winWidth)+1
        height = int(14/100*winHeight+1)+1
        first_row = int(30/100*winHeight)
        second_row= int((30+14)/100*winHeight)
        third_row= int((30+14*2)/100*winHeight)
        fourth_row= int((30+14*3)/100*winHeight)
        fifth_row= int((30+14*4)/100*winHeight)
        big_1st_column = int((25*0)/100*winWidth)
        big_2nd_column = int((25*1)/100*winWidth)
        big_3rd_column = int((25*2)/100*winWidth)
        big_4th_column = int((25*3)/100*winWidth)
        small_1st_column = int((12.5*0)/100*winWidth)
        small_2nd_column = int((12.5*1)/100*winWidth)
        small_3rd_column = int((12.5*2)/100*winWidth)
        small_4th_column = int((12.5*3)/100*winWidth)
        small_5th_column = int((16.6666*3)/100*winWidth)
        small_6th_column = int((16.6666*4)/100*winWidth)
        small_7th_column = int((16.6666*5)/100*winWidth)
    else:
        fullWinWidth = winWidth
        winWidth = winWidth*0.75
        big_width = int(25/100*winWidth)+1
        tiny_width = int(12.5/100*winWidth)+1
        small_width = int(17/100*winWidth)+1
        height = int(14/100*winHeight+1)+1
        first_row = int(30/100*winHeight)
        second_row= int((30+14)/100*winHeight)
        third_row= int((30+14*2)/100*winHeight)
        fourth_row= int((30+14*3)/100*winHeight)
        fifth_row= int((30+14*4)/100*winHeight)
        big_1st_column = int((25*0)/100*winWidth)
        big_2nd_column = int((25*1)/100*winWidth)
        big_3rd_column = int((25*2)/100*winWidth)
        big_4th_column = int((25*3)/100*winWidth)
        small_1st_column = int((12.5*0)/100*winWidth)
        small_2nd_column = int((12.5*1)/100*winWidth)
        small_3rd_column = int((12.5*2)/100*winWidth)
        small_4th_column = int((12.5*3)/100*winWidth)
        small_5th_column = int((16.6666*3)/100*winWidth)
        small_6th_column = int((16.6666*4)/100*winWidth)
        small_7th_column = int((16.6666*5)/100*winWidth)
    textbox.resize(fullWinWidth ,int((winHeight/100*30)-29))
    if(_platform=='darwin'):
        grips['bottom-right'].setGeometry(int(calc.width()/2)+1, int(calc.height()-2), int(calc.width()/2)+1, 2)
        grips['right-bottom'].setGeometry(int(calc.width())-2, int(calc.height()/2)+1, 2, int(calc.height()/2)+1)
        grips['bottom-left'].setGeometry(0, int(calc.height()-2), int(calc.width()/2)+1, 2)
        grips['left-bottom'].setGeometry(0, int(calc.height()/2)+1, 2, int(calc.height()/2)+1)
        grips['top-right'].setGeometry(int(calc.width()/2)+1, 0, int(calc.width()/2)+1, 2)
        grips['right-top'].setGeometry(int(calc.width())-2, 0, 2, int(calc.height()/2)+1)
        grips['top-left'].setGeometry(0, 0, int(calc.width()/2)+1, 2)
        grips['left-top'].setGeometry(0, 0, 2, int(calc.height()/2)+1)
    if(int(20/900*fullWinWidth)<int(20/500*winHeight)):
        fontsize = str(int(20/900*fullWinWidth))
        log("[   OK   ] Width > Height, font size is {0}".format(fontsize))
    else:
        fontsize = str(int(20/500*winHeight))
        log("[   OK   ] Width < Height, font size is {0}".format(fontsize))
    if(int(fontsize)<18):
        log("[   OK   ] Font size under 18, setting 18 value")
        buttons['CA'].setText('CA')
        buttons['CO'].setText('C')
        buttons['Del'].setText('Del')
        log("[   OK   ] Changing Ca, C and Del text to minified label")
        fontsize="18"
    else:
        buttons['CA'].setText('Clear All')
        buttons['CO'].setText('Clear')
        buttons['Del'].setText('Delete')
        log("[   OK   ] Changing Ca, C and Del text to full label")
    if(int(fontsize)>28):
        log("[   OK   ] Font size over 28, setting 28 value")
        fontsize="28"
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
    buttons['^('].resize(tiny_width, height) #Resize button
    buttons['√'].move(small_4th_column, first_row)
    buttons['√'].resize(tiny_width, height) #Resize button
    buttons['+'].move(big_4th_column, fourth_row)
    buttons['+'].resize(big_width, height) #Resize button
    buttons['-'].move(big_4th_column, fifth_row)
    buttons['-'].resize(big_width, height) #Resize button
    buttons['='].move(big_3rd_column, fifth_row)
    buttons['='].resize(big_width, height) #Resize button
    buttons['.'].move(big_1st_column, fifth_row)
    buttons['.'].resize(big_width, height) #Resize button
    buttons['('].move(small_1st_column, first_row)
    buttons['('].resize(tiny_width, height) #Resize button
    buttons[')'].move(small_2nd_column, first_row)
    buttons[')'].resize(tiny_width, height) #Resize button
    buttons['Del'].move(small_5th_column, first_row)
    buttons['Del'].resize(small_width, height) #Resize button
    buttons['CO'].move(small_6th_column, first_row)
    buttons['CO'].resize(small_width, height) #Resize button
    buttons['CA'].move(small_7th_column, first_row)
    buttons['CA'].resize(small_width, height) #Resize button
    if(_platform=='darwin'):
        buttons['exit'].move(fullWinWidth-42, 2)
        buttons['exit'].resize(40, 26) #Resize button
        buttons['maximize'].move(fullWinWidth-82, 2)
        buttons['maximize'].resize(40, 26) #Resize button
        buttons['minimize'].move(fullWinWidth-122, 2)
        buttons['minimize'].resize(40, 26) #Resize button
    if(fullWinWidth<1100):
        if(not popup):
            buttons["="].setStyleSheet("""
            QPushButton
            { 
                border: none; 
                background-color: #33998a; 
                font-size:"""+fontsize+"""px; 
                color: #DDDDDD; 
                font-family: \""""+font+"""\", monospace;
                font-weight: bold;
                border-radius: 0px; 
            }
            
            #top-left{
                border-top-left-radius: 3px;
                }
            #top-right{
                border-top-right-radius: 3px;
                }
            #bottom-left{
                border-bottom-left-radius: 3px;
                }
            #bottom-right{
                border-bottom-right-radius: 3px;
            }
            #equal {
                border-top-left-radius: 3px;
            }
            QPushButton::hover
            {
                background-color: #222222;
            }
            """)
            buttons['POPUP'].move(winWidth-26, int(winHeight/2)-25)
            pX = int(winWidth)
            pY = int(winHeight/2)
            pWidth = int(winWidth/100*20)
            pHeight = int(height)
            buttons["X"].move(pX, (pY-height*2))
            buttons["X"].resize(pWidth, pHeight)
            buttons["Y"].move(pX, pY-height)
            buttons["Y"].resize(pWidth, pHeight)
            buttons["PI"].move(pX, pY)
            buttons["PI"].resize(pWidth, pHeight)
            buttons["E"].move(pX, pY+height)
            buttons["E"].resize(pWidth, pHeight)
            buttons["Z"].move(pX, (pY-height*2))
            buttons["Z"].resize(pWidth, pHeight)
            buttons["A"].move(pX, pY-height)
            buttons["A"].resize(pWidth, pHeight)
            buttons["B"].move(pX, pY)
            buttons["B"].resize(pWidth, pHeight)
            buttons["C"].move(pX, pY+height)
            buttons["C"].resize(pWidth, pHeight)
            buttons["GOLDEN-RATIO"].move(pX, pY)
            buttons["GOLDEN-RATIO"].resize(pWidth, pHeight)
            buttons["ANS"].move(pX, pY+height)
            buttons["ANS"].resize(pWidth, pHeight)
            buttons["EDIT"].move(pX, pY+height)
            buttons["EDIT"].resize(pWidth, pHeight)
            buttons["PASTE"].move(pX, pY+height)
            buttons["PASTE"].resize(pWidth, pHeight)
            buttons['POPUP'].show()
        else:
            buttons["="].setStyleSheet("""
            QPushButton
            { 
                border: none; 
                background-color: #222222; 
                font-size:"""+fontsize+"""px; 
                color: #DDDDDD; 
                font-family: \""""+font+"""\", monospace;
                font-weight: bold;
                border-radius: 0px;
            }
        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }
            QPushButton::hover
            {
                background-color: #222222;
            }
            """)
            buttons["="]
            pX = int(winWidth/100*80)
            pY = int(winHeight/2)
            pWidth = int(winWidth/100*20)
            pHeight = height
            buttons['POPUP'].move(pX-pWidth-25, int(winHeight/2)-25)
            buttons["X"].move(pX, pY-height*3)
            buttons["X"].resize(pWidth, pHeight+1)
            buttons["Y"].move(pX, pY-height*2)
            buttons["Y"].resize(pWidth, pHeight+1)
            buttons["Z"].move(pX, pY-height)
            buttons["Z"].resize(pWidth, pHeight+1)
            buttons["A"].move(pX, pY)
            buttons["A"].resize(pWidth, pHeight+1)
            buttons["B"].move(pX, pY+height)
            buttons["B"].resize(pWidth, pHeight+1)
            buttons["C"].move(pX, pY+height*2)
            buttons["C"].resize(pWidth, pHeight+1)
            buttons["PI"].move(pX-pWidth, pY-height*3)
            buttons["PI"].resize(pWidth, pHeight+1)
            buttons["E"].move(pX-pWidth, pY-height*2)
            buttons["E"].resize(pWidth, pHeight+1)
            buttons["GOLDEN-RATIO"].move(pX-pWidth, pY-height)
            buttons["GOLDEN-RATIO"].resize(pWidth, pHeight+1)
            buttons["ANS"].move(pX-pWidth, pY)
            buttons["ANS"].resize(pWidth, pHeight+1)
            buttons["EDIT"].move(pX-pWidth, pY+height)
            buttons["EDIT"].resize(pWidth, pHeight+1)
            buttons["PASTE"].move(pX-pWidth, pY+height*2)
            buttons["PASTE"].resize(pWidth, pHeight+1)
        buttons['POPUP'].resize(50, 50) #Resize button
        buttons['POPUP'].show()
    else:
        buttons["="].setStyleSheet("""
            QPushButton
            { 
                border: none; 
                background-color: #33998a; 
                font-size:"""+fontsize+"""px; 
                color: #DDDDDD; 
                font-family: \""""+font+"""\", monospace;
                font-weight: bold;
                border-radius: 0px;
            }
            
        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }
            QPushButton::hover
            {
                background-color: #222222;
            }
            """)
        buttons["="]
        pX = int(fullWinWidth*0.75)-1
        pY = int(winHeight*0.3)
        pWidth = int((fullWinWidth*0.25)/2)
        pHeight = int((winHeight*0.7)/6)
        buttons['POPUP'].move(pX-pWidth-25, int(winHeight/2)-25)
        buttons["X"].move(pX+pWidth, pY)
        buttons["X"].resize(pWidth+5, pHeight+5)
        buttons["Y"].move(pX+pWidth, pY+pHeight)
        buttons["Y"].resize(pWidth+5, pHeight+5)
        buttons["Z"].move(pX+pWidth, pY+pHeight*2)
        buttons["Z"].resize(pWidth+5, pHeight+5)
        buttons["A"].move(pX+pWidth, pY+pHeight*3)
        buttons["A"].resize(pWidth+5, pHeight+5)
        buttons["B"].move(pX+pWidth, pY+pHeight*4)
        buttons["B"].resize(pWidth+5, pHeight+5)
        buttons["C"].move(pX+pWidth, pY+pHeight*5)
        buttons["C"].resize(pWidth+5, pHeight+5)
        buttons["PI"].move(pX, pY)
        buttons["PI"].resize(pWidth+5, pHeight+5)
        buttons["E"].move(pX, pY+pHeight)
        buttons["E"].resize(pWidth+5, pHeight+5)
        buttons["GOLDEN-RATIO"].move(pX, pY+pHeight*2)
        buttons["GOLDEN-RATIO"].resize(pWidth+5, pHeight+5)
        buttons["ANS"].move(pX, pY+pHeight*3)
        buttons["ANS"].resize(pWidth+5, pHeight+5)
        buttons["EDIT"].move(pX, pY+pHeight*4)
        buttons["EDIT"].resize(pWidth+5, pHeight+5)
        buttons["PASTE"].move(pX, pY+pHeight*5)
        buttons["PASTE"].resize(pWidth+5, pHeight+5)
        buttons['POPUP'].hide()
    if(_platform=='darwin'):
        title.setGeometry(175, 2, fullWinWidth-295, 26)
        dragBar.setGeometry(175, 2, fullWinWidth-295, 26)
        title.setAlignment(QtCore.Qt.AlignCenter)
        if(fullWinWidth>600):
            title.show()
            dragBar.hide()
        else:
            dragBar.show()
            title.hide()
        buttons["exit"].setStyleSheet("""
            QPushButton
            {
                border: none;
                background-color: #DD0000;
                color: #DDDDDD;
                font-weight: bold;
            }
            QPushButton::hover
            {
                background-color: #BB0000;
            }
                    """)
        for button in ["maximize", "minimize"]:
            buttons[button].setStyleSheet("""
            QPushButton
            {
                border: none;
                background-color: #333333;
                color: #DDDDDD;
                font-weight: bold;
            }
            QPushButton::hover
            {
                background-color: #202020;
            }
            """)
        buttons['maximize'].setStyleSheet("""
            QPushButton
            {
                border: none;
                background-color: #333333;
                color: #DDDDDD;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton::hover
            {
                background-color: #202020;
            }
            """)
    for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(', '√']: #Grey (#333333)
        buttons[button].setStyleSheet("""
            QPushButton
            {
                border: none;
                background-color: #333333;
                font-size:"""+fontsize+"""px;
                color: #DDDDDD;
                font-family: \""""+font+"""\", monospace;
                font-weight: bold;
                width: 25%;
                border-radius: 0px;
            }
            

            
            #top-left{
                border-top-left-radius: 3px;
                }
            #top-right{
                border-top-right-radius: 3px;
                }
            #bottom-left{
                border-bottom-left-radius: 3px;
                }
            #bottom-right{
                border-bottom-right-radius: 3px;
                }
            QPushButton::hover
            {
                background-color: #222222;
            }
            """)
    for button in ['.', '+', '-', '*', '/']:# blue grey (#49525C)
        buttons[button].setStyleSheet("""
        QPushButton
        { 
            border: none; 
            background-color: #49525C; 
            font-size:"""+fontsize+"""px; 
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold; 
            border-radius: 0px;
        }
        

        
        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }
        QPushButton::hover
        {
            background-color: #222222;
        }
        """)
    for button in ['Del', 'CO', 'CA']:#Dark Grey (#222222)
        buttons[button].setStyleSheet("""
        QPushButton 
        { 
            border: none; 
            background-color: #222222; 
            font-size:"""+fontsize+"""px;
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold;
            border-radius: 0px; 
        }
        

        
        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }
        QPushButton::hover
        {
            background-color: #111111;
        }
        """)
    for button in ['PI', 'X', 'Y', 'Z', 'A', 'B', 'C', 'E', "GOLDEN-RATIO", "ANS", "EDIT", "PASTE"]: #Turquoise (#33998a)
        buttons[button].setStyleSheet("""
        QPushButton
        {
            border: none; 
            background-color: #33998a; 
            font-size:"""+fontsize+"""px; 
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold;
            border-radius: 0px; 
        }  
        

        
        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }
        QPushButton::hover
        {
            color: #DDDDDD;
            background-color: #222222;
        }
        """)
    textbox.setStyleSheet("""
        QPlainTextEdit
        {
            border:none; 
            background-color: #222222; 
            font-size:"""+fontsize+"""px; 
            color: #DDDDDD; 
            font-family: \""""+font+"""\", monospace;
            font-weight: bold;
        }
        """)
    if(fullWinWidth<300 or winHeight<300 or fullWinWidth >= 1100):
        buttons["POPUP"].hide()
    else:
        buttons["POPUP"].show()
    buttons["POPUP"].setStyleSheet("""
        QPushButton
        { 
            border-radius: 25px;
            background-color: "#33998a";
        }
        QPushButton::hover
        {
            background-color: "#222222";
        }
        """)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class Window(QtWidgets.QMainWindow):
    resized = QtCore.Signal()
    keyRelease = QtCore.Signal(int)
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.resized.connect(resizeWidgets)
        self.oldPos = self.pos()
        self.canMove=False
        self.widget = QtWidgets.QWidget(self)
        self.widget.setObjectName('app')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def keyReleaseEvent(self, event):
        super(Window, self).keyReleaseEvent(event)
        self.keyRelease.emit(event.key())

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.canMove = True

    def mouseReleaseEvent(self, event):
        self.canMove = False
        screen = self.screen()
        size = screen.size()
        if(event.globalPos().y() == 0):
            maximizeCalc('center')
        elif(event.globalPos().x() == 0):
            maximizeCalc(side='right')
        elif(event.globalPos().x() >= size.width()-1):
            maximizeCalc(side='left')

    def mouseMoveEvent(self, event):
        global needResize
        if(self.canMove):
            if(needResize[0]):
                calc.resize(needResize[2], needResize[1])
                needResize=[False, calc.height(), calc.width()]
            delta = QtCore.QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

if(__name__=="__main__"):
    if(len(sys.argv)>1):
        if('debug' in sys.argv[1]):
            debugging=True
    log("[        ] Welcome to SomePythonThings Calc {0} log. debugging is set to {1}".format(actualVersion, debugging))
    if _platform == "linux" or _platform == "linux2":
        log("[   OK   ] Platform is linux")
        os.chdir("/bin/")
        font = "Ubuntu Mono"
        x_char = "x"
        y_char = "y"
        z_char = "z"
        a_char = "a"
        b_char = "b"
        c_char = "c"
        e_char = "e"
        pi_char = "π"
        fi_char = "φ"
        sqr_char="√"
        close_icon = "✕"
        maximize_icon = "□"
        minimize_icon = "-"
        realpath = "/bin"
    elif _platform == "darwin":
        log("[   OK   ] Platform is macOS")
        font = "Courier"
        x_char = "x"
        y_char = "y"
        z_char = "z"
        a_char = "a"
        b_char = "b"
        c_char = "c"
        e_char = "π"
        pi_char = "π"
        fi_char = "φ"
        sqr_char="√"
        close_icon = "✕"
        maximize_icon = "□"
        minimize_icon = "-"
        realpath = "/Applications/SomePythonThings Calc.app/Contents/Resources"
    elif _platform == "win32":
        log("[   OK   ] Platform is windows")
        if int(platform.release()) >= 10: #Font check: os is windows 10
            font = "Cascadia Mono"#"Cascadia Mono"
            log("[   OK   ] OS detected is win32 release 10 ")
        else:# os is windows 7/8
            font="Consolas"#"Consolas"
            log("[   OK   ] OS detected is win32 release 8 or less ")
        if(os.path.exists("\\Program Files\\SomePythonThingsCalc\\resources-sptmusic")):
            realpath = "/Program Files/SomePythonThingsCalc/resources-sptmusic"
            log("[   OK   ] Directory set to /Program Files/SomePythonThingsCalc/resources-sptmusic")
        else:
            realpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
            log("[  WARN  ] Directory /Program Files/SomePythonThingsCalc/ not found, getting working directory...")
        x_char = "𝑥"
        y_char = "𝑦"
        z_char = "𝑧"
        a_char = "𝑎"
        b_char = "𝑏"
        c_char = "𝑐"
        e_char = "𝑒"
        pi_char = "𝜋"
        fi_char = "𝜙"
        sqr_char="√"
        close_icon = "x"
        maximize_icon = "□"
        minimize_icon = "-"
    else:
        log("[  WARN  ] Platform is unknown")
        font = "Ubuntu Mono"
        x_char = "x"
        y_char = "y"
        z_char = "z"
        a_char = "a"
        b_char = "b"
        c_char = "c"
        e_char = "e"
        pi_char = "π"
        fi_char = "φ"
        sqr_char="√"
        close_icon = "✕"
        maximize_icon = "□"
        minimize_icon = "-"
        realpath='.'
    resized = QtCore.Signal()
    QtWidgets.QApplication.setStyle('Fusion')
    app = QtWidgets.QApplication(argv)
    app.setStyle('Fusion')
    calc = Window()
    calc.resize(900, 500)
    calc.setWindowTitle('SomePythonThings Calc')
    calc.setStyleSheet('''
        * {
            background-color: #333333;
            color:#EEEEEE; 
            font-family: "'''+font+'''", monospace;
            font-weight: bold; 
            font-size:15px;
        }
        #app
        {
            border-radius: 500px;
        }

        QSizeGrip{
            background-color: #333333;
        }
        QScrollBar:vertical {
            background-color: #222222;
            border:none;
        }
        QMenu::item {
            border: 5px solid #333333;
            border-right: 10px solid #333333;
        }
        QMenu::item:selected {
            background-color: #000000;
            border:5px solid  #000000;
        }
        QMenuBar::item{
            background-color: #333333;
            border:5px solid  #333333;

        }
        QMenuBar::item:selected{
            background-color: #000000;
            border:5px solid  #000000;

        }
        QPushButton {
            border: none;
            height: 30px;
            width: 100px;
            border-radius: 3px;
            background-color:#222222;
        }
        QPushButton:hover {
            border: none;
            height: 30px;
            width: 100px;
            background-color:#111111;
        }

        QScrollBar
        {
            background-color: #222222;
        }

        QScrollBar:vertical
        {
            background-color: #222222;
        }

        QScrollBar::handle:vertical 
        {
            margin-top: px;
            margin-bottom: 0px;
            border: none;
            min-height: 30px;
            background-color: #333333;
        }

        QScrollBar::add-line:vertical 
        {
            border: none;
            background-color: #333333;
            height: 0px;
        }

        QScrollBar::sub-line:vertical 
        {
            border: none;
            background-color: #333333;
            height: 0px;
        }

        #top-left{
            border-top-left-radius: 3px;
            }
        #top-right{
            border-top-right-radius: 3px;
            }
        #all-right{
            border-radius: 3px;
            }
        #bottom-left{
            border-bottom-left-radius: 3px;
            }
        #bottom-right{
            border-bottom-right-radius: 3px;
            }

    ''')
    try:
        calc.setWindowIcon(QtGui.QIcon(realpath+"/calc-icon.png"))
    except: pass
    buttons = {}
    for number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        buttons[number] = QtWidgets.QPushButton(calc, objectName="button") # number button
        buttons[number].setText(str(number))
        buttons[number].move(1, 1)
        buttons[number].clicked.connect(partial(print_number, str(number)))
    buttons['='] = QtWidgets.QPushButton(calc) # "=" button
    buttons['='].setText('=')
    buttons['='].setObjectName('top-left')
    buttons['='].move(1, 1)
    buttons['='].clicked.connect(calculate)
    for operation in ['*', '/', '+', '-', '^(', '√']:
        buttons[operation] = QtWidgets.QPushButton(calc) # operation button
        buttons[operation].setText(str(operation))
        buttons[operation].move(1, 1)
        buttons[operation].clicked.connect(partial(print_operation, str(operation)))
    for bracket in ['(', ')']:
        buttons[bracket] = QtWidgets.QPushButton(calc) # bracket button
        buttons[bracket].setText(str(bracket))
        buttons[bracket].move(1, 1)
        buttons[bracket].clicked.connect(partial(print_bracket, str(bracket)))
    buttons['.'] = QtWidgets.QPushButton(calc) # Dot button
    buttons['.'].setText('.')
    buttons['.'].move(1, 1)
    buttons['.'].setObjectName('top-right')
    buttons['.'].clicked.connect(dot)
    buttons['Del'] = QtWidgets.QPushButton(calc) # Backspace button (clear one charartcer)
    buttons['Del'].setText('Delete')
    buttons['Del'].setObjectName('bottom-left')
    buttons['Del'].move(1, 1)
    buttons['Del'].clicked.connect(delete)
    buttons['CO'] = QtWidgets.QPushButton(calc) # Clear Operation (CO)
    buttons['CO'].setText('Clear')
    buttons['CO'].move(1, 1)
    buttons['CO'].clicked.connect(clear)
    buttons['CA'] = QtWidgets.QPushButton(calc) # Clear All (CA)
    buttons['CA'].setText('Clear All')
    buttons['CA'].move(1, 1)
    buttons['CA'].clicked.connect(clear_all)
    buttons['POPUP'] = QtWidgets.QPushButton(calc) # Clear All (CA)
    buttons['POPUP'].setText("<  ")
    buttons['POPUP'].move(1, 1)
    buttons['POPUP'].clicked.connect(show_popup)
    textbox =  QtWidgets.QPlainTextEdit(calc)
    textbox.move(0, 29)
    textbox.setWindowOpacity(0.5)
    textbox.setReadOnly(True)
    textbox.setPlainText('')
    buttons['PI'] = QtWidgets.QPushButton(calc)
    buttons['PI'].setText(pi_char)
    buttons['PI'].setObjectName('top-left')
    buttons['PI'].move(1, 1)
    buttons['PI'].clicked.connect(partial(print_symbol_and_close, pi_char))
    buttons['E'] = QtWidgets.QPushButton(calc)
    buttons['E'].setText(e_char)
    buttons['E'].move(1, 1)
    buttons['E'].clicked.connect(partial(print_symbol_and_close, e_char))
    buttons['ANS'] = QtWidgets.QPushButton(calc)
    buttons['ANS'].setText("Ans")
    buttons['ANS'].move(1, 1)
    buttons['ANS'].clicked.connect(ANSWER)
    buttons['GOLDEN-RATIO'] = QtWidgets.QPushButton(calc)
    buttons['GOLDEN-RATIO'].setText(fi_char)
    buttons['GOLDEN-RATIO'].move(1, 1)
    buttons['GOLDEN-RATIO'].clicked.connect(partial(print_symbol_and_close, fi_char))
    buttons['PASTE'] = QtWidgets.QPushButton(calc)
    buttons['PASTE'].setText("Paste Custom\nOperation")
    buttons['PASTE'].setObjectName("bottom-left")
    buttons['PASTE'].move(1, 1)
    buttons['PASTE'].clicked.connect(pasteOperation)
    buttons['EDIT'] = QtWidgets.QPushButton(calc)
    buttons['EDIT'].setText("Edit\nOperation")
    buttons['EDIT'].move(1, 1)
    buttons['EDIT'].clicked.connect(editOperation)
    buttons['X'] = QtWidgets.QPushButton(calc)
    buttons['X'].setText(x_char)
    buttons['X'].move(1, 1)
    buttons['X'].clicked.connect(partial(print_symbol_and_close, x_char))
    buttons['Y'] = QtWidgets.QPushButton(calc)
    buttons['Y'].setText(y_char)
    buttons['Y'].move(1, 1)
    buttons['Y'].clicked.connect(partial(print_symbol_and_close, y_char))
    buttons['Z'] = QtWidgets.QPushButton(calc)
    buttons['Z'].setText(z_char)
    buttons['Z'].move(1, 1)
    buttons['Z'].clicked.connect(partial(print_symbol_and_close, z_char))
    buttons['A'] = QtWidgets.QPushButton(calc)
    buttons['A'].setText(a_char)
    buttons['A'].move(1, 1)
    buttons['A'].clicked.connect(partial(print_symbol_and_close, a_char))
    buttons['B'] = QtWidgets.QPushButton(calc)
    buttons['B'].setText(b_char)
    buttons['B'].move(1, 1)
    buttons['B'].clicked.connect(partial(print_symbol_and_close, b_char))
    buttons['C'] = QtWidgets.QPushButton(calc)
    buttons['C'].setText(c_char)
    buttons['C'].move(1, 1)
    buttons['C'].clicked.connect(partial(print_symbol_and_close, c_char))
    calc.keyRelease.connect(on_key)
    menuBar = calc.menuBar()
    fileMenu = menuBar.addMenu("File")
    settingsMenu = menuBar.addMenu("Settings")
    helpMenu = menuBar.addMenu("Help")
    saveAction = QtWidgets.QAction(" Save History", calc)
    saveAction.setShortcut("")
    quitAction = QtWidgets.QAction(" Quit", calc)
    quitAction.setShortcut("")
    topAction = QtWidgets.QAction(" Enable Stay-On-Top mode", calc)
    topAction.setCheckable(True)
    openHelpAction = QtWidgets.QAction(" Online manual", calc)
    openHelpAction.setShortcut("")
    aboutAction = QtWidgets.QAction(" About SomePythonThings Calc", calc)
    aboutAction.setShortcut("")
    updatesAction = QtWidgets.QAction(" Check for updates", calc)
    updatesAction.setShortcut("")
    reinstallAction = QtWidgets.QAction("   Re-install SomePythonThings Calc", calc)
    reinstallAction.setShortcut("")
    updatesAction.triggered.connect(checkDirectUpdates)
    quitAction.triggered.connect(quitCalc)
    reinstallAction.triggered.connect(reinstallCalc)
    saveAction.triggered.connect(saveHistory)
    aboutAction.triggered.connect(partial(throw_info, "About SomePythonThings Calc", "SomePythonThings Calc\nVersion "+str(actualVersion)+"\n\nThe SomePythonThings Project\n\n © 2020 Martí Climent, SomePythonThings\nhttps://www.somepythonthings.tk\n\n\nThe iconset has a CC Non-Commercial Atribution 4.0 License"))
    openHelpAction.triggered.connect(openHelp)
    topAction.triggered.connect(showOnTop)
    fileMenu.addAction(saveAction)
    fileMenu.addAction(quitAction)
    helpMenu.addAction(openHelpAction)
    helpMenu.addAction(updatesAction)
    helpMenu.addAction(aboutAction)
    settingsMenu.addAction(topAction)
    settingsMenu.addAction(reinstallAction)
    sizeMenu = settingsMenu.addMenu("   Resize")
    minResize = QtWidgets.QAction(" Mini", calc)
    smallResize = QtWidgets.QAction(" Small", calc)
    mediumResize = QtWidgets.QAction(" Medium     ", calc)
    wideResize = QtWidgets.QAction(" Wide", calc)
    bigResize = QtWidgets.QAction(" Big", calc)
    giantResize = QtWidgets.QAction(" Huge", calc)
    minResize.triggered.connect(partial(resizeWidgets, True, 250, 210))
    smallResize.triggered.connect(partial(resizeWidgets, True, 500, 400))
    mediumResize.triggered.connect(partial(resizeWidgets, True, 500, 900))
    wideResize.triggered.connect(partial(resizeWidgets, True, 500, 1100))
    bigResize.triggered.connect(partial(resizeWidgets, True, 750, 1200))
    giantResize.triggered.connect(partial(resizeWidgets, True, 900, 1500))
    sizeMenu.addAction(minResize)
    sizeMenu.addAction(smallResize)
    sizeMenu.addAction(mediumResize)
    sizeMenu.addAction(wideResize)
    sizeMenu.addAction(bigResize)
    sizeMenu.addAction(giantResize)
    if(_platform=='darwin'):
        buttons['exit'] = QtWidgets.QPushButton(calc)
        buttons['exit'].setObjectName("all-right")
        buttons['exit'].setText(close_icon)
        buttons['exit'].move(1, 1)
        buttons['exit'].clicked.connect(quitCalc)
        buttons['minimize'] = QtWidgets.QPushButton(calc)
        buttons['minimize'].setText(minimize_icon)
        buttons['minimize'].move(1, 1)
        buttons['minimize'].clicked.connect(minimizeCalc)
        buttons['maximize'] = QtWidgets.QPushButton(calc)
        buttons['maximize'].setText(maximize_icon)
        buttons['maximize'].move(1, 1)
        buttons['maximize'].clicked.connect(partial(maximizeCalc, 'center'))
        dragBar = QtWidgets.QLabel(calc)
        dragBar.move(1, 1)
        dragBar.hide()
        title = QtWidgets.QLabel(calc)
        title.setText("SomePythonThings Calc")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.move(2, 2)
        grips = {}
        grips['bottom-right'] = QtWidgets.QSizeGrip(calc)
        grips['bottom-right'].setGeometry(int(calc.width()/2)+1, int(calc.height()-2), int(calc.width()/2), 2)
        grips['right-bottom'] = QtWidgets.QSizeGrip(calc)
        grips['right-bottom'].setGeometry(int(calc.width())-2, int(calc.height()/2)+1, 2, int(calc.height()/2))
        grips['bottom-left'] = QtWidgets.QSizeGrip(calc)
        grips['bottom-left'].setGeometry(0, int(calc.height()-2), int(calc.width()/2), 2)
        grips['left-bottom'] = QtWidgets.QSizeGrip(calc)
        grips['left-bottom'].setGeometry(0, int(calc.height()/2)+1, 2, int(calc.height()/2))
        grips['top-right'] = QtWidgets.QSizeGrip(calc)
        grips['top-right'].setGeometry(int(calc.width()/2)+1, 0, int(calc.width()/2), 2)
        grips['right-top'] = QtWidgets.QSizeGrip(calc)
        grips['right-top'].setGeometry(int(calc.width())-2, 0, 2, int(calc.height()/2))
        grips['top-left'] = QtWidgets.QSizeGrip(calc)
        grips['top-left'].setGeometry(0, 0, int(calc.width()/2), 2)
        grips['left-top'] = QtWidgets.QSizeGrip(calc)
        grips['left-top'].setGeometry(0, 0, 2, int(calc.height()/2))
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        calc.setWindowFlags(flags)
    for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(', '√']: #Grey (#333333)
        buttons[button].setStyleSheet("""
            QPushButton
            {
                border: none;
                background-color: #333333;
                color: #DDDDDD;
                width: 25%;
                border-radius: 0px;
            }
            

            
            #top-left{
                border-top-left-radius: 3px;
                }
            #top-right{
                border-top-right-radius: 3px;
                }
            #bottom-left{
                border-bottom-left-radius: 3px;
                }
            #bottom-right{
                border-bottom-right-radius: 3px;
                }
            QPushButton::hover
            {
                background-color: #222222;
            }
            """)
    resizeWidgets()
    calc.setMinimumSize(210, 250)
    print_number(3)
    print_symbol(x_char)
    clear_all()
    calc.show()
    t = Thread(target=checkUpdates)
    t.daemon = True
    t.start()
    app.exec_()
    log("[  EXIT  ] Reached end of the script")
    if(debugging):
        input("Press any key to continue...")
    sys.exit()

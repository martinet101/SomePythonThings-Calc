#Modules
import os

os.environ["QT_MAC_WANTS_LAYER"] = "1"

import sys
import time
import math
import wget
import json
import tempfile
import platform
import traceback
import subprocess
import darkdetect
import webbrowser
from ast import literal_eval
from sys import platform as _platform
from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
from threading import Thread
from urllib.request import urlopen
from qt_thread_updater import get_updater

#Globals definition
debugging = False
actualVersion = 3.8

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
fontsize = 14
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
angleUnit = 'degree'


needResize=[False, 900, 500]

tempDir = tempfile.TemporaryDirectory()



defaultSettings = {
    "settings_version": actualVersion,
    "angleUnit": 'degree',
    "mode":'auto',
}

settings = defaultSettings.copy() # Default settings loaded, those which change will be overwritten


lightStyleSheet ="""
     * {{
        color: #222222;
        background-color: #EEEEEE;
        font-size: 12px;
    }}
    
    QMenuBar
    {{
        background-color: #EEEEEE;
        color: #222222;
    }}
    QMenu 
    {{
        background-color: #EEEEEE;
        border-radius: 10px;
    }}
    QMenu::item 
    {{
        border: 3px solid #EEEEEE;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #222222;
        padding-left: 8px;
    }}
    QMenu::item:selected 
    {{
        border: 3px solid #3dbaa8;
        background-color: #3dbaa8;
    }}
    QMenuBar::item 
    {{
        background-color: #EEEEEE;
        border: 3px solid  #EEEEEE;
        padding-right: 5px;
        padding-left: 5px;
    }}
    QMenuBar::item:default 
    {{
        background-color: #3dbaa8;
        border: 3px solid  #3dbaa8;
    }}
    QMenuBar::item:selected 
    {{
        background-color: #3dbaa8;
        border: 3px solid  #3dbaa8;
    }}
    QSizeGrip
    {{
        background-color: #EEEEEE;
    }}
    QScrollBar:vertical
    {{
        background-color: #EEEEEE;
        border:none;
    }}
    QPushButton
    {{
        border: none;
        height: 30px;
        width: 100px;
        border-radius: 3px;
        background-color: #3dbaa8;
    }}
    QPushButton:hover
    {{
        border: none;
        height: 30px;
        width: 100px;
        background-color: #3dbaa8;
        border-radius: 3px;
    }}
    QScrollBar
    {{
        background-color: #FFFFFF;
    }}
    QScrollBar:vertical
    {{
        background-color: #FFFFFF;
    }}
    QScrollBar::handle:vertical 
    {{
        margin-top: 0px;
        margin-bottom: 0px;
        border: none;
        min-height: 30px;
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        background-color: #EEEEEE;
    }}
    QScrollBar::add-line:vertical 
    {{
        border: none;
        background-color: #EEEEEE;
        height: 0px;
    }}
    QScrollBar::sub-line:vertical 
    {{
        border: none;
        background-color: #EEEEEE;
        height: 0px;
    }}
    QPlainTextEdit
    {{
        selection-background-color: #3dbaa8;
        selection-color: white;
        border:none; 
        background-color: #FFFFFF; 
        font-size:{0}px;
        font-weight: light;
        color: #222222; 
        font-family: "{1}";
        padding-bottom: 5px;
    }}
    QLineEdit{{
        border: none;
        background-color: #FFFFFF;
        border-radius: 3px;
        padding: 5px;
        margin: 5px;
    }}
    #regularButton {{
        border: none;
        background-color: #EEEEEE;
        color: #222222;
        font-weight: light;
        font-size:{0}px; 
        font-family: "{1}", monospace;
        border-radius: 0px;
    }}
    
    #regularButton::hover
    {{
        background-color: #FFFFFF;
        border-radius: 3px;
    }}
    #equalNormal {{
        border: none; 
        background-color: #3dbaa8; 
        font-size:{0}px; 
        font-weight: light;
        color: #222222; 
        font-family: "{1}";
        border-radius: 0px; 
    }}
    #equalNormal::hover
    {{
        background-color: #FFFFFF;
        border-radius: 3px;
        color: #3dbaa8; 
    }}
    #equalLight {{
        border: none; 
        background-color: #FFFFFF; 
        font-size:{0}px; 
        font-weight: light;
        color: #3dbaa8; 
        font-family: "{1}";
        border-radius: 0px; 
    }}
    #equalLight::hover
    {{
        background-color: #FFFFFF;
        border-radius: 3px;
    }}
    #operationButton{{
        border: none; 
        background-color: #7f8fa1; 
        font-size:{0}px;
        color: black;
        font-family: "{1}";
        font-weight: light;
        border-radius: 0px;
    }}
    #operationButton::hover
    {{
        background-color: #FFFFFF;
        color: black;
        border-radius: 3px;
    }}
    #darkButton{{
        border: none; 
        background-color: #FFFFFF; 
        font-size:{0}px; 
        font-weight: light;
        color: #222222; 
        font-family: "{1}";
        border-radius: 0px;
    }}
    #darkButton::hover
    {{
        background-color: #FFFFFF;
        border-radius: 3px;
    }}
    #popupButton{{
        font-size:{0}px; 
        font-family: "{1}";
        font-weight: light;
        color: #FFFFFF;
        background-color: #3dbaa8; 
        border-radius: 3px;
    }}
    #popupButton::hover{{
        background-color: #FFFFFF;
        color: #3dbaa8; 
    }}
    QComboBox{{
        selection-background-color: #3dbaa8;
        margin:0px;
        border: 0px;
        background-color: #FFFFFF;
        border-radius: 3px;
        padding-left: 7px;
    }}
    QMenuBar::item:default {{
        background-color: #3dbaa8;
    }}

"""


darkStyleSheet = """
    * {{
        color: #dddddd;
        background-color: #333333;
        font-size: 12px;
    }}
    
    QMenuBar
    {{
        background-color: #333333;
        color: #EEEEEE;;
    }}
    QMenu 
    {{
        background-color: #333333;
        border-radius: 10px;
    }}
    QMenu::item 
    {{
        border: 3px solid #333333;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #EEEEEE;;
        padding-left: 8px;
    }}
    QMenu::item:selected 
    {{
        border: 3px solid #33998a;
        background-color: #33998a;
    }}
    QMenuBar::item 
    {{
        background-color: #333333;
        border: 3px solid  #333333;
        padding-right: 5px;
        padding-left: 5px;
    }}
    QMenuBar::item:default 
    {{
        background-color: #33998a;
        border: 3px solid  #33998a;
    }}
    QMenuBar::item:selected 
    {{
        background-color: #33998a;
        border: 3px solid  #33998a;
    }}
    QSizeGrip
    {{
        background-color: #333333;
    }}
    QScrollBar:vertical
    {{
        background-color: #222222;
        border:none;
    }}
    QPushButton
    {{
        border: none;
        height: 30px;
        width: 100px;
        border-radius: 3px;
        background-color: #33998a;
    }}
    QPushButton:hover
    {{
        border: none;
        height: 30px;
        width: 100px;
        background-color: #33998a;
        border-radius: 3px;
    }}
    QScrollBar
    {{
        background-color: #222222;
    }}
    QScrollBar:vertical
    {{
        background-color: #222222;
    }}
    QScrollBar::handle:vertical 
    {{
        margin-top: 0px;
        margin-bottom: 0px;
        border: none;
        min-height: 30px;
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        background-color: #333333;
    }}
    QScrollBar::add-line:vertical 
    {{
        border: none;
        background-color: #333333;
        height: 0px;
    }}
    QScrollBar::sub-line:vertical 
    {{
        border: none;
        background-color: #333333;
        height: 0px;
    }}
    QPlainTextEdit
    {{
        selection-background-color: #33998a;
        selection-color: white;
        border:none; 
        background-color: #222222; 
        font-size:{0}px; 
        color: #DDDDDD; 
        font-family: "{1}";
        padding-bottom: 5px;
    }}
    QLineEdit{{
        border: none;
        background-color: #222222;
        border-radius: 3px;
        padding: 5px;
        margin: 5px;
    }}
    #regularButton {{
        border: none;
        background-color: #333333;
        color: #DDDDDD;
        font-size:{0}px; 
        font-family: "{1}", monospace;
        border-radius: 0px;
    }}
    
    #regularButton::hover
    {{
        background-color: #222222;
        border-radius: 3px;
    }}
    #equalNormal {{
        border: none; 
        background-color: #33998a; 
        font-size:{0}px; 
        color: #DDDDDD; 
        font-family: "{1}";
        border-radius: 0px; 
    }}
    #equalNormal::hover
    {{
        background-color: #222222;
        border-radius: 3px;
        color: #33998a; 
    }}
    #equalLight {{
        border: none; 
        background-color: #222222; 
        font-size:{0}px; 
        color: #33998a; 
        font-family: "{1}";
        border-radius: 0px; 
    }}
    #equalLight::hover
    {{
        background-color: #222222;
        border-radius: 3px;
    }}
    #operationButton{{
        border: none; 
        background-color: #49525C; 
        font-size:{0}px; 
        font-family: "{1}";
        color: #DDDDDD; 
        border-radius: 0px;
    }}
    #operationButton::hover
    {{
        background-color: #222222;
        border-radius: 3px;
    }}
    #darkButton{{
        border: none; 
        background-color: #222222; 
        font-size:{0}px; 
        color: #DDDDDD; 
        font-family: "{1}";
        border-radius: 0px;
    }}
    #darkButton::hover
    {{
        background-color: #111111;
        border-radius: 3px;
    }}
    #popupButton{{
        font-size:{0}px; 
        font-family: "{1}";
        background-color: #33998a; 
        border-radius: 3px;
    }}
    #popupButton::hover{{
        background-color: #222222;
        color: #33998a; 
    }}
    QComboBox{{
        selection-background-color: #33998a;
        margin:0px;
        border: 0px;
        background-color: #222222;
        border-radius: 3px;
        padding-left: 7px;
    }}
    QMenuBar::item:default {{
        background-color: #33998a;
    }}

"""




def getTheme():
    if(platform.system()=="Windows"):
        import winreg
        if(int(platform.release())>=10):
            access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            access_key = winreg.OpenKey(access_registry, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
            readKeys = {}
            for n in range(20):
                try:
                    x = winreg.EnumValue(access_key, n)
                    readKeys[x[0]]=x[1]
                except:
                    pass
            try:
                return readKeys["AppsUseLightTheme"]
            except:
                return 1
        else:
            return 1
    elif(platform.system()=="Darwin"):
        return int(darkdetect.isLight())
    else:
        return 1

def getWindowStyleSheet():
    global settings, realpath
    mode = 'auto'
    try:
        if(str(settings["mode"]).lower() in 'darklightauto'):
            mode = str(settings['mode'])
        else:
            log("[  WARN  ] Mode is invalid")
    except KeyError:
        log("[  WARN  ] Mode key does not exist on settings")
    if(mode=='auto' and _platform == 'linux'):
        log('[        ] Auto mode selected and os is not macOS. Swithing to light...')
        mode='dark'
    if(mode=='auto'):
        if(getTheme()==0):
            log('[        ] Auto mode selected. Swithing to dark...')
            mode='dark'
        else:
            log('[        ] Auto mode selected. Swithing to light...')
            mode='light'
    log('[   OK   ] mode set to '+str(mode))
    if(mode=='light'):
        return lightStyleSheet.format(fontsize, font)
    else:
        return darkStyleSheet.format(fontsize, font)


def checkModeThread():
    lastMode = getTheme()
    while True:
        if(lastMode!=getTheme()):
            get_updater().call_in_main(calc.setStyleSheet, getWindowStyleSheet())
            lastMode = getTheme()
        time.sleep(0.1)






#Essential functions
def log(s, file=True):
    global debugging
    if(debugging or "WARN" in str(s) or "FAILED" in str(s)):
        print((time.strftime('[%H:%M:%S] ', time.gmtime(time.time())))+str(s))
    if(file):
        try:
            f = open(tempDir.name.replace('\\', '/')+'/log.txt', 'a+')
            f.write("\n"+time.strftime('[%H:%M:%S]', time.gmtime(time.time())), str(s))
            f.close()
        except:
            pass




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
        throw_info("SomePythonThings Calc Updater", "The update has been downloaded and is going to be installed.\nYou may be prompted for permissions, click YES.\nClick OK to start installation")
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
        throw_info("SomePythonThings Updater", "The update is being downloaded. Please wait.")
        get_updater().call_in_main(textbox.setPlainText, "The update is being downloaded. Please wait.")
        time.sleep(0.07)
        get_updater().call_in_main(textbox.setPlainText, "The update is being downloaded. Please wait.")
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
        get_updater().call_in_main(throw_info, "SomePythonThings Update", "The update is being downloaded. Please wait.")
        t = Thread(target=download_win, args=(url,))
        t.start()
        #throw_info("SomePythonThings Calc Updater","The update is being downloaded and the installer is going to be launched at the end. Please, don't quit the application until the process finishes.")
    elif _platform == 'darwin':
        log("[   OK   ] platform is macOS, starting auto-update...")
        t = Thread(target=download_macOS, args=(links,))
        t.start()
    else:  # If os is unknown
        webbrowser.open_new('http://www.somepythonthings.tk/programs/somepythonthings-calc/')

def download_macOS(links):
    get_updater().call_in_main(throw_info, "SomePythonThings Updater", "The new version is going to be downloaded and installed automatically. \nThe installation time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nPlease DO NOT kill the program until the update is done, because it may corrupt the executable files.\nClick OK to start downloading.")
    get_updater().call_in_main(textbox.setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
    os.system('cd; rm somepythonthings-calc_update.dmg')
    try:  
        wget.download(links['macos'], out='{0}/somepythonthings-calc_update.dmg'.format(os.path.expanduser('~')))
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


def saveSettings(silent=True, angleUnit='degree', mode='auto'):
    global defaultSettings
    try:
        os.chdir(os.path.expanduser('~'))
        try:
            os.chdir('.SomePythonThings')
        except FileNotFoundError:
            log("[  WARN  ] Can't acces .SomePythonThings folder, creating .SomePythonThings...")
            os.mkdir(".SomePythonThings")
            os.chdir('.SomePythonThings')
        try:
            os.chdir('Calc')
        except FileNotFoundError:
            log("[  WARN  ] Can't acces Calc folder, creating Calc...")
            os.mkdir("Calc")
            os.chdir('Calc')
        try:
            settingsFile = open('settings.conf', 'w')
            settingsFile.write(str({
                "settings_version": actualVersion,
                "angleUnit": angleUnit,
                "mode":mode,
                }))
            settingsFile.close()
            log("[   OK   ] Settings saved successfully")
            return True
        except Exception as e:
            throw_error('SomePythonThings Calc', "An error occurred while loading the settings file. \n\nError details:\n"+str(e))
            log('[        ] Creating new settings.conf')
            saveSettings()
            if(debugging):
                raise e
            return False
    except Exception as e:
        if(not(silent)):
            throw_info("SomePythonThings Calc", "Unable to save settings. \n\nError details:\n"+str(e))
        log("[ FAILED ] Unable to save settings")
        if(debugging):
            raise e
        return False


def openSettings():
    global defaultSettings
    os.chdir(os.path.expanduser('~'))
    try:
        os.chdir('.SomePythonThings')
        try:
            os.chdir('Calc')
            try:
                settingsFile = open('settings.conf', 'r')
                settings = json.loads("\""+str(settingsFile.read().replace('\n', '').replace('\n\r', ''))+"\"")
                settingsFile.close()
                log('[        ] Loaded settings are: '+str(settings))
                return literal_eval(settings)
            except Exception as e:
                log('[        ] Creating new settings.conf')
                saveSettings()
                if(debugging):
                    raise e
                return defaultSettings
        except FileNotFoundError:
            log("[  WARN  ] Can't acces Calc folder, creating settings...")
            saveSettings()
            return defaultSettings
    except FileNotFoundError:
        log("[  WARN  ] Can't acces .SomePythonThings folder, creating settings...")
        saveSettings()
        return defaultSettings

def openSettingsWindow():
    global calc, settings
    settingsWindow = Window(calc)
    settingsWindow.setMinimumSize(300, 170)
    settingsWindow.setMaximumSize(300, 170)
    settingsWindow.setWindowTitle("SomePythonThings Calc Settings")
    settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
    settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    if(_platform == 'darwin'):
        settingsWindow.setAutoFillBackground(True)
        settingsWindow.setWindowModality(QtCore.Qt.WindowModal)
        settingsWindow.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        settingsWindow.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    modeSelector = QtWidgets.QComboBox(settingsWindow)
    modeSelector.insertItem(0, 'Light')
    modeSelector.insertItem(1, 'Dark')
    if(_platform!='linux'):
        modeSelector.insertItem(2, 'Auto')
    modeSelector.resize(130, 30)
    modeSelector.move(150, 20)
    modeSelectorLabel = QtWidgets.QLabel(settingsWindow)
    modeSelectorLabel.setText("Application theme: ")
    modeSelectorLabel.move(20, 20)
    modeSelectorLabel.setObjectName('settingsBackground')
    modeSelectorLabel.resize(130, 30)

    traySelector = QtWidgets.QComboBox(settingsWindow)
    traySelector.insertItem(0, 'Degrees (circumference = 360°)')
    traySelector.insertItem(1, f'Radians (circumference = 2{pi_char}rad)')
    traySelector.resize(130, 30)
    traySelector.move(150, 60)
    traySelectorLabel = QtWidgets.QLabel(settingsWindow)
    traySelectorLabel.setText("Default angle units: ")
    traySelectorLabel.move(20, 60)
    traySelectorLabel.setObjectName('settingsBackground')
    traySelectorLabel.resize(130, 30)

    saveButton = QtWidgets.QPushButton(settingsWindow)
    saveButton.setText("Save settings and close")
    saveButton.resize(260, 40)
    saveButton.move(20, 110)
    saveButton.setObjectName('squarePurpleButton')
    saveButton.clicked.connect(partial(saveAndCloseSettings, modeSelector, traySelector, settingsWindow))

    try:
        if(settings['mode'].lower() == 'light'):
            modeSelector.setCurrentIndex(0)
        elif(settings['mode'].lower() == 'auto'):
            if(_platform!='linux'):
                modeSelector.setCurrentIndex(2)
            else:
                modeSelector.setCurrentIndex(1)
        elif(settings['mode'].lower() == 'dark'):
            modeSelector.setCurrentIndex(1)
        else:
            log("[  WARN  ] Could not detect mode!")
    except KeyError:
        log("[  WARN  ] Could not detect mode!")

    try:
        if(settings['angleUnit'] == 'degree'): #the "== False" is here to avoid eval of invalid values and crash of the program
            traySelector.setCurrentIndex(0)
        elif(settings['angleUnit'] == 'radian'):
            traySelector.setCurrentIndex(1)
        else:
            log("[  WARN  ] Could not detect default angle unit!")
    except KeyError:
        log("[  WARN  ] Could not detect default angle unit!")
    
    settingsWindow.show()

def saveAndCloseSettings(modeSelector: QtWidgets.QComboBox, traySelector: QtWidgets.QComboBox, settingsWindow):
    global settings, forceClose
    if(traySelector.currentIndex() == 1):
        settings['angleUnit'] = 'radian'
    else:
        settings['angleUnit'] = 'degree'
    if(modeSelector.currentIndex() == 0):
        settings['mode'] = 'light'
    elif(modeSelector.currentIndex() == 1):
        settings['mode'] = 'dark'
    else:
        settings['mode'] = 'auto'
    forceClose = True
    settingsWindow.close()
    saveSettings(silent=True, angleUnit=settings['angleUnit'], mode=settings['mode'])
    calc.setStyleSheet(getWindowStyleSheet())


def changeAngleUnit():
    global settings
    if(settings["angleUnit"] == "degree"):
        log("[   OK   ] Calculator in radians")
        settings["angleUnit"] = "radian"
        angleAction.setText("Radians (rad)")
        saveSettings(silent=True, angleUnit=settings['angleUnit'], mode=settings['mode'])

    else:
        log("[   OK   ] Calculator in degrees")
        settings["angleUnit"] = "degree"
        angleAction.setText("Degrees (deg)")
        saveSettings(silent=True, angleUnit=settings['angleUnit'], mode=settings['mode'])


def throw_info(title, body):
    global a_char, b_char, c_char, z_char, calc
    log("[  INFO  ] "+body)
    msg = QtWidgets.QMessageBox(calc)
    if(os.path.exists(str(realpath)+"/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/ok.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_warning(title, body, warning="Not Specified"):
    global a_char, b_char, c_char, z_char, calc
    log("[  WARN  ] "+body+"\n\tWarning reason: "+warning)
    msg = QtWidgets.QMessageBox(calc)
    if(os.path.exists(str(realpath)+"/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/warn.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_error(title, body, error="Not Specified"):
    global a_char, b_char, c_char, z_char, calc
    log("[ FAILED ] "+body+"\n\tError reason: "+error)
    msg = QtWidgets.QMessageBox(calc)
    if(os.path.exists(str(realpath)+"/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/error.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
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

def sin(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        n = math.radians(n)
    return math.sin(n)

def cos(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        n = math.radians(n)
    return math.cos(n)

def tan(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        n = math.radians(n)
    return math.tan(n)

def arcsin(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        return math.degrees(math.asin(n))
    else:
        return math.asin(n)

def arccos(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        return math.degrees(math.acos(n))
    else:
        return math.acos(n)

def arctan(n):
    log("[   OK   ] Angle unit set to "+settings["angleUnit"])
    if(settings["angleUnit"] == 'degree'):
        return math.degrees(math.atan(n))
    else:
        return math.atan(n)

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
        appendText(f" {s} ")
        scrollBottom()
        currentOperation += f" {s} "
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
            if not o in '√arcsinarccosarctan':
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
            if o in "√arcsinarccosarctan":
                if not(symbolAvailable):
                    o = "* "+o
                o += '('
                bracketsToClose += 1
            appendText(' '+o+' ')
            currentOperation += ' '+o+' '
        operationAvailable = False
        dotAvailable = True
        symbolAvailable = True
        numberAvailable = True
        if(popup):
            show_popup()
        if o == '^(' or o=='√(' or o in " arcsin arccos arctan ":
            bracketsToClose += 1
    scrollBottom()

def print_bracket(b):
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  operationAvailable, bracketsToClose, currentOperation, needClear, canWrite, dotAvailable, numberAvailable, symbolAvailable
    log("[  INFO  ] Starting print_bracket(): canWrite={0}, needClear={1}, operationAvailable={2}, o={3}, bracketsToClose={4}".format(canWrite, needClear, operationAvailable, b, bracketsToClose))
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
        log("[  WARN  ] Brackets Missing! (missing {0} brackets)".format(currentOperation.count('(')-currentOperation.count(')')))
        canWrite=True
        missingBrackets = currentOperation.count('(')-currentOperation.count(')')
        get_updater().call_in_main(print_bracket, ')')
        while(missingBrackets==currentOperation.count('(')-currentOperation.count(')')):
            time.sleep(0.01)
        canWrite=False
    get_updater().call_in_main(calc.setWindowTitle, "SomePythonThings Calc: "+currentOperation)
    log("[   OK   ] No missing brackets")
    currentOperation = currentOperation.split(" ")
    for i in range(len(currentOperation)):
        if(currentOperation[i] != '0'):
            currentOperation[i] = currentOperation[i].lstrip('0')
    currentOperation = ' '.join(currentOperation)
    result = pure_calculate(currentOperation.replace('^', '**').replace('√', 'sqr'))
    if use_x:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}" '.format(x_char, x_prev_value))
    if use_y:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}"'.format(y_char, y_prev_value))
    if use_z:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}" '.format(z_char, z_prev_value))
    if use_a:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}"'.format(a_char, a_prev_value))
    if use_b:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}" '.format(b_char, b_prev_value))
    if use_c:
        get_updater().call_in_main(textbox.appendPlainText, ' {0} value is "{1}"'.format(c_char, c_prev_value))
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
    if use_x or use_y or use_z or use_a or use_b or use_c:
        log("[   OK   ] X, Y, Z, A, B or C detected.")
        try:
            result = int(result)
            get_updater().call_in_main(textbox.appendPlainText, ' result = '+f"{result:,}".replace('e+', ' * 10^'))
        except:
            get_updater().call_in_main(textbox.appendPlainText, ' result = '+str(result).replace('e+', ' * 10^'))
            try:
                log("[  WARN  ] Unable to int() result. Result value is "+result)
            except:
                pass
    else:
        log("[  WARN  ] X, Y, Z, A, B or C NOT detected.")
        try:
            result = int(result)
            get_updater().call_in_main(textbox.appendPlainText, ' = '+f"{result:,}".replace('e+', ' * 10^'))
        except ValueError:
            log("[  WARN  ] Unable to int() result.")
            get_updater().call_in_main(textbox.appendPlainText, ' = '+str(result).replace('e+', ' * 10^'))
        except Exception as e:
            if(debugging):
                raise e
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
    except Exception as e:
        result = "Oh \ud83d\udca9, You did it! The operation is too hard to be calculated!  "
        if(debugging):
            raise e
    return result
def calculate():
    global a_char, b_char, showOnTopEnabled, c_char, z_char, x_prev_value, use_x, use_y, use_z, use_a, use_b, use_c, y_prev_value, z_prev_value, a_prev_value, b_prev_value, c_prev_value, x_char, y_char, e_char, pi_char,  calc, currentOperation, operationAvailable, needClear, previousResult, dotAvailable, bracketsToClose, calcHistory, textbox, result, calc, numberAvailable, symbolAvailable
    if(not needClear):
        disableAll()
        use_x = False
        use_y = False
        use_z = False
        use_a = False
        use_b = False
        use_c = False
        calc.setWindowTitle('SomePythonThings Calc:  '+currentOperation)
        if(pi_char in currentOperation):
            currentOperation = currentOperation.replace(pi_char, "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
        if(fi_char in currentOperation):
            currentOperation = currentOperation.replace(fi_char, "1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374")
        if(e_char in currentOperation):
            currentOperation = currentOperation.replace(e_char, "2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274")
        if("Ans" in currentOperation):
            currentOperation = currentOperation.replace("Ans", previousResult)
        if(f" {x_char} " in currentOperation):
            x = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+x_char+" on the operation.\nEnter value for "+x_char+": ", QtWidgets.QLineEdit.Normal, str(x_prev_value))
            x_prev_value = (x[0].replace(",", "."))
            use_x = True
            currentOperation = currentOperation.replace(x_char, '({0})'.format(x[0].replace(",", ".")))
        if(f" {y_char} " in currentOperation):
            y = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+y_char+" on the operation.\nEnter value for "+y_char+": ", QtWidgets.QLineEdit.Normal, str(y_prev_value))
            y_prev_value = (y[0].replace(",", "."))
            use_y = True
            currentOperation = currentOperation.replace(y_char, '({0})'.format(y[0].replace(",", ".")))
        if(f" {z_char} " in currentOperation):
            z = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+z_char+" on the operation.\nEnter value for "+z_char+": ", QtWidgets.QLineEdit.Normal, str(z_prev_value))
            z_prev_value = (z[0].replace(",", "."))
            use_z = True
            currentOperation = currentOperation.replace(z_char, '({0})'.format(z[0].replace(",", ".")))
        if(f" {a_char} " in currentOperation):
            a = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+a_char+" on the operation.\nEnter value for "+a_char+": ", QtWidgets.QLineEdit.Normal, str(a_prev_value))
            a_prev_value = (a[0].replace(",", "."))
            use_a = True
            currentOperation = currentOperation.replace(f" {a_char} ", ' ({0}) '.format(a[0].replace(",", ".")))
        if(f" {b_char} " in currentOperation):
            b = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+b_char+" on the operation.\nEnter value for "+b_char+": ", QtWidgets.QLineEdit.Normal, str(b_prev_value))
            b_prev_value = (b[0].replace(",", "."))
            use_b = True
            currentOperation = currentOperation.replace(b_char, '({0})'.format(b[0].replace(",", ".")))
        print(currentOperation)
        if(c_char in currentOperation):
            c = QtWidgets.QInputDialog.getText(calc, "SomePythonThings Calc", "It seems like you entered an "+c_char+" on the operation.\nEnter value for "+c_char+": ", QtWidgets.QLineEdit.Normal, str(c_prev_value))
            c_prev_value = (c[0].replace(",", "."))
            use_c = True
            currentOperation = currentOperation.replace(" {0} ".format(c_char), ' ({0}) '.format(c[0].replace(",", ".")))
        if(not(needClear)):
            Thread(target=huge_calculate, daemon=True).start()
        
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

def delete(nocheck=False):
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  textbox, currentOperation
    scrollBottom()
    text = textbox.toPlainText()
    char = text[-1:]
    log(f"[   OK   ] Starting del char {char}")
    text = textbox.toPlainText()
    char = text[-1:]
    if not(nocheck):
        checkChar(char)
    if char == ' ':
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        if not(nocheck):
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
    log(f"[   OK   ] Starting delAfterSpace char {char}")
    checkChar(char)
    text = textbox.toPlainText()
    char = text[-1:]
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
    log(f"[   OK   ] Starting delOnlyIfSpace char {char}")
    checkChar(char)
    text = textbox.toPlainText()
    char = text[-1:]
    if char == ' ':
        textbox.setPlainText(text[:-1])
        currentOperation = currentOperation[:-1]
        delOnlyIfSpace()
    scrollBottom()

def checkChar(c):
    global a_char, b_char, c_char, z_char, x_char, y_char, e_char, pi_char,  dotAvailable, bracketsToClose, operationAvailable, numberAvailable, symbolAvailable
    text = textbox.toPlainText()
    log(f"[   OK   ] Starting delAfterSpace char {c}")
    if(c == "("):
        s = text[-7:-1]
        log("[   OK   ] Special string "+s)
        if(s=="arcsin" or s=="arccos" or s=="arctan"):
            for _ in range(6):
                delete(nocheck=True)
            numberAvailable = True
            operationAvailable = True
        else:
            s = text[-4:-1]
            log("[   OK   ] New special string "+s)
            if(s == "sin" or s == "cos" or s == "tan"):
                for _ in range(3):
                    delete(nocheck=True)
                numberAvailable = True
                operationAvailable = True
            else:
                s = text[-2:-1]
                log("[   OK   ] New special string "+s)
                if(s=="^" or s=="√"):
                    for _ in range(1):
                        delete(nocheck=True)        
                    numberAvailable = True
                    operationAvailable = True
                    
    if c == '.':
        log("[   OK   ] Char is dot")
        dotAvailable = True
    elif c == '(':
        log("[   OK   ] Char is (")
        bracketsToClose = textbox.toPlainText().count('(') - textbox.toPlainText().count(')')
    elif c == ')':
        log("[   OK   ] Char is )")
        bracketsToClose = textbox.toPlainText().count('(') - textbox.toPlainText().count(')')
    elif c in '*/^√+-':
        log("[   OK   ] Char is operation")
        operationAvailable = True
    elif c == pi_char or c == e_char or c == x_char or c == y_char or c == z_char or c == a_char or c == b_char or c == c_char:
        log("[   OK   ] Char is symbol")
        numberAvailable = True
        symbolAvailable = True
    else:
        log(f"[  WARN  ] Unknown char \"{c}\"")

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
    elif key == 94:#Windows "^" key code
        print_operation('^(')
    elif key == 33554431:#macOS "^" key code
        print_operation('^(')
    elif key == 16781906:#ubuntu "^" key code
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
    log('[   OK   ] Key pressed: %i' % key)
    
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
            subprocess.Popen('start /B notepad.exe "'+fname.replace('\\', '/')+'"', shell=True)
        else:
            subprocess.Popen('open "'+fname.replace('\\', '/')+'"', shell=True)
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
        calc.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint))
        topAction.setCheckable(True)
        log("[   OK   ] Re-showing Window...")
        calc.show()
        resizeWidgets()
    else:
        showOnTopEnabled = False
        calc.setWindowFlags(QtCore.Qt.WindowFlags())
        topAction.setCheckable(True)
        log("[   OK   ] Re-showing Window...")
        calc.hide()
        calc.show()
        resizeWidgets()
    showCalc()

def openOnExplorer(file, force=False):
    if    (_platform == 'win32'):
        try:
            os.system('start explorer /select,"{0}"'.format(file.replace("/", "\\")))
        except:
            log("[  WARN  ] Unable to show file {0} on file explorer.".format(file))
    elif (_platform == 'darwin' and force):
        try:
            os.system("open "+file)
        except:
            log("[  WARN  ] Unable to show file {0} on finder.".format(file))
    elif (_platform == 'linux' or _platform == 'linux2'):
        try:
            t = Thread(target=os.system, args=("xdg-open "+file,))
            t.daemon=True
            t.start()
        except:
            log("[  WARN  ] Unable to show file {0} on default file explorer.".format(file))

def openLog():
    log("[        ] Opening log...")
    openOnExplorer(tempDir.name.replace('\\', '/')+'/log.txt', force=True)

def resizeWidgets(resizeWindow=False, winHeight=600, winWidth=900):
    log("[  INFO  ] Starting resizeWidgets()", file=False)
    global a_char, b_char, c_char, z_char, fontsize, x_char, y_char, e_char, pi_char,  buttons, popup, textbox, calc
    if(not(resizeWindow)):
        winHeight = calc.height()
        winWidth = calc.width()
    else:
        calc.resize(winWidth, winHeight)
    log("[   OK   ] Window size is {0}*{1}px".format(winHeight, winWidth), file=False)
    buttons['POPUP'].show()
    if(winWidth<1100):
        fullWinWidth = winWidth
        big_width = int(25/100*winWidth)
        tiny_width = int(big_width/2)+1
        small_width = int(17/100*winWidth)+1
        height = int(14/100*winHeight)+1
        first_row = int(30/100*winHeight)
        second_row= first_row+height
        third_row= second_row+height
        fourth_row= third_row+height
        fifth_row= fourth_row+height
        big_1st_column = int((25*0)/100*winWidth)
        big_2nd_column = big_width
        big_3rd_column = big_width*2
        big_4th_column = big_width*3
        small_1st_column = 0
        small_2nd_column = int((12.5)/100*winWidth)
        small_3rd_column = big_width
        small_4th_column = int((12.5*3)/100*winWidth)
        small_5th_column = big_width*2
        small_6th_column = int((16.6666*4)/100*winWidth)
        small_7th_column = int((16.6666*5)/100*winWidth)
    else:
        fullWinWidth = winWidth
        winWidth = winWidth*0.6
        big_width = int(25/100*winWidth)
        tiny_width = int(big_width/2)+1
        small_width = int(17/100*winWidth)+1
        height = int(14/100*winHeight)+1
        first_row = int(30/100*winHeight)
        second_row= first_row+height
        third_row= second_row+height
        fourth_row= third_row+height
        fifth_row= fourth_row+height
        big_1st_column = int((25*0)/100*winWidth)
        big_2nd_column = big_width
        big_3rd_column = big_width*2
        big_4th_column = big_width*3
        small_1st_column = 0
        small_2nd_column = int((12.5)/100*winWidth)
        small_3rd_column = big_width
        small_4th_column = int((12.5*3)/100*winWidth)
        small_5th_column = big_width*2
        small_6th_column = int((16.6666*4)/100*winWidth)
        small_7th_column = int((16.6666*5)/100*winWidth)
    textbox.resize(fullWinWidth ,int((winHeight/100*30-15)))
    if(int(20/1100*fullWinWidth)<int(20/500*winHeight)):
        fontsize = str(int(20/1100*fullWinWidth))
        log("[   OK   ] Width > Height, font size is {0}".format(fontsize), file=False)
    else:
        fontsize = str(int(20/500*winHeight))
        log("[   OK   ] Width < Height, font size is {0}".format(fontsize), file=False)
    if(int(fontsize)<18):
        log("[   OK   ] Font size under 18, setting 18 value", file=False)
        buttons['CA'].setText('CA')
        buttons['CO'].setText('C')
        buttons['Del'].setText('Del')
        log("[   OK   ] Changing Ca, C and Del text to minified label", file=False)
        fontsize="18"
    else:
        buttons['CA'].setText('Clear All')
        buttons['CO'].setText('Clear')
        buttons['Del'].setText('Delete')
        log("[   OK   ] Changing Ca, C and Del text to full label", file=False)
    if(int(fontsize)>28):
        log("[   OK   ] Font size over 28, setting 28 value", file=False)
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
    buttons['/'].resize(big_width+5, height) #Resize button
    buttons['*'].move(big_4th_column, third_row)
    buttons['*'].resize(big_width+5, height) #Resize button
    buttons['^('].move(small_3rd_column, first_row)
    buttons['^('].resize(tiny_width, height) #Resize button
    buttons['√'].move(small_4th_column, first_row)
    buttons['√'].resize(tiny_width, height) #Resize button
    buttons['+'].move(big_4th_column, fourth_row)
    buttons['+'].resize(big_width+5, height) #Resize button
    buttons['-'].move(big_4th_column, fifth_row)
    buttons['-'].resize(big_width+5, height) #Resize button
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
    if(fullWinWidth<1100):
        if(not popup):
            buttons["="].setObjectName("equalNormal")
            buttons['POPUP'].move(winWidth-26, int(winHeight/2)-25)
            pX = int(winWidth)
            pY = int(winHeight/2)
            pWidth = int(winWidth/100*20)
            pHeight = int(height)
            
            buttons['SIN'].resize(pWidth, pHeight)
            buttons['SIN'].move(pX+pWidth*2, pY)
            buttons['COS'].resize(pWidth, pHeight)
            buttons['COS'].move(pX+pWidth*2, pY+pHeight)
            buttons['TAN'].resize(pWidth, pHeight)
            buttons['TAN'].move(pX+pWidth*2, pY+pHeight*2)
            buttons['ARCSIN'].resize(pWidth, pHeight)
            buttons['ARCSIN'].move(pX+pWidth*2, pY+pHeight*3)
            buttons['ARCCOS'].resize(pWidth, pHeight)
            buttons['ARCCOS'].move(pX+pWidth*2, pY+pHeight*4)
            buttons['ARCTAN'].resize(pWidth, pHeight)
            buttons['ARCTAN'].move(pX+pWidth*2, pY+pHeight*5)
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
            buttons["="].setObjectName("equalLight")
            pX = int(winWidth/100*60)
            pY = int(winHeight/2)
            pWidth = int(winWidth/100*20)
            pHeight = height
            
            buttons['SIN'].resize(pWidth, pHeight)
            buttons['SIN'].move(pX+pWidth, pY-pHeight*3)
            buttons['COS'].resize(pWidth, pHeight)
            buttons['COS'].move(pX+pWidth, pY-pHeight*2)
            buttons['TAN'].resize(pWidth, pHeight)
            buttons['TAN'].move(pX+pWidth, pY-pHeight)
            buttons['ARCSIN'].resize(pWidth, pHeight)
            buttons['ARCSIN'].move(pX+pWidth, pY)
            buttons['ARCCOS'].resize(pWidth, pHeight)
            buttons['ARCCOS'].move(pX+pWidth, pY+pHeight)
            buttons['ARCTAN'].resize(pWidth, pHeight)
            buttons['ARCTAN'].move(pX+pWidth, pY+pHeight*2)
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
        buttons["="].setObjectName("equalNormal")
        pX = int(fullWinWidth*0.6)
        pY = int(winHeight*0.3)
        pWidth = int((fullWinWidth*0.4)/3)+1
        pHeight = int((winHeight*0.7)/6)+1
        buttons['POPUP'].move(pX-pWidth-25, int(winHeight/2)-25)
        buttons["X"].move(pX+pWidth, pY)
        buttons["X"].resize(pWidth, pHeight)
        buttons["Y"].move(pX+pWidth, pY+pHeight)
        buttons["Y"].resize(pWidth, pHeight)
        buttons["Z"].move(pX+pWidth, pY+pHeight*2)
        buttons["Z"].resize(pWidth, pHeight)
        buttons["A"].move(pX+pWidth, pY+pHeight*3)
        buttons["A"].resize(pWidth, pHeight)
        buttons["B"].move(pX+pWidth, pY+pHeight*4)
        buttons["B"].resize(pWidth, pHeight)
        buttons["C"].move(pX+pWidth, pY+pHeight*5)
        buttons["C"].resize(pWidth, pHeight)
        buttons["PI"].move(pX, pY)
        buttons["PI"].resize(pWidth, pHeight)
        buttons["E"].move(pX, pY+pHeight)
        buttons["E"].resize(pWidth, pHeight)
        buttons["GOLDEN-RATIO"].move(pX, pY+pHeight*2)
        buttons["GOLDEN-RATIO"].resize(pWidth, pHeight)
        buttons["ANS"].move(pX, pY+pHeight*3)
        buttons["ANS"].resize(pWidth, pHeight)
        buttons["EDIT"].move(pX, pY+pHeight*4)
        buttons["EDIT"].resize(pWidth, pHeight)
        buttons["PASTE"].move(pX, pY+pHeight*5)
        buttons["PASTE"].resize(pWidth, pHeight)
        buttons['SIN'].resize(pWidth, pHeight)
        buttons['SIN'].move(pX+pWidth*2, pY)
        buttons['COS'].resize(pWidth, pHeight)
        buttons['COS'].move(pX+pWidth*2, pY+pHeight)
        buttons['TAN'].resize(pWidth, pHeight)
        buttons['TAN'].move(pX+pWidth*2, pY+pHeight*2)
        buttons['ARCSIN'].resize(pWidth, pHeight)
        buttons['ARCSIN'].move(pX+pWidth*2, pY+pHeight*3)
        buttons['ARCCOS'].resize(pWidth, pHeight)
        buttons['ARCCOS'].move(pX+pWidth*2, pY+pHeight*4)
        buttons['ARCTAN'].resize(pWidth, pHeight)
        buttons['ARCTAN'].move(pX+pWidth*2, pY+pHeight*5)
        buttons['POPUP'].hide()
    
    if(fullWinWidth<300 or winHeight<300 or fullWinWidth >= 1100):
        buttons["POPUP"].hide()
    else:
        buttons["POPUP"].show()
    calc.setStyleSheet(getWindowStyleSheet())

def showCalc():
    calc.show()
    calc.raise_()
    calc.activateWindow()

class MainApplication(QtWidgets.QApplication):
    def __init__(self, parent):
        super(MainApplication, self).__init__(parent)
        self.installEventFilter(self)
        self._prevAppState = QtCore.Qt.ApplicationActive
    
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if (watched == self and event.type() == QtCore.QEvent.ApplicationStateChange):
            ev = QtGui.QGuiApplication.applicationState()
            if (self._prevAppState == QtCore.Qt.ApplicationActive and ev == QtCore.Qt.ApplicationActive):
                if(_platform=="darwin"):
                    log("[   OK   ] Dock icon clicked, showing...")
                    showCalc()
            self._prevAppState = ev

        
        return super().eventFilter(watched, event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
    try:
        if(len(sys.argv)>1):
            if('debug' in sys.argv[1]):
                debugging=True
        log("[        ] Welcome to SomePythonThings Calc {0} log. debugging is set to {1}".format(actualVersion, debugging))
            
        
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        

        os.chdir(os.path.expanduser("~"))

        try:
            readSettings = openSettings()
            i = 0
            for key in readSettings.keys():
                settings[key] = readSettings[key]
                i +=1
            log("[   OK   ] Settings loaded (settings={0})".format(str(settings)))
        except Exception as e:
            log("[ FAILED ] Unable to read settings! ({0})".format(str(e)))
            if(debugging):
                raise e
        
        
        
        if _platform == "linux" or _platform == "linux2":
            log("[   OK   ] Platform is linux")
            os.chdir("/bin/")
            font = "Ubuntu Mono"
            mathFont = ""
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
            mathFont = ""
            font = "Menlo"
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
            realpath = "/Applications/SomePythonThings Calc.app/Contents/Resources"
        elif _platform == "win32":
            log("[   OK   ] Platform is windows")
            if int(platform.release()) >= 10: #Font check: os is windows 10
                font = "Cascadia Mono"#"Cascadia Mono"
                log("[   OK   ] OS detected is win32 release 10 ")
            else:# os is windows 7/8
                font="Consolas"#"Consolas"
                log("[   OK   ] OS detected is win32 release 8 or less ")
            if(os.path.exists("\\Program Files\\SomePythonThingsCalc\\")):
                realpath = "/Program Files/SomePythonThingsCalc/"
                log("[   OK   ] Directory set to /Program Files/SomePythonThingsCalc/")
            else:
                realpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
                log("[  WARN  ] Directory /Program Files/SomePythonThingsCalc/ not found, getting working directory...")
            mathFont = "Cambria Math"
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
            font = ""
            mathFont = ""
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
        app = MainApplication(sys.argv)
        QtWidgets.QApplication.setStyle('Fusion')
        calc = Window()
        calc.resize(900, 500)
        calc.setWindowTitle('SomePythonThings Calc')
        try:
            calc.setWindowIcon(QtGui.QIcon(realpath+"/calc-icon.png"))
        except: pass
        buttons = {}
        textbox =  QtWidgets.QPlainTextEdit(calc)
        textbox.move(0, 20)
        textbox.setWindowOpacity(0.5)
        textbox.setReadOnly(True)
        textbox.setPlainText('')
        for number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            buttons[number] = QtWidgets.QPushButton(calc) # number button
            buttons[number].setText(str(number))
            buttons[number].clicked.connect(partial(print_number, str(number)))
        buttons['='] = QtWidgets.QPushButton(calc) # "=" button
        buttons['='].setText('=')
        buttons['='].clicked.connect(calculate)
        for operation in ['*', '/', '+', '-', '^(', '√']:
            buttons[operation] = QtWidgets.QPushButton(calc) # operation button
            buttons[operation].setText(str(operation))
            buttons[operation].clicked.connect(partial(print_operation, str(operation)))
        for bracket in ['(', ')']:
            buttons[bracket] = QtWidgets.QPushButton(calc) # bracket button
            buttons[bracket].setText(str(bracket))
            buttons[bracket].clicked.connect(partial(print_bracket, str(bracket)))
        buttons['.'] = QtWidgets.QPushButton(calc) # Dot button
        buttons['.'].setText('.')
        buttons['.'].clicked.connect(dot)
        buttons['Del'] = QtWidgets.QPushButton(calc) # Backspace button (clear one charartcer)
        buttons['Del'].setText('Delete')
        buttons['Del'].clicked.connect(delete)
        buttons['CO'] = QtWidgets.QPushButton(calc) # Clear Operation (CO)
        buttons['CO'].setText('Clear')
        buttons['CO'].clicked.connect(clear)
        buttons['CA'] = QtWidgets.QPushButton(calc) # Clear All (CA)
        buttons['CA'].setText('Clear All')
        buttons['CA'].clicked.connect(clear_all)
        buttons['POPUP'] = QtWidgets.QPushButton(calc)
        buttons['POPUP'].setText("<  ")
        buttons['POPUP'].clicked.connect(show_popup)
        buttons['PI'] = QtWidgets.QPushButton(calc)
        buttons['PI'].setText(pi_char)
        buttons['PI'].clicked.connect(partial(print_symbol_and_close, pi_char))
        buttons['E'] = QtWidgets.QPushButton(calc)
        buttons['E'].setText(e_char)
        buttons['E'].clicked.connect(partial(print_symbol_and_close, e_char))
        buttons['ANS'] = QtWidgets.QPushButton(calc)
        buttons['ANS'].setText("Ans")
        buttons['ANS'].clicked.connect(ANSWER)
        buttons['GOLDEN-RATIO'] = QtWidgets.QPushButton(calc)
        buttons['GOLDEN-RATIO'].setText(fi_char)
        buttons['GOLDEN-RATIO'].clicked.connect(partial(print_symbol_and_close, fi_char))
        buttons['PASTE'] = QtWidgets.QPushButton(calc)
        buttons['PASTE'].setText("Paste Custom\nOperation")
        buttons['PASTE'].clicked.connect(pasteOperation)
        buttons['EDIT'] = QtWidgets.QPushButton(calc)
        buttons['EDIT'].setText("Edit\nOperation")
        buttons['EDIT'].clicked.connect(editOperation)
        buttons['X'] = QtWidgets.QPushButton(calc)
        buttons['X'].setText(x_char)
        buttons['X'].clicked.connect(partial(print_symbol_and_close, x_char))
        buttons['Y'] = QtWidgets.QPushButton(calc)
        buttons['Y'].setText(y_char)
        buttons['Y'].clicked.connect(partial(print_symbol_and_close, y_char))
        buttons['Z'] = QtWidgets.QPushButton(calc)
        buttons['Z'].setText(z_char)
        buttons['Z'].clicked.connect(partial(print_symbol_and_close, z_char))
        buttons['A'] = QtWidgets.QPushButton(calc)
        buttons['A'].setText(a_char)
        buttons['A'].clicked.connect(partial(print_symbol_and_close, a_char))
        buttons['B'] = QtWidgets.QPushButton(calc)
        buttons['B'].setText(b_char)
        buttons['B'].clicked.connect(partial(print_symbol_and_close, b_char))
        buttons['C'] = QtWidgets.QPushButton(calc)
        buttons['C'].setText(c_char)
        buttons['C'].clicked.connect(partial(print_symbol_and_close, c_char))


        for button in ["SIN", "COS", "TAN", "ARCSIN", "ARCCOS", "ARCTAN"]:
            buttons[button] = QtWidgets.QPushButton(calc)
        buttons['SIN'].setText("sine")
        buttons['SIN'].clicked.connect(partial(print_operation, "sin"))
        buttons['COS'].setText("cosine")
        buttons['COS'].clicked.connect(partial(print_operation, "cos"))
        buttons['TAN'].setText("tangent")
        buttons['TAN'].clicked.connect(partial(print_operation, "tan"))
        buttons['ARCSIN'].setText("arcsin")
        buttons['ARCSIN'].clicked.connect(partial(print_operation, "arcsin"))
        buttons['ARCCOS'].setText("arccos")
        buttons['ARCCOS'].clicked.connect(partial(print_operation, "arccos"))
        buttons['ARCTAN'].setText("arctan")
        buttons['ARCTAN'].clicked.connect(partial(print_operation, "arctan"))



        for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(', '√']: #Grey (#333333)
            buttons[button].setObjectName("regularButton")
        for button in ['.', '+', '-', '*', '/']:# blue grey (#49525C)
            buttons[button].setObjectName("operationButton")
        for button in ['Del', 'CO', 'CA']:#Dark Grey (#222222)
            buttons[button].setObjectName("darkButton")
        for button in ['PI', 'X', 'Y', 'Z', 'A', 'B', 'C', 'E', "GOLDEN-RATIO", "ANS", "EDIT", "PASTE", "SIN", "COS", "TAN", "ARCSIN", "ARCCOS", "ARCTAN"]: #Turquoise (#33998a)
            buttons[button].setObjectName("equalNormal")
        for button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '^(', '√']: #Grey (#333333)
            buttons[button].setObjectName("regularButton")
        buttons["POPUP"].setObjectName("popupButton")
        
        buttons['='].setStyleSheet('border-top-left-radius: 3px;')
        buttons['.'].setStyleSheet('border-top-right-radius: 3px;')
        buttons['/'].setStyleSheet('border-top-left-radius: 3px;')
        buttons['Del'].setStyleSheet('border-bottom-left-radius: 3px;')
        buttons['PI'].setStyleSheet('border-top-left-radius: 3px;')
        buttons['√'].setStyleSheet('border-top-right-radius: 3px;')
        buttons['PASTE'].setStyleSheet('border-bottom-left-radius: 3px;')

        calc.keyRelease.connect(on_key)
        menuBar = calc.menuBar()
        menuBar.setNativeMenuBar(False)

        fileMenu = menuBar.addMenu("File")
        settingsMenu = menuBar.addMenu("Settings")
        sizeMenu = settingsMenu.addMenu("Resize")
        trigonoMenu = menuBar.addMenu("Trigonometry")
        helpMenu = menuBar.addMenu("Help")


        saveAction = QtWidgets.QAction("Save History", calc)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(saveHistory)
        fileMenu.addAction(saveAction)

        quitAction = QtWidgets.QAction("Quit", calc)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(quitCalc)
        fileMenu.addAction(quitAction)

        topAction = QtWidgets.QAction("Enable Stay-On-Top mode", calc)
        topAction.setShortcut("Ctrl+T")
        topAction.setCheckable(True)
        topAction.triggered.connect(showOnTop)

        openHelpAction = QtWidgets.QAction("Online manual", calc)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)

        updatesAction = QtWidgets.QAction("Check for updates", calc)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)

        aboutAction = QtWidgets.QAction("About SomePythonThings Calc", calc)
        aboutAction.triggered.connect(partial(throw_info, "About SomePythonThings Calc", "SomePythonThings Calc\nVersion "+str(actualVersion)+"\n\nThe SomePythonThings Project\n\n © 2021 Martí Climent, SomePythonThings\nhttps://www.somepythonthings.tk\n\n\nThe iconset has a CC Non-Commercial Atribution 4.0 License"))
        helpMenu.addAction(aboutAction)

        openSettingsAction = QtWidgets.QAction("Settings    ", calc)
        openSettingsAction.triggered.connect(openSettingsWindow)
        settingsMenu.addAction(openSettingsAction)

        logAction = QtWidgets.QAction("Open Log", calc)
        logAction.triggered.connect(openLog)
        settingsMenu.addAction(logAction)

        reinstallAction = QtWidgets.QAction("Re-install SomePythonThings Calc", calc)
        reinstallAction.triggered.connect(reinstallCalc)
        settingsMenu.addAction(reinstallAction)

        settingsMenu.addAction(topAction)
        minResize = QtWidgets.QAction("Mini", calc)
        minResize.triggered.connect(partial(resizeWidgets, True, 250, 210))
        sizeMenu.addAction(minResize)

        smallResize = QtWidgets.QAction("Small", calc)
        smallResize.triggered.connect(partial(resizeWidgets, True, 500, 400))
        sizeMenu.addAction(smallResize)

        mediumResize = QtWidgets.QAction("Medium     ", calc)
        mediumResize.triggered.connect(partial(resizeWidgets, True, 500, 900))
        sizeMenu.addAction(mediumResize)

        wideResize = QtWidgets.QAction("Wide", calc)
        wideResize.triggered.connect(partial(resizeWidgets, True, 500, 1100))
        sizeMenu.addAction(wideResize)

        bigResize = QtWidgets.QAction("Big", calc)
        bigResize.triggered.connect(partial(resizeWidgets, True, 750, 1200))
        sizeMenu.addAction(bigResize)

        giantResize = QtWidgets.QAction("Huge", calc)
        giantResize.triggered.connect(partial(resizeWidgets, True, 900, 1500))
        sizeMenu.addAction(giantResize)

        for _ in range(4):
            separator = QtWidgets.QAction("      ", calc)
            separator.setEnabled(False)
            menuBar.addAction(separator)

        angleAction = QtWidgets.QAction(calc)
        angleAction.triggered.connect(changeAngleUnit)
        menuBar.addAction(angleAction)

        sinAction = QtWidgets.QAction("Sine", calc)
        sinAction.triggered.connect(partial(print_operation, "sin"))
        sinAction.setShortcut("Shift+S")
        trigonoMenu.addAction(sinAction)
        cosAction = QtWidgets.QAction("Cosine", calc)
        cosAction.triggered.connect(partial(print_operation, "cos"))
        cosAction.setShortcut("Shift+C")
        trigonoMenu.addAction(cosAction)
        tanAction = QtWidgets.QAction("Tangent", calc)
        tanAction.triggered.connect(partial(print_operation, "tan"))
        tanAction.setShortcut("Shift+T")
        trigonoMenu.addAction(tanAction)
        arcsinAction = QtWidgets.QAction("Arcsine", calc)
        arcsinAction.triggered.connect(partial(print_operation, "arcsin"))
        arcsinAction.setShortcut("Ctrl+Shift+S")
        trigonoMenu.addAction(arcsinAction)
        arccosAction = QtWidgets.QAction("Arccosine", calc)
        arccosAction.triggered.connect(partial(print_operation, "arccos"))
        arccosAction.setShortcut("Ctrl+Shift+C")
        trigonoMenu.addAction(arccosAction)
        arctanAction = QtWidgets.QAction("Arctangent", calc)
        arctanAction.triggered.connect(partial(print_operation, "arctan"))
        arctanAction.setShortcut("Ctrl+Shift+T")
        trigonoMenu.addAction(arctanAction)



        if(_platform=='darwin'):
            newMenuBar = QtWidgets.QMenuBar(calc)
            newMenuBar.setNativeMenuBar(True)

            fileMenu = newMenuBar.addMenu("File")
            settingsMenu = newMenuBar.addMenu("Settings")
            sizeMenu = settingsMenu.addMenu("Resize")
            trigonoMenu = newMenuBar.addMenu("Trigonometry")
            helpMenu = newMenuBar.addMenu("Help")

            fileMenu.addAction(saveAction)
            fileMenu.addAction(quitAction)
            helpMenu.addAction(openHelpAction)
            helpMenu.addAction(updatesAction)
            helpMenu.addAction(aboutAction)
            settingsMenu.addAction(openSettingsAction)
            settingsMenu.addAction(logAction)
            settingsMenu.addAction(reinstallAction)
            sizeMenu.addAction(minResize)
            sizeMenu.addAction(smallResize)
            sizeMenu.addAction(mediumResize)
            sizeMenu.addAction(wideResize)
            sizeMenu.addAction(bigResize)
            sizeMenu.addAction(giantResize)

            for _ in range(4):
                separator = QtWidgets.QAction("      ", calc)
                separator.setEnabled(False)
                newMenuBar.addAction(separator)

            newMenuBar.addAction(angleAction)

            trigonoMenu.addAction(sinAction)
            trigonoMenu.addAction(cosAction)
            trigonoMenu.addAction(tanAction)
            trigonoMenu.addAction(arcsinAction)
            trigonoMenu.addAction(arccosAction)
            trigonoMenu.addAction(arctanAction)



        if(settings["angleUnit"] == "degree"):
            log("[   OK   ] Calculator in degrees")
            angleAction.setText("Degrees (deg)")
        else:
            log("[   OK   ] Calculator in radians")
            angleAction.setText("Radians (rad)")


        resizeWidgets()
        calc.setMinimumSize(210, 250)
        print_symbol(x_char)
        calc.show()
        clear_all()

        Thread(target=checkUpdates, daemon=True).start()
        Thread(target=checkModeThread, daemon=True).start()
        app.exec_()
    except Exception as e:
        log("[ FAILED ] A FATAL ERROR OCCURRED. PROGRAM WILL BE TERMINATED AFTER ERROR REPORT")
        try:
            throw_error('SomePythonThings Calc', "SomePythonThings Calc crashed because of a fatal error.\n\nAn Error Report will be generated and opened automatically\n\nSending the report would be very appreciated. Sorry for any inconveniences")
        except:
            pass
        os_info = f"" + \
        f"                        OS: {platform.system()}\n"+\
        f"                   Release: {platform.release()}\n"+\
        f"           OS Architecture: {platform.machine()}\n"+\
        f"          APP Architecture: {platform.architecture()[0]}\n"+\
        f"                   Program: SomePythonThings Calc Version {actualVersion}"+\
        "\n\n-----------------------------------------------------------------------------------------"
        traceback_info = "Traceback (most recent call last):\n"
        try:
            for line in traceback.extract_tb(e.__traceback__).format():
                traceback_info += line
            traceback_info += f"\n{type(e).__name__}: {str(e)}"
        except:
            traceback_info += "\nUnable to get traceback"
            if(debugging):
                raise e
        f = open(tempDir.name.replace('\\', '/')+'/log.txt', 'r')
        webbrowser.open("https://www.somepythonthings.tk/error-report/?appName=SomePythonThings Calc&errorBody="+os_info.replace('\n', '{newline}').replace(' ', '{space}')+"{newline}{newline}{newline}{newline}SomePythonThings Calc Log:{newline}"+str(f.read()+"\n\n\n\n"+traceback_info).replace('\n', '{newline}').replace(' ', '{space}'))
        f.close()
        if(debugging):
            raise e
else:
    log("[ FAILED ] __name__ is not __main__, not running program!")
log('[  EXIT  ] Reached end of the script')

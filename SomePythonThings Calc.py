import eel
@eel.expose
def checkUpdates_py():
    actualVersion = 3.0
    if True:
        import struct
        import urllib.request
        response = urllib.request.urlopen("http://www.somepythonthings.tk/versions/calc.html")
        response = response.read().decode("utf8")
        if float(response)>actualVersion:
            return True
        else:
            return False
    else:
        return False
@eel.expose
def downloadUpdates():
    import webbrowser
    webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-calc/')
    
def eval2(s):
    try:
        return str(eval(str(s)))
    except:
        return 'Oh 💩, You did it again! The operation is too hard to be calculated!'
@eel.expose
def py_eval(s):
    return eval2(s)
@eel.expose
def python_alive():
    return True

def server_thread():
    global kill_server
    global port
    print('[      ] Starting Eel on localhost:'+str(port))
    eel.start('index.html',mode=None, size=(900, 500), port=port,  block=False)
    print('[  OK  ] Eel running')
    while not kill_server:
        eel.sleep(0.1)
    print('[  OK  ] Server killed')




if True:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtWebEngineWidgets import *
    from threading import Thread
    import sys
    from random import randint
    port=randint(1000, 9999)
    
    class MainWindow(QMainWindow):

        def __init__(self, *args, **kwargs):
            eel.sleep(0.1)
            global port
            print('[      ] Creating window')
            super(MainWindow,self).__init__(*args, **kwargs)
            try:
                self.setWindowIcon(QIcon('icon.png'))
            except:
                pass
            self.setWindowTitle("SomePythonThings Calc")
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl("http://localhost:"+str(port)+"/index.html"))
            self.browser.sizeHint = lambda: QSize (900, 500)
            self.setCentralWidget(self.browser)
            self.show()
            print('[  OK  ] Window created')
            
    app = QApplication(sys.argv)
    kill_server = False
    eel.init('web')
    t = Thread(target=server_thread)
    t.start()
    window = MainWindow()
    app.exec_()
    print('[  OK  ] Application created')
    kill_server=True
    print('[  OK  ] Application terminated')
    print('[      ] Killing server')
    t.join()
    print('[ EXIT ] Reached end of the script')
else:
    from tkinter.messagebox import showerror
    showerror(title='SomePythonThings Calc', message='An error has occurred while running SomePythonThings Calc. Try to run the program later. If the error persists, please report it at https://github.com/martinet101/SomePythonThings-Calc/issues')


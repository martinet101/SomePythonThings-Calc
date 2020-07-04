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
@eel.expose()
def python_alive():
    return True

def server_process():
    print('Starting Eel')
    eel.start('index.html',mode=None, size=(900, 500), port=6938,  block=False)
    while True:
        print("Eel Server Running")
        eel.sleep(1.0)   

try:
    import eel
    eel.init('web')

    if __name__ == '__main__':
        from cefpython3 import cefpython as cef
        from multiprocessing import Process
        import sys
        p = Process(target=server_process)
        p.start()
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        print("Starting window at localhost:6938/index.html")
        try:
            cef.CreateBrowserSync(url="localhost:6938/index.html",
                              window_title="SomePythonThings Calc")
        except:
            cef.CreateBrowserSync(url="localhost:6938/index.html")
        cef.MessageLoop()
        cef.Shutdown()
        eel.sleep(1)
        print("Server closed. 2 seconds to destroy program")
        eel.sleep(2)
except:
    from tkinter.messagebox import showerror
    showerror(title='SomePythonThings Calc', message='An error has occurred while running SomePythonThings Calc. Try to run the program later. If the error persists, please report it at https://github.com/martinet101/SomePythonThings-Calc/issues')


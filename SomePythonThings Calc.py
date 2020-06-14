import eel
@eel.expose
def checkUpdates_py():
    actualVersion = 2.4
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
eel.init('web')



eel.start('index.html', mode='chrome', size=(900, 500), port=0)
while True:
    eel.sleep(1)

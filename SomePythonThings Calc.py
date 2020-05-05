import eel
@eel.expose
def checkUpdates_py():
    actualVersion = 2.3
    if True:
        import struct
        import urllib.request
        response = urllib.request.urlopen("http://www.somepythonthings.tk/versions/windows/calc.html")
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
    webbrowser.open_new('https://www.somepythonthings.tk/programs/sptcalc.html')
@eel.expose
def py_eval(s):
    print(s)
    return str(eval(str(s)))
@eel.expose()
def python_alive():
    return True
eel.init('web')
eel.start('index.html', mode='chrome', size=(900, 500), port=0)
while True:
    eel.sleep(1)

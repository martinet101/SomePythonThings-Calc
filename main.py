import eel
@eel.expose
def checkUpdates_py():
    import wget
    actualVersion = 2.0
    try:
        url = 'https://www.somepythonthings.tk/versions/windows/calc.html'
        file = wget.download(url)
        version = open(file, "r")
        lastVersion = float(version.read())
        version.close()
        import os
        os.remove(file)
        if float(actualVersion)<lastVersion:
            return True
        else:
            return False
    except:
        return False
@eel.expose
def downloadUpdates():
    import webbrowser
    webbrowser.open_new('https://www.somepythonthings.tk/programs/sptcalc.html')
@eel.expose
def py_eval(s):
    return str(eval(s))
eel.init('web')
eel.start('index.html', mode='chrome', size=(900, 500), port=0)
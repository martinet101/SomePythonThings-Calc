import wget
actualVersion = 2.0
if True:
    url = 'https://www.somepythonthings.tk/versions/windows/calc.html'
    file = wget.download(url)
    version = open(file, "r")
    lastVersion = float(version.read())
    version.close()
    import os
    os.remove(file)
    if float(actualVersion)<lastVersion:
        from tkinter import Tk
        from tkinter.messagebox import *
        root = Tk()
        root.withdraw()
        goAndDownload = askquestion("Updates available!","Actual version: "+str(actualVersion)+"\nNew version: "+str(lastVersion)+"\nDo you want to go to the web and download it?")
        root.destroy()
        root.mainloop()
        if goAndDownload == 'yes':
            import webbrowser
            webbrowser.open_new('https://www.somepythonthings.tk/programs/sptcalc.html')
#except:
#    pass
import eel
@eel.expose
def py_eval(s):
    return str(eval(s))
eel.init('web')
eel.start('index.html', mode='chrome', size=(900, 500), port=0)
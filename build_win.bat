rmdir /Q /S build
rmdir /Q /S dist
python -m PyInstaller "SomePythonThings Calc.py" --icon icon.ico --noconsole --add-data calc-icon.png;. --exclude-module tkinter --exclude-module PyQt5 --add-data "ok.png;." --add-data "./warn.png;." --add-data "./error.png;."
pause

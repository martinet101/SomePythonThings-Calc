cd "$( dirname "$0" )"
python3 -m PyInstaller 'SomePythonThings Calc.py' --icon icon.ico --noconsole --onefile --add-data "./calc-icon.png":. --exclude-module tkinter --exclude-module PyQt5 --add-data "ok.png:." --add-data "./warn.png:." --add-data "./error.png:."

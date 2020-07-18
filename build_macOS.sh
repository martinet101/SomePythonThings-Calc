#!/bin/bash
python3.7 -m eel "SomePythonThings Calc.py" web --onefile --exclude-module tkinter --windowed  --hidden-import="pkg_resources.py2_warn" --icon="macOSicon.icns" --hidden-import="PyQtWebEngine"
zsh




#!/bin/bash
rmdir -rf build dist
python3.7 -m PyInstaller "SomePythonThings Calc.py" --onefile --exclude-module tkinter --windowed  --icon "./macOSicon.icns" --add-data "./icon.png":"./"
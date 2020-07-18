#!/bin/bash
python3.7 -m PyInstaller 'SomePythonThings Calc.py' --icon icon.ico --noconsole --onefile --add-data "./icon.png":.


#!/bin/bash
cd "$( dirname "$0" )"
python3.7 -m PyInstaller "SomePythonThings Calc.py" --icon "./macOSicon.icns" --windowed
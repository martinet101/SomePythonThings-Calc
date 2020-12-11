#!/bin/bash
cd "$( dirname "$0" )"
python3.8 -m PyInstaller "SomePythonThings Calc.py" --icon "./macOSicon.icns" --windowed
cd dist/SomePythonThings\ Calc.app/Contents/MacOS
sudo codesign --remove-signature "Python"
#!/bin/bash
cd "$( dirname "$0" )"
python3.8 -m PyInstaller "SomePythonThings Calc.py" --icon "./macOSicon.icns" --windowed --add-data "./ok.png:." --add-data "./warn.png:." --add-data "./error.png:."
cd dist/SomePythonThings\ Calc.app/Contents/MacOS
sudo codesign --remove-signature "Python"
echo
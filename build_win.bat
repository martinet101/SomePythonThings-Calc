rmdir /Q /S build
rmdir /Q /S dist
python -m PyInstaller "SomePythonThings Calc.py" --icon icon.ico --noconsole --add-data calc-icon.png;.
pause

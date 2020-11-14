rmdir /Q /S build
rmdir /Q /S dist
python -m PyInstaller "SomePythonThings Calc.py" --icon icon.ico --onefile --add-data calc-icon.png;.
cd "dist"
"SomePythonThings Calc.exe"
cmd
pause

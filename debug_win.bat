rmdir /Q /S build
rmdir /Q /S dist
python -m eel "SomePythonThings Calc.py" web --icon icon.ico --add-data icon.png;.
cd "dist\SomePythonThings Calc"
"SomePythonThings Calc.exe"
pause
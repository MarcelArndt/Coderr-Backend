@echo off
setlocal

if not exist env (
    echo Erstelle virtuelle Umgebung "env"...
    python -m venv env
)
call env\Scripts\activate

echo Installiere Requirements...
pip install -r requirements.txt


echo Führe utils.py aus...
python utils.py
endlocal
echo Daten sind installiert und Fenster kann geschlossen werden
pause
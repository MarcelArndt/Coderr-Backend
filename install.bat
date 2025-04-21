@echo off
setlocal


if not exist env (
    echo Erstelle virtuelle Umgebung "env"...
    python -m venv env
)


call env\Scripts\activate


echo Installiere Requirements...
pip install -r requirements.txt


echo Führe Datenbankmigrationen durch...
python manage.py makemigrations
python manage.py migrate


endlocal
echo Daten sind installiert und fenster kann geschlossen werden
pause
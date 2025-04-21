@echo off
setlocal

if not exist env (
    echo Erstelle virtuelle Umgebung "env"...
    python -m venv env
)
call env\Scripts\activate

echo Installiere Requirements...
pip install -r requirements.txt

if exist db.sqlite3 del db.sqlite3
del /Q market_app\migrations\0*.py 2>nul
del /Q auth_app\migrations\0*.py 2>nul

echo Erstelle neue Migrationen...
python manage.py makemigrations market_app
python manage.py makemigrations auth_app

echo Führe Migrationen durch...
python manage.py migrate

echo Führe utils.py aus...
python utils.py
endlocal
echo Daten sind installiert und Fenster kann geschlossen werden
pause
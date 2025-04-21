@echo off
setlocal


if not exist env (
    echo Erstelle virtuelle Umgebung "env"...
    python -m venv env
)


call env\Scripts\activate


echo Starte Django-Server...
python manage.py runserver

endlocal

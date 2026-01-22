@echo off
echo ========================================
echo   Installation de l'Auto-Clicker
echo ========================================
echo.

echo Creation de l'environnement virtuel...
python -m venv venv

echo.
echo Activation de l'environnement...
call venv\Scripts\activate.bat

echo.
echo Installation des dependances...
pip install -r requirements.txt

echo.
echo ========================================
echo   Installation terminee!
echo   Lancez run.bat pour demarrer l'application
echo ========================================
pause

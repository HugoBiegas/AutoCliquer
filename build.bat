@echo off
echo ========================================
echo   Construction de l'executable
echo ========================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

echo Construction en cours...
echo.

pyinstaller --noconfirm --onefile --windowed ^
    --name "AutoClicker" ^
    --icon "assets/icon.ico" ^
    --add-data "src;src" ^
    --add-data "assets;assets" ^
    --hidden-import "pynput.keyboard._win32" ^
    --hidden-import "pynput.mouse._win32" ^
    main.py

echo.
echo ========================================
if exist "dist\AutoClicker.exe" (
    echo   Succes! Executable cree dans: dist\AutoClicker.exe
) else (
    echo   Erreur lors de la creation de l'executable
)
echo ========================================
pause

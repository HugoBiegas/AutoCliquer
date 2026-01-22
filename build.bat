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
    --add-data "src;src" ^
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

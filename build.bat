@echo off
echo ========================================
echo   Construction de l'executable
echo ========================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Nettoyer les anciens builds
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo Construction en cours...
echo.

python setup.py build_exe

echo.
echo ========================================
if exist "build\exe.win-amd64-3.12\AutoClicker.exe" (
    echo   Succes! Executable cree dans: build\exe.win-amd64-3.12\

    REM Copier vers dist pour coherence
    if not exist "dist" mkdir dist
    xcopy /s /e /y "build\exe.win-amd64-3.12\*" "dist\" >nul
    echo   Copie dans: dist\
) else (
    echo   Erreur lors de la creation de l'executable
)
echo ========================================
pause

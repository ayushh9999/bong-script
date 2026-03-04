@echo off
:: ─────────────────────────────────────────────────────────
:: bongScript Installer for Windows
:: Downloads and installs bong.exe to your system
:: ─────────────────────────────────────────────────────────

echo.
echo  ============================================
echo    🙏 bongScript Installer
echo    Bengali Programming Language
echo  ============================================
echo.

:: Create install directory
set "INSTALL_DIR=%USERPROFILE%\bongscript"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Check if bong.exe exists in dist folder (local install)
if exist "%~dp0dist\bong.exe" (
    echo  [1/3] Copying bong.exe...
    copy /Y "%~dp0dist\bong.exe" "%INSTALL_DIR%\bong.exe" >nul
) else if exist "%~dp0bong.exe" (
    echo  [1/3] Copying bong.exe...
    copy /Y "%~dp0bong.exe" "%INSTALL_DIR%\bong.exe" >nul
) else (
    echo  ERROR: bong.exe not found!
    echo  Please build first: pyinstaller --onefile --name bong --console bong.py
    pause
    exit /b 1
)

echo  [2/3] Adding to PATH...

:: Check if already in PATH
echo %PATH% | findstr /i "%INSTALL_DIR%" >nul
if %errorlevel%==0 (
    echo        Already in PATH. Skipping.
) else (
    :: Add to user PATH
    for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%B"
    if defined USER_PATH (
        setx PATH "%USER_PATH%;%INSTALL_DIR%" >nul 2>&1
    ) else (
        setx PATH "%INSTALL_DIR%" >nul 2>&1
    )
    echo        Done! Added %INSTALL_DIR% to PATH.
)

echo  [3/3] Verifying installation...
echo.

"%INSTALL_DIR%\bong.exe" --help

echo.
echo  ============================================
echo    ✅ bongScript installed successfully!
echo.
echo    Location: %INSTALL_DIR%\bong.exe
echo.
echo    Usage:
echo      bong file.bong     Run a .bong file
echo      bong               Start interactive REPL
echo.
echo    ⚠️  RESTART your terminal for PATH to work!
echo  ============================================
echo.

pause

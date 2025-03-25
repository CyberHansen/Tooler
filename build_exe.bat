@echo off
echo Building optimized Tooler executable...
echo.

REM Install UPX if not already installed (for compression)
echo Checking for UPX...
if not exist "upx\" (
    echo Downloading UPX for compression...
    mkdir upx
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/upx/upx/releases/download/v4.0.2/upx-4.0.2-win64.zip' -OutFile 'upx.zip'"
    powershell -Command "Expand-Archive -Path 'upx.zip' -DestinationPath 'upx' -Force"
    del upx.zip
    echo UPX downloaded and extracted.
) else (
    echo UPX already installed.
)

REM Build the executable using our optimized spec file
echo.
echo Building executable with PyInstaller...
pyinstaller --clean --upx-dir=upx tooler.spec

echo.
if exist "dist\Tooler\" (
    echo Build successful! Executable is in the dist\Tooler folder.
) else (
    echo Build failed. Check the output for errors.
)

echo.
pause

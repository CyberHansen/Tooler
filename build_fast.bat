@echo off
echo Building optimized Tooler executable with onedir option...
echo.

pyinstaller --noconfirm --onedir --windowed --icon "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\tooler.ico" ^
--exclude-module matplotlib ^
--exclude-module scipy ^
--exclude-module pandas ^
--exclude-module numpy.random ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\ffmpeg.exe;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\gui desgin.png;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\tooler.ico;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\tooler.png;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\wave.png;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\yt-dlp.exe;." ^
--add-data "C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\Tesseract-OCR;Tesseract-OCR" ^
"C:\Users\mathi\OneDrive - Buskerud fylkeskommune\Din Daglige App\Tooler2.0\app.py"

echo.
if exist "dist\app\" (
    echo Build successful! Executable is in the dist\app folder.
) else (
    echo Build failed. Check the output for errors.
)

echo.
pause

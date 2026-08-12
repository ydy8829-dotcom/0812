@echo off
cd /d "%~dp0"

where conda >nul 2>nul
if %errorlevel%==0 (
    call conda activate base
) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    call "%USERPROFILE%\anaconda3\Scripts\activate.bat" base
) else if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    call "%USERPROFILE%\miniconda3\Scripts\activate.bat" base
) else (
    echo Anaconda installation was not found.
    pause
    exit /b 1
)

python -m streamlit run app.py
pause

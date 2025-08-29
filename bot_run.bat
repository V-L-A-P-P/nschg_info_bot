@echo off

call %~dp0venv\Scripts\activate

cd %~dp0

set TOKEN=yourToken

python info_bot.py

pause

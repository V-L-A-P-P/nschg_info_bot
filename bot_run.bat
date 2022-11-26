@echo off

call %~dp0venv\Scripts\activate

cd %~dp0

set TOKEN=5674708123:AAERfxk3EDL8yitGepyTs-ynI9yGjLlIuBs

python info_bot.py

pause
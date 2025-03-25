@echo off
cd /d "%~dp0"
pyinstaller --noconfirm --onedir --windowed --icon "src/assets/img/icon_rpc.ico" ^
--name "RPCYummyAnime" ^
--add-data "src;src/" ^
--add-data "logs;logs/" ^
--add-data "config;config/" ^
--hidden-import "pygetwindow" ^
--add-data "platforms;platforms/" ^
--add-data "src/assets/img;assets/img/" ^
"src/main.py"
pause

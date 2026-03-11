@echo off
title BonBon Launcher
cd C:\Users\deads\PycharmProjects\BonBon

echo Closing any existing backend...
taskkill /f /im python.exe >nul 2>&1

echo Launching BonBon...
npx electron .

echo Closing backend...
taskkill /f /im python.exe >nul 2>&1

exit
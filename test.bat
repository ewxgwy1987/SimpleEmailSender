@echo off
echo %1
if not -%1-==-- echo Argument one provided
if -%1-==-- echo Argument one not provided & exit /b
Pause

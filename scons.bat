:: -c  -clean
@echo off 
if "%1"=="-c" ( 
    @echo -----------start clean--------
    C:\Python27\Scripts\scons.bat  -c  target=opencpu_bc28
    rd /s /Q .\build_scons   
    del  .\tools\SCons\*.pyc 
    del /a /Q .\scons_targets\*.pyc 
    del /a /Q .\*.dblite >nul 2>nul
    @echo ------------clean over--------
) else (
    @echo -----------start building--------   
    C:\Python27\Scripts\scons.bat target=opencpu_bc28 && \ >nul 2>nul
    @echo ------------build over--------
) 

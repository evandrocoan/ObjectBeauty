

@echo off

:: Path to your Visual Studio folder.
::
:: Examples:
::     C:\Program Files\Microsoft Visual Studio 9.0
::     F:\VisualStudio2015
set VISUAL_STUDIO_FOLDER=F:\VisualStudio2015

:: Load compilation environment
call "%VISUAL_STUDIO_FOLDER%\VC\vcvarsall.bat"

:: Invoke compiler with any options passed to this batch file
"%VISUAL_STUDIO_FOLDER%\VC\bin\cl.exe" %*


@echo off
REM Deploy MPK Mini IV Remote files to Reason (Windows)

setlocal

set "SCRIPT_DIR=%~dp0"
set "SOURCE_DIR=%SCRIPT_DIR%reason_remote"

REM Reason Remote locations on Windows (user AppData)
set "REMOTE_BASE=%APPDATA%\Propellerhead Software\Remote"
set "CODECS_DIR=%REMOTE_BASE%\Codecs\Lua Codecs\Akai"
set "MAPS_DIR=%REMOTE_BASE%\Maps\Akai"

echo Deploying MPK Mini IV Remote files...
echo.

REM Create directories if they don't exist
if not exist "%CODECS_DIR%" mkdir "%CODECS_DIR%"
if not exist "%MAPS_DIR%" mkdir "%MAPS_DIR%"

REM Copy codec files
copy /Y "%SOURCE_DIR%\MPK mini IV.luacodec" "%CODECS_DIR%\"
copy /Y "%SOURCE_DIR%\MPK mini IV.lua" "%CODECS_DIR%\"

REM Copy map file (rename to match expected name)
copy /Y "%SOURCE_DIR%\MPK_mini_IV.remotemap" "%MAPS_DIR%\MPK mini IV.remotemap"

echo.
echo Deployed to:
echo   -^> %CODECS_DIR%\MPK mini IV.luacodec
echo   -^> %CODECS_DIR%\MPK mini IV.lua
echo   -^> %MAPS_DIR%\MPK mini IV.remotemap
echo.
echo Restart Reason to load the new Remote files.
echo.
pause

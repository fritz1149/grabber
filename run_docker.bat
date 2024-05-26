@echo off
for /L %%i in (1 1 1) do (
    docker run -v E:\projects\grab\save\%%i:/home/seluser/save ^
    -d -e file_name=test.txt -e max_turn=2 ^
    19231149/grabber
)
@REM for /L %%i in (1 1 5) do (
@REM     if not exist "save\%%i" (
@REM         mkdir "save\%%i"
@REM     )
@REM )
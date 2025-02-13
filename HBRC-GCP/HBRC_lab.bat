@echo off
setlocal

REM Set the local folder path and Google Cloud Storage bucket path
set "localFolder=<PATH-TO-LOCAL-FOLDER>"
set "bucketPath=gs://hcg-data/HBRC/"

REM Create log file with current date and time
set "logFile=%localFolder%\move_files_log.txt"
echo ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- >> "%logFile%"

REM Record start time
for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set "startHour=%%a"
    set "startMinute=%%b"
    set "startSecond=%%c"
    set "startMillis=%%d"
)
echo Date - %date% >> "%logFile%"
echo Day - %date:~0,3% >> "%logFile%"
echo. >> "%logFile%"
echo Start time = %startHour%:%startMinute%:%startSecond%.%startMillis% >> "%logFile%"
echo. >> "%logFile%"

REM Move files to Google Cloud Storage
for %%I in ("%localFolder%\*") do (
    if /I not "%%~xI"==".bat" (
        if /I not "%%~xI"==".log" (
            if /I not "%%~xI"==".txt" (
                echo Moving "%%~nxI"... >> "%logFile%"
                gcloud storage mv "%%~fI" "%bucketPath%%%~nxI" >> "%logFile%" 2>&1
                if errorlevel 1 (
                    echo ERROR: Failed to move "%%~nxI" on %date% at %time% >> "%logFile%"
                ) else (
                    echo Successfully moved "%%~nxI" >> "%logFile%"
                )
            )
        )
    )
)

REM Record end time
for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set "endHour=%%a"
    set "endMinute=%%b"
    set "endSecond=%%c"
    set "endMillis=%%d"
)
echo End time = %endHour%:%endMinute%:%endSecond%.%endMillis% >> "%logFile%"

REM Calculate total time taken
set /a "totalSeconds=((%endHour%*3600)+(%endMinute%*60)+(%endSecond%))-((%startHour%*3600)+(%startMinute%*60)+(%startSecond%))"
set /a "minutes=totalSeconds / 60"
set /a "seconds=totalSeconds %% 60"

echo Total time taken = %minutes% minutes %seconds% seconds >> "%logFile%"
echo. >> "%logFile%"
echo ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- >> "%logFile%"
echo. >> "%logFile%"
echo. >> "%logFile%"

echo Successfully moved all files. >> "%logFile%"

endlocal
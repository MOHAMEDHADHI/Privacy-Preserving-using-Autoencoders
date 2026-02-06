@echo off
echo ===================================================================
echo   VIEWING YOUR RESULTS
echo ===================================================================
echo.

echo Opening Admin Dashboard...
start http://localhost:5001

timeout /t 2 /nobreak >nul

echo Opening HTML Report...
start reports\report_None.html

timeout /t 2 /nobreak >nul

echo Opening Performance Chart...
start reports\performance_None.png

echo.
echo ===================================================================
echo   All results opened!
echo ===================================================================
pause

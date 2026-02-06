@echo off
REM Windows batch script to run the integrated pipeline

echo ===================================================================
echo   PRIVACY-PRESERVING ML PIPELINE - INTEGRATED EXECUTION
echo ===================================================================
echo.

REM Set environment variables
set RENDER_ENDPOINT=https://privacy-preserving-using-autoencoders-1.onrender.com
set RENDER_API_KEY=rnd_GY3hBI68fZ1nhHsPLIaMLCrFxHwC

echo Render Endpoint: %RENDER_ENDPOINT%
echo API Key: %RENDER_API_KEY%
echo.

REM Run the integrated pipeline
python integrated_pipeline.py

echo.
echo ===================================================================
echo   Pipeline execution complete!
echo   View dashboard at: http://localhost:5001
echo ===================================================================
pause

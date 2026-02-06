# PowerShell script to run the integrated pipeline

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  PRIVACY-PRESERVING ML PIPELINE - INTEGRATED EXECUTION" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables
$env:RENDER_ENDPOINT = "https://privacy-preserving-using-autoencoders-1.onrender.com"
$env:RENDER_API_KEY = "rnd_GY3hBI68fZ1nhHsPLIaMLCrFxHwC"

Write-Host "Render Endpoint: $env:RENDER_ENDPOINT" -ForegroundColor Green
Write-Host "API Key: $env:RENDER_API_KEY" -ForegroundColor Green
Write-Host ""

# Run the integrated pipeline
python integrated_pipeline.py

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  Pipeline execution complete!" -ForegroundColor Green
Write-Host "  View dashboard at: http://localhost:5001" -ForegroundColor Yellow
Write-Host "===================================================================" -ForegroundColor Cyan

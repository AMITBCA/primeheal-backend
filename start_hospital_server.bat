@echo off
title Prime Heal - Hospital Server (Lifetime Unlimited)
color 0A
cls
echo =====================================================================
echo           PRIME HEAL - CLINICAL DECISION SUPPORT SERVER
echo                   LIFETIME UNLIMITED HOSPITAL EDITION
echo =====================================================================
echo.
echo [1/3] Starting Local Clinical Backend Server (Port 8000)...
start "PrimeHeal Backend" /min cmd /c "cd /d "%~dp0" && python server.py"

echo [2/3] Starting Secure Cloud Tunnel (prime-heal-hospital-app)...
start "PrimeHeal Tunnel" /min cmd /c "npx localtunnel --port 8000 --subdomain prime-heal-hospital-app"

echo [3/3] Waiting for server initialization...
timeout /t 3 /nobreak >nul

echo.
echo =====================================================================
echo  SERVER STATUS: ONLINE & READY
echo =====================================================================
echo  * Local Address:    http://127.0.0.1:8000
echo  * Admin Dashboard:  http://127.0.0.1:8000/admin
echo  * Cloud Tunnel:     https://prime-heal-hospital-app.loca.lt
echo  * Mobile App APK:   prime-heal-unlimited.apk
echo =====================================================================
echo.
echo Opening Admin Dashboard in browser...
start http://127.0.0.1:8000/admin
echo.
echo Keep this window open while using Prime Heal app in the hospital.
echo Press any key to exit...
pause >nul

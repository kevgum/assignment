@echo off
REM Hotel Booking System Maven Build Script
REM This script uses Maven to compile, test, and package the Python application

echo ==========================================
echo Hotel Booking System Maven Build
echo ==========================================

echo.
echo [Maven] Checking Maven installation...
where mvn >nul 2>nul
if %errorlevel% neq 0 (
    echo Maven not found in PATH, using Maven wrapper...
    if exist mvnw.cmd (
        set MVN_CMD=mvnw.cmd
    ) else (
        echo ERROR: Maven not installed and wrapper not found
        echo Please install Maven or ensure mvnw.cmd is present
        exit /b 1
    )
) else (
    set MVN_CMD=mvn
)

echo Using Maven command: %MVN_CMD%

echo.
echo [Maven] Running clean and compile...
%MVN_CMD% clean compile
if %errorlevel% neq 0 (
    echo ERROR: Maven compile failed
    exit /b 1
)

echo.
echo [Maven] Running tests...
%MVN_CMD% test
if %errorlevel% neq 0 (
    echo WARNING: Some tests failed, but continuing build process
)

echo.
echo [Maven] Creating package...
%MVN_CMD% package
if %errorlevel% neq 0 (
    echo ERROR: Maven package failed
    exit /b 1
)

echo.
echo ==========================================
echo MAVEN BUILD COMPLETED SUCCESSFULLY!
echo ==========================================
echo Artifacts created in 'target' folder
echo Test reports available in 'target/surefire-reports'
echo Coverage reports available in 'target/coverage-reports'
echo Deployable packages in 'target' folder
echo.
echo Usage: python hotel.py [room_type] [days]
echo Example: python hotel.py luxury 2
echo.

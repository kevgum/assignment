@echo off
REM Maven Wrapper for Windows
REM Automatically downloads and installs Maven if not present

setlocal

set MAVEN_VERSION=3.9.4
set MAVEN_HOME=%USERPROFILE%\.m2\wrapper\dists\apache-maven-%MAVEN_VERSION%
set MAVEN_DOWNLOAD_URL=https://archive.apache.org/dist/maven/maven-3/%MAVEN_VERSION%/binaries/apache-maven-%MAVEN_VERSION%-bin.zip

if not exist "%MAVEN_HOME%" (
    echo Installing Maven %MAVEN_VERSION%...
    if not exist "%USERPROFILE%\.m2\wrapper\dists" mkdir "%USERPROFILE%\.m2\wrapper\dists"
    
    REM Download Maven
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%MAVEN_DOWNLOAD_URL%' -OutFile '%TEMP%\maven.zip'}"
    
    REM Extract Maven
    powershell -Command "& {Expand-Archive -Path '%TEMP%\maven.zip' -DestinationPath '%USERPROFILE%\.m2\wrapper\dists' -Force}"
    
    del "%TEMP%\maven.zip"
    echo Maven installed successfully!
)

set PATH=%MAVEN_HOME%\bin;%PATH%
mvn %*

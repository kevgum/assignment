Hotel Booking System - Maven Build
=====================================

Requirements:
- Python 3.7+
- Internet connection (for Maven auto-download)

Maven Plugins Used:
==================
- exec-maven-plugin (3.1.0) - Executes Python commands
- maven-surefire-plugin (3.1.2) - Test reporting
- maven-clean-plugin (3.2.0) - Cleans build artifacts
- maven-assembly-plugin (3.4.2) - Creates packages

How to Build and Test:
=====================

1. Clean and compile:
   .\mvnw.cmd clean compile

2. Run tests:
   .\mvnw.cmd test

3. Build everything:
   .\mvnw.cmd clean compile test

Notes:
- First run downloads Maven automatically
- Test results in target/surefire-reports/
- 5 tests total: 3 pass, 2 fail (by design)

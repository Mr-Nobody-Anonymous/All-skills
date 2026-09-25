@echo off
REM ⚡ All Skills — Automated Environment & Harness Initializer
setlocal EnableDelayedExpansion

set REPO_ROOT=%~dp0
cd /d "%REPO_ROOT%"

echo =================================================================
echo ⚡ ALL SKILLS — AGENT HARNESS INITIALIZER (/setup-skills)
echo =================================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python 3.10+ is required but not found in PATH.
    exit /b 1
)

python "%REPO_ROOT%scripts\setup_skills.py" %*

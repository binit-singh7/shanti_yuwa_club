@echo off
echo ===================================================
echo Shanti Yuwa Club Website - Image File Checker
echo ===================================================
echo.

set IMG_DIR=static\images
set REQUIRED_IMAGES=logo.png hero-bg.jpg about-home.jpg about-story.jpg

echo Checking for required image files...
echo.

for %%i in (%REQUIRED_IMAGES%) do (
    if exist "%IMG_DIR%\%%i" (
        for /F "usebackq" %%F in (`dir /b /a:-d /s "%IMG_DIR%\%%i"^|find /c /v ""`) do (
            echo [OK] %%i exists
        )
    ) else (
        echo [MISSING] %%i is missing!
    )
)

echo.
echo ===================================================
echo Remember to add real images to replace placeholders!
echo ===================================================

pause

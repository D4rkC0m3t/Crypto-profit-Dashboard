@echo off
echo Initializing Git repository for TradeProfitAnalytics...

git init
git add .
git commit -m "Initial commit of TradeProfitAnalytics dashboard"

echo.
echo Git repository initialized successfully!
echo.
echo Next steps:
echo 1. Create a repository on GitHub, GitLab, or your preferred Git hosting service
echo 2. Run the following commands to push your code:
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git push -u origin master
echo.
echo Happy coding!
pause

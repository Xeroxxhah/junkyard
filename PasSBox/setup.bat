@echo off 
echo Setting up PassBox
mkdir PasSBox
type NUL  >PasSBox\users.txt
ping localhost -n 2 >nul
echo setup complete
pause
exit
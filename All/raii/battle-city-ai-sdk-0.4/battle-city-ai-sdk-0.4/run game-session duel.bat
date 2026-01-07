@echo off
SET MapPath=../maps/Duel.json
:: Генерируем строку с датой и временем в формате ГГГГММДД_ЧЧММСС
FOR /f "tokens=2 delims==" %%G IN ('wmic os get localdatetime /value') DO SET datetime=%%G
SET datetime=%datetime:~0,8%_%datetime:~8,6%
SET LogsPath=../logs/log-duel_%datetime%.json
SET URLS=http://localhost:6469
cd game-session
dotnet BattleCityAI.GameSession.dll
pause

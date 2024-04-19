@echo off
REM browse [modelPath] [port]
REM browse ..\lda\model 8080

@IF "%~1"=="" goto usage
@IF "%~2"=="" goto usage
goto ok

:usage
ECHO Usage:    browse [modelPath] [port]
ECHO Example:  browse ..\lda\model 8080
ECHO -
ECHO     This lauches an HTTP server that allows you to browse the documents
ECHO     in your corpus by topic and the topics.
ECHO -
ECHO - modelPath refers to a model created by "train".
ECHO   It must point to a path with the prefix name of the model.
ECHO - port is the TCP port on which the web browser will listen.
ECHO -
ECHO python must be in your path.
ECHO -
goto eof

:ok
set OUT=%~f1
set PORT=%2

ECHO Consult http://localhost:%PORT%/topics/
python python\result_browser.py %PORT% %OUT%

:eof

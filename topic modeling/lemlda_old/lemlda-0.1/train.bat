@echo off
REM train [topics] [docsDir] [outPath]
REM train 5 c:\lemlda\corpusTaggedDotted\ c:\lemlda\lda\model

@IF "%~1"=="" goto usage
@IF "%~2"=="" goto usage
@IF "%~3"=="" goto usage
goto ok

:usage
ECHO Usage:    train [topics] [docsDir] [outPath]
ECHO Example:  train 5 ..\corpusTaggedDotted ..\lda\model
ECHO - java and python must be in your path.
ECHO - topics is the desired number of topics to be learned by the LDA algorithm.
ECHO - docsDir must be a full path where the documents encoded in UTF8 must be located.
ECHO   train will iterate over files with extension txt.
ECHO   The files must have been tagged and dotted using tag and dot.
ECHO - outPath must be a full path to a file (for example model).
ECHO   train will generate several files in this folder whose name starts with the prefix given.
ECHO   for example model.dat, model.doc etc.
ECHO -
goto eof

:ok
set TOPICS=%1
set DOCS_DIR=%~f2
set OUT=%~f3

REM alpha near 0 -> sparser documents (less topics per document)
REM beta near 0 -> sparser topics (less lemmas per topic) [require more topics]
REM gamma near 0 -> sparser lemmas (less words per lemma)

set DOCS_PAT=*.txt
set ITERATIONS=2500
set ALPHA=0.5
set BETA=0.1
set GAMMA=0.1

python python\files_to_lemmlda.py %DOCS_DIR% %DOCS_PAT% %OUT%

java -cp java\trove-2.0.4.jar;java\bin LemmLdaGibbsSampler %OUT%.dat %OUT%.lemlex %OUT% %TOPICS% %ITERATIONS% %ALPHA% %BETA% %GAMMA%

python python\show_topics.py %OUT% > %OUT%.topics.html
echo -
echo Done
:eof


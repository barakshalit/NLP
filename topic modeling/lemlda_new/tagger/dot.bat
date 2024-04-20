@echo off
REM dot [corpusTagged] [corpusTaggedDotted]
REM dot ..\corpusTagged\ ..\corpusTaggedDotted\

@IF "%~1"=="" goto usage
@IF "%~2"=="" goto usage
@IF "%~3"=="" goto usage
goto ok

:usage
ECHO Usage:    dot [corpusTagged] [corpusTaggedDotted] [model:-token/-word/-lemma]
ECHO Example:  dot ..\corpusTagged ..\corpusTaggedDotted -lemma
ECHO -
ECHO     This will iterate over text files found in [corpusTagged]
ECHO     and add vocalization (nikud) to each tagged word in each file.
ECHO     The dotted files will be placed in [corpusTaggedDotted] in the format
ECHO     of one word per line followed by its vocalized version.
ECHO     The dotted files are encoded in UTF8.
ECHO - 
ECHO     The files in corpusTagged must have been produced by tag.
ECHO -
ECHO     The model can be either: -token, -word or -lemma
ECHO     If your text can be reasonably well handled by the tagger use -lemma, otherwise choose -token
ECHO -
ECHO java must be in your path.
ECHO -
goto eof

:ok
java -cp trove-2.0.2.jar;tagger.jar vohmm.application.GenerateLDAInputFromTaggedCompactCorpus %~f1 %~f2 %~dp0dotted-lexicon.txt %~dp0known-bitmasks %3

:eof

@echo off
REM tag [corpusIn] [corpusOut]
REM tag ..\corpus\ ..\corpusTagged\

@IF "%~1"=="" goto usage
@IF "%~2"=="" goto usage
goto ok

:usage
ECHO Usage:    tag [corpusIn] [corpusOut]
ECHO Example:  tag ..\corpus\ ..\corpusTagged\
ECHO - 
ECHO     This will iterate over text files found in [corpusIn]
ECHO     and perform morphological tagging on each file.
ECHO     The tagged files will be placed in [corpusOut] in the format
ECHO     of one word per line followed by a number which is a compact encoding as
ECHO     a bitmask of the tag.  The tag includes the Part of speech of the word,
ECHO     its segmentation (in case of prefixes like ha- and bklm, mshvklv) and
ECHO     its morphological properties (number, gender, tense, person etc).
ECHO     The tagged files are encoded in UTF8.
ECHO -
ECHO java must be in your path.
ECHO -
goto eof

:ok

REM Use -bWST for white space tagger instead of the broken Mila tagger.
REM This assumes the text has been tokenized before with hebtokenizer.py
java -Xmx1200m -cp trove-2.0.2.jar;XMLAnalyzer.jar;morphAnalyzer.jar;opennlp.jar;gnu.jar;chunker.jar;splitsvm.jar;duck1.jar;tagger.jar vohmm.application.BasicTagger %~dp0 %~f1 %~f2 -bWST 


:eof

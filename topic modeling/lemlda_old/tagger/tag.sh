#! /bin/bash
java -Xmx1200m -cp trove-2.0.2.jar:morphAnalyzer.jar:opennlp.jar:gnu.jar:chunker.jar:splitsvm.jar:duck1.jar:tagger.jar vohmm.application.BasicTagger ./ $1 $2 -wBST

#! /bin/bash
java -cp trove-2.0.2.jar:tagger.jar vohmm.application.GenerateLDAInputFromTaggedCompactCorpus $1 $2 dotted-lexicon.txt known-bitmasks -lemma
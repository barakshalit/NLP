#!/usr/bin/python
import sys
from path import path

from preprocLem import preproc
from lemlex import CorpusBasedLemmatizer, NullLematizer
from corpus_readers import read_dotted_lemma_files

if __name__=='__main__':

   DIRNAME=sys.argv[1]
   FILE_PAT=sys.argv[2]
   OUT=sys.argv[3]

   files = [f.normpath() for f in path(DIRNAME).walkfiles(FILE_PAT)]

   docs_names = list(read_dotted_lemma_files(files, True))
   docs = [doc for doc,name in docs_names]
   names = [name for doc,name in docs_names]

   lematizer = CorpusBasedLemmatizer(files,"utf-8")

   p=preproc(docs, OUT, lematizer, names)

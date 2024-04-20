#!/usr/bin/ptyhon

import random
from collections import defaultdict
import itertools
from vocab import VocabTranslator
from codecs import open

import yutils

from lemlex import HSpellLex as LemLex
from lemlex import CorpusBasedLemmatizer, NullLematizer


def write_docs(docs,out):
   trans = VocabTranslator()
   res=[]
   for doc in docs:
      ints = list(trans.doc_to_ints(doc))
      res.append(ints)
   out.write("%s\n" % len(docs))
   out.write("%s\n" % trans.vocabsize())
   for ints in res:
      out.write("%s\n" % " ".join(map(str,ints)))

def _remove_rare_words(docs):
   word_docs_counter = yutils.Counter()
   for doc in docs:
      word_docs_counter.update(set(doc))
   ndocs = []
   filters=[]
   UPPER = float(len(docs))*0.9
   LOWER = 5
   for doc in docs:
      filter = []
      ndoc   = []
      for w in doc:
         c = word_docs_counter[w]
         if c > UPPER or c < LOWER:
            filter.append(False)
         else:
            ndoc.append(w)
            filter.append(True)
      ndocs.append(ndoc)
      filters.append(filter)
   return ndocs,filters

class Preprocess:
   def __init__(self, lemmatizer):
      self._lemmatizer = lemmatizer
      self._vtrans = VocabTranslator()  # words  <-> ints
      self._ltrans = VocabTranslator()  # lemmas <-> ints
      self._docs = []   # each item is a list of words
      self._wints = []   # each item is a list of ints (mapped from words)
      self._lemmas = [] # each item is a list of tuples of possible lemmas 
      self._lints = []   # each item is a list of tuples of ints (mapped from possible lemmas)
      self._remlist = [] # like docs, but each item is a list of booleans. True: word is in. False: word is out

   def add_docs(self, docs):
      lemmatizer = self._lemmatizer
      docs = [list(d) for d in docs]
      rdocs,remlist = _remove_rare_words(docs)
      self._remlist = remlist
      #rdocs = docs[:]
      self._docs.extend(rdocs)
      self._wints.extend((list(self._vtrans.doc_to_ints(doc)) for doc in rdocs))
      
      # lemmas stuff
      for doc in self._docs:
         dlemmas = []
         for word in doc:
            wlems = lemmatizer.lemmasFor(word)
            if not wlems: wlems = [word]
            wlems = tuple(wlems)
            dlemmas.append(wlems)
         self._lemmas.append(dlemmas)
         self._lints.append([tuple(self._ltrans.doc_to_ints(list(wlem))) for wlem in dlemmas])
      
      self._docs  = [x for x in self._docs if x]
      self._wints = [x for x in self._wints if x]
      self._lemmas= [x for x in self._lemmas if x]
      self._lints = [x for x in self._lints if x]

   def add_lemmad_docs(self, docs):
      """
      lemmad_docs: a list of lemmad_doc
      lemmad_doc: a sequence of (word,(lemma1,...lemmak)) tuples.
      @TODO: untested!
      """
      # convert each sequence to a list (to remove iterators and such)
      lemmad_docs = [list(ld) for ld in docs]
      just_word_docs = [[w for w,lems in ldoc] for ldoc in lemmad_docs]
      rdocs,remlist = _remove_rare_words(just_word_docs)
      self._remlist = remlist
      #rdocs = docs[:]
      self._docs.extend(rdocs)
      self._wints.extend((list(self._vtrans.doc_to_ints(doc)) for doc in rdocs))
      
      # lemmas stuff
      for remlist,ldoc in zip(self._remlist,lemmad_docs):
         dlemmas = []
         for keep,(word,wlems) in zip(remlist,ldoc):
            if not keep: continue
            if not wlems: wlems = [word]
            wlems = tuple(wlems)
            dlemmas.append(wlems)
         self._lemmas.append(dlemmas)
         self._lints.append([tuple(self._ltrans.doc_to_ints(list(wlem))) for wlem in dlemmas])
      
      self._docs  = [x for x in self._docs if x]
      self._wints = [x for x in self._wints if x]
      self._lemmas= [x for x in self._lemmas if x]
      self._lints = [x for x in self._lints if x]

   def write_docs(self, fh):
      fh.write("%s\n" % len(self._docs))
      fh.write("%s\n" % self._vtrans.vocabsize())
      for doc in self._docs:
         fh.write("%s\n" % " ".join(("%s" % x for x in doc)))
      fh.write("\n")

   def write_ldocs(self, fh):
      fh.write("%s\n" % len(self._docs))
      fh.write("%s %s\n" % (self._vtrans.vocabsize(), self._ltrans.vocabsize()))
      for doc,dlems in zip(self._docs,self._lemmas):
         lems = [":".join([x.replace(":","_COL_") for x in lems]) for lems in dlems]
         doc  = [x.replace(":","_COL_") for x in doc]
         fh.write("%s\n" % " ".join(["%s:%s" % (w,ls) for w,ls in zip(doc,lems)]))
      fh.write("\n")

   def write_dat(self, fh):
      fh.write("%s\n" % len(self._docs))
      fh.write("%s\n" % self._vtrans.vocabsize())
      for ints in self._wints:
         fh.write("%s\n" % " ".join(map(str,ints)))
      fh.write("\n")

   def write_filter(self, fh):
      for fs in self._remlist:
         fh.write("%s\n" % " ".join(map(str,fs)))
      fh.write("\n")

   def write_ldat(self, fh):
      fh.write("%s\n" % len(self._docs))
      fh.write("%s %s\n" % (self._vtrans.vocabsize(), self._ltrans.vocabsize()))
      for wints,lints in zip(self._wints,self._lints):
         fh.write("%s\n" % " ".join(["%s:%s" % (wi,":".join(map(str,lis))) for wi,lis in zip(wints,lints)]))
      fh.write("\n")

   def write_vocab(self, fh):
      self._vtrans.write(fh)

   def write_lvocab(self, fh):
      self._ltrans.write(fh)
   
   def write_lemlex_info(self, fh):
      # num of lemmas
      lemmas = set()
      for ldoc in self._lemmas:
         for lems in ldoc: lemmas.update(lems)
      fh.write("%s\n" % len(lemmas))
      # num of tokens
      toks = set()
      for doc in self._docs:
         toks.update(doc)
      fh.write("%s\n" % len(toks))

      # num of words for each lemma
      for lem in lemmas:
         tokens = self._lemmatizer.wordsFor(lem)
         #count = len(tokens)*73 # assume all prefixes are always possible
         count = len(tokens)
         if not tokens: count = 1
         lemid = self._ltrans.word_to_int(lem)
         fh.write("%s %s\n" % (lemid, count))
      fh.write("\n")

      # possible lemmas for each word
      for tok in toks:
         tokid = self._vtrans.word_to_int(tok)
         lems = list(self._lemmatizer.lemmasFor(tok))
         if not lems: lems = [tok]
         lemid= [self._ltrans.word_to_int(l) for l in lems]
         fh.write("%s %s\n" % (tokid, " ".join(map(str,lemid)))) 

def preproc(docs, outname, lematizer=NullLematizer(), doc_names=None):
   if doc_names:
      nout = open(outname+".docnames","w","utf-8")
      for name in doc_names: 
         nout.write("%s\n" % str(name))
      nout.close()
   vout = open(outname+".vocab","w","utf-8")
   lvout = open(outname+".lvocab","w","utf-8")
   dout = open(outname+".dat","w","utf-8")
   ldout = open(outname+".ldat","w","utf-8")
   wout = open(outname+".doc","w","utf-8")
   lout = open(outname+".ldoc","w","utf-8")
   llout = open(outname+".lemlex","w","utf-8")
   fout = open(outname+".filtered","w","utf-8")

   p = Preprocess(lematizer)
   p.add_docs(docs)

   p.write_dat(dout)
   p.write_ldat(ldout)
   p.write_vocab(vout)
   p.write_lvocab(lvout)
   p.write_docs(wout)
   p.write_ldocs(lout)
   p.write_filter(fout)
   p.write_lemlex_info(llout)
   dout.close()
   vout.close()
   lvout.close()
   wout.close()
   ldout.close()
   lout.close()
   llout.close()
   fout.close()
   return p


# encoding: utf-8
from codecs import open
from collections import defaultdict
import os.path

def is_numeric(str):
   try:
      x = float(str)
      return True
   except ValueError:
      return False

class NullLematizer: #{{{
   def __init__(self):pass
   def lemmasFor(self, word):
      return [word]
   def wordsFor(self, lemma):
      return [lemma]
#}}}

class LemLex: # {{{
   def __init__(self,lexdir="."):
      self._loadlex(lexdir)
      print("loaded")

   def _loadlex(self,lexdir):
      self._prefs = {}
      for line in open(os.path.join(lexdir,"bgupreflex.utf8.hr"),"r","utf-8"):
         pref,anal = line.strip().split(None,1)
         self._prefs[pref]=anal
      self._toklem = defaultdict(set)
      self._lemtok = defaultdict(set)
      for line in open(os.path.join(lexdir,"bgulex.utf8.hr"),"r","utf-8"):
         token,info = line.strip().split(None,1)
         lemmas = info.split()[1::2]
         for lem in lemmas:
            self._toklem[token].add(lem)
            self._lemtok[lem].add(token)

   def prefixate(self,token):
      for pref in self._prefs:
         if token.startswith(pref) and token[len(pref):] in self._toklem:
            yield pref, token[len(pref):]
         elif token.startswith(pref) and is_numeric(token[len(pref):]):
            yield pref, "__NUM__"

   def lemmasFor(self,token, tryPrefix=True):
      if token == '__NUM__': return [token]
      res = []
      # as is:
      if token in self._toklem:
         res.extend(self._toklem[token])
      elif is_numeric(token): res.append("__NUM__")
      # try removing the prefixes
      if tryPrefix:
         for pref,tok in self.prefixate(token):
            if tok in self._toklem or tok == '__NUM__':
               res.extend(self.lemmasFor(tok, tryPrefix=False))
               #res.append(tok)
      return list(set(res))

   def wordsFor(self, lemma):
      return self._lemtok[lemma]
# }}}

class CorpusBasedLemmatizer:
   def __init__(self, fnames, encoding):
      self._wordLem = defaultdict(set)
      self._lemWord = defaultdict(set)
      self._read(fnames, encoding)

   def _read(self, fnames, encoding):
      for fname in fnames:
         for line in open(fname,"r",encoding):
            line = line.strip().split()
            if not line: continue
            word = line[0]
            lemmas = set(line[1:])
            if 'unspecified' in lemmas:
               lemmas.remove('unspecified')
               lemmas.add(word)
            self._wordLem[word].update(lemmas)
            for lem in lemmas: self._lemWord[lem].add(word)

   def lemmasFor(self, token, pref=None):
      """
      pref is ignored
      """
      assert(pref==None)
      return self._wordLem[token]

   def wordsFor(self, lem):
      return self._lemWord[lem]



class HSpellLex(LemLex):
   def _loadlex(self,lexdir):
      self._prefs = defaultdict(int)
      for line in open(os.path.join(lexdir,"bgupreflex.utf8.hr"),"r","utf-8"):
         pref,anal = line.strip().split(None,1)
         self._prefs[pref]=0

      for line in open(os.path.join(lexdir,"hspell_preflex"),"r","utf-8"):
         pref, mask = line.strip().split()
         mask = int(mask)
         if pref in self._prefs or pref[-1] == "ה":
            self._prefs[pref] |= mask
      assert (0 not in list(self._prefs.values()))
      self._prefs = dict(self._prefs)

      self._toklem = defaultdict(set)
      self._lemtok = defaultdict(set)
      self._tokpref= defaultdict(int) # from token to prefix mask
      for line in open(os.path.join(lexdir,"hspelllex"),"r","utf-8"):
         token, prefinfo, dinfo,  lem= line.strip().split()
         self._toklem[token].add(lem)
         self._lemtok[lem].add(token)
         self._tokpref[token] |= int(prefinfo)

   # from libhspell.c {{{
   #/* if a prefix has a certain 'mask', and lookup on a word returns
   # * 'val' (a bitmask of prefixes allowed for it), our prefix is
   # * allowed on this word if and only if (mask & val)!=0.
   # *
   # * This means that 'mask' defines the bits that this prefix "supplies"
   # * and he 'val' defined for a word is the bits this words insists on
   # * getting at least one of (i.e., val is the list of types of
   # * prefixes that are allowed for this word).
   # */ }}}
   def prefixate(self,token):
      for pref,mask in list(self._prefs.items()):
         _tok = token[len(pref):]
         if token.startswith(pref) and _tok in self._toklem and ((self._tokpref[_tok] & mask) != 0):
            yield pref, token[len(pref):]
         elif token.startswith(pref) and is_numeric(token[len(pref):]):
            yield pref, "__NUM__"
   
if __name__=='__main__':
   ll = HSpellLex()
   bcl = ll.lemmasFor("בצל")
   hbcl = ll.lemmasFor("הבצל")
   lhr = ll.lemmasFor("להריון")
   hr = ll.lemmasFor("הריון")
   krk = ll.lemmasFor("הכרוכות")
   krk = ll.lemmasFor("כרוכות")
   krk2 = ll.lemmasFor("הכרוךות")
   kr = "כרוך"
   kr2 = "כרוכות"
   h = "ה"

   import sys
   def vocab(fname):
      v = set()
      for line in open(fname,"r","utf-8"):
         line = line.strip().split()
         if line: v.add(line[0])
      return v
   
   #ll = LemLex()
   #for v in vocab(sys.argv[1]):
   #   print v.encode("utf-8")," ".join(ll.lemmasFor(v)).encode("utf-8")


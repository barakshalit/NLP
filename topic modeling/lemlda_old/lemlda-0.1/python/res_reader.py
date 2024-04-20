# encoding: utf-8
import vocab
import sys
from codecs import open
from collections import defaultdict

class LemmaModel:
   def __init__(self): #{{{
      self.fz  = None
      self.fw  = None
      self.fl  = None
      self.fzw = None
      self.fzl = None
      self.flw = None
      #}}}

   @classmethod
   def load(cls,filename_prefix): #{{{
      ls = open(filename_prefix + ".dat.l")
      ws = open(filename_prefix + ".doc","r","utf-8")
      zs = open(filename_prefix + ".dat.z")
      vt = vocab.VocabTranslator.from_file(open(filename_prefix+".lvocab","r","utf-8"))

      docs = open(filename_prefix + ".doc","r","utf-8").readlines()[2:]


      next(ws); next(ws)

      fzw = defaultdict(lambda :defaultdict(int))
      fz  = defaultdict(int)
      fw  = defaultdict(int)

      fzd = defaultdict(lambda :defaultdict(int))
      fdz = defaultdict(lambda :defaultdict(int))

      fzl = defaultdict(lambda :defaultdict(int))

      flw = defaultdict(lambda: defaultdict(int))
      fl  = defaultdict(int)

      for did,(ll,lw,lz) in enumerate(zip(ls,ws,zs)):
         ll = list(vt.ints_to_doc([int(x) for x in ll.strip().split()]))
         lw = list(lw.strip().split())
         lz = list(lz.strip().split())
         for z in lz: 
            fzd[z][did]+=1
            fdz[did][z]+=1
         assert(len(ll)==len(lw))
         assert(len(lw)==len(lz))
         for (l,w,z) in zip(ll,lw,lz):
            fzw[z][w]+=1
            fzl[z][l]+=1
            fz[z]+=1
            fw[w]+=1

            fl[l]+=1
            flw[l][w]+=1

      new = cls()
      new.fzd = fzd
      new.fdz = fdz
      new.fzw = fzw
      new.fz  = fz
      new.fw  = fw
      new.fl  = fl
      new.fzl = fzl
      new.flw = flw
      
      new.docs = docs

      new._topics_for_word  = None
      new._topics_for_lemma = None
      new._lemmas_for_word = None

      new._docs_for_topic = None
      new._topics_for_doc = None

      new.ZD_THRESH = 2
      return new
      #}}}

   def set_new_docs(self, doc_names_f, doc_words_f, doc_topics_f, zd_thresh=1):
      self.ZD_THRESH = zd_thresh
      doc_names = open(doc_names_f)
      doc_words = list(open(doc_words_f,"r","utf8"))
      doc_topics= open(doc_topics_f)

      self._docs_for_topic = None
      self._topics_for_doc = None
      self.fzd = defaultdict(lambda :defaultdict(int))
      self.fdz = defaultdict(lambda :defaultdict(int))
      self.fz = defaultdict(int)
      self.docs = doc_words

      for i, (name, words, topics) in enumerate(zip(doc_names, doc_words, doc_topics)):
         for topic in topics.strip().split():
            self.fzd[topic][i]+=1
            self.fdz[i][topic]+=1
            self.fz[topic]+=1
   
   def topics(self):
      return list(self.fz.keys())

   def docs_for_topic(self, z):
      if not self._docs_for_topic:
         dft = defaultdict(set)
         for _z in [z]: # self.fz:
            for d,cnt in list(self.fzd[z].items()):
               if cnt>self.ZD_THRESH: dft[_z].add(d)
         return dft[z]
         self._docs_for_topic = dft
      return self._docs_for_topic[z]

   def topics_for_doc(self, docid):
      if not self._topics_for_doc:
         tfd = defaultdict(set)
         for _d in [docid]: 
            for z,cnt in list(self.fdz[_d].items()):
               if cnt>0: tfd[docid].add(z)
         print("topics for doc:",tfd[docid])
         return tfd[docid]
         self._topics_for_doc = tfd
      return self._topics_for_doc[docid]

   def topics_for_word(self,w):
      if not self._topics_for_word:
         tfw = defaultdict(set)
         for _w in [w]: # self.fw:
            for (z,ws) in list(self.fzw.items()):
               if ws[_w]>0: tfw[_w].add(z)
         return tfw[w]
         self._topics_for_word = tfw
      return self._topics_for_word[w]

   def topics_for_lemma(self,l):
      if not self._topics_for_lemma:
         tfl = defaultdict(set)
         for _l in [l]: #self.fl.keys():
            for (z,ls) in list(self.fzl.items()):
               if ls[_l]>0: tfl[_l].add(z)
         return tfl[l]
         self._topics_for_lemma = tfl
      return self._topics_for_lemma[l]

   def lemmas_for_word(self,w):
      if not self._lemmas_for_word:
         lfw = defaultdict(set)
         for _w in [w]: # self.fw:
            for l,ws in list(self.flw.items()):
               if ws[_w]>0: lfw[_w].add(l)
         return lfw[w]
         self._lemmas_for_word = lfw
      return self._lemmas_for_word[w]

   def p_wGl(self,w,l):
      return self.flw[l][w] / float(self.fl[l])

   def p_lGt(self,l,t):
      return self.fzl[t][l] / float(self.fz[t])

   def p_wGt(self,w,t):
      return self.fzw[t][w] / float(self.fz[t])

   def p_dGt(self, d, t):
      return self.fzd[t][d] / float(self.fz[t])


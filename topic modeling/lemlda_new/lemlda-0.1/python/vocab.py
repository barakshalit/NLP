import itertools

class VocabTranslator: #{{{
   def __init__(self):
      self._counter = itertools.count(0)
      self._wmap = {}
      self._back = {}

   def doc_to_ints(self, doc):
      """
      doc is a sequence of tokens,
      which is translated to a list of numbers
      """
      for word in doc: 
         if word not in self._wmap: 
            c = next(self._counter)
            self._wmap[word] = c
            self._back[c] = word
            yield c
         else:
            yield self._wmap[word]
   
   def ints_to_doc(self, ints):
      for i in ints:
         yield self._back[i]
   
   def int_to_word(self, int): return self._back[int]
   def word_to_int(self,word): return self._wmap[word]

   def vocabsize(self): return len(list(self._wmap.keys()))

   def write(self,fh):
      for word,num in self._wmap.items():
         fh.write("%s %s\n" % (word,num)) 

   @classmethod
   def from_file(cls,fh):
      new = cls()
      for line in fh:
         line = line.strip().split()
         if not line: break
         word,num=line
         num=int(num)
         new._wmap[word]=num
         new._back[num]=word
      return new

#}}}

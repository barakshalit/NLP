#!/usr/bin/python
# encoding: utf-8
import vocab
import sys
from codecs import open
from collections import defaultdict

ls = open(sys.argv[1] + ".dat.l")
ws = open(sys.argv[1] + ".doc","r","utf-8")
zs = open(sys.argv[1] + ".dat.z")
vt = vocab.VocabTranslator.from_file(open(sys.argv[1]+".lvocab","r","utf-8"))

next(ws); next(ws)

fzw = defaultdict(lambda :defaultdict(int))
fz  = defaultdict(int)
fw  = defaultdict(int)

fzl = defaultdict(lambda :defaultdict(int))

flw = defaultdict(lambda: defaultdict(int))
fl  = defaultdict(int)

for ll,lw,lz in zip(ls,ws,zs):
   ll = list(vt.ints_to_doc([int(x) for x in ll.strip().split()]))
   lw = list(lw.strip().split())
   lz = list(lz.strip().split())
   #print len(ll),len(lw),len(lz)
   assert(len(ll)==len(lw))
   assert(len(lw)==len(lz))
   for (l,w,z) in zip(ll,lw,lz):
      fzw[z][w]+=1
      fzl[z][l]+=1
      fz[z]+=1
      fw[w]+=1

      fl[l]+=1
      flw[l][w]+=1
      #print ("%s/%s/%s" % (w,l,z)).encode("utf-8"),
   #print

def words_for_lemma():
   lemms = {}
   for l in sorted(fl.keys()):
      _fl = float(fl[l])
      pw_l = [(w,(c/_fl)) for (w,c) in flw[l].items()]
      words = [w for w,p in sorted(pw_l,key=lambda x:-x[1])[:100]]
      lemms[l] = words
   return lemms
   
words_for_lemmas = words_for_lemma()

def format(topic, lemmas, wfldict):
   s="""
   <tr><td>%s</td><td>%s</td></tr>
   """
   lemmas = ["<span title='%s'>%s</span> " % (" ".join(wfldict[l]),l) for l in lemmas if l != 'שונות']
   return s % (topic, " ".join(lemmas))

sys.stdout.reconfigure(encoding="utf-8")
print("<html><body dir=rtl><table>")
for z in sorted(list(fz.keys()),key=int):
   _fz = float(fz[z])
   pl_z = [(l,(c/_fz)) for (l,c) in fzl[z].items()]
   pw_z = [(w,(c/_fz)) for (w,c) in fzw[z].items()]

   words  = [w for w,p in sorted(pw_z,key=lambda x:-x[1])[:20]]
   lemmas = [l for l,p in sorted(pl_z,key=lambda x:-x[1])[:20]]
   frm = format(z,lemmas,words_for_lemmas)
   #frm = format(z,words,defaultdict(str))
   # print(frm.encode("utf-8"))
   print(frm)
print("</table></body></html>")

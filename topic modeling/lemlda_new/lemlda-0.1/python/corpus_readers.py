import glob
from codecs import open

def read_docs(fh): #{{{
   doc = []
   for line in fh:
      words = line.strip().split()
      if not words:
         yield doc
         doc = []
      else:
         doc.extend(words)
   if doc: yield doc
#}}}

def read_ap_docs(): #{{{
   doc = []
   for line in open("ap/ap.txt"):
      line = line.strip()
      if not line: continue
      if line.startswith("<TEXT"):
         doc = []
      elif line.startswith("</TEXT"):
         if doc: yield doc
         doc = None
      elif line[0] == "<": continue
      else:
         line = line.replace(","," ").replace("."," ").replace("''"," ").replace("``"," ")
         doc.extend(line.strip().split())
#}}}

def read_rafi_docs(num=10000): #{{{
   for fn in glob.glob("/Users/yoavg/Vork/Research/corpora/hebrew-med/*")[:num]:
      doc = []
      for line in open(fn,"r","utf-8"):
         line = line.strip().split()
         if not line: continue
         doc.append(line[0])
      yield doc
#}}}

def read_rambam_word_lem(with_names=True): #{{{
   """
   every file a chapter
   every blank line a halacha

   #returns:
   #   yield each "chapter" as a lemmad_doc [(word,(lemma1,...,lemmak)),(word,(lemma1,...lemmaj)) ... ]
   """
   #for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/lemma/*.txt"):
   #for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/tagged-dotted-lemma/*.txt"):
   for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/tagged-dotted-lemma/*/*/*.txt"):
      print(fname)
      ldoc = []
      #for line in open(fname,"r","cp1255"):
      for line in open(fname,"r","utf8"):
         line = line.strip().split()
         if not line:
            #if ldoc: yield ldoc
            #ldoc = []
            continue
         word = line[0]
         ldoc.append(word)
      if ldoc:
         if with_names: 
            name = "all",tuple(fname.split("/")[-3:])
            yield ldoc,name
         else: yield ldoc
#}}}

def read_rafi_med_word_lem(with_names=True): #{{{
   for fname in glob.glob("/freespace/phd/adlerm/corpora/medical/tagged-dotted-lemma/*.*"):
      print(fname)
      ldoc = []
      for line in open(fname,"r","utf8"):
         line = line.strip().split()
         if not line:
            continue
         word = line[0]
         ldoc.append(word)
      if ldoc:
         if with_names: 
            name = tuple(fname.split("/")[-1:])
            yield ldoc,name
         else: yield ldoc
#}}}

def read_rambam_word_lem_seifim(with_names=True): #{{{
   """
   every file a chapter
   every blank line a halacha /seif

   #returns:
   #   yield each "seif" as a lemmad_doc [(word,(lemma1,...,lemmak)),(word,(lemma1,...lemmaj)) ... ]
   """
   #for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/lemma/*.txt"):
   #for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/tagged-dotted-lemma/*.txt"):
   for fname in glob.glob("/freespace/phd/adlerm/corpora/respona/rambam/tagged-dotted-lemma/*/*/*.txt"):
      print(fname)
      ldoc = []
      #for line in open(fname,"r","cp1255"):
      snum = 0
      for line in open(fname,"r","utf8"):
         line = line.strip().split()
         if not line:
            if ldoc: 
               snum+=1
               if with_names: 
                  name = str(snum),tuple(fname.split("/")[-3:])
                  yield ldoc,name
               else:
                  yield ldoc
            ldoc = []
            continue
         word = line[0]
         ldoc.append(word)
      if ldoc:
         if with_names: 
            name = "all",tuple(fname.split("/")[-3:])
            yield ldoc,name
         else: yield ldoc
#}}}

def read_lines(fh):
   for line in fh:
      yield line.strip().split()

def read_dotted_lemma_files(files, with_names=True): #{{{
   """
   meni's "dotted-lemma" format:
   each file is a document.
   document name==filename
   each line is a token.
   line format: TOKEN lemma1 ... lemmak
   at least one lemma
   blank lines are ignored
   """
   for fname in files:
      print("[%s]" %fname)
      ldoc = []
      for line in open(fname,"r","utf8"):
         line = line.strip().split()
         if not line:
            continue
         word = line[0]
         ldoc.append(word)
      if ldoc:
         if with_names: 
            name = "all",tuple(fname.split("/")[-3:])
            yield ldoc,name
         else: yield ldoc
#}}}

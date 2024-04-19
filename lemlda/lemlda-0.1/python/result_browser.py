#!/usr/bin/python
# encoding: utf-8
import web

from queries import *
from res_reader import *

import sys
try:
   BASE_NAME=sys.argv[2]
except: 
   BASE_NAME = "rambam-tdl"
   BASE_NAME = "rambam-tdl-names"
   #BASE_NAME = "rambam-tdl-seifim-names"
try:
   DOCS_ARE_SEIFIM = eval(sys.argv[3])
except:
   DOCS_ARE_SEIFIM = False


_doc_name = []
if DOCS_ARE_SEIFIM:
   name = BASE_NAME + ".seif"
else:
   name = BASE_NAME
for i,line in enumerate(open(name+".docnames")):
   _doc_name.append(line.strip())
   
m = LemmaModel.load(BASE_NAME)
if DOCS_ARE_SEIFIM:
   m.set_new_docs("rambam-tdl-names.seif.docnames","rambam-tdl-names.seif.ws","rambam-tdl-names.seif.zs")

lquerier = TopicsFromWordMarginalizeLemma(m)
wquerier = TopicsFromWord(m)

mwquerier = MultiwordToDocs(lquerier)

def _link(what,term):
   return "<a href=../%s/%s>%s</a>" % (what,term,term)

def _check(name,val):
   return "<input type=checkbox name='%s' value='%s'>" % (name,val)

def _linkify(what, terms_probs):
   return [(_link(what,x),p) for x,p in terms_probs]

def _probed_topics_rendered(probed_topics):
   return "".join("%s %s" % (_topic_renderer(tnum),prob) for tnum,prob in probed_topics)

def _topic_renderer(tnum):
   return "<p dir=rtl>%s %s %s" % (_check("topic",tnum),_link("topic",tnum), format_topic(tnum))

topics_url_builder_func = """
<script>
function build_topics_url() {
   s = ""
   topics = document.getElementsByName("topic");
   for (var item in topics) {
      if (topics[item].checked) {
         s+="-"+topics[item].value
      }
   }
   return "../topic/"+s.substr(1);
}
</script>

"""

topics_nav_button = """
<script>
function nav(url) {
   window.location.href = url;
   }
</script>
<INPUT type=submit onclick=nav(build_topics_url())>
"""


def probed_docs_render(docs_probs):
   fmt = "<a href=../doc/%s>%s</a>,%s" 
   res=[]
   for docid,prb in docs_probs:
      docname = _doc_name[int(docid)]
      res.append(fmt % (docid,docname,prb))
   return "<br>".join(res)
   
def words_for_lemma():
   lemms = {}
   for l in sorted(m.fl.keys()):
      _fl = float(m.fl[l])
      pw_l = [(w,(c/_fl)) for (w,c) in m.flw[l].items()]
      words = [w for w,p in sorted(pw_l,key=lambda x:-x[1])[:100]]
      lemms[l] = words
   return lemms

wfl = words_for_lemma()

def format_topic(t):
   _fz = float(m.fz[t]) + 0.00001 # @@@ lazy to do real fix, so added 0.00001 to prevent zero-div in next line
   pl_z = [(l,(c/_fz)) for (l,c) in m.fzl[t].items()]
   pw_z = [(w,(c/_fz)) for (w,c) in m.fzw[t].items()]
   lemmas = [l for l,p in sorted(pl_z,key=lambda x:-x[1])[:20]]
   lemmas = ["<span title='%s'>%s</span> " % (" ".join(wfl[l]),l) for l in lemmas if l != 'שונות']
   return " ".join(lemmas)

class LemmaQuery:
   def GET(self, q):
      web.header('Content-Type', 'text/html; charset=utf-8')
      frmt = """
      <html>%s<body>
      %s
      <p>
      p(w|t) <br>
      %s

      <hr/>
      <p>
      sum_l p(w|l)p(l|t) <br>
      %s
      """ % (topics_url_builder_func, topics_nav_button, _probed_topics_rendered(wquerier.query(q)), _probed_topics_rendered(lquerier.query(q)))
      return frmt

class MultiWordQueryToDocs:
   def GET(self, words):
      web.header('Content-Type', 'text/html; charset=utf-8')
      words = words.strip().split("-")
      doc_scores = mwquerier.query(words)
      return "<html><body><h2>%s</h2>%s</body></html>" % (" ".join(words).encode("utf8"),probed_docs_render(doc_scores))



class ShowTopic:
   def GET(self, tnums):
      web.header('Content-Type', 'text/html; charset=utf-8')
      tnums = tnums.strip().split("-")
      relevant_docs = wquerier.m.docs_for_topic(tnums[0])
      for tnum in tnums[1:]: relevant_docs = relevant_docs.intersection(set(wquerier.m.docs_for_topic(tnum)))
      docs = sorted([(d,wquerier.m.p_dGt(d,tnums[0])) for d in wquerier.m.docs_for_topic(tnums[0]) if d in relevant_docs],key=lambda x_p:-x_p[1])
      if len(tnums)>1: docs = [(doc,"NA") for doc,prb in docs]
      #docs = [(_link('doc',x),p) for x,p in docs]
      topics = [_topic_renderer(tnum) for tnum in tnums]
      topics = "<p>%s" % "<p>".join(topics)
      return "<html>%s<body>%s<p>%s<p> p(doc|topic):<br>%s</body></html>" % (topics_url_builder_func, topics , topics_nav_button, probed_docs_render(docs))

class ShowAllTopics:
   def GET(self):
      web.header('Content-Type', 'text/html; charset=utf-8')
      topics = [_topic_renderer(tnum) for tnum in sorted(list(wquerier.m.fz.keys()),key=lambda x:int("0%s" % x))]
      topics = "<p>%s" % "<p>".join(topics)
      return "<html>%s<body dir=rtl>%s <p>%s</body></html>" % (topics_url_builder_func, topics_nav_button,topics)

class ShowDoc:
   def GET(self, docid):
      web.header('Content-Type', 'text/html; charset=utf-8')
      docid = int(docid)
      docprobs = wquerier.m.docs[docid]
      topics = wquerier.m.topics_for_doc(docid)
      topics = sorted([(tnum, wquerier.m.p_dGt(docid, tnum)) for tnum in topics],key=lambda x_p1:-x_p1[1])
      topics = "<p>".join(["%s %s" % (_topic_renderer(tnum),p) for tnum,p in topics if p > 0.005])
      return "<html>%s<body dir=rtl><h1>topics:</h1>%s <br/>%s<hr><h1>content</h1>%s</body></html>" % (topics_url_builder_func, topics, topics_nav_button, docprobs)


urls = ('/topic/(.*)', 'ShowTopic', 
      '/topics/','ShowAllTopics',
      '/query/(.*)', 'LemmaQuery',
      '/mquery/(.*)', 'MultiWordQueryToDocs',
      '/doc/(.*)', 'ShowDoc')

app = web.application(urls, globals())

if __name__ == '__main__':
   app.run()


